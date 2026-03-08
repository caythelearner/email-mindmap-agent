# Email Intelligence Hub

Fetch your Gmail, analyze with Claude AI, and generate an interactive dashboard with mind maps, word clouds, and deadline tracking.

## Features

- **Interactive Mind Map** — Emails classified by topic, rendered as a zoomable/pannable tree (radial, horizontal, or vertical layout). Click nodes to expand/collapse.
- **Word Cloud** — AI-extracted keywords sized by importance. Hover for details.
- **DDL Tracker** — Deadlines and action items extracted from emails, color-coded by urgency with countdown timers and filter buttons.

## Demo

![Dashboard Preview](assets/dashboard-preview.png)

## Requirements

- Python 3.8+
- [gws](https://github.com/googleworkspace/cli) (Google Workspace CLI for Gmail access via OAuth)
- Anthropic API Key ([get one here](https://console.anthropic.com/))

## Installation

```bash
git clone https://github.com/caythelearner/email-mindmap-agent.git
cd email-mindmap-agent

pip install -r requirements.txt

cp config.example.json config.json
# Edit config.json with your API key and personal context
```

## Configuration

| Field | Description |
|-------|-------------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `GMAIL_USER_ID` | Usually `"me"` (current authenticated user) |
| `MAX_EMAILS` | Number of recent emails to fetch (default: 10) |
| `MY_CONTEXT` | Your background info so the AI understands your emails better |

## Usage

```bash
python main_agent.py
```

This generates `dashboard.html` and opens it in your browser with three interactive panels:

1. **Mind Map** — Switch between radial/horizontal/vertical layouts
2. **Word Cloud** — Visual keyword analysis with top-10 sidebar
3. **DDL Tracker** — Filter by urgency (Urgent / This Week / Later)

## Gmail Authorization

Set up Gmail access via the `gws` CLI:

```bash
# Install gws: https://github.com/googleworkspace/cli
gws auth login
# Grant Gmail read permissions when prompted
```

## Tech Stack

- **Claude Haiku** — Email classification, keyword extraction, deadline detection
- **ECharts** — Interactive tree charts and word cloud visualization
- **gws CLI** — Gmail API access

## License

MIT
