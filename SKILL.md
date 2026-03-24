---
name: browser-use
description: Browser Use Clone - AI-native browser automation with structured output, session management, and coding agent integration.
---

# Browser Use Clone - Friday AI Edition

> AI-native browser automation with Playwright, structured output, and coding agent support.

## Features

- 🤖 AI-Native: Describe goal in plain text, get structured data
- 🎯 Structured Output: Define schemas, get typed JSON
- 🔒 Stealth Mode: Anti-fingerprint, bypasses Cloudflare
- 💾 Session Management: Persistent login states
- 📡 Real-time View: Live browser monitoring
- 🔧 Coding Agent Support: Claude Code, Codex integration

## Quick Start

```bash
# Install
pip install playwright pydantic
npx playwright install chromium

# Run task
python3 $SKILL_DIR/src/browser_agent.py "Find headlines from bbc.com"
```

## Architecture

```
browser-use/
├── SKILL.md           # This file
├── src/
│   ├── browser_agent.py   # Main agent
│   ├── session.py         # Session management  
│   ├── playwright_lib.py   # Playwright wrapper
│   └── schema.py          # Structured output
└── scripts/
    └── cli.py             # CLI tool
```

## Configuration

Edit `config/settings.json`:

```json
{
  "headless": false,
  "stealth": true,
  "timeout": 30000
}
```

---

*Built for Friday AI | Powered by OpenClaw*
