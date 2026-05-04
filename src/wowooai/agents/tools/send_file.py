# -*- coding: utf-8 -*-
# flake8: noqa: E501
# pylint: disable=line-too-long,too-many-return-statements
import os
import mimetypes
import unicodedata
from urllib.parse import quote

from agentscope.tool import ToolResponse
from agentscope.message import (
    TextBlock,
    ImageBlock,
    AudioBlock,
    VideoBlock,
)

from ..schema import FileBlock
from .file_io import _resolve_file_path


def _path_to_preview_url(path: str) -> str:
    """Convert a local file path to a same-origin preview URL.

    The returned URL is a *relative* path of the form
    ``/api/files/preview/<percent-encoded-absolute-path>``. The browser /
    pywebview WebView will resolve it against the current page origin,
    which is the same FastAPI process that serves the static frontend, so
    the URL works regardless of:

    - desktop bundle random port (chosen by ``_find_free_port``),
    - ``wowooai app`` default port 8088,
    - Docker deployments behind a reverse proxy.

    Why not ``file://``: pywebview WebView refuses to navigate to
    ``file://`` from an ``http://`` page (cross-protocol), and
    ``WebViewAPI.save_file`` only accepts ``http(s)``. Producing a same-
    origin HTTP URL keeps the frontend, the desktop save-dialog bridge,
    and the DefaultCards/Files lib all on a single happy path.

    On Windows, converts:
      C:\\path\\file.txt        →  /api/files/preview/C:/path/file.txt
      \\\\server\\share\\f.txt  →  /api/files/preview//server/share/f.txt

    Non-ASCII characters and ``%`` are percent-encoded so the URL is
    always valid ASCII.
    """
    # Normalize to absolute path
    abs_path = os.path.abspath(path)

    # Convert backslashes to forward slashes (Windows)
    if os.name == "nt":
        abs_path = abs_path.replace("\\", "/")

    # Percent-encode non-ASCII and special characters.
    # ``%`` must NOT be in *safe* — otherwise a literal ``%25`` in a
    # filename would survive un-encoded and be mis-decoded later.
    encoded_path = quote(abs_path, safe="/:@")

    # The preview router (`src/wowooai/app/routers/files.py`) accepts a
    # leading "/" and resolves the rest as an absolute filesystem path.
    # On POSIX abs_path already starts with "/"; on Windows it's "C:/…"
    # so we prepend a "/" to match the router's normalization rules.
    if not encoded_path.startswith("/"):
        encoded_path = "/" + encoded_path
    return f"/api/files/preview{encoded_path}"


def _auto_as_type(mt: str) -> str:
    if mt.startswith("image/"):
        return "image"
    if mt.startswith("audio/"):
        return "audio"
    if mt.startswith("video/"):
        return "video"
    return "file"


async def send_file_to_user(
    file_path: str,
) -> ToolResponse:
    """Send a file to the user.

    Args:
        file_path (`str`):
            Path to the file to send.

    Returns:
        `ToolResponse`:
            The tool response containing the file or an error message.
    """

    # Normalize the path: expand ~ and fix Unicode normalization differences
    # (e.g. macOS stores filenames as NFD but paths from the LLM arrive as NFC,
    # causing os.path.exists to return False for files that do exist).
    file_path = os.path.expanduser(unicodedata.normalize("NFC", file_path))

    # Resolve relative paths to absolute paths based on workspace directory
    file_path = _resolve_file_path(file_path)

    if not os.path.exists(file_path):
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Error: The file {file_path} does not exist.",
                ),
            ],
        )

    if not os.path.isfile(file_path):
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Error: The path {file_path} is not a file.",
                ),
            ],
        )

    # Detect MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        # Default to application/octet-stream for unknown types
        mime_type = "application/octet-stream"
    as_type = _auto_as_type(mime_type)

    try:
        # Use a same-origin HTTP preview URL instead of a file:// URL.
        # The Agentscope frontend file card only reads `file_url` / `file_name`;
        # keeping `source.url` as the same value preserves the generic block
        # shape while making desktop and browser download behavior consistent.
        file_url = _path_to_preview_url(file_path)
        filename = os.path.basename(file_path)
        source = {"type": "url", "url": file_url}

        if as_type == "image":
            return ToolResponse(
                content=[
                    ImageBlock(type="image", source=source),
                    TextBlock(type="text", text="File sent successfully."),
                ],
            )
        if as_type == "audio":
            return ToolResponse(
                content=[
                    AudioBlock(type="audio", source=source),
                    TextBlock(type="text", text="File sent successfully."),
                ],
            )
        if as_type == "video":
            return ToolResponse(
                content=[
                    VideoBlock(type="video", source=source),
                    TextBlock(type="text", text="File sent successfully."),
                ],
            )

        return ToolResponse(
            content=[
                FileBlock(
                    type="file",
                    source=source,
                    filename=filename,
                    file_url=file_url,
                    file_name=filename,
                ),
                TextBlock(type="text", text="File sent successfully."),
            ],
        )

    except Exception as e:
        return ToolResponse(
            content=[
                TextBlock(
                    type="text",
                    text=f"Error: Send file failed due to \n{e}",
                ),
            ],
        )
