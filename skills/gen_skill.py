"""
gen_skill.py

Collects Meta.md from each sub-skill directory, parses [#Tag] markers,
groups skills by [#group], and injects the generated Sub-Skill Directory
Index into Base.md to produce the final SKILL.md.

Usage:
    python skills/gen_skill.py

Or from any working directory — the script auto-detects its location relative
to the skills/ folder.
"""

import os
import re
import sys
from typing import Optional

# ── Paths ──────────────────────────────────────────────────────────────

# Script lives in skills/ — use that as the root
SKILLS_ROOT = os.path.abspath(os.path.dirname(__file__))
BASE_PATH = os.path.join(SKILLS_ROOT, "Base.md")
SKILL_OUTPUT_PATH = os.path.join(SKILLS_ROOT, "SKILL.md")
TABLE_OUTPUT_PATH = os.path.join(SKILLS_ROOT, "INDEX.md")

# Directories to skip when scanning for sub-skills
_SKIP_DIRS = {"__pycache__", ".git", ".github"}

# Regex to detect a [#Tag] at the start of a line
_TAG_RE = re.compile(r"^\[#(\w+)\](?:\s+(.*))?$")


# ── Meta.md Parser ────────────────────────────────────────────────────

def parse_meta(path: str) -> dict[str, str]:
    """Parse a Meta.md file and return a dict of {tag: content}.

    Tags are identified by ``[#tagname]`` at the start of a line.
    Content continues until the next ``[#tagname]`` or EOF.
    Leading/trailing blank lines are stripped from each tag's content.
    """
    result: dict[str, str] = {}
    current_tag: Optional[str] = None
    current_lines: list[str] = []

    def flush():
        if current_tag is not None:
            text = "\n".join(current_lines).strip()
            if text:
                result[current_tag] = text

    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n")
                m = _TAG_RE.match(line)
                if m:
                    flush()
                    current_tag = m.group(1)
                    trailing = m.group(2)
                    current_lines = [trailing] if trailing else []
                elif current_tag is not None:
                    current_lines.append(line)
        flush()
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"[gen_skill] WARNING: Error reading {path}: {e}", file=sys.stderr)

    return result


# ── Table Generator ───────────────────────────────────────────────────

def escape_pipe(text: str) -> str:
    """Escape pipe characters for markdown table cells."""
    return text.replace("|", "\\|")


# Preferred group display order (any group not listed appears at the end)
_GROUP_ORDER = [
    "基础设置",
    "约束加载",
    "内容编写",
    "质量保障",
]


def _group_sort_key(group: str) -> int:
    try:
        return _GROUP_ORDER.index(group)
    except ValueError:
        return len(_GROUP_ORDER)


def generate_skill_index(skills: list[dict]) -> str:
    """Generate the full Sub-Skill Directory Index markdown section.

    *skills* is a list of dicts with keys: group, route, description, workflow, phase, rules.
    Skills are grouped by [group] in the order defined by _GROUP_ORDER.
    Returns the markdown string (without the surrounding --- separators).
    """
    # Group by [group]
    groups: dict[str, list[dict]] = {}
    for s in skills:
        group = s.get("group", "Uncategorized")
        groups.setdefault(group, []).append(s)

    # Sort groups by preferred order
    sorted_groups = sorted(groups.items(), key=lambda kv: _group_sort_key(kv[0]))

    # Sort skills within each group by route
    for group_name in groups:
        groups[group_name].sort(key=lambda s: s.get("route", ""))

    parts: list[str] = []
    parts.append(
        "子技能按场景组织到独立目录中。Agent 仅在用户请求匹配对应场景时加载子技能的 "
        "`SKILL.md`，切勿预加载。"
    )
    parts.append("")

    for group_name, items in sorted_groups:
        parts.append(f"### {group_name}")
        parts.append("")
        parts.append("| 路径 | 场景 | 触发关键词 |")
        parts.append("|---|---|---|")

        for s in items:
            route = s.get("route", "")
            description = s.get("description", "")
            workflow = s.get("workflow", "")
            phase = s.get("phase", "")
            depth = s.get("depth", 0)

            # Indent route by nesting depth
            indent = "  " * depth
            display_route = route
            if depth > 0:
                display_route = f"{indent}{route}"

            # Combine description + phase info
            scenario = description
            if phase:
                scenario = f"{description} — {phase}"

            # Trigger keywords from workflow lines
            triggers = _format_workflow(workflow)

            parts.append(
                f"| `{escape_pipe(display_route)}`"
                f" | {escape_pipe(scenario)}"
                f" | {escape_pipe(triggers)} |"
            )

        parts.append("")

    return "\n".join(parts).rstrip("\n") + "\n"


