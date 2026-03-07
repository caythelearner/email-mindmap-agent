import subprocess
import json
import sys
import re
import os
from datetime import datetime
from email.utils import parsedate_to_datetime
from anthropic import Anthropic
from visualizer import render_styled_mindmap

# 强制 UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def load_config():
    if not os.path.exists("config.json"):
        print("❌ 未找到 config.json，请复制 config.example.json 为 config.json 并填入你的 API Key")
        print("   cp config.example.json config.json")
        sys.exit(1)
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()
client = Anthropic(api_key=CONFIG["ANTHROPIC_API_KEY"])

def parse_date(date_str):
    """解析邮件日期+小时，如 '03-07 14:30'"""
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
    print(f"🛰️ 正在抓取最近的 {CONFIG['MAX_EMAILS']} 封邮件...")
    params = json.dumps({"userId": CONFIG["GMAIL_USER_ID"], "maxResults": CONFIG["MAX_EMAILS"]})
    res = subprocess.run(["gws", "gmail", "users", "messages", "list", "--params", params],
                         capture_output=True, text=True, encoding='utf-8', shell=True)

    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"Gmail API 返回无效 JSON: {res.stderr or res.stdout[:200]}")

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
    """只移除真正会破坏 Mermaid 解析的字符"""
    if not text:
        return ""
    s = str(text).replace('"', "'").replace("\n", " ").replace("\\", " ")
    for ch in '()[]{}#/<>|`':
        s = s.replace(ch, " ")
    return " ".join(s.split()).strip()

def get_ai_structured_data(emails):
    print("🧠 Claude Haiku 正在分析并分类...")
    prompt = f"""你是 Anyue 的个人助手。背景：{CONFIG['MY_CONTEXT']}。
请将以下邮件按主题分类，返回纯 JSON。

要求：
1. 格式：{{"分类名": ["邮件简述1", "邮件简述2"]}}
2. 每个邮件简述：保留邮件中的日期时间信息，格式为"简述内容 MM-DD HH:MM"
3. 分类名用简短的中文，如"银行通知"、"云服务"等
4. 不要用特殊符号如 # $ () [] {{}} / 等
5. 只返回纯 JSON，不要 markdown 代码块，不要任何解释

邮件数据：{json.dumps(emails, ensure_ascii=False)}"""

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
        raise ValueError(f"AI 返回的 JSON 解析失败: {e}\n原始内容: {content[:300]}...")

def build_mermaid_code(structured_data):
    """构建 Mermaid 思维导图代码"""
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
        render_styled_mindmap(mermaid_code)
    except Exception as e:
        print(f"❌ 运行失败: {repr(e)}")
