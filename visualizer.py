import os
import webbrowser
from datetime import datetime

def render_styled_mindmap(mermaid_code, output_file="mindmap_preview.html"):
    """
    高颜值思维导图渲染引擎
    仅转义 < > & 防止破坏 HTML，保留引号供 Mermaid 正确解析
    """
    safe_mermaid_code = (mermaid_code.replace("&", "&amp;")
                                        .replace("<", "&lt;")
                                        .replace(">", "&gt;"))

    time_now = datetime.now().strftime('%Y-%m-%d %H:%M')

    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Anyue's Intelligent Inbox Hub</title>
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: 'base',
                securityLevel: 'loose',
                themeVariables: {{
                    'primaryColor': '#6366f1',
                    'primaryTextColor': '#fff',
                    'primaryBorderColor': '#4f46e5',
                    'lineColor': '#818cf8',
                    'secondaryColor': '#e0e7ff',
                    'tertiaryColor': '#f5f3ff',
                    'fontSize': '15px',
                    'fontFamily': 'DM Sans, sans-serif'
                }}
            }});
        </script>
        <style>
            * {{ box-sizing: border-box; }}
            body {{ 
                background: linear-gradient(160deg, #0f172a 0%, #1e293b 50%, #334155 100%);
                min-height: 100vh;
                margin: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                font-family: 'DM Sans', -apple-system, sans-serif;
                color: #e2e8f0;
            }}
            h1 {{ 
                color: #f8fafc; 
                font-weight: 700; 
                margin: 32px 0 16px;
                font-size: 1.75rem;
                letter-spacing: -0.02em;
            }}
            .card {{
                background: rgba(255,255,255,0.97);
                padding: 40px 48px;
                border-radius: 20px;
                box-shadow: 0 25px 50px -12px rgba(0,0,0,0.4);
                margin: 0 auto 24px;
                max-width: 95%;
                color: #1e293b;
            }}
            .card .mermaid {{ background: transparent !important; }}
            .footer {{ 
                color: #94a3b8; 
                font-size: 0.875rem; 
                padding-bottom: 32px;
            }}
        </style>
    </head>
    <body>
        <h1>📬 Intelligence Hub</h1>
        <div class="card">
            <pre class="mermaid">
{safe_mermaid_code}
            </pre>
        </div>
        <div class="footer">Generated at {time_now}</div>
    </body>
    </html>
    """

    file_path = os.path.abspath(output_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print("高颜值渲染引擎已就绪！")
    file_url = "file:///" + file_path.replace("\\", "/")
    webbrowser.open(file_url)
