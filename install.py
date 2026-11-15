#!/usr/bin/env python3
"""Vic Awesome MCP installer: add any server from this repo to your AI client in one line.

Run straight from GitHub (Python 3.9+, standard library only):

    curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - list
    curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - playwright --client cursor
    curl -fsSL https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/install.py | python3 - playwright --client cursor --write

Clients: claude-desktop, claude-code, cursor, vscode, codex.
Without --write it only prints the config. With --write it merges the server into the client's
config file, after saving a .bak copy. Secrets are never written: configs reference environment
variables (or VS Code's secure input prompt), and you set the key yourself.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import shutil
import sys
import urllib.request
from pathlib import Path

CATALOG_URL = "https://raw.githubusercontent.com/voidgazer009/vic-awesome-mcp/main/catalog.json"
CLIENTS = ["claude-desktop", "claude-code", "cursor", "vscode", "codex"]


def load_catalog() -> dict:
    local = Path(__file__).resolve().parent / "catalog.json" if "__file__" in globals() else None
    if local and local.exists():
        return json.loads(local.read_text(encoding="utf-8"))
    with urllib.request.urlopen(CATALOG_URL, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def find(catalog: dict, slug: str) -> dict:
    for s in catalog["servers"]:
        if s["slug"] == slug:
            return s
    names = ", ".join(s["slug"] for s in catalog["servers"])
    sys.exit(f"Unknown server '{slug}'. Available: {names}")


# ---------------------------------------------------------------- config builders

def server_url(s: dict, full: bool) -> str:
    h = s["http"]
    return h.get("url_full", h["url"]) if full else h["url"]


def bearer_env(s: dict, client: str, with_key: bool) -> str | None:
    """Env var holding the bearer token, or None when this client should not send one."""
    h = s.get("http") or {}
    env = h.get("bearer_env")
    if not env:
        return None
    if client in h.get("oauth_clients", []) and not with_key:
        return None  # client signs in with OAuth on first use
    if h.get("bearer_optional") and not with_key:
        return None  # works without a key; --with-key adds one
    return env


PLACEHOLDER_DIR = "/path/to/your/folder"
FOLDER = [PLACEHOLDER_DIR]  # set from --dir in main()


def stdio_args(s: dict, full: bool = False) -> list:
    """Args with the {dir} token replaced by the folder given with --dir (a single token may expand to several)."""
    out: list = []
    for a in (s["stdio"].get("args_full") if full and s["stdio"].get("args_full") else s["stdio"]["args"]):
        if a == "{dir}":
            out += FOLDER
        else:
            out.append(a)
    return out


def stdio_env_values(s: dict) -> dict:
    """Fixed, non-secret env vars (e.g. a file path); {home} becomes your home directory."""
    home = str(Path.home())
    return {k: v.replace("{home}", home) for k, v in (s["stdio"].get("env_values") or {}).items()}


def json_entry(s: dict, client: str, with_key: bool = False, full: bool = False) -> dict:
    """Entry for JSON-config clients (claude-desktop, cursor, vscode)."""
    if "stdio" in s:
        e = {"command": s["stdio"]["command"], "args": stdio_args(s, full)}
        envs = stdio_env_values(s)
        if s["stdio"].get("env"):
            envs.update({k: f"${{env:{k}}}" if client == "cursor" else f"<set {k}>" for k in s["stdio"]["env"]})
        if envs:
            e["env"] = envs
        if client == "vscode":
            e = {"type": "stdio", **e}
        return e
    h = s["http"]
    env = bearer_env(s, client, with_key)
    if client == "claude-desktop":
        # Claude Desktop's JSON config only launches local processes; bridge remote servers with mcp-remote.
        args = ["-y", "mcp-remote", server_url(s, full)]
        e: dict = {"command": "npx", "args": args}
        if env:
            args += ["--header", "Authorization:${AUTH_HEADER}"]
            e["env"] = {"AUTH_HEADER": f"Bearer <your {env}>"}
        return e
    if client == "cursor":
        e = {"url": server_url(s, full)}
        if env:
            e["headers"] = {"Authorization": f"Bearer ${{env:{env}}}"}
        return e
    # vscode
    e = {"type": "http", "url": server_url(s, full)}
    if env:
        e["headers"] = {"Authorization": f"Bearer ${{input:{env.lower()}}}"}
    return e


def vscode_inputs(s: dict, with_key: bool = False) -> list:
    env = bearer_env(s, "vscode", with_key)
    if not env:
        return []
    return [{"type": "promptString", "id": env.lower(), "description": f"{s['name']} token ({env})", "password": True}]


def codex_toml(s: dict, with_key: bool = False, full: bool = False) -> str:
    lines = [f"[mcp_servers.{s['slug']}]"]
    if "stdio" in s:
        lines.append(f'command = {json.dumps(s["stdio"]["command"])}')
        lines.append("args = [" + ", ".join(json.dumps(a) for a in stdio_args(s, full)) + "]")
        envs = stdio_env_values(s)
        if envs:
            lines.append("env = { " + ", ".join(f"{k} = {json.dumps(v)}" for k, v in envs.items()) + " }")
    else:
        lines.append(f'url = {json.dumps(server_url(s, full))}')
        env = bearer_env(s, "codex", with_key)
        if env:
            lines.append(f'bearer_token_env_var = {json.dumps(env)}')
    return "\n".join(lines) + "\n"


def claude_code_cmd(s: dict, with_key: bool = False, full: bool = False) -> str:
    if "stdio" in s:
        envs = "".join(f" -e {k}={shlex.quote(v)}" for k, v in stdio_env_values(s).items())
        return f"claude mcp add {s['slug']}{envs} -- {s['stdio']['command']} " + " ".join(shlex.quote(a) for a in stdio_args(s, full))
    h = s["http"]
    url = server_url(s, full)
    if any(ch in url for ch in "?&*"):
        url = f'"{url}"'  # keep zsh/bash from globbing the query string
    cmd = f"claude mcp add --transport http {s['slug']} {url}"
    env = bearer_env(s, "claude-code", with_key)
    if env:
        cmd += f' --header "Authorization: Bearer ${env}"'
    return cmd


# ---------------------------------------------------------------- config file locations

def config_path(client: str) -> Path:
    home = Path.home()
    system = platform.system()
    if client == "claude-desktop":
        if system == "Darwin":
            return home / "Library/Application Support/Claude/claude_desktop_config.json"
        if system == "Windows":
            return Path(os.environ.get("APPDATA", home / "AppData/Roaming")) / "Claude/claude_desktop_config.json"
        return home / ".config/Claude/claude_desktop_config.json"
    if client == "cursor":
        return home / ".cursor/mcp.json"
    if client == "vscode":
        return Path.cwd() / ".vscode/mcp.json"
    if client == "codex":
        return Path(os.environ.get("CODEX_HOME", home / ".codex")) / "config.toml"
    raise ValueError(client)


def backup(p: Path) -> None:
    if p.exists():
        shutil.copy2(p, p.with_suffix(p.suffix + ".bak"))


def write_json(p: Path, key: str, slug: str, entry: dict, inputs: list | None = None) -> None:
    data = {}
    if p.exists() and p.read_text(encoding="utf-8").strip():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            sys.exit(f"{p} is not valid JSON (comments?). Fix it or paste the printed config by hand. Nothing was changed.")
    data.setdefault(key, {})
    if slug in data[key]:
        print(f"'{slug}' already exists in {p}; it will be replaced.")
    data[key][slug] = entry
    if inputs:
        existing = {i.get("id") for i in data.get("inputs", [])}
        data.setdefault("inputs", []).extend(i for i in inputs if i["id"] not in existing)
    p.parent.mkdir(parents=True, exist_ok=True)
    backup(p)
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_toml(p: Path, slug: str, block: str) -> None:
    text = p.read_text(encoding="utf-8") if p.exists() else ""
    header = f"[mcp_servers.{slug}]"
    if header in text:
        sys.exit(f"{header} already exists in {p}. Edit it by hand; nothing was changed.")
    p.parent.mkdir(parents=True, exist_ok=True)
    backup(p)
    p.write_text(text + ("\n" if text and not text.endswith("\n") else "") + "\n" + block, encoding="utf-8")


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description="Install an MCP server from vic-awesome-mcp into your AI client.")
    ap.add_argument("server", help="server slug, or 'list'")
    ap.add_argument("--client", choices=CLIENTS, help="target client")
    ap.add_argument("--write", action="store_true", help="merge into the client's config file (a .bak copy is kept)")
    ap.add_argument("--full-access", action="store_true", help="use the read-write endpoint where the default is read-only")
    ap.add_argument("--with-key", action="store_true", help="send an API key even where it is optional or OAuth is available")
    ap.add_argument("--dir", help="folder to expose, for servers that need one (e.g. filesystem)")
    a = ap.parse_args()

    cat = load_catalog()
    if a.server == "list":
        for s in cat["servers"]:
            auth = {"none": "no key", "optional_api_key": "key optional", "oauth_or_token": "OAuth/token"}.get(s["auth"], s["auth"])
            print(f"{s['slug']:<18} {s['score']:>3}  {s['category']:<20} {auth:<13} {s['name']}")
        return
    s = find(cat, a.server)
    if not a.client:
        sys.exit("Add --client " + "|".join(CLIENTS))

    if "stdio" in s and "{dir}" in s["stdio"]["args"]:
        if a.dir:
            FOLDER[0] = str(Path(a.dir).expanduser().resolve())
        elif a.write:
            sys.exit(f"{s['slug']} needs a folder to work in: add --dir /path/to/folder (it can only touch that folder).")
    env = bearer_env(s, a.client, a.with_key)
    if a.client == "claude-code":
        print(claude_code_cmd(s, a.with_key, a.full_access))
    elif a.client == "codex":
        block = codex_toml(s, a.with_key, a.full_access)
        print(block)
        if a.write:
            p = config_path("codex")
            write_toml(p, s["slug"], block)
            print(f"Added to {p}")
    else:
        key = "servers" if a.client == "vscode" else "mcpServers"
        entry = json_entry(s, a.client, a.with_key, a.full_access)
        inputs = vscode_inputs(s, a.with_key) if a.client == "vscode" else None
        snippet = {key: {s["slug"]: entry}}
        if inputs:
            snippet["inputs"] = inputs
        print(json.dumps(snippet, indent=2, ensure_ascii=False))
        if a.write:
            p = config_path(a.client)
            write_json(p, key, s["slug"], entry, inputs)
            print(f"Added to {p}")
    h = s.get("http") or {}
    if "stdio" in s and "{dir}" in s["stdio"]["args"] and not a.dir:
        print(f"\nReplace {PLACEHOLDER_DIR} with the folder you want the AI to see, or re-run with --dir /your/folder.")
    if (h.get("url_full") or (s.get("stdio") or {}).get("args_full")) and not a.full_access:
        print("\nRead-only by default (safer). Add --full-access to let the AI write too.")
    if env:
        print(f"\nKey: set {env} in your environment"
              + (" (for Claude Desktop, replace the AUTH_HEADER placeholder in the config)" if a.client == "claude-desktop" else "")
              + ". Never commit it.")
    elif h.get("bearer_optional"):
        print("\nNo key needed. Add --with-key to send " + h["bearer_env"] + " for higher rate limits.")
    elif a.client in h.get("oauth_clients", []):
        print("\nNo key needed here: your client opens the service's sign-in page (OAuth) on first use.")
    print(f"Requires: {s['requires']}\nDocs: {s['repo']}\nRestart your client to load the server.")


if __name__ == "__main__":
    main()
