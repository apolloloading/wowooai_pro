# -*- coding: utf-8 -*-
"""
Agent tools schema: type definitions for agent tool responses.
"""
from typing import Literal, Optional
from typing_extensions import TypedDict, Required

from agentscope.message import Base64Source, URLSource


class FileBlock(TypedDict, total=False):
    """File block for sending files to users."""

    type: Required[Literal["file"]]
    """The type of the block"""

    source: Required[Base64Source | URLSource]
    """The source of the file"""

    filename: Optional[str]
    """The filename of the file"""

    file_url: Optional[str]
    """Frontend-compatible URL used by @agentscope-ai/chat file cards"""

    file_name: Optional[str]
    """Frontend-compatible display name used by @agentscope-ai/chat file cards"""
