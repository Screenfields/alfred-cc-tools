#!/usr/bin/env python3
"""
Validate .claude-plugin/marketplace.json structure.

Exit codes:
  0  — valid (warnings may still be printed)
  1  — structural validation failed (hard gate)
"""

import json
import re
import sys
import urllib.request
import urllib.error
import os

MARKETPLACE_PATH = ".claude-plugin/marketplace.json"
KEBAB_RE = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')

errors = []
warnings = []


def fail(msg):
    errors.append(msg)
    print(f"ERROR: {msg}", file=sys.stderr)


def warn(msg):
    warnings.append(msg)
    print(f"WARNING: {msg}")


# ── 1. Load and parse JSON ──────────────────────────────────────────────────
try:
    with open(MARKETPLACE_PATH) as f:
        data = json.load(f)
    print(f"OK: {MARKETPLACE_PATH} is valid JSON")
except FileNotFoundError:
    fail(f"File not found: {MARKETPLACE_PATH}")
    sys.exit(1)
except json.JSONDecodeError as exc:
    fail(f"Invalid JSON: {exc}")
    sys.exit(1)

# ── 2. Top-level required fields ─────────────────────────────────────────────
if not isinstance(data.get("name"), str) or not data["name"]:
    fail("Top-level 'name' must be a non-empty string")

owner = data.get("owner")
if not isinstance(owner, dict):
    fail("Top-level 'owner' must be an object")
elif not isinstance(owner.get("name"), str) or not owner["name"]:
    fail("'owner.name' must be a non-empty string")

plugins = data.get("plugins")
if not isinstance(plugins, list):
    fail("Top-level 'plugins' must be an array")
    sys.exit(1)  # Can't validate plugins without the array

# ── 3. Per-plugin validation ──────────────────────────────────────────────────
seen_names = {}
github_repos_to_check = []

for idx, plugin in enumerate(plugins):
    prefix = f"plugins[{idx}]"

    # name: required, string, kebab-case
    pname = plugin.get("name")
    if not isinstance(pname, str) or not pname:
        fail(f"{prefix}: 'name' must be a non-empty string")
        pname = None
    elif not KEBAB_RE.match(pname):
        fail(f"{prefix}: 'name' must be kebab-case (got '{pname}')")

    if pname is not None:
        if pname in seen_names:
            fail(f"{prefix}: duplicate plugin name '{pname}' (first seen at plugins[{seen_names[pname]}])")
        else:
            seen_names[pname] = idx

    # source: required, object with 'source' key
    source = plugin.get("source")
    if not isinstance(source, dict):
        fail(f"{prefix} ({pname!r}): 'source' must be an object")
    elif "source" not in source:
        fail(f"{prefix} ({pname!r}): 'source' object must have a 'source' key")
    else:
        # Collect GitHub repos for existence check (warning-only)
        if source.get("source") == "github":
            repo = source.get("repo")
            if isinstance(repo, str) and repo:
                github_repos_to_check.append((pname, repo))
            else:
                fail(f"{prefix} ({pname!r}): github source must have a non-empty 'repo' field")

if errors:
    print(f"\nStructural validation FAILED with {len(errors)} error(s).", file=sys.stderr)
    sys.exit(1)

print(f"OK: All {len(plugins)} plugin(s) passed structural validation")

# ── 4. GitHub repo existence checks (warning-only) ───────────────────────────
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
if GITHUB_TOKEN:
    headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

for pname, repo in github_repos_to_check:
    api_url = f"https://api.github.com/repos/{repo}"
    req = urllib.request.Request(api_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                print(f"OK: plugin '{pname}' repo '{repo}' is reachable")
            else:
                warn(f"plugin '{pname}' repo '{repo}' returned HTTP {resp.status} — verify the repo exists")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            warn(f"plugin '{pname}' repo '{repo}' not found (HTTP 404) — verify 'source.repo' is correct")
        elif exc.code == 403:
            warn(f"plugin '{pname}' repo '{repo}' returned 403 (rate-limited or private) — skipping existence check")
        else:
            warn(f"plugin '{pname}' repo '{repo}' returned HTTP {exc.code} — could not verify existence")
    except Exception as exc:
        warn(f"plugin '{pname}' repo '{repo}' could not be reached ({exc}) — check network or repo name")

if warnings:
    print(f"\n{len(warnings)} warning(s) emitted (non-blocking).")

print("\nValidation complete.")
sys.exit(0)
