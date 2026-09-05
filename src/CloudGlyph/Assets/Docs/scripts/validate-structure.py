"""
validate-structure.py

Deterministic, dependency-free validation of the *directory-level* rules that the
CloudGlyph skill relies on but that previously had no machine check:

  1. **index.md coverage**  — every directory under a language root MUST contain an
     index.md (it may be empty). A directory without one is not a valid page dir.
  2. **Cross-language structural parity** — when multiple languages exist, each must
     have the SAME tree *shape*. Comparison is by numeric-prefix topology only, so
     translated directory names (en `00_user-registration` vs zh `00_用户注册`) still
     match, while a page/sub-page that exists in one language but not the other is an
     ERROR. (Names are intentionally ignored here — translation makes them differ.)
  3. **QuickStart ⇄ API feature-set parity (within one language)** — the immediate
     feature directories under the `1_*` (QuickStart) and `2_*` (API) top-level
     dimensions must be identical sets. Run per language, names compared literally.
     Only enforced when both dimensions are present; otherwise a WARN is emitted.

Structural-consistency items that need the *text* of pages (cross-page links, anchor
slugs, code authenticity, cross-dimension naming at depth) remain the job of
validate-links.py and the Review checklist — this script is the machine half of the
"every directory must contain index.md" and "cross-language parity" rules.

Usage:
    python validate-structure.py                 # auto-detect content root, all languages
    python validate-structure.py --lang en       # only one language dir
    python validate-structure.py <dir-or-file>   # scan an explicit path (a language root or the content root)

Exit code: 0 = clean, 1 = at least one ERROR.
"""

import argparse
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "bin", "obj", "__pycache__"}

_PREFIX_RE = re.compile(r"^(\d+)_")


def _prefix_num(name: str) -> int | None:
    m = _PREFIX_RE.match(name)
    return int(m.group(1)) if m else None


def lang_roots(target: Path, lang: str | None) -> list[Path]:
    """Resolve the language roots to scan from the target path."""
    if target.is_file():
        return [target.parent]
    if (target / "languages_index.json").exists():
        roots = sorted(
            p for p in target.iterdir()
            if p.is_dir() and not p.name.startswith(".") and p.name not in SKIP_DIRS
        )
    else:
        roots = [target]
    if lang:
        roots = [r for r in roots if r.name == lang]
    return roots


def check_index_coverage(root: Path) -> tuple[int, int]:
    """Every directory under *root* (recursively, excluding the root itself) must have index.md."""
    errors = 0
    for dirpath, dirnames, _files in os.walk(root):
        p = Path(dirpath)
        if p == root:
            continue
        rel = p.relative_to(root).as_posix()
        if any(seg in SKIP_DIRS for seg in p.relative_to(root).parts):
            continue
        if not (p / "index.md").is_file():
            errors += 1
            print(f"{root.name}/{rel}: ERROR directory has no index.md"
                  f" (every directory in a page tree must contain index.md, even an empty one)")
    return errors, 0


def _shape_key(name: str) -> str:
    """Sort/compare key: numeric prefix if present, else the whole name (grammar forbids unprefixed sub-dirs)."""
    n = _prefix_num(name)
    return f"{n:02d}" if n is not None else f"x_{name}"


def canonical_shape(dir_path: Path) -> tuple:
    """Structure signature of a dir: tuple of sorted (prefix-key, child-shape). Names are ignored
    except as the sort key when a child has no numeric prefix. Only directories are traversed."""
    children = []
    for entry in sorted(os.listdir(dir_path)):
        child = dir_path / entry
        if not child.is_dir():
            continue
        children.append((_shape_key(entry), canonical_shape(child)))
    children.sort(key=lambda kv: kv[0])
    return tuple(kv[1] for kv in children) if children else ()


def describe_shape(shape: tuple, indent: int = 0) -> str:
    if not shape:
        return ""
    lines = []
    for node in shape:
        if not node:
            lines.append("  " * indent + "- (page)")
        else:
            lines.append("  " * indent + "- (has sub-pages)")
            for sub in node:
                lines.append("  " * (indent + 1) + repr(sub))
    return "\n".join(lines) if lines else ""


def check_cross_language_parity(roots: list[Path]) -> tuple[int, int]:
    """Structural (numeric-prefix topology) equality across languages."""
    errors = 0
    if len(roots) < 2:
        return 0, 0
    shapes = {r.name: canonical_shape(r) for r in roots}
    base_name = roots[0].name
    base_shape = shapes[base_name]
    for name in list(shapes):
        if shapes[name] == base_shape:
            continue
        errors += 1
        print(f"PARITY: ERROR language '{name}' tree shape differs from '{base_name}'."
              f" Add/remove pages so every language has the same structure (page names may differ).")
    return errors, 0


def check_quickstart_api_parity(root: Path) -> tuple[int, int]:
    """Within one language: feature dirs under 1_* must equal feature dirs under 2_* (names literal)."""
    errors = 0
    warnings = 0
    by_prefix: dict[int, Path] = {}
    for entry in os.listdir(root):
        p = root / entry
        if not p.is_dir():
            continue
        n = _prefix_num(entry)
        if n in (1, 2):
            by_prefix[n] = p

    d1, d2 = by_prefix.get(1), by_prefix.get(2)
    if d1 is None and d2 is None:
        return 0, 0
    if d1 is None or d2 is None:
        warnings += 1
        missing = "1_QuickStart" if d1 is None else "2_API"
        print(f"{root.name}: WARN dimension '{missing}' absent — cannot verify QuickStart/API feature parity")
        return 0, warnings

    def features(d: Path) -> list[str]:
        return sorted(e for e in os.listdir(d) if (d / e).is_dir())

    f1, f2 = features(d1), features(d2)
    if f1 != f2:
        errors += 1
        only_qs = sorted(set(f1) - set(f2))
        only_api = sorted(set(f2) - set(f1))
        print(f"{root.name}: ERROR feature sets differ between QuickStart ('{d1.name}') and API ('{d2.name}')")
        for f in only_qs:
            print(f"    only in QuickStart: {f}")
        for f in only_api:
            print(f"    only in API:        {f}")
    return errors, warnings


def main() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    parser = argparse.ArgumentParser(description="Validate wiki directory-structure rules")
    parser.add_argument("path", nargs="?", help="file or directory to scan (default: auto-detect content root)")
    parser.add_argument("--lang", help="only scan this language subdir (e.g. en, zh)")
    args = parser.parse_args()

    if args.path:
        target = Path(args.path)
    else:
        content = Path(__file__).resolve().parent.parent / "content"
        target = content / args.lang if args.lang else content

    if not target.exists():
        print(f"ERROR: path not found: {target}", file=sys.stderr)
        sys.exit(2)

    roots = lang_roots(target, args.lang)
    total_errors = 0
    total_warns = 0

    for root in roots:
        errors, warns = check_index_coverage(root)
        total_errors += errors
        total_warns += warns
        errors, warns = check_quickstart_api_parity(root)
        total_errors += errors
        total_warns += warns

    errors, warns = check_cross_language_parity(roots)
    total_errors += errors
    total_warns += warns

    print(f"[structure] scanned {len(roots)} language root(s); {total_errors} error(s), {total_warns} warning(s)")
    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()
