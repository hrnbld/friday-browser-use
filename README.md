# 🤖 Friday AI - Browser Use Clone

AI-native browser automation skill for Friday AI Agent, built with Playwright.

## 🌟 Features

- **🤖 AI-Native**: Describe goals in plain text, get structured data
- **🎯 Structured Output**: Define Pydantic schemas for typed JSON results
- **🔒 Stealth Mode**: Anti-fingerprint, bypasses Cloudflare
- **💾 Session Management**: Persistent login states
- **📡 Real-time View**: Live browser monitoring
- **🔧 Coding Agent Support**: Claude Code, Codex integration ready

## 📦 Installation

```bash
pip install playwright pydantic
npx playwright install chromium
```

## 🚀 Quick Start

```bash
# Run a simple task
python3 scripts/cli.py "Find headlines from bbc.com"

# Use as a module
python3 -c "
from src.browser_agent import BrowserAgent
agent = BrowserAgent(headless=False)
result = agent.run('Search for AI news on Google')
print(result.output)
"
```

## 📁 Project Structure

```
browser-use/
├── SKILL.md              # Skill definition
├── README.md             # This file
├── config/
│   └── settings.json     # Configuration
├── scripts/
│   └── cli.py            # CLI tool
└── src/
    ├── __init__.py
    ├── browser_agent.py  # Main agent
    ├── session.py        # Session management
    ├── playwright_lib.py # Playwright wrapper
    └── schema.py         # Structured output
```

## ⚙️ Configuration

Edit `config/settings.json`:

```json
{
  "headless": false,
  "stealth": true,
  "timeout": 30000,
  "model": "minimax-m2.7:cloud"
}
```

## 📖 Usage Examples

### CLI Usage

```bash
# Search and extract
python3 scripts/cli.py "Find pricing plans on browser-use.com"

# Take screenshot
python3 scripts/cli.py "Take a screenshot of github.com"

# Extract structured data
python3 scripts/cli.py "Get all blog post titles from medium.com"
```

### Python API

```python
from src.browser_agent import BrowserAgent

# Initialize
agent = BrowserAgent(headless=False, stealth=True)

# Run task
result = agent.run(
    "Find the top 5 trending topics on Hacker News",
    schema={
        "topics": ["string"]
    }
)

print(result.output)
```

## 🔐 Powered by

- **OpenClaw** - AI Agent Gateway
- **Playwright** - Browser Automation
- **Pydantic** - Structured Output

---

*Built for Friday AI Agent | @hrnbld*
