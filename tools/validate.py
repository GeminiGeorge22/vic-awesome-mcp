#!/usr/bin/env python3
"""Validate the catalog against SELECTION_STANDARD.md.

    python3 tools/validate.py            # structure, cards, scores, install configs
    python3 tools/validate.py --live     # + GitHub: not archived, pushed in last 30 days
    python3 tools/validate.py --smoke    # + connect to every no-key server and list tools (needs `pip install mcp`, Node for npx)
"""
from __future__ import annotations

import asyncio
import datetime as dt
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = ["slug", "name", "maintainer", "repo", "license", "stars", "category", "vic_lines", "auth", "requires",
            "verified", "score", "added"]
LINES = {"foreign-trade", "logistics", "one-person-company", "social-media"}
AUTH = {"none", "optional_api_key", "oauth_or_token", "api_key"}
CLIENTS = ["claude-desktop", "claude-code", "cursor", "vscode", "codex"]
errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def main() -> int:
    cat = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
    slugs = [s.get("slug") for s in cat["servers"]]
    if len(slugs) != len(set(slugs)):
        err("duplicate slugs")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for s in cat["servers"]:
        sl = s.get("slug", "?")
        for k in REQUIRED:
            if k not in s:
                err(f"{sl}: missing {k}")
        if ("stdio" in s) == ("http" in s):
            err(f"{sl}: needs exactly one of stdio/http")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", sl):
            err(f"{sl}: bad slug")
        if not set(s.get("vic_lines", [])) <= LINES or not s.get("vic_lines"):
            err(f"{sl}: vic_lines must be a non-empty subset of {sorted(LINES)}")
        if s.get("auth") not in AUTH:
            err(f"{sl}: auth must be one of {sorted(AUTH)}")
        if s.get("score", 0) < 85:
            err(f"{sl}: score {s.get('score')} below 85, not allowed in catalog")
        card = ROOT / "servers" / f"{sl}.md"
        if not card.exists():
            err(f"{sl}: missing card servers/{sl}.md")
        else:
            txt = card.read_text(encoding="utf-8")
            m = re.search(r"\*\*合计\*\* \| \*\*(\d+)\*\*", txt)
            parts = re.findall(r"^\| [^|]+ \| (\d+) / (\d+)", txt, flags=re.M)
            if not m:
                err(f"{sl}: card has no 合计 row")
            else:
                if int(m.group(1)) != s.get("score"):
                    err(f"{sl}: card total {m.group(1)} != catalog score {s.get('score')}")
                if sum(int(a) for a, _ in parts) != int(m.group(1)) or sum(int(b) for _, b in parts) != 100:
                    err(f"{sl}: score breakdown does not add up")
            for h in ["## 为什么收录", "## Vic 的用法", "## 一行安装", "## 手动配置", "## 注意事项与风险", "## 评分明细"]:
                if h not in txt:
                    err(f"{sl}: card missing section {h}")
        if f"servers/{sl}.md" not in readme:
            err(f"{sl}: not listed in README")
        for c in CLIENTS:
            r = subprocess.run([sys.executable, str(ROOT / "install.py"), sl, "--client", c], capture_output=True, text=True)
            if r.returncode != 0:
                err(f"{sl}: install.py failed for {c}: {r.stderr[-200:]}")
    if "--live" in sys.argv:
        live(cat)
    if "--smoke" in sys.argv:
        asyncio.run(smoke(cat))
    for e in errors:
        print("❌", e)
    print(f"{len(cat['servers'])} servers, {len(errors)} problems")
    return 1 if errors else 0


def live(cat: dict) -> None:
    now = dt.datetime.now(dt.timezone.utc)
    for s in cat["servers"]:
        m = re.match(r"https://github.com/([^/]+)/([^/#?]+)", s["repo"])
        if not m:
            continue
        try:
            with urllib.request.urlopen(f"https://api.github.com/repos/{m[1]}/{m[2]}", timeout=20) as r:
                d = json.loads(r.read())
        except Exception as e:  # noqa: BLE001
            err(f"{s['slug']}: GitHub lookup failed ({e})")
            continue
        if d.get("archived"):
            err(f"{s['slug']}: repo is archived")
        pushed = dt.datetime.fromisoformat(d["pushed_at"].replace("Z", "+00:00"))
        if (now - pushed).days > 30:
            err(f"{s['slug']}: no push in {(now - pushed).days} days")
        print(f"   {s['slug']}: ★{d.get('stargazers_count')} pushed {d['pushed_at'][:10]}")


async def smoke(cat: dict) -> None:
    from mcp import Client, StdioServerParameters

    for s in cat["servers"]:
        if s["auth"] not in {"none", "optional_api_key"}:
            print(f"   {s['slug']}: skipped smoke (needs a personal credential)")
            continue
        target = StdioServerParameters(command=s["stdio"]["command"], args=(["-y"] if s["stdio"]["command"] == "npx" else []) + list(s["stdio"]["args"])) \
            if "stdio" in s else s["http"]["url"]
        try:
            async with Client(target, read_timeout_seconds=90) as c:
                n = len((await c.list_tools()).tools)
            print(f"   {s['slug']}: {n} tools")
            if s.get("tools_count") and n != s["tools_count"]:
                print(f"   {s['slug']}: note, catalog says {s['tools_count']} tools; update it")
        except Exception as e:  # noqa: BLE001
            err(f"{s['slug']}: smoke test failed ({type(e).__name__}: {str(e)[:150]})")


if __name__ == "__main__":
    sys.exit(main())
