#!/usr/bin/env python3
"""
入职指引 — 检索知识库，按相关度排序表格展示

用法：
    python3 query.py "入职流程"
    python3 query.py "公司资料" --json
"""

import os
import sys
import json
import argparse
import urllib.request

API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-a54432e26d3b44138fe1ac84d6420b23")
APP_ID = os.environ.get("DASHSCOPE_APP_ID", "581e6a8127824e9283e363a1239407d3")
API_URL = "https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion"


def parse_content(content_str):
    result = {}
    for line in content_str.strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if value:
                result[key] = value
    return result


def query_api(prompt):
    payload = {"input": {"prompt": prompt}, "parameters": {}}
    url = API_URL.format(app_id=APP_ID)
    req = urllib.request.Request(
        url, json.dumps(payload).encode(),
        {"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = json.loads(resp.read().decode())
        text = raw.get("output", {}).get("text", "{}")
        return json.loads(text)


def build_table(rows, columns):
    if not rows:
        return "(无数据)"

    for row in rows:
        for col in columns:
            if col not in row:
                row[col] = ""

    col_widths = {}
    for col in columns:
        col_widths[col] = max(
            len(col),
            max(len(str(row.get(col, ""))) for row in rows)
        )

    lines = []

    hdr_cells = [" " + c.ljust(col_widths[c]) + " " for c in columns]
    lines.append("+" + "+".join(["-" * len(h) for h in hdr_cells]) + "+")
    lines.append("|" + "|".join(hdr_cells) + "|")

    sep = "+".join(["-" * (col_widths[c] + 2) for c in columns])
    lines.append("+" + sep + "+")

    for row in rows:
        cells = [" " + str(row.get(c, "")).ljust(col_widths[c]) + " " for c in columns]
        lines.append("|" + "|".join(cells) + "|")

    lines.append("+" + sep + "+")

    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="入职指引查询")
    p.add_argument("prompt", help="检索条件")
    p.add_argument("--json", action="store_true", help="JSON 原始格式输出")
    a = p.parse_args()

    print("检索: " + a.prompt)

    try:
        data = query_api(a.prompt)
    except Exception as e:
        print("查询失败: " + str(e))
        sys.exit(1)

    result = data.get("result", {})
    rewrite = result.get("rewriteQuery", a.prompt)
    chunks = result.get("chunkList", [])

    print("检索词: " + rewrite)
    print("命中: " + str(len(chunks)) + " 条\n")

    if a.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    rows = []
    for chunk in chunks:
        row = parse_content(chunk.get("content", ""))
        row["相关度"] = "{:.4f}".format(chunk.get("score", 0))
        rows.append(row)

    if rows:
        all_keys = set()
        for row in rows:
            all_keys.update(row.keys())
        table_cols = ["相关度"] + sorted([k for k in all_keys if k != "相关度"])
    else:
        table_cols = ["相关度"]

    print(build_table(rows, table_cols))
    print()
    print("共 " + str(len(rows)) + " 条记录")


if __name__ == "__main__":
    main()
