#!/usr/bin/env python3
"""
scpe.py — engine for the SCPE (Spec-Compiled Product Engineering) workflow.

Everything is plain Markdown inside one product workspace. The workspace root is
`SCPE_WORKSPACE` when set, otherwise the first directory walking up from the cwd
that contains `product_vision.md` and `features/`. Templates live in
`../templates/` relative to this file. Standard library only.

Subcommands:
    init <name> [--path DIR] [--app NAME:TYPE]... [--no-git]
    feature <slug> "<Title>"
    epic <feature> <slug> "<Title>"
    validate [--strict]
    gate-check <feature>/<epic>
    set-state <feature>/<epic> <State> --by "<who>" [--note "..."]
    mark-stale [<path>] [--from-hook]
    status [--json] [--write]
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    # Windows consoles default to a non-UTF-8 codepage; the ✅/❌ markers below
    # would otherwise crash this script there.
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"

ROOT_FILES = [
    "index.md", "product_vision.md", "roadmap.md", "glossary.md",
    "architecture.md", "technical_deal.md", "team_playbook.md", "quick_status.md",
]
ROOT_DIRS = ["apps", "features", "assets"]
# Compact layout ("tiny SCPE"): no apps/ or assets/ folders, one app.md at the
# workspace root, and one features/roadmap.md instead of a feat_roadmap.md per
# feature. Detected, never configured, so classic workspaces are unaffected.
COMPACT_ROOT_DIRS = ["features"]
FEATURE_FILES = ["index.md", "feat_roadmap.md", "quick_status.md"]
COMPACT_FEATURE_FILES = ["index.md", "quick_status.md"]
EPIC_FILES = ["index.md", "plan.md", "tasks.md", "quick_status.md", "epic_roadmap.md"]
APP_FIELDS = [
    "name", "type", "description", "stack", "standards",
    "entrypoint", "depends_on", "run", "test",
]
FEATURE_FIELDS = ["goal", "users", "bounded_context", "business_value"]

STATES = ["Draft", "Ready", "WIP", "Blocked", "Done", "Stale"]
# SCPE_METHOD.md §4.4 (state machine) and §4.5 (spec drift).
TRANSITIONS = {
    "Draft": {"Ready"},
    "Ready": {"WIP", "Blocked"},
    "WIP": {"Done", "Blocked"},
    "Blocked": {"Ready", "Draft"},
    "Done": {"Stale"},
    "Stale": {"Ready", "Done"},
}

SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")
STATUS_START = "<!-- scpe:status:start -->"
STATUS_END = "<!-- scpe:status:end -->"


# ---------------------------------------------------------------- infra -----

def die(msg: str, code: int = 1) -> "NoReturn":  # type: ignore[valid-type]
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(code)


def today() -> str:
    return dt.date.today().isoformat()


def is_workspace(path: Path) -> bool:
    return (path / "product_vision.md").is_file() and (path / "features").is_dir()


def find_workspace(start: Path | None = None) -> Path | None:
    env = os.environ.get("SCPE_WORKSPACE")
    if env:
        p = Path(env).expanduser().resolve()
        return p if is_workspace(p) else None
    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if is_workspace(p):
            return p
    return None


def workspace() -> Path:
    ws = find_workspace()
    if ws is None:
        die(
            "no SCPE workspace found (a folder with product_vision.md and features/).\n"
            "   cd into the product workspace, set SCPE_WORKSPACE, or run `scpe.py init`."
        )
    return ws


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="ignore") if p.is_file() else ""
    except Exception:
        return ""



def render(template: Path, values: dict) -> str:
    text = template.read_text(encoding="utf-8")
    for key, val in values.items():
        text = text.replace("{{" + key + "}}", str(val))
    return text


def write_new(dest: Path, text: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")


def check_slug(slug: str, what: str) -> None:
    if not SLUG_RE.match(slug):
        die(f"invalid {what} slug '{slug}': use lowercase letters, digits, '-' or '_'.")


# ------------------------------------------------------------- markdown -----

def field(text: str, name: str) -> str | None:
    m = re.search(rf"^- \*\*{re.escape(name)}:\*\*[ \t]*(.*)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def section(text: str, heading: str) -> str | None:
    """Body of `## heading` up to the next `## ` heading, or None if absent."""
    m = re.search(rf"^## {re.escape(heading)}[ \t]*$", text, re.MULTILINE)
    if not m:
        return None
    rest = text[m.end():]
    nxt = re.search(r"^## ", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def append_to_section(text: str, heading: str, line: str, placeholder: str | None = None) -> str:
    """Append a list line at the end of `## heading`, replacing a placeholder line."""
    m = re.search(rf"^## {re.escape(heading)}[ \t]*$", text, re.MULTILINE)
    if not m:
        return text.rstrip("\n") + f"\n\n## {heading}\n\n{line}\n"
    start = m.end()
    nxt = re.search(r"^## ", text[start:], re.MULTILINE)
    end = start + nxt.start() if nxt else len(text)
    body = text[start:end]
    if placeholder and placeholder in body:
        body = body.replace(placeholder, line, 1).rstrip("\n") + "\n"
    else:
        body = body.rstrip("\n") + f"\n{line}\n"
    tail = text[end:]
    return text[:start] + body + ("\n" if tail else "") + tail


def epic_state(qs_text: str) -> tuple[str | None, int]:
    found = re.findall(r"^- \*\*state:\*\*[ \t]*(\S*)", qs_text, re.MULTILINE)
    if not found:
        found = re.findall(r"^- \*\*status:\*\*[ \t]*`?([A-Za-z]+)`?", qs_text, re.IGNORECASE | re.MULTILINE)
    if not found:
        for line in qs_text.strip().splitlines():
            clean = line.strip("`*-_ \t#")
            words = clean.split()
            if words and words[0] in STATES:
                found = [words[0]]
                break
    return (found[0] if found else None), len(found)


def rule_ids(text: str) -> list[str]:
    return re.findall(r"\*\*(R\d+)\b", text)


def example_ids(text: str) -> list[str]:
    return re.findall(r"\*\*(S\d+)\b", text)


def list_items(body: str) -> list[str]:
    return [l.strip() for l in strip_comments(body).splitlines() if re.match(r"\s*(-|\d+\.)\s+\S", l)]


def tasks_of(tasks_text: str) -> list[tuple[bool, str]]:
    return [
        (m.group(1).lower() == "x", m.group(2))
        for m in re.finditer(r"^\s*- \[( |x|X)\]\s+(.*)$", strip_comments(tasks_text), re.MULTILINE)
    ]


def get_epic_state(epic_dir: Path) -> tuple[str | None, int]:
    """Return (state, count). Checks tasks.toml first, then quick_status.md."""
    tasks_toml = epic_dir / "tasks.toml"
    if tasks_toml.is_file():
        try:
            with open(tasks_toml, "rb") as f:
                data = tomllib.load(f)
            st = data.get("state", {}).get("current")
            if st in STATES:
                return st, 1
        except Exception:
            pass
    qs_path = epic_dir / "quick_status.md"
    if qs_path.is_file():
        return epic_state(read(qs_path))
    return None, 0


def get_epic_tasks(epic_dir: Path) -> list[tuple[bool, str]]:
    """Return [(done, desc), ...]. Checks tasks.toml first, then tasks.md."""
    tasks_toml = epic_dir / "tasks.toml"
    if tasks_toml.is_file():
        try:
            with open(tasks_toml, "rb") as f:
                data = tomllib.load(f)
            res = []
            for t in data.get("task", []):
                done = bool(t.get("done") or str(t.get("status", "")).lower() == "done")
                title = t.get("title", "")
                covers = ", ".join(t.get("covers", []))
                cov_str = f" ({covers})" if covers else ""
                desc = f"{t.get('id', '')} — {title}{cov_str}".strip()
                res.append((done, desc))
            if res:
                return res
        except Exception:
            pass
    tasks_md = epic_dir / "tasks.md"
    if tasks_md.is_file():
        return tasks_of(read(tasks_md))
    return []


def is_flat_feature(p: Path) -> bool:
    """True if directory is a flat feature (has plan.md or tasks.toml directly)."""
    return p.is_dir() and ((p / "plan.md").is_file() or (p / "tasks.toml").is_file())


def next_feature_prefix(ws: Path) -> str:
    """Scan features/ for NNN- prefix and return the next formatted 3-digit string."""
    fdir = ws / "features"
    if not fdir.is_dir():
        return "001"
    nums = []
    for p in fdir.iterdir():
        if p.is_dir():
            m = re.match(r"^(\d{3})-", p.name)
            if m:
                nums.append(int(m.group(1)))
    next_num = max(nums) + 1 if nums else 1
    return f"{next_num:03d}"



# ------------------------------------------------------------ workspace -----

def features(ws: Path) -> list[Path]:
    fdir = ws / "features"
    return sorted(p for p in fdir.iterdir() if p.is_dir()) if fdir.is_dir() else []


def epics(feature_dir: Path) -> list[Path]:
    if is_flat_feature(feature_dir):
        return [feature_dir]
    edir = feature_dir / "epics"
    if edir.is_dir():
        return sorted(p for p in edir.iterdir() if p.is_dir())
    return sorted(
        p for p in feature_dir.iterdir()
        if p.is_dir() and (p.name.startswith("epic") or (p / "quick_status.md").is_file() or (p / "plan.md").is_file() or (p / "tasks.toml").is_file())
    )


def resolve_epic(ws: Path, ref: str) -> Path:
    ref_clean = ref.strip("/")
    parts = ref_clean.split("/")
    if len(parts) == 1:
        # Check flat feature: features/<ref>
        p = ws / "features" / parts[0]
        if is_flat_feature(p):
            return p
        # Check matching prefix or substring (e.g. '001' or 'pix' matching '001-pix-checkout')
        for feat in features(ws):
            if is_flat_feature(feat):
                if feat.name == parts[0] or feat.name.startswith(f"{parts[0]}-") or feat.name.endswith(f"-{parts[0]}") or parts[0] in feat.name:
                    return feat
        die(f"feature/epic '{ref}' not found in features/.")
    elif len(parts) == 2:
        path = ws / "features" / parts[0] / "epics" / parts[1]
        if not path.is_dir():
            path = ws / "features" / parts[0] / parts[1]
        if not path.is_dir():
            die(f"epic not found: features/{parts[0]}/{parts[1]} (or under epics/)")
        return path
    else:
        die(f"invalid reference '{ref}'. Expected <feature> or <feature>/<epic>.")


def is_compact(ws: Path) -> bool:
    """True for the compact layout: a root app.md and no apps/ folder."""
    return (ws / "app.md").is_file() and not (ws / "apps").is_dir()


def app_manifests(ws: Path) -> list[Path]:
    """Every app.toml or app.md in the workspace, whichever layout it uses."""
    if is_compact(ws):
        return [ws / "app.toml"] if (ws / "app.toml").is_file() else [ws / "app.md"]
    apps_dir = ws / "apps"
    if not apps_dir.is_dir():
        return []
    res = []
    for a in sorted(p for p in apps_dir.iterdir() if p.is_dir()):
        if (a / "app.toml").is_file():
            res.append(a / "app.toml")
        elif (a / "app.md").is_file():
            res.append(a / "app.md")
    return res


def source_roots(ws: Path) -> list[Path]:
    """Where to look for code when checking <epic>#S# test names.

    Classic keeps code under apps/. Compact keeps it outside the workspace, so
    app.md may name it with `- **source:** <path>`; otherwise the workspace's
    parent is scanned, minus the workspace itself.
    """
    if not is_compact(ws):
        return [ws / "apps"]
    declared = field(read(ws / "app.md"), "source")
    if declared:
        candidate = (ws / declared.strip().strip("`")).resolve()
        if candidate.is_dir():
            return [candidate]
    return [ws.parent]


def epic_line(epic_slug: str, state: str) -> str:
    return f"- [{epic_slug}](epics/{epic_slug}/index.md) — {state}"


def write_state(epic_dir: Path, new: str, who: str, note: str) -> str:
    qs_path = epic_dir / "quick_status.md"
    text = read(qs_path)
    old, count = epic_state(text)
    if count == 0:
        die(f"{qs_path}: expected state line, found none.")
    if re.search(r"^- \*\*state:\*\*", text, re.MULTILINE):
        text = re.sub(r"^(- \*\*state:\*\*)[ \t]*\S*", rf"\g<1> {new}", text, count=1, flags=re.MULTILINE)
    else:
        text = f"- **state:** {new}\n\n" + text.strip() + "\n"
    entry = f"- {today()} — {old} → {new} by {who}." + (f" {note.strip()}" if note.strip() else "")
    text = append_to_section(text, "Log", entry)
    qs_path.write_text(text, encoding="utf-8")

    # keep the feature index epic list in sync
    feat_dir = epic_dir.parent.parent if epic_dir.parent.name == "epics" else epic_dir.parent
    feat_index = feat_dir / "index.md"
    if feat_index.is_file():
        ftext = read(feat_index)
        slug = epic_dir.name
        pattern = rf"^- \[{re.escape(slug)}\]\((?:epics/)?{re.escape(slug)}/index\.md\).*$"
        if re.search(pattern, ftext, re.MULTILINE):
            ftext = re.sub(pattern, epic_line(slug, new), ftext, count=1, flags=re.MULTILINE)
            feat_index.write_text(ftext, encoding="utf-8")
    return old or "?"


def git(ws: Path, *args: str) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(ws), *args], capture_output=True, text=True, check=True)
        return out.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def looks_stale(ws: Path, epic_dir: Path) -> bool:
    """A Done epic whose plan.md changed after its quick_status.md (git-based)."""
    if git(ws, "rev-parse", "--is-inside-work-tree") is None:
        return False
    plan, qs = epic_dir / "plan.md", epic_dir / "quick_status.md"
    plan_dirty = bool((git(ws, "status", "--porcelain", "--", str(plan)) or "").strip())
    qs_dirty = bool((git(ws, "status", "--porcelain", "--", str(qs)) or "").strip())
    if plan_dirty and not qs_dirty:
        return True
    if plan_dirty or qs_dirty:
        return False
    try:
        plan_ts = int((git(ws, "log", "-1", "--format=%ct", "--", str(plan)) or "0").strip() or 0)
        qs_ts = int((git(ws, "log", "-1", "--format=%ct", "--", str(qs)) or "0").strip() or 0)
    except ValueError:
        return False
    return plan_ts > qs_ts


# ------------------------------------------------------------ subcommands ---

def cmd_init(args) -> int:
    base = Path(args.path).expanduser().resolve() if args.path else Path.cwd().resolve()
    check_slug(args.name, "product")
    dest = base / args.name
    if dest.exists() and any(dest.iterdir()):
        die(f"{dest} already exists and is not empty. Aborting to avoid overwriting.")

    apps = []
    for spec in args.app or []:
        name, _, kind = spec.partition(":")
        check_slug(name, "app")
        apps.append((name, kind or "backend-api"))

    apps_list = "\n".join(f"- [{n}](apps/{n}/app.md) — {k}" for n, k in apps) or "_No apps yet._"
    values = {"product_name": args.name, "date": today(), "apps_list": apps_list}

    for name in ROOT_FILES + ["CLAUDE.md", "AGENTS.md"]:
        write_new(dest / name, render(TEMPLATES_DIR / "product" / name, values))
    for d in ROOT_DIRS:
        (dest / d).mkdir(parents=True, exist_ok=True)
    (dest / "assets" / ".gitkeep").touch()
    (dest / "features" / ".gitkeep").touch()
    if not apps:
        (dest / "apps" / ".gitkeep").touch()
    for name, kind in apps:
        write_new(
            dest / "apps" / name / "app.md",
            render(TEMPLATES_DIR / "app" / "app.md", {**values, "app_name": name, "app_type": kind}),
        )

    git_msg = "git: skipped (--no-git)"
    if not args.no_git:
        try:
            subprocess.run(["git", "init", "-q", str(dest)], check=True)
            git_msg = "git: repository initialized (nothing committed yet)"
        except (subprocess.CalledProcessError, FileNotFoundError):
            git_msg = "git: not available — initialize the repository manually"

    print(f"✅ SCPE workspace created at {dest}")
    print(f"   {git_msg}")
    print("   Next: Upstream — fill product_vision.md, glossary.md and technical_deal.md,")
    print("   then open the most critical feature with `scpe.py feature <slug> \"<Title>\"`.")
    return 0


def cmd_feature(args) -> int:
    ws = workspace()
    raw_slug = args.slug.strip()
    if re.match(r"^\d{3}-", raw_slug):
        slug = raw_slug
    else:
        prefix = next_feature_prefix(ws)
        slug = f"{prefix}-{raw_slug}"
    check_slug(slug, "feature")

    dest = ws / "features" / slug
    if dest.exists():
        die(f"features/{slug} already exists. Aborting to avoid overwriting.")

    dest.mkdir(parents=True, exist_ok=True)

    if getattr(args, "branch", False):
        branch_name = f"feat/{slug}"
        print(f"🌿 Creating and checking out branch '{branch_name}'...")
        git(ws, "checkout", "-b", branch_name)

    values = {
        "feature_slug": slug, "feature_title": args.title,
        "epic_slug": slug, "epic_title": args.title,
        "date": today(), "today": today()
    }

    # Write plan.md and tasks.toml in features/<slug>/
    plan_template = TEMPLATES_DIR / "epic" / "plan.md"
    tasks_template = TEMPLATES_DIR / "feature" / "tasks.toml"
    if not tasks_template.is_file():
        tasks_template = TEMPLATES_DIR / "epic" / "tasks.toml"

    write_new(dest / "plan.md", render(plan_template, values))
    if tasks_template.is_file():
        write_new(dest / "tasks.toml", render(tasks_template, values))

    index = ws / "index.md"
    if index.is_file():
        line = f"- [{args.title}](features/{slug}/plan.md)"
        index.write_text(append_to_section(read(index), "Features", line, "_No features yet._"), encoding="utf-8")

    if (ws / "roadmap.md").is_file():
        sync_roadmap_file(ws)

    print(f"✅ Feature created at features/{slug}/ (state: Draft)")
    return 0


def cmd_epic(args) -> int:
    ws = workspace()
    check_slug(args.slug, "epic")
    feature_dir = ws / "features" / args.feature
    if not (feature_dir / "index.md").is_file():
        die(f"feature '{args.feature}' not found. Create it first with `scpe.py feature`.")
    dest = feature_dir / "epics" / args.slug
    if dest.exists():
        die(f"features/{args.feature}/epics/{args.slug} already exists. Aborting to avoid overwriting.")
    bc = field(read(feature_dir / "index.md"), "bounded_context") or ""
    values = {
        "feature_slug": args.feature, "epic_slug": args.slug, "epic_title": args.title,
        "bounded_context": bc, "date": today(),
    }
    for name in EPIC_FILES:
        write_new(dest / name, render(TEMPLATES_DIR / "epic" / name, values))

    index = feature_dir / "index.md"
    index.write_text(
        append_to_section(read(index), "Epics", epic_line(args.slug, "Draft"), "_No epics yet._"),
        encoding="utf-8",
    )
    print(f"✅ Epic created at features/{args.feature}/epics/{args.slug}/ (state: Draft)")
    return 0


def cmd_validate(args) -> int:
    ws = workspace()
    errors: list[str] = []
    warnings: list[str] = []
    rel = lambda p: str(p.relative_to(ws))  # noqa: E731

    for name in ROOT_FILES:
        if not (ws / name).is_file():
            hint = ""
            if name == "technical_deal.md" and (ws / "techinal_deal.md").is_file():
                hint = " (found legacy techinal_deal.md — rename it: git mv techinal_deal.md technical_deal.md)"
            errors.append(f"missing product root file: {name}{hint}")
    compact = is_compact(ws)
    for d in (COMPACT_ROOT_DIRS if compact else ROOT_DIRS):
        if not (ws / d).is_dir():
            errors.append(f"missing product root folder: {d}/")
    if compact and not (ws / "features" / "roadmap.md").is_file():
        errors.append("compact layout: missing features/roadmap.md")

    # apps (apps/<name>/app.md in the classic layout, app.md at the root in compact)
    for manifest in app_manifests(ws):
        app = manifest.parent
        text = read(manifest)
        if not text:
            errors.append(f"{rel(manifest)}: missing app.md")
            continue
        for f in APP_FIELDS:
            if field(text, f) is None:
                errors.append(f"{rel(manifest)}: missing field '{f}'")
        if section(text, "Boundaries") is None:
            errors.append(f"{rel(manifest)}: missing '## Boundaries'")
        pointer = app / "repo_pointer.md"
        if pointer.is_file() and not field(read(pointer), "repository"):
            errors.append(f"{rel(pointer)}: missing value for 'repository'")

    # features and epics
    for feat in features(ws):
        for name in (COMPACT_FEATURE_FILES if compact else FEATURE_FILES):
            if not (feat / name).is_file():
                errors.append(f"{rel(feat)}: missing {name}")
        if not (feat / "epics").is_dir():
            errors.append(f"{rel(feat)}: missing epics/")
        ftext = read(feat / "index.md")
        for f in FEATURE_FIELDS:
            if field(ftext, f) is None:
                errors.append(f"{rel(feat)}/index.md: missing field '{f}'")

        listed = dict(re.findall(r"^- \[([^\]]+)\]\(epics/[^)]+/index\.md\)\s*—\s*(\S+)", ftext, re.MULTILINE))
        on_disk = {e.name for e in epics(feat)}
        for missing in sorted(set(listed) - on_disk):
            errors.append(f"{rel(feat)}/index.md: lists epic '{missing}' that does not exist")

        for ep in epics(feat):
            where = rel(ep)
            for name in EPIC_FILES:
                if not (ep / name).is_file():
                    errors.append(f"{where}: missing {name}")
            state, count = get_epic_state(ep)
            if count != 1:
                errors.append(f"{where}/quick_status.md: expected exactly one state line, found {count}")
                continue
            if state not in STATES:
                errors.append(f"{where}: invalid state '{state}' (valid: {', '.join(STATES)})")
                continue
            if ep.name not in listed:
                errors.append(f"{rel(feat)}/index.md: epic '{ep.name}' is not listed under ## Epics")
            elif listed[ep.name] != state:
                errors.append(f"{rel(feat)}/index.md: epic '{ep.name}' listed as {listed[ep.name]} but state is {state}")

            plan = read(ep / "plan.md")
            tasks = get_epic_tasks(ep)
            examples = sorted(set(example_ids(strip_comments(section(plan, "Examples") or ""))), key=lambda s: int(s[1:]))

            if state in {"WIP", "Done", "Stale"}:
                if not tasks:
                    errors.append(f"{where}/tasks.md: no tasks for an epic in {state}")
                for _, t in tasks:
                    if not re.search(r"\b[SR]\d+\b", t):
                        errors.append(f"{where}/tasks.md: task does not cite S#/R#: '{t}'")
                cited = set(re.findall(r"\b(S\d+)\b", " ".join(t for _, t in tasks)))
                for s in examples:
                    if s not in cited:
                        (warnings if state == "WIP" else errors).append(f"{where}: example {s} is not covered by any task")
            if state == "Done":
                open_tasks = [t for done, t in tasks if not done]
                if open_tasks:
                    errors.append(f"{where}: state Done but {len(open_tasks)} task(s) still open")
                if looks_stale(ws, ep):
                    errors.append(f"{where}: plan.md changed after the epic was Done — it should be Stale (§4.5)")
                if args.strict:
                    # Compiled and vendored artifacts must not satisfy the check:
                    # a .pyc carrying a docstring is not a test.
                    skip = {"target", "node_modules", "dist", ".git", "__pycache__",
                            ".venv", "venv", "build", ".mypy_cache", ".pytest_cache",
                            "htmlcov", ws.name}
                    corpus = "\n".join(
                        read(f)
                        for root in source_roots(ws) if root.is_dir()
                        for f in root.rglob("*")
                        if f.is_file()
                        and f.name not in {"app.md", "repo_pointer.md"}
                        and not any(part in skip for part in f.relative_to(root).parts)
                        and f.stat().st_size < 2_000_000
                    )
                    for s in examples:
                        if f"{ep.name}#{s}" not in corpus:
                            where_src = ", ".join(str(r) for r in source_roots(ws))
                            errors.append(f"{where}: no test named '{ep.name}#{s}' found under {where_src}")
            if state == "Blocked":
                blockers = strip_comments(section(read(ep / "quick_status.md"), "Blockers") or "").strip()
                if not blockers or blockers.lower().startswith("none"):
                    warnings.append(f"{where}: state Blocked but ## Blockers is empty")

    if args.strict:
        errors.extend(warnings)
        warnings = []
    for w in warnings:
        print(f"⚠️  {w}")
    for e in errors:
        print(f"❌ {e}")
    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"✅ Workspace is SCPE-compliant ({len(warnings)} warning(s)).")
    return 0


def cmd_gate_check(args) -> int:
    ws = workspace()
    ep = resolve_epic(ws, args.epic)
    plan = read(ep / "plan.md")
    state, _ = get_epic_state(ep)
    results: list[tuple[str, str]] = []

    def check(ok: bool, msg: str, level: str = "FAIL") -> None:
        results.append(("PASS" if ok else level, msg))

    check(state in {"Draft", "Stale", "Blocked"}, f"epic state is {state} (gate applies to Draft, Stale or Blocked)", "WARN")

    for heading in ["Intent", "Domain Model", "Business Rules", "Examples", "Slices", "Open Questions"]:
        check(section(plan, heading) is not None, f"plan.md has '## {heading}'")

    intent = strip_comments(section(plan, "Intent") or "").strip()
    check(bool(intent), "Intent is written")

    dm = strip_comments(section(plan, "Domain Model") or "")
    terms_raw = field(dm, "Terms") or ""
    terms = [re.sub(r"\(.*?\)", "", t).strip() for t in terms_raw.split(",")]
    terms = [t for t in terms if t]
    check(bool(terms), "Domain Model lists Terms")
    glossary_heads = {h.strip().lower() for h in re.findall(r"^## (.+)$", read(ws / "glossary.md"), re.MULTILINE)}
    for t in terms:
        check(t.lower() in glossary_heads, f"term '{t}' is defined in glossary.md")

    rules = rule_ids(strip_comments(section(plan, "Business Rules") or ""))
    check(bool(rules), f"Business Rules numbered R# ({len(rules)} found)")

    ex_items = [l for l in list_items(section(plan, "Examples") or "") if re.search(r"\*\*S\d+", l)]
    check(bool(ex_items), f"Examples numbered S# ({len(ex_items)} found)")
    for item in ex_items:
        sid = example_ids(item)[0]
        whens = len(re.findall(r"\bWhen\b", item))
        check("Given" in item and whens == 1 and "Then" in item,
              f"{sid} has Given / exactly one When / Then")

    examples = set(example_ids(strip_comments(section(plan, "Examples") or "")))
    slices = list_items(section(plan, "Slices") or "")
    check(bool(slices), f"Slices defined ({len(slices)} found)")
    cited: set[str] = set()
    for i, s in enumerate(slices, 1):
        refs = set(re.findall(r"\b([SR]\d+)\b", s))
        cited |= refs
        check(bool(refs), f"slice {i} cites S#/R#")
    for s in sorted(examples - cited, key=lambda x: int(x[1:])):
        check(False, f"example {s} is not assigned to any slice", "WARN")

    oq = [q for q in list_items(section(plan, "Open Questions") or "")
          if not re.search(r"\(non-blocking\)|\[resolved\]", q, re.IGNORECASE)]
    check(not oq, f"no blocking open questions ({len(oq)} blocking)")
    for q in oq:
        results.append(("FAIL", f"blocking question: {q.lstrip('-0123456789. ')}"))

    if is_compact(ws):
        # Compact trades epic-level verticality for smaller epics: the feature is
        # the unit that has to deliver value on its own.
        results.append(("MANUAL", "the feature this epic belongs to is a vertical slice; "
                                  "the epic itself need not be"))
    else:
        results.append(("MANUAL", "slices are vertical, or the reason they are not is written under ## Slices"))
    results.append(("MANUAL", "model fits architecture.md and technical_deal.md"))
    results.append(("MANUAL", "every Then is observable by a user or another system"))

    icons = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️ ", "MANUAL": "👤"}
    print(f"Readiness Gate check — {args.epic}\n")
    for level, msg in results:
        print(f"{icons[level]} {level:<6} {msg}")
    fails = sum(1 for l, _ in results if l == "FAIL")
    print(f"\n{'FAIL' if fails else 'PASS'}: {fails} blocking issue(s). "
          "Only a human acting as Tech Lead may mark the epic Ready.")
    return 1 if fails else 0


def cmd_set_state(args) -> int:
    ws = workspace()
    ep = resolve_epic(ws, args.epic)
    if args.state not in STATES:
        die(f"invalid state '{args.state}' (valid: {', '.join(STATES)})")
    current, _ = get_epic_state(ep)
    if current not in TRANSITIONS:
        die(f"current state '{current}' is invalid; fix quick_status.md first.")
    if args.state not in TRANSITIONS[current]:
        allowed = ", ".join(sorted(TRANSITIONS[current])) or "none"
        die(f"transition {current} → {args.state} is not allowed (from {current}: {allowed}).")
    write_state(ep, args.state, args.by, args.note or "")
    print(f"✅ {args.epic}: {current} → {args.state}")
    return 0


def cmd_mark_stale(args) -> int:
    path_str = args.path
    if args.from_hook:
        try:
            payload = json.load(sys.stdin)
            path_str = (payload.get("tool_input") or {}).get("file_path")
        except (json.JSONDecodeError, AttributeError):
            return 0
    if not path_str:
        return 0
    try:
        plan = Path(path_str).expanduser().resolve()
        if plan.name != "plan.md" or plan.parent.parent.name != "epics":
            return 0
        epic_dir = plan.parent
        ws = find_workspace(epic_dir)
        if ws is None:
            return 0
        state, count = epic_state(read(epic_dir / "quick_status.md"))
        if count != 1 or state != "Done":
            return 0
        write_state(epic_dir, "Stale", "scpe hook",
                    "plan.md edited after delivery; back to the Readiness Gate (spec drift).")
    except Exception as exc:  # a hook must never break the edit that triggered it
        if not args.from_hook:
            die(str(exc))
        return 0

    ref = f"{epic_dir.parent.parent.name}/{epic_dir.name}"
    msg = (f"SCPE: epic {ref} was Done and its plan.md changed, so it is now Stale. "
           "The Tech Lead must review the difference and record Re-execute or Accept the drift "
           "in epic_roadmap.md (run /scpe-gate).")
    if args.from_hook:
        print(json.dumps({
            "systemMessage": msg,
            "hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": msg},
        }))
    else:
        print(f"✅ {msg}")
    return 0


def collect_status(ws: Path) -> list[dict]:
    rows = []
    for feat in features(ws):
        for ep in epics(feat):
            state, _ = get_epic_state(ep)
            tasks = get_epic_tasks(ep)
            blockers = ""
            qs = ep / "quick_status.md"
            if qs.is_file():
                b = strip_comments(section(read(qs), "Blockers") or "").strip()
                if not b.lower().startswith("none"):
                    blockers = b
            tasks_toml = ep / "tasks.toml"
            if tasks_toml.is_file():
                try:
                    with open(tasks_toml, "rb") as f:
                        tdata = tomllib.load(f)
                    bitems = tdata.get("blockers", {}).get("items", [])
                    if bitems:
                        blockers = "; ".join(bitems)
                except Exception:
                    pass
            rows.append({
                "feature": feat.name, "epic": ep.name, "state": state or "?",
                "rel_path": str(ep.relative_to(ws)),
                "tasks_done": sum(1 for d, _ in tasks if d), "tasks_total": len(tasks),
                "blockers": blockers,
            })
    return rows


def status_table(rows: list[dict]) -> str:
    if not rows:
        return "_No epics yet._"
    lines = ["| Feature | Epic | State | Tasks |", "| :--- | :--- | :---: | :---: |"]
    for r in rows:
        tasks = f"{r['tasks_done']}/{r['tasks_total']}" if r["tasks_total"] else "—"
        rel_epic = r.get("rel_path", f"features/{r['feature']}/epics/{r['epic']}")
        lines.append(
            f"| [{r['feature']}](features/{r['feature']}/index.md) "
            f"| [{r['epic']}]({rel_epic}/quick_status.md) "
            f"| `{r['state']}` | {tasks} |"
        )
    counts = {s: sum(1 for r in rows if r["state"] == s) for s in STATES}
    lines.append("")
    lines.append(" · ".join(f"**{s}:** {n}" for s, n in counts.items()))
    return "\n".join(lines)



def sync_roadmap_file(ws: Path) -> str:
    rpath = ws / "roadmap.md"
    rows = collect_status(ws)

    wip = [r for r in rows if r["state"] == "WIP"]
    ready = [r for r in rows if r["state"] == "Ready"]
    done = [r for r in rows if r["state"] == "Done"]
    draft = [r for r in rows if r["state"] in {"Draft", "Blocked", "Stale"}]

    lines = [
        "# 🗺️ Product Roadmap",
        "",
        f"_Última sincronização: {today()} via `scpe.py roadmap --sync`_",
        "",
        "## 🚀 Em Implementação (WIP)",
        "| Ordem | Feature | Responsável | Tarefas | Bloqueios |",
        "| :---: | :--- | :--- | :---: | :--- |",
    ]
    if wip:
        for r in wip:
            tasks = f"{r['tasks_done']}/{r['tasks_total']}" if r["tasks_total"] else "—"
            lines.append(f"| **{r['feature']}** | [{r['epic']}]({r['rel_path']}) | agent | {tasks} | {r['blockers'] or 'Nenhum'} |")
    else:
        lines.append("| — | _Nenhuma feature em WIP no momento_ | — | — | — |")

    lines.extend([
        "",
        "## ⏳ Próximos Prontos (Ready)",
        "| Ordem | Feature | Dependências | Tarefas |",
        "| :---: | :--- | :--- | :---: |",
    ])
    if ready:
        for r in ready:
            tasks = f"{r['tasks_done']}/{r['tasks_total']}" if r["tasks_total"] else "—"
            lines.append(f"| **{r['feature']}** | [{r['epic']}]({r['rel_path']}) | — | {tasks} |")
    else:
        lines.append("| — | _Nenhuma feature pronta para dev_ | — | — |")

    lines.extend([
        "",
        "## ✅ Já Entregues (Done)",
        "| Ordem | Feature | Data de Conclusão | Tarefas |",
        "| :---: | :--- | :---: | :---: |",
    ])
    if done:
        for r in done:
            tasks = f"{r['tasks_done']}/{r['tasks_total']}" if r["tasks_total"] else "—"
            lines.append(f"| **{r['feature']}** | [{r['epic']}]({r['rel_path']}) | {today()} | {tasks} |")
    else:
        lines.append("| — | _Nenhuma feature entregue ainda_ | — | — |")

    lines.extend([
        "",
        "## 💡 Backlog (Draft / Blocked / Stale)",
        "| Estado | Feature | Caminho |",
        "| :---: | :--- | :--- |",
    ])
    if draft:
        for r in draft:
            lines.append(f"| `{r['state']}` | {r['feature']}/{r['epic']} | `{r['rel_path']}` |")
    else:
        lines.append("| — | _Backlog vazio_ | — |")

    content = "\n".join(lines) + "\n"
    rpath.write_text(content, encoding="utf-8")
    return content


def cmd_roadmap(args) -> int:
    ws = workspace()
    content = sync_roadmap_file(ws)
    if getattr(args, "sync", False):
        print("✅ roadmap.md sincronizado na raiz do workspace.")
    else:
        print(content)
    return 0


def cmd_term(args) -> int:
    ws = workspace()
    gpath = ws / "glossary.md"
    if not gpath.is_file():
        die(f"glossary.md not found at {gpath}.")
    gtext = read(gpath)
    target = args.word.strip().lower()

    pattern = re.compile(r"^##\s+([^\n]+)\n(.*?)(?=^##\s+|\Z)", re.MULTILINE | re.DOTALL)
    for m in pattern.finditer(gtext):
        heading = m.group(1).strip()
        if heading.lower() == target or target in heading.lower():
            print(f"## {heading}\n{m.group(2).strip()}")
            return 0
    die(f"Term '{args.word}' not found in glossary.md.")
    return 1


def cmd_pack(args) -> int:
    ws = workspace()
    ep_dir = resolve_epic(ws, args.feature)
    slice_id = int(args.slice_id)

    tasks_toml = ep_dir / "tasks.toml"
    if not tasks_toml.is_file():
        die(f"tasks.toml not found at {ep_dir / 'tasks.toml'}. Run on a feature with tasks.toml.")
    with open(tasks_toml, "rb") as f:
        tasks_data = tomllib.load(f)

    slices = tasks_data.get("slice", [])
    target_slice = next((s for s in slices if s.get("id") == slice_id), None)
    if not target_slice:
        avail = [str(s.get("id")) for s in slices]
        die(f"Slice {slice_id} not found in {ep_dir.name}. Available slices: {', '.join(avail)}")

    covers = target_slice.get("covers", [])
    plan_text = read(ep_dir / "plan.md") if (ep_dir / "plan.md").is_file() else ""

    invariants = {}
    br_sec = strip_comments(section(plan_text, "Business Rules") or "")
    for line in br_sec.splitlines():
        line_s = line.strip()
        m = re.match(r"^\s*-\s*\*\*(R\d+):\*\*\s*(.*)$", line_s)
        if m and m.group(1) in covers:
            invariants[m.group(1)] = m.group(2).strip()

    scenarios = {}
    ex_sec = strip_comments(section(plan_text, "Examples") or "")
    for line in ex_sec.splitlines():
        line_s = line.strip()
        m = re.match(r"^\s*-\s*\*\*(S\d+)[^:]*:\*\*\s*(.*)$", line_s)
        if not m:
            m = re.match(r"^\s*-\s*\*\*(S\d+)\b[^*]*\*\*\s*(.*)$", line_s)
        if m and m.group(1) in covers:
            scenarios[m.group(1)] = m.group(2).strip()

    dm_sec = strip_comments(section(plan_text, "Domain Model") or "")
    terms_raw = field(dm_sec, "Terms") or ""
    terms = [re.sub(r"\(.*?\)", "", t).strip() for t in terms_raw.split(",") if t.strip()]

    domain_terms = {}
    glossary_path = ws / "glossary.md"
    if glossary_path.is_file():
        gtext = read(glossary_path)
        for t in terms:
            m = re.search(rf"^## {re.escape(t)}[ \t]*$(.*?)(?=^## |\Z)", gtext, re.MULTILINE | re.DOTALL)
            if m:
                domain_terms[t] = m.group(1).strip()

    apps_info = {}
    for app_name in target_slice.get("apps", []):
        app_toml = ws / "apps" / app_name / "app.toml"
        app_md = ws / "apps" / app_name / "app.md"
        if app_toml.is_file():
            with open(app_toml, "rb") as f:
                apps_info[app_name] = tomllib.load(f)
        elif app_md.is_file():
            mtext = read(app_md)
            apps_info[app_name] = {
                "name": field(mtext, "name"),
                "stack": field(mtext, "stack"),
                "run": field(mtext, "run"),
                "test": field(mtext, "test"),
                "boundaries": strip_comments(section(mtext, "Boundaries") or "").strip()
            }

    logs = tasks_data.get("log", [])
    last_learning = logs[-1] if logs else None
    tasks = [t for t in tasks_data.get("task", []) if t.get("slice_id") == slice_id]

    payload = {
        "slice": target_slice,
        "tasks": tasks,
        "invariants": invariants,
        "scenarios": scenarios,
        "domain_terms": domain_terms,
        "apps": apps_info,
        "previous_learning": last_learning,
    }

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        lines = [
            "# ================================================================",
            f"# SCPE SLICE PACK: {ep_dir.name} [Slice {slice_id}]",
            "# ================================================================",
            "",
            "[slice]",
            f'id = {target_slice.get("id")}',
            f'name = "{target_slice.get("name", "")}"',
            f'description = "{target_slice.get("description", "")}"',
            f'covers = {json.dumps(covers)}',
            f'apps = {json.dumps(target_slice.get("apps", []))}',
            f'verify = "{target_slice.get("verify", "")}"',
            "",
            "[invariants]",
        ]
        for rid, rdesc in invariants.items():
            lines.append(f'{rid} = "{rdesc}"')
        if not invariants:
            lines.append("# No invariants in covers")

        lines.extend(["", "[scenarios]"])
        for sid, sdesc in scenarios.items():
            lines.append(f'{sid} = "{sdesc}"')
        if not scenarios:
            lines.append("# No scenarios in covers")

        lines.extend(["", "[domain_terms]"])
        for tname, tdef in domain_terms.items():
            first_line = tdef.splitlines()[0] if tdef else ""
            lines.append(f'# {tname}: {first_line}')

        lines.extend(["", "[app_boundaries]"])
        for aname, ainfo in apps_info.items():
            bounds = ainfo.get("boundaries") or ainfo.get("boundaries", {}).get("forbidden", [])
            lines.append(f'# {aname}: {bounds}')

        if last_learning:
            lines.extend([
                "",
                "[previous_learning]",
                f'date = "{last_learning.get("date")}"',
                f'entry = "{last_learning.get("entry")}"'
            ])

        print("\n".join(lines))
    return 0


def cmd_status(args) -> int:
    ws = workspace()
    rows = collect_status(ws)
    if args.json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
    else:
        print(status_table(rows))
    if args.write:
        qs = ws / "quick_status.md"
        text = read(qs)
        block = f"{STATUS_START}\n{status_table(rows)}\n{STATUS_END}"
        if STATUS_START in text and STATUS_END in text:
            text = re.sub(re.escape(STATUS_START) + r".*?" + re.escape(STATUS_END),
                          lambda _: block, text, flags=re.DOTALL)
        else:
            text = append_to_section(text, "Epics", block)
        text = re.sub(r"^(- \*\*updated:\*\*).*$", rf"\g<1> {today()}", text, count=1, flags=re.MULTILINE)
        qs.write_text(text, encoding="utf-8")
        if not args.json:
            print("\n✅ quick_status.md updated")
    return 0


def cmd_complete_task(args) -> int:
    ws = workspace()
    epic_dir = resolve_epic(ws, args.epic)
    tasks_path = epic_dir / "tasks.md"
    if not tasks_path.is_file():
        die(f"tasks.md not found at {tasks_path}")
    text = read(tasks_path)
    lines = text.splitlines()
    target = args.task.strip()
    updated = False

    new_lines = []
    task_idx = 0
    matched_desc = ""
    for line in lines:
        m = re.match(r"^(\s*-\s*\[)( |x|X)(\]\s+)(.*)$", line)
        if m:
            task_idx += 1
            prefix, state_char, mid, rest = m.groups()
            is_match = False
            if target.isdigit() and int(target) == task_idx:
                is_match = True
            elif target.lower() in rest.lower() or target in line:
                is_match = True

            if is_match:
                matched_desc = rest.strip()
                if state_char == " ":
                    line = f"{prefix}x{mid}{rest}"
                    updated = True
                else:
                    print(f"ℹ️ Task already marked as done: {matched_desc}")
                    return 0
        new_lines.append(line)

    if not updated:
        die(f"No pending task matched '{target}' in {tasks_path}")

    tasks_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    print(f"✅ Marked task as complete: {matched_desc}")
    return 0


# ------------------------------------------------------------------ main ----

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="scpe.py", description="SCPE workspace engine")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create a new SCPE product workspace")
    p.add_argument("name")
    p.add_argument("--path", help="parent directory (default: cwd)")
    p.add_argument("--app", action="append", metavar="NAME:TYPE", help="add apps/<NAME>/app.md")
    p.add_argument("--no-git", action="store_true", help="do not run git init")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("feature", help="scaffold features/<slug>/")
    p.add_argument("slug")
    p.add_argument("title")
    p.add_argument("--branch", action="store_true", help="create and checkout git branch feat/<slug>")
    p.set_defaults(func=cmd_feature)

    p = sub.add_parser("pack", help="compile slice context for JIT agent execution")
    p.add_argument("feature", help="<feature> or <feature>/<epic>")
    p.add_argument("slice_id", help="slice id (e.g. 1)")
    p.add_argument("--json", action="store_true", help="output as JSON")
    p.set_defaults(func=cmd_pack)

    p = sub.add_parser("term", help="lookup term in glossary.md")
    p.add_argument("word", help="term to lookup")
    p.set_defaults(func=cmd_term)

    p = sub.add_parser("roadmap", help="display or sync product root roadmap.md")
    p.add_argument("--sync", action="store_true", help="write/update roadmap.md at product root")
    p.set_defaults(func=cmd_roadmap)

    p = sub.add_parser("epic", help="scaffold features/<feature>/epics/<slug>/ in Draft")
    p.add_argument("feature")
    p.add_argument("slug")
    p.add_argument("title")
    p.set_defaults(func=cmd_epic)

    p = sub.add_parser("complete-task", help="mark a task in tasks.md as done [x]")
    p.add_argument("epic", help="<feature>/<epic>")
    p.add_argument("task", help="task number (1-based) or substring/ID (e.g. TASK-01.1.1)")
    p.set_defaults(func=cmd_complete_task)

    p = sub.add_parser("validate", help="check structure, states and traceability")
    p.add_argument("--strict", action="store_true", help="also require <epic>#S# tests; warnings fail")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("gate-check", help="Readiness Gate lint for one epic (never changes state)")
    p.add_argument("epic", help="<feature>/<epic>")
    p.set_defaults(func=cmd_gate_check)

    p = sub.add_parser("set-state", help="apply a valid state transition and log it")
    p.add_argument("epic", help="<feature>/<epic>")
    p.add_argument("state", choices=STATES)
    p.add_argument("--by", required=True, help="who performs the transition")
    p.add_argument("--note", default="")
    p.set_defaults(func=cmd_set_state)

    p = sub.add_parser("mark-stale", help="Done → Stale when an epic plan.md is edited")
    p.add_argument("path", nargs="?")
    p.add_argument("--from-hook", action="store_true", help="read PostToolUse JSON from stdin")
    p.set_defaults(func=cmd_mark_stale)

    p = sub.add_parser("status", help="product status panel")
    p.add_argument("--json", action="store_true")
    p.add_argument("--write", action="store_true", help="rewrite the table in quick_status.md")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
