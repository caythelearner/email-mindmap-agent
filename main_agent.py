import subprocess
import json
import sys
import os
import re
from datetime import datetime
from email.utils import parsedate_to_datetime
from anthropic import Anthropic
from visualizer import render_dashboard

# Force UTF-8 on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_config():
    config_path = os.path.join(SCRIPT_DIR, "config.json")
    if not os.path.exists(config_path):
        print("config.json not found. Copy config.example.json to config.json and add your API key:")
        print("  cp config.example.json config.json")
        sys.exit(1)
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_config()
client = Anthropic(api_key=CONFIG["ANTHROPIC_API_KEY"])


def parse_date(date_str):
    """Parse email date header into 'MM-DD HH:MM' format."""
    if not date_str or not date_str.strip():
        return "Unknown"
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime('%m-%d %H:%M')
    except Exception:
        try:
            parts = date_str.split()
            if len(parts) < 5:
                return "Unknown"
            dt = datetime.strptime(
                f"{parts[1]} {parts[2]} {parts[3]} {parts[4]}",
                '%d %b %Y %H:%M:%S')
            return dt.strftime('%m-%d %H:%M')
        except (IndexError, ValueError):
            return "Unknown"


def fetch_data():
    """Fetch recent emails via gws CLI."""
    print(f"Fetching the latest {CONFIG['MAX_EMAILS']} emails...")
    params = json.dumps({
        "userId": CONFIG["GMAIL_USER_ID"],
        "maxResults": CONFIG["MAX_EMAILS"]
    })
    res = subprocess.run(
        ["gws", "gmail", "users", "messages", "list", "--params", params],
        capture_output=True, text=True, encoding='utf-8', shell=True)

    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(
            f"Gmail API returned invalid JSON: {res.stderr or res.stdout[:200]}")

    msg_ids = [m['id'] for m in data.get('messages', [])]
    emails = []
    for mid in msg_ids:
        detail = subprocess.run(
            ["gws", "gmail", "users", "messages", "get",
             "--params", json.dumps({"userId": "me", "id": mid})],
            capture_output=True, text=True, encoding='utf-8', shell=True)
        try:
            msg_data = json.loads(detail.stdout)
        except json.JSONDecodeError:
            continue
        headers = msg_data.get('payload', {}).get('headers', [])
        date_raw = next(
            (h['value'] for h in headers if h['name'] == 'Date'), "")
        emails.append({
            "date": parse_date(date_raw),
            "subject": next(
                (h['value'] for h in headers if h['name'] == 'Subject'),
                "No Subject"),
            "snippet": msg_data.get('snippet', "")
        })
    return emails


def get_ai_structured_data(emails):
    """Classify emails into categories via Claude."""
    print("Claude is classifying emails...")
    prompt = f"""You are a personal email assistant. Context about the user: {CONFIG['MY_CONTEXT']}.
Classify the following emails by topic and return pure JSON only.

Requirements:
1. Format: {{"CategoryName": ["Brief1 MM-DD HH:MM", "Brief2 MM-DD HH:MM"]}}
2. Each brief: keep date/time from the email, format as "brief content MM-DD HH:MM"
3. Use short category names, e.g. "Banking", "Cloud Services", "Job Search"
4. No special symbols like # $ () [] {{}} / etc.
5. Return pure JSON only, no markdown code blocks, no explanation

Emails: {json.dumps(emails, ensure_ascii=False)}"""

    response = client.messages.create(
        model="claude-haiku-4-5", max_tokens=2000,
        messages=[{"role": "user", "content": prompt}])
    content = response.content[0].text.strip()
    if "```" in content:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        content = match.group() if match else content
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse AI JSON: {e}\n{content[:300]}...")


def get_wordcloud_data(emails):
    """Extract keywords and weights for word cloud visualization."""
    print("Claude is extracting keywords...")
    prompt = f"""You are a personal email assistant. Context about the user: {CONFIG['MY_CONTEXT']}.
Extract keywords and importance weights from these emails for a word cloud.

Requirements:
1. Extract 30-60 meaningful keywords (any language is fine)
2. Weight range 1-100, more important/frequent = higher weight
3. Ignore stopwords (the, is, a, of, etc.)
4. Focus on: names, organizations, projects, technical terms, key events
5. Return pure JSON array: [{{"word": "keyword", "weight": 50}}, ...]
6. Return pure JSON only, no markdown code blocks, no explanation

Emails: {json.dumps(emails, ensure_ascii=False)}"""

    response = client.messages.create(
        model="claude-haiku-4-5", max_tokens=2000,
        messages=[{"role": "user", "content": prompt}])
    content = response.content[0].text.strip()
    if "```" in content:
        match = re.search(r'\[.*\]', content, re.DOTALL)
        content = match.group() if match else content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return [{"word": "parse_error", "weight": 100}]


def get_deadline_data(emails):
    """Extract deadlines, action items, and important dates."""
    print("Claude is extracting deadlines...")
    today = datetime.now().strftime('%Y-%m-%d')
    prompt = f"""You are a personal email assistant. Context about the user: {CONFIG['MY_CONTEXT']}.
Today is {today}. Extract all deadlines, action items, and important dates from these emails.

Requirements:
1. Identify items with explicit or implied deadlines
2. Identify action items (even without a clear date, suggest a reasonable deadline)
3. Return pure JSON array:
   [{{"title": "Item name", "date": "YYYY-MM-DD", "source": "Source email subject", "urgency": "high/medium/low", "description": "Brief explanation"}}]
4. Urgency rules:
   - high: due within 3 days or overdue
   - medium: due within a week
   - low: more than a week out
5. If no deadlines found, return empty array []
6. Return pure JSON only, no markdown code blocks, no explanation

Emails: {json.dumps(emails, ensure_ascii=False)}"""

    response = client.messages.create(
        model="claude-haiku-4-5", max_tokens=2000,
        messages=[{"role": "user", "content": prompt}])
    content = response.content[0].text.strip()
    if "```" in content:
        match = re.search(r'\[.*\]', content, re.DOTALL)
        content = match.group() if match else content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return []


if __name__ == "__main__":
    try:
        emails = fetch_data()
        structured_json = get_ai_structured_data(emails)
        wordcloud_data = get_wordcloud_data(emails)
        deadline_data = get_deadline_data(emails)
        output_path = os.path.join(SCRIPT_DIR, "dashboard.html")
        render_dashboard(structured_json, wordcloud_data, deadline_data,
                         output_path)
        print("Dashboard generated and opened!")
    except Exception as e:
        print(f"Run failed: {repr(e)}")
