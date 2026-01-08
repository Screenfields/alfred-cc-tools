# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a Claude Code plugin marketplace repository for the Alfred platform. It serves as a central registry for distributing Claude Code plugins related to Alfred platform tools and utilities.

This marketplace uses **remote plugins** - the repository contains only marketplace metadata that points to external plugin repositories hosted on GitHub. The actual plugin code lives in separate repositories.

## Repository Structure

```
.claude-plugin/
└── marketplace.json    # Marketplace registry - defines available plugins

README.md              # User-facing documentation
```

## Marketplace Configuration

The `.claude-plugin/marketplace.json` file is the core of this repository. It defines:

**Required Fields:**
- `name`: Marketplace identifier (kebab-case, e.g., "alfred-cc-tools")
- `owner`: Maintainer info with `name` (required) and `email` (optional)
- `plugins`: Array of available plugins

**Optional Fields:**
- `metadata.description`: Marketplace description
- `metadata.version`: Marketplace version

### Plugin Entry Structure

Each plugin in the `plugins` array has:

**Required:**
- `name`: Plugin identifier (used as `plugin-name@marketplace-name`)
- `source`: Where to fetch the plugin

**Optional:**
- `description`: What the plugin does
- `version`: Plugin version
- `keywords`: Array of tags for discovery
- `category`: Plugin category (e.g., "productivity")
- `author`: Author info object
- `homepage`: Documentation URL
- `license`: SPDX identifier
- `strict`: Boolean (default: true) - when true, plugin repo must have `.claude-plugin/plugin.json`

### Plugin Source Types

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

Other supported source types (not currently used):
- Local/relative paths: `"source": "./plugins/plugin-name"`
- Generic git URLs: `"source": { "source": "url", "url": "https://..." }`

## Adding New Plugins

When adding a new plugin to the marketplace:

1. Ensure the plugin repository exists and has `.claude-plugin/plugin.json`
2. Add a new entry to the `plugins` array in `.claude-plugin/marketplace.json`
3. Update the README.md "Available Plugins" section with plugin details
4. Validate the marketplace: `/plugin validate .`
5. Commit and push changes

**Important:**
- Each plugin repository must contain its own `.claude-plugin/plugin.json` (since `strict` defaults to true)
- Use kebab-case for plugin names
- Ensure source repository is publicly accessible

## Validation

Before committing changes, validate the marketplace:

```bash
# Using CLI
claude plugin validate .

# Or using slash command in Claude Code
/plugin validate .
```

Common validation errors:
- Invalid JSON syntax in marketplace.json
- Duplicate plugin names
- Missing required fields

## Installation Commands

Users install this marketplace and its plugins using:

```bash
# Add marketplace
/plugin marketplace add screenfields/alfred-cc-tools

# Install specific plugin
/plugin install plugin-name@alfred-cc-tools

# Update marketplace catalog
/plugin marketplace update
```

## Team Configuration

For teams, plugins can be pre-configured in `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "alfred-cc-tools": {
      "source": {
        "source": "github",
        "repo": "screenfields/alfred-cc-tools"
      }
    }
  },
  "enabledPlugins": {
    "alfred-content@alfred-cc-tools": true
  }
}
```

This automatically adds the marketplace and enables specified plugins for all team members.

## Important Constraints

### Reserved Marketplace Names

Cannot use these reserved names:
- `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`
- `anthropic-marketplace`, `anthropic-plugins`
- `agent-skills`, `life-sciences`

### Plugin Caching Behavior

When plugins are installed, they're copied to a cache location. This means:
- Plugins **cannot reference files outside their directory** (no `../shared-utils`)
- Use symlinks if sharing code between plugins (followed during copying)
- Use `${CLAUDE_PLUGIN_ROOT}` variable for internal plugin references in hooks/MCP configs

## Development Workflow

1. **Adding a plugin**: Update marketplace.json → validate → update README → commit
2. **Testing locally**: `/plugin marketplace add .` to test the marketplace before pushing
3. **Validation**: Always run `/plugin validate .` before committing changes