def generate_flat_table(skills: list[dict]) -> str:
    """Generate a standalone mapping table Markdown file.

    Produces a single flat table with columns: 分组, 路径, 场景, 触发关键词.
    """
    # Group and sort same as generate_skill_index
    groups: dict[str, list[dict]] = {}
    for s in skills:
        group = s.get("group", "Uncategorized")
        groups.setdefault(group, []).append(s)

    sorted_groups = sorted(groups.items(), key=lambda kv: _group_sort_key(kv[0]))

    for group_name in groups:
        groups[group_name].sort(key=lambda s: s.get("route", ""))

    parts: list[str] = []
    parts.append("# 技能索引 — 对照表")
    parts.append("")
    parts.append("| 分组 | 路径 | 场景 | 触发关键词 |")
    parts.append("|---|---|---|---|")

    for group_name, items in sorted_groups:
        first = True
        for s in items:
            route = s.get("route", "")
            description = s.get("description", "")
            workflow = s.get("workflow", "")
            phase = s.get("phase", "")
            depth = s.get("depth", 0)

            indent = "  " * depth
            display_route = route
            if depth > 0:
                display_route = f"{indent}{route}"

            scenario = description
            if phase:
                scenario = f"{description} — {phase}"

            triggers = _format_workflow(workflow)

            cell_group = group_name if first else ""
            parts.append(
                f"| {escape_pipe(cell_group)}"
                f" | `{escape_pipe(display_route)}`"
                f" | {escape_pipe(scenario)}"
                f" | {escape_pipe(triggers)} |"
            )
            first = False

    parts.append("")
    return "\n".join(parts) + "\n"


def _format_workflow(workflow_text: str) -> str:
    """Format workflow trigger keywords into a comma-separated string.

    Handles various list formats:
    - "- \"keyword\"" (markdown list with quoted strings)
    - "- keyword" (plain markdown list)
    - "keyword1, keyword2" (comma-separated)
    """
    if not workflow_text:
        return ""

    lines = workflow_text.strip().split("\n")
    keywords: list[str] = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Remove leading "- " or "* " (markdown list markers)
        if line.startswith("- "):
            line = line[2:]
        elif line.startswith("* "):
            line = line[2:]
        # Strip surrounding quotes
        line = line.strip('"').strip("'")
        if line:
            keywords.append(line)

    return ", ".join(keywords)


# ── Main ──────────────────────────────────────────────────────────────

def _collect_skills_recursive(
    search_root: str,
    skills: list[dict],
    parent_meta: Optional[dict] = None,
    depth: int = 0,
) -> None:
    """Recursively walk *search_root* subdirectories and collect Meta.md data.

    *parent_meta* is the parsed Meta.md of the parent directory (used for
    group inheritance). *depth* tracks nesting level for indented display.
    """
    for entry in sorted(os.listdir(search_root)):
        sub_path = os.path.join(search_root, entry)
        if not os.path.isdir(sub_path):
            continue
        if entry.startswith(".") or entry in _SKIP_DIRS:
            continue

        meta_path = os.path.join(sub_path, "Meta.md")
        meta = parse_meta(meta_path) if os.path.isfile(meta_path) else {}

        # Build skill entry if Meta.md exists and has at minimum a description
        if meta:
            # Inherit group from parent if not explicitly set
            group = meta.get("group") or (parent_meta.get("group") if parent_meta else None) or "Uncategorized"

            # Auto-generate route relative to SKILLS_ROOT if not explicitly set
            route = meta.get("route")
            if not route:
                rel = os.path.relpath(sub_path, SKILLS_ROOT).replace("\\", "/")
                route = f"skills/{rel}/SKILL.md"
                meta["route"] = route

            skill = {
                "group": group,
                "route": route,
                "description": meta.get("description", ""),
                "workflow": meta.get("hook", "") or meta.get("workflow", ""),
                "rules": meta.get("rules", ""),
                "phase": meta.get("phase", ""),
                "depth": depth,
            }
            skills.append(skill)
            print(
                f"[gen_skill] Collected: {'  ' * depth}{os.path.relpath(sub_path, SKILLS_ROOT)}"
                f" → group={group} (depth={depth})"
            )

        # Recurse into this subdirectory (pass current meta for group inheritance)
        _collect_skills_recursive(sub_path, skills, meta if meta else parent_meta, depth + 1)


def collect_skills() -> list[dict]:
    """Walk SKILLS_ROOT subdirectories (recursively), collect Meta.md data."""
    skills: list[dict] = []
    _collect_skills_recursive(SKILLS_ROOT, skills, parent_meta=None, depth=0)
    return skills


def assemble_skill_md(skills: list[dict]) -> str:
    """Read Base.md, inject the generated skill index, return full content."""
    if not os.path.isfile(BASE_PATH):
        print(f"[gen_skill] ERROR: Base.md not found at {BASE_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(BASE_PATH, "r", encoding="utf-8") as f:
        base_content = f.read()

    index_md = generate_skill_index(skills)
    placeholder = "<!-- SKILL_INDEX -->"
    if placeholder not in base_content:
        print(
            f"[gen_skill] ERROR: Placeholder '{placeholder}' not found in Base.md",
            file=sys.stderr,
        )
        sys.exit(1)

    return base_content.replace(placeholder, index_md, 1)


def main():
    print("[gen_skill] Scanning skills/ for Meta.md files...")
    skills = collect_skills()

    if not skills:
        print("[gen_skill] No sub-skills with Meta.md found — SKILL.md will have an empty index.")
    else:
        print(f"[gen_skill] Found {len(skills)} sub-skill(s) with Meta.md")

    # Generate SKILL.md (Base.md + skill index)
    full_content = assemble_skill_md(skills)

    with open(SKILL_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"[gen_skill] Generated: {SKILL_OUTPUT_PATH}")

    # Generate standalone index table
    table_md = generate_flat_table(skills)
    with open(TABLE_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(table_md)

    print(f"[gen_skill] Generated: {TABLE_OUTPUT_PATH}")
    print("[gen_skill] Done.")


if __name__ == "__main__":
    main()
