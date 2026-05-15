# -*- coding: utf-8 -*-
"""Shared agent template definitions and builders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..config.config import (
    AgentProfileConfig,
    ChannelConfig,
    HeartbeatConfig,
    MCPConfig,
    ToolsConfig,
    build_local_agent_tools_config,
    build_qa_agent_tools_config,
)
from ..constant import BUILTIN_QA_AGENT_NAME, BUILTIN_QA_AGENT_SKILL_NAMES

DEFAULT_AGENT_TEMPLATE = "default"
LOCAL_AGENT_TEMPLATE = "local"
QA_AGENT_TEMPLATE = "qa"
SUPPORTED_AGENT_TEMPLATES = (
    DEFAULT_AGENT_TEMPLATE,
    LOCAL_AGENT_TEMPLATE,
    QA_AGENT_TEMPLATE,
)

LOCAL_TEMPLATE_SKILL_NAMES = ("make_plan",)
DEFAULT_TEMPLATE_SKILL_NAMES = (
    "make_plan",
    "file_reader",
    "pdf",
    "docx",
    "xlsx",
    "pptx",
    "cron",
    "browser_visible",
    "browser_cdp",
    "desktop_control",
    "agent_browser",
)
QA_TEMPLATE_DESCRIPTION = (
    "面向人力窝/仁励窝新员工的公司入职指引智能体，用于查询和引导新人了解公司常见入职事务。"
    "当前知识库对公司WiFi、OpenVPN配置、9号线小南门至久事附楼路线、BFC开心食堂路线、"
    "司印打印机、快递收发等内容覆盖较明确；对邮箱、共享盘、Cisco Jabber、会议室投屏、储物柜、"
    "6S、财务报销、员工手册、入职表单等内容可能仅有目录级或部分信息，回答时必须以知识库实际命中为准，"
    "不能自行补全。智能体应帮助新人完成入职待办梳理、问题分流和下一步引导；知识库未明确收录时，"
    "应提示联系IT、行政、HR或财务确认。"
)


@dataclass(frozen=True)
class AgentTemplateBuildResult:
    """Materialized result for creating an agent from a builtin template."""

    agent_config: AgentProfileConfig
    initial_skill_names: tuple[str, ...]
    md_template_id: str | None


def list_supported_agent_templates() -> tuple[str, ...]:
    """Return builtin agent template IDs supported by the application."""
    return SUPPORTED_AGENT_TEMPLATES


def get_workspace_md_template_id(template_id: str | None) -> str | None:
    """Map an agent template id to the workspace markdown template id."""
    if template_id in {LOCAL_AGENT_TEMPLATE, QA_AGENT_TEMPLATE}:
        return template_id
    return None


def build_agent_template(
    template_id: str,
    *,
    agent_id: str,
    workspace_dir: Path,
    fallback_language: str,
    name: str | None = None,
    description: str | None = None,
    language: str | None = None,
) -> AgentTemplateBuildResult:
    """Build a builtin template into a concrete agent configuration."""
    resolved_language = language or fallback_language or "zh"

    if template_id == DEFAULT_AGENT_TEMPLATE:
        if name is None:
            raise ValueError("Default template requires a name")
        agent_config = AgentProfileConfig(
            id=agent_id,
            name=name,
            description=description or "",
            workspace_dir=str(workspace_dir),
            template_id=template_id,
            language=resolved_language,
            channels=ChannelConfig(),
            mcp=MCPConfig(),
            heartbeat=HeartbeatConfig(),
            tools=ToolsConfig(),
        )
        return AgentTemplateBuildResult(
            agent_config=agent_config,
            initial_skill_names=DEFAULT_TEMPLATE_SKILL_NAMES,
            md_template_id=get_workspace_md_template_id(template_id),
        )

    if template_id == LOCAL_AGENT_TEMPLATE:
        agent_config = AgentProfileConfig(
            id=agent_id,
            name=name or "Local Agent",
            description=(
                description or "An agent running on local deployed models."
            ),
            workspace_dir=str(workspace_dir),
            template_id=template_id,
            language=resolved_language,
            channels=ChannelConfig(),
            mcp=MCPConfig(),
            heartbeat=HeartbeatConfig(),
            tools=build_local_agent_tools_config(),
        )
        return AgentTemplateBuildResult(
            agent_config=agent_config,
            initial_skill_names=LOCAL_TEMPLATE_SKILL_NAMES,
            md_template_id=get_workspace_md_template_id(template_id),
        )

    if template_id == QA_AGENT_TEMPLATE:
        agent_config = AgentProfileConfig(
            id=agent_id,
            name=name or BUILTIN_QA_AGENT_NAME,
            description=description or QA_TEMPLATE_DESCRIPTION,
            workspace_dir=str(workspace_dir),
            template_id=template_id,
            language=resolved_language,
            channels=ChannelConfig(),
            mcp=MCPConfig(),
            heartbeat=HeartbeatConfig(),
            tools=build_qa_agent_tools_config(),
        )
        return AgentTemplateBuildResult(
            agent_config=agent_config,
            initial_skill_names=tuple(BUILTIN_QA_AGENT_SKILL_NAMES),
            md_template_id=get_workspace_md_template_id(template_id),
        )

    raise ValueError(
        f"Unsupported template: {template_id!r}. "
        f"Expected one of {SUPPORTED_AGENT_TEMPLATES}.",
    )
