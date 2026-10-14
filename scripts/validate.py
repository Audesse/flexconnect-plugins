#!/usr/bin/env python3
"""Checks that every plugin under plugins/ is wired up consistently for all
supported clients. Run from anywhere:

    python3 scripts/validate.py

Checks:
- every JSON manifest parses
- each plugin has the per-client manifests (Claude Code, Agent Plugins 1.0
  for Codex/Copilot, Cursor) and they agree on name, version and description
- each plugin is listed in all four marketplaces, with a source path that
  points at it, and nothing is listed that doesn't exist
- skills have SKILL.md frontmatter whose `name` matches the folder
- no MCP config contains something that looks like a real credential
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = ROOT / "plugins"

MARKETPLACES = {
    "claude": ROOT / ".claude-plugin/marketplace.json",
    "copilot": ROOT / ".github/plugin/marketplace.json",
    "cursor": ROOT / ".cursor-plugin/marketplace.json",
    "codex": ROOT / ".agents/plugins/marketplace.json",
}

# Manifests whose name/version/description must agree, per plugin.
MANIFESTS = {
    "claude": ".claude-plugin/plugin.json",
    "agent-plugins": "plugin.json",
    "cursor": ".cursor-plugin/plugin.json",
}
REQUIRED_FILES = [".mcp.json", "mcp.json", "README.md"]
AGENT_PLUGINS_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
SECRET_PATTERN = re.compile(r"flx_[A-Za-z0-9]{8,}|eyJ[A-Za-z0-9_-]{10,}\.|sk-[A-Za-z0-9]{16,}")

errors: list[str] = []


def load(path: Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        errors.append(f"missing: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as e:
        errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {e}")
    return None


def source_path(entry: dict) -> str | None:
    src = entry.get("source")
    if isinstance(src, dict):  # Codex: {"source": "local", "path": "./plugins/x"}
        src = src.get("path")
    return src


def check_plugin(plugin_dir: Path) -> tuple[str, str] | None:
    rel = plugin_dir.relative_to(ROOT)
    manifests = {client: load(plugin_dir / path) for client, path in MANIFESTS.items()}
    for f in REQUIRED_FILES:
        if not (plugin_dir / f).exists():
            errors.append(f"missing: {rel}/{f}")
    if any(m is None for m in manifests.values()):
        return None

    for key in ("name", "version", "description"):
        values = {client: m.get(key) for client, m in manifests.items()}
        if len(set(values.values())) != 1:
            errors.append(f"{rel}: '{key}' differs between manifests: {values}")
    if manifests["agent-plugins"].get("$schema") != AGENT_PLUGINS_SCHEMA:
        errors.append(f"{rel}/plugin.json: $schema must be {AGENT_PLUGINS_SCHEMA}")
    name = manifests["claude"]["name"]
    if name != plugin_dir.name:
        errors.append(f"{rel}: plugin name '{name}' doesn't match its folder name")

    # Cursor's mcpServers may point at a non-default file; it must exist.
    cursor_mcp = manifests["cursor"].get("mcpServers")
    if isinstance(cursor_mcp, str) and not (plugin_dir / cursor_mcp).exists():
        errors.append(f"{rel}/.cursor-plugin/plugin.json: mcpServers -> missing {cursor_mcp}")

    for mcp_file in plugin_dir.glob("*mcp.json"):
        load(mcp_file)
        if SECRET_PATTERN.search(mcp_file.read_text()):
            errors.append(f"{mcp_file.relative_to(ROOT)}: looks like it contains a credential")

    for skill in (plugin_dir / "skills").glob("*/"):
        skill_md = skill / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"missing: {skill_md.relative_to(ROOT)}")
            continue
        match = re.match(r"---\n(.*?)\n---\n", skill_md.read_text(), re.S)
        fm_name = re.search(r"^name:\s*(\S+)", match.group(1), re.M) if match else None
        if not fm_name or fm_name.group(1) != skill.name:
            errors.append(f"{skill_md.relative_to(ROOT)}: frontmatter name must be '{skill.name}'")

    return name, manifests["claude"]["version"]


def main() -> int:
    plugins = {}
    for plugin_dir in sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir()):
        result = check_plugin(plugin_dir)
        if result:
            plugins[result[0]] = (plugin_dir, result[1])

    for client, path in MARKETPLACES.items():
        market = load(path)
        if market is None:
            continue
        listed = {e.get("name"): e for e in market.get("plugins", [])}
        for name in plugins.keys() - listed.keys():
            errors.append(f"{path.relative_to(ROOT)}: plugin '{name}' not listed")
        for name, entry in listed.items():
            if name not in plugins:
                errors.append(f"{path.relative_to(ROOT)}: lists unknown plugin '{name}'")
                continue
            plugin_dir, version = plugins[name]
            src = source_path(entry)
            if not src or (ROOT / src).resolve() != plugin_dir.resolve():
                errors.append(f"{path.relative_to(ROOT)}: '{name}' source {src!r} != {plugin_dir.relative_to(ROOT)}")
            if "version" in entry and entry["version"] != version:
                errors.append(f"{path.relative_to(ROOT)}: '{name}' version {entry['version']} != {version}")
            if client == "codex" and not {"policy", "category"} <= entry.keys():
                errors.append(f"{path.relative_to(ROOT)}: '{name}' needs 'policy' and 'category'")

    for e in errors:
        print(f"error: {e}")
    print(f"{len(plugins)} plugin(s) checked, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
