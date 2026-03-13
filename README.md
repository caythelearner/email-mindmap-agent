# Email Intelligence Hub

Fetch your Gmail, analyze with Claude AI, and generate an interactive dashboard with mind maps, word clouds, and deadline tracking.

## Features

- **Interactive Mind Map** — Emails classified by topic, rendered as a zoomable/pannable tree (radial, horizontal, or vertical layout). **Click any leaf node to view the original email** (subject, date, snippet) and verify AI accuracy.
- **Anti-Hallucination** — Each mind map node is linked back to source emails via index tracking. AI is strictly prompted to only use provided emails. Invalid indices are auto-filtered with warnings.
- **Gmail Quick Search** — Click "Search in Gmail" in the email detail popup to jump directly to the matching email in your inbox.
- **Word Cloud** — AI-extracted keywords sized by importance. Hover for details.
- **DDL Tracker** — Deadlines and action items extracted from emails, color-coded by urgency with countdown timers and filter buttons.

## Demo

📹 **[Watch demo video](https://github.com/caythelearner/email-mindmap-agent/releases/download/v1.0.0/example.mp4)** (5.8 MB)

<video src="https://github.com/caythelearner/email-mindmap-agent/releases/download/v1.0.0/example.mp4" controls width="640"></video>

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
| `MAX_EMAILS` | Number of recent emails to fetch (default: 30) |
| `MY_CONTEXT` | Your background info so the AI understands your emails better |
| `FILTER` | Optional: `TIME_RANGE`, `INCLUDE_LABEL`, `INCLUDE_SENDERS`. See [FILTER_README.md](FILTER_README.md) |

## Usage

```bash
python main_agent.py
```

This generates `dashboard.html` and opens it in your browser with three interactive panels:

1. **Mind Map** — Switch between radial/horizontal/vertical layouts. Click leaf nodes to see original email content and verify AI summaries.
2. **Word Cloud** — Visual keyword analysis with top-10 sidebar
3. **DDL Tracker** — Filter by urgency (Urgent / This Week / Later)

**Dashboard filters** (header): Date range (All / 7 days / 30 days) and exclude filters (Promotions, Social, Updates, Keywords) — no re-run needed.

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
