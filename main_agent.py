import subprocess
import json
import sys
import re
import os
from datetime import datetime
from email.utils import parsedate_to_datetime
from anthropic import Anthropic
from visualizer import render_styled_mindmap

# Force UTF-8 on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_config():
    if not os.path.exists("config.json"):
        print("❌ config.json not found. Copy config.example.json to config.json and add your API Key")
        print("   cp config.example.json config.json")
        sys.exit(1)
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()
client = Anthropic(api_key=CONFIG["ANTHROPIC_API_KEY"])

def parse_date(date_str):
    """Parse email date+time, e.g. '03-07 14:30'"""
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
            dt = datetime.strptime(f"{parts[1]} {parts[2]} {parts[3]} {parts[4]}", '%d %b %Y %H:%M:%S')
            return dt.strftime('%m-%d %H:%M')
        except (IndexError, ValueError):
            return "Unknown"

def fetch_data():
    print(f"🛰️ Fetching the latest {CONFIG['MAX_EMAILS']} emails...")
    params = json.dumps({"userId": CONFIG["GMAIL_USER_ID"], "maxResults": CONFIG["MAX_EMAILS"]})
    res = subprocess.run(["gws", "gmail", "users", "messages", "list", "--params", params],
                         capture_output=True, text=True, encoding='utf-8', shell=True)

    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Gmail API returned invalid JSON: {res.stderr or res.stdout[:200]}")

    msg_ids = [m['id'] for m in data.get('messages', [])]
    emails = []

    for mid in msg_ids:
        detail = subprocess.run(["gws", "gmail", "users", "messages", "get", "--params", json.dumps({"userId": "me", "id": mid})],
                                capture_output=True, text=True, encoding='utf-8', shell=True)
        try:
            msg_data = json.loads(detail.stdout)
        except json.JSONDecodeError:
            continue
        headers = msg_data.get('payload', {}).get('headers', [])
        date_raw = next((h['value'] for h in headers if h['name'] == 'Date'), "")

        emails.append({
            "date": parse_date(date_raw),
            "subject": next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject"),
            "snippet": msg_data.get('snippet', "")
        })
    return emails

def clean_text(text):
    """Remove characters that break Mermaid parsing"""
    if not text:
        return ""
    s = str(text).replace('"', "'").replace("\n", " ").replace("\\", " ")
    for ch in '()[]{}#/<>|`':
        s = s.replace(ch, " ")
    return " ".join(s.split()).strip()

def get_ai_structured_data(emails):
    print("🧠 Claude Haiku is analyzing and classifying...")
    prompt = f"""You are Anyue's personal assistant. Context: {CONFIG['MY_CONTEXT']}.
Classify the following emails by topic and return pure JSON only.

Requirements:
1. Format: {{"CategoryName": ["Brief1 MM-DD HH:MM", "Brief2 MM-DD HH:MM"]}}
2. Each brief: keep date/time from the email, format as "brief content MM-DD HH:MM"
3. Use short English category names, e.g. "Bank Notifications", "Cloud Services"
4. No special symbols like # $ () [] {{}} / etc.
5. Return pure JSON only, no markdown code blocks, no explanation

Emails: {json.dumps(emails, ensure_ascii=False)}"""

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.content[0].text.strip()
    if "```" in content:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        content = match.group() if match else content
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse AI JSON: {e}\nRaw content: {content[:300]}...")

def build_mermaid_code(structured_data):
    """Build Mermaid mindmap code"""
    if not isinstance(structured_data, dict):
        structured_data = {}
    lines = ["mindmap", "  hub((Anyue Intelligence Hub))"]

    for category, items in structured_data.items():
        safe_cat = clean_text(str(category))
        lines.append(f'    "{safe_cat}"')
        item_list = items if isinstance(items, list) else [str(items)]
        for item in item_list:
            safe_item = clean_text(str(item))
            if safe_item:
                lines.append(f'      "{safe_item}"')

    return "\n".join(lines)

if __name__ == "__main__":
    try:
        data = fetch_data()
        structured_json = get_ai_structured_data(data)
        mermaid_code = build_mermaid_code(structured_json)
        item_count = 1 + sum(1 + len(v) if isinstance(v, list) else 2 for v in structured_json.values())
        render_styled_mindmap(mermaid_code, item_count=item_count)
    except Exception as e:
        print(f"❌ Run failed: {repr(e)}")
