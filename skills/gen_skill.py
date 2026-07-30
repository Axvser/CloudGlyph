"""
gen_skill.py

Scans skills/{lang}/ for sub-skill directories containing Meta.md,
parses [#pipeline] and [#description] tags, dynamically constructs
the workflow section, and inlines each sub-skill's SKILL.md content
after its corresponding workflow step.

Supports multiple languages via --lang parameter.

Usage:
    python skills/gen_skill.py                  # default: en
    python skills/gen_skill.py --lang zh        # Chinese
    python skills/gen_skill.py --lang en        # English

Or from any working directory — the script auto-detects its location relative
to the skills/ folder.
"""

import argparse
import os
import re
import sys
from typing import Optional

# Script lives in skills/ — use that as the root
SKILLS_ROOT = os.path.abspath(os.path.dirname(__file__))

WORKFLOW_PLACEHOLDER = "<!-- WORKFLOW -->"

_SKIP_DIRS = {"__pycache__", ".git", ".github"}

_TAG_RE = re.compile(r"^\[#(\w+)\](?:\s+(.*))?$")

_HEADING_RE = re.compile(r"^(#{1,6})\s")


def get_paths(lang: str) -> tuple[str, str]:
    template_path = os.path.join(SKILLS_ROOT, lang, "TEMPLATE.md")
    skill_output = os.path.join(SKILLS_ROOT, "SKILL.md")
    return template_path, skill_output


def parse_meta(path: str) -> dict[str, str]:
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


def demote_headings(text: str, levels: int = 1) -> str:
    if levels <= 0:
        return text

    lines = text.split("\n")
    result: list[str] = []
    for line in lines:
        m = _HEADING_RE.match(line)
        if m:
            prefix = m.group(1)
            rest = line[m.end() - 1:]
            result.append(f"{'#' * (len(prefix) + levels)}{rest}")
        else:
            result.append(line)
    return "\n".join(result)


def collect_skills(lang: str) -> list[dict]:
    lang_root = os.path.join(SKILLS_ROOT, lang)
    skills: list[dict] = []

    for entry in sorted(os.listdir(lang_root)):
        sub_path = os.path.join(lang_root, entry)
        if not os.path.isdir(sub_path):
            continue
        if entry.startswith(".") or entry in _SKIP_DIRS:
            continue

        meta_path = os.path.join(sub_path, "Meta.md")
        if not os.path.isfile(meta_path):
            continue

        meta = parse_meta(meta_path)
        pipeline = meta.get("pipeline", "")
        description = meta.get("description", "")

        if not pipeline:
            print(f"[gen_skill] WARNING: {entry}/Meta.md has no [#pipeline] - skipping", file=sys.stderr)
            continue

        skill_path = os.path.join(sub_path, "SKILL.md")
        if not os.path.isfile(skill_path):
            print(f"[gen_skill] WARNING: {entry}/SKILL.md not found - skipping", file=sys.stderr)
            continue

        skills.append({
            "pipeline": pipeline,
            "description": description,
            "sub_dir": entry,
            "skill_path": skill_path,
        })
        print(f"[gen_skill] Collected: {entry} -> pipeline={pipeline}")

    skills.sort(key=lambda s: int(s["pipeline"]))
    return skills


def generate_workflow_with_content(skills: list[dict]) -> str:
    parts: list[str] = []

    for s in skills:
        parts.append(f"> {s['pipeline']}.{s['description']}")
        parts.append("")

        try:
            with open(s["skill_path"], "r", encoding="utf-8") as f:
                content = f.read()
            content = demote_headings(content, levels=1)
            parts.append(content)
            parts.append("")
        except Exception as e:
            print(f"[gen_skill] WARNING: Error reading {s['skill_path']}: {e}", file=sys.stderr)

    return "\n".join(parts).rstrip("\n") + "\n"


def assemble_skill_md(skills: list[dict], lang: str) -> str:
    template_path, _ = get_paths(lang)
    if not os.path.isfile(template_path):
        print(f"[gen_skill] ERROR: TEMPLATE.md not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    if WORKFLOW_PLACEHOLDER not in template_content:
        print(f"[gen_skill] ERROR: Placeholder '{WORKFLOW_PLACEHOLDER}' not found in TEMPLATE.md", file=sys.stderr)
        sys.exit(1)

    workflow_md = generate_workflow_with_content(skills)
    template_content = template_content.replace(WORKFLOW_PLACEHOLDER, workflow_md, 1)

    return template_content


def main():
    parser = argparse.ArgumentParser(description="Generate SKILL.md from Meta.md files")
    parser.add_argument("--lang", default="en", help="Language code (e.g. 'en', 'zh'). Default: en")
    args = parser.parse_args()
    lang = args.lang

    template_path, skill_output_path = get_paths(lang)

    print(f"[gen_skill] Language: {lang}")
    print(f"[gen_skill] Template: {template_path}")
    print(f"[gen_skill] Output: {skill_output_path}")
    print("[gen_skill] Scanning skills/ for Meta.md files...")
    skills = collect_skills(lang)

    if not skills:
        print("[gen_skill] No sub-skills with Meta.md found.")
        sys.exit(1)

    print(f"[gen_skill] Found {len(skills)} sub-skill(s)")

    full_content = assemble_skill_md(skills, lang)

    with open(skill_output_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"[gen_skill] Generated: {skill_output_path}")
    print("[gen_skill] Done.")


if __name__ == "__main__":
    main()
