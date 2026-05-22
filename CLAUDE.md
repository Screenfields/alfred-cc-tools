# CLAUDE.md

Guidance for Claude Code sessions running as the **alfred-cc-tools lead-agent**. This repo is the catalog hub of a 3-repo constellation that ships Claude Code plugins to every other agent on the Alfred platform.

## Lead-agent role

- **Messaging identity:** `alfred-cc-tools` (registered in agent-messaging service). One identity owns all 3 repos in the constellation; worker sub-agents do not have their own identities.
- **Scope:** marketplace catalog, plugin source repos, cross-agent reusable GH Actions workflows.
- **Blast radius:** tooling shipped here propagates to every platform agent via the marketplace. Mistakes here propagate fastest of any project on the platform — **be conservative on releases**, prefer minor version bumps with cache-invalidation rationale documented in the PR, and run `alfred-agent:review` on PRs once that skill exists.
- **Coordination:** when changes affect architecture (alfred-platform) or project scaffolding (project-manager), message those agents via agent-messaging before merging. Do not unilaterally land changes that other leads need to adopt.

## Constellation map

The lead-agent's domain spans 3 repos. Which repo holds what:

| Repo | Role |
|------|------|
| `Screenfields/alfred-cc-tools` (this repo) | Marketplace catalog (`.claude-plugin/marketplace.json`), cross-agent reusable GH Actions workflows (e.g., `.github/workflows/path-acl.yml` once it lands), README/LICENSE |
| `Screenfields/ccplugin-alfred-agent-workflow` | Source for `alfred-agent:*` skills (SKILL.md files). New skills like `alfred-agent:review`, `alfred-agent:merge`, `alfred-agent:troubleshoot`, `alfred-agent:drop-issue` land HERE, **not in this repo** |
| `Screenfields/ccplugin-alfred-content` | Source for `alfred-content:*` skills (transcript, summarize) |

**Common mistake to avoid:** authoring a new `alfred-agent:*` skill in this repo. Skill SKILL.md files live in the plugin source repos. This repo only references them by version pin.

## Self-bootstrap rhythm

When the lead-agent authors a new skill or updates an existing one, the loop is:

1. Author/edit SKILL.md in the relevant plugin source repo (`ccplugin-alfred-agent-workflow` or `ccplugin-alfred-content`)
2. Merge that PR
3. Bump the version pin for the plugin in this repo's `.claude-plugin/marketplace.json`
4. Merge the bump PR
5. Lead-agent's devbox cold-restart picks up the new version via the `install-alfred-plugin` init container
6. New session in the devbox has the new/updated skill loaded

**The rhythm is "author -> release-bump -> restart -> use."** Not instant; cache + restart latency factor. Don't get confused why the skill you just authored isn't immediately available in the current session — it requires a devbox cold-restart. For urgent in-session use, the SKILL.md content can be referenced directly from the source repo, but the canonical loading path is via the marketplace pin.

## Cross-project doctrine (forward reference)

Cross-project rules (the 9 doctrine items from the 2026-05-22 retro) will eventually live in `Screenfields/alfred-platform-docs`. **That repo does not exist yet.** When it lands, this CLAUDE.md should be thinned to reference it for cross-project rules instead of restating them.

## Repository purpose (this repo)

Claude Code plugin marketplace for the Alfred platform — a central registry that distributes plugins to all platform agents. Uses **remote plugins**: contains only marketplace metadata pointing to external plugin repositories. Actual plugin code lives in the constellation's plugin source repos (see map above).

## Repository structure

```
.claude-plugin/
└── marketplace.json    # Marketplace registry - defines available plugins

.github/workflows/      # Reusable cross-agent GH Actions (e.g., path-acl.yml)
README.md               # User-facing documentation
CLAUDE.md               # This file
```

## Marketplace configuration

`.claude-plugin/marketplace.json` is the core of this repo.

**Required fields:** `name` (kebab-case), `owner` (with `name`, optional `email`), `plugins` (array).

**Optional fields:** `metadata.description`, `metadata.version`.

### Plugin entry structure

Each entry in `plugins`:

- **Required:** `name` (plugin identifier, used as `plugin-name@marketplace-name`), `source` (where to fetch).
- **Optional:** `description`, `version`, `keywords`, `category`, `author`, `homepage`, `license`, `strict` (default `true` — plugin repo must have `.claude-plugin/plugin.json`).

### Plugin source types

This marketplace uses GitHub sources:

```json
{
  "name": "plugin-name",
  "source": {
    "source": "github",
    "repo": "owner/repo-name"
  }
}
```

Other supported types (not currently used): local/relative paths (`"source": "./plugins/plugin-name"`), generic git URLs (`"source": { "source": "url", "url": "https://..." }`).

## Adding / bumping plugins

**Adding a new plugin to the catalog:**

1. Ensure the plugin repository exists and has `.claude-plugin/plugin.json`
2. Add an entry to `plugins` in `.claude-plugin/marketplace.json`
3. Update README.md "Available Plugins" section
4. Validate: `/plugin validate .` (or `claude plugin validate .`)
5. Commit, push, PR

**Bumping a version pin** (most common operation here):

1. Confirm the upstream plugin repo has the target version tagged + merged
2. Edit `version` in the matching plugin entry in `marketplace.json`
3. Commit message style: `alfred-agent: bump pin X.Y.Z -> A.B.C (<reason>)` — match recent commits
4. Open PR; merge after CI

**Constraints:**

- Each plugin repository must contain its own `.claude-plugin/plugin.json` (since `strict` defaults to `true`)
- Use kebab-case for plugin names
- Source repository must be publicly accessible

## Validation

Always validate before committing:

```bash
claude plugin validate .
# or in Claude Code:
/plugin validate .
```

Common validation errors: invalid JSON, duplicate plugin names, missing required fields.

## Installation commands (for users of the marketplace)

```bash
/plugin marketplace add screenfields/alfred-cc-tools
/plugin install plugin-name@alfred-cc-tools
/plugin marketplace update
```

## Team configuration

Teams pre-configure in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "alfred-cc-tools": {
      "source": { "source": "github", "repo": "screenfields/alfred-cc-tools" }
    }
  },
  "enabledPlugins": {
    "alfred-content@alfred-cc-tools": true
  }
}
```

This auto-adds the marketplace and enables specified plugins for all team members.

## Important constraints

### Reserved marketplace names

Cannot use: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `life-sciences`.

### Plugin caching behavior

Installed plugins are copied to a cache location, so:

- Plugins **cannot reference files outside their directory** (no `../shared-utils`)
- Use symlinks to share code between plugins (followed during copying)
- Use `${CLAUDE_PLUGIN_ROOT}` for internal plugin references in hooks/MCP configs

### Release conservatism

- Don't bump pins speculatively — only when the upstream change is merged and verified
- Document the reason for cache-invalidation-only bumps in the PR title (see commit history pattern)
- A bad pin here breaks every downstream agent's next devbox cold-restart

## Development workflow

1. **Adding a plugin:** update `marketplace.json` -> validate -> update README -> commit -> PR
2. **Testing locally:** `/plugin marketplace add .` to test before pushing
3. **Validation:** always run `/plugin validate .` before committing
4. **Cross-repo work:** if a change requires updating a plugin source repo AND this catalog, land the source-repo PR first, then the catalog bump (otherwise consumers race ahead of the source)
