# Alfred CC Tools

Claude Code plugin marketplace for the Alfred platform - content processing, automation, and productivity tools.

## Installation

### Add the Marketplace

```bash
/plugin marketplace add screenfields/alfred-cc-tools
```

### Install Plugins

```bash
# Install the alfred-content plugin
/plugin install alfred-content@alfred-cc-tools
```

### Update Plugins

```bash
/plugin marketplace update
```

## Available Plugins

### alfred-agent

Agent workflow utilities — messaging, coordination, ECR, and development discipline for the Alfred platform.

**Features:**
- **Messaging:** Inter-agent communication via bundled `agent-messaging` MCP (send, receive, threads, inbox management)
- **Skills:** `design`, `develop`, `documentation`, `ecr`, `git-commit`, `land`, `retro`, `messaging`
- **Slash commands:** `init`, `check-messages`, `show-inbox`, `show-threads`, plus one per skill
- **ECR:** Expert Consulting Review — multi-model architectural feedback via LiteLLM (gpt-5.4, gemini-3.1-pro, glm-5)

**Installation:**
```bash
/plugin install alfred-agent@alfred-cc-tools
```

**Usage:**
```
/alfred-agent:init                  # One-time project setup
/alfred-agent:check-messages        # Check inbox from other agents
/alfred-agent:develop               # Pick up a GitHub issue and implement it
/alfred-agent:retro                 # Session retrospective + RSI
```

### alfred-platform-ops

Platform operations utilities for managing Alfred platform repositories.

**Skills:**
- `alfred-platform-ops:repo-management` — Repository lifecycle management with four sub-modes:
  - `setup`: Scaffold a new repo with standard protection, labels, and structure
  - `verify-access`: Diagnose the full App → gitops manifest → live token permission chain (all three layers)
  - `audit`: Read-only compliance sweep — protection rules, required labels, standard files
  - `update-protection`: Apply standard branch protection to a repo's main branch

**Installation:**
```bash
/plugin install alfred-platform-ops@alfred-cc-tools
```

### alfred-content

Content processing utilities for YouTube transcripts, web articles, and document summarization.

**Features:**
- **Transcript Skill**: Fetch YouTube video transcripts with metadata
- **Summarize Skill**: Generate concise summaries with optional domain context
- **Summarizer Agent**: Token-efficient sub-agent for large documents

**Installation:**
```bash
/plugin install alfred-content@alfred-cc-tools
```

**Usage:**
```
"Get the transcript from https://youtube.com/watch?v=xyz"
"Summarize ./content/youtube/20250108_Video/Video-details.md"
```

**Output Structure:**
```
./content/
└── youtube/
    └── YYYYMMDD_Title/
        ├── Title-details.md    # Full transcript
        └── Title-summary.md    # Summary
```

## Team Configuration

Add to `.claude/settings.json` for automatic availability:

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

## Plugin Development

Want to add your plugin to this marketplace? Open a PR with:

1. Add your plugin entry to `.claude-plugin/marketplace.json`
2. Update this README with plugin details
3. Ensure your plugin repo has `.claude-plugin/plugin.json`

## Support

- [Alfred CC Tools on GitHub](https://github.com/Screenfields/alfred-cc-tools)
- [Claude Code Plugin Docs](https://code.claude.com/docs/en/plugins)
- Issues: Open an issue in the relevant plugin repository

## License

Each plugin maintains its own license. See individual plugin repositories for details.
