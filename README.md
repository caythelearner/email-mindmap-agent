# 📬 Email Mindmap Agent

用 Claude AI 分析 Gmail 邮件，自动生成思维导图可视化。

## 功能

- 抓取最近 N 封 Gmail 邮件
- 使用 Claude Haiku 按主题分类
- 生成带日期时间的 Mermaid 思维导图
- 自动在浏览器中打开高颜值 HTML 预览

## 环境要求

- Python 3.8+
- [gws](https://github.com/nicksanders/gws)（Gmail 命令行工具，需完成 OAuth 授权）
- Anthropic API Key

## 安装

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/email-mindmap-agent.git
cd email-mindmap-agent

# 安装依赖
pip install -r requirements.txt

# 配置
cp config.example.json config.json
# 编辑 config.json，填入你的 ANTHROPIC_API_KEY 和 MY_CONTEXT
```

## 配置说明

| 字段 | 说明 |
|------|------|
| ANTHROPIC_API_KEY | 在 [Anthropic Console](https://console.anthropic.com/) 申请 |
| GMAIL_USER_ID | 通常填 `me` |
| MAX_EMAILS | 抓取邮件数量，默认 10 |
| MY_CONTEXT | 你的背景描述，帮助 AI 更好理解邮件 |

## 使用

```bash
python main_agent.py
```

运行后会生成 `mindmap_preview.html` 并在浏览器中打开。

## Gmail 授权

需先安装并配置 gws：

```bash
# 安装 gws（见 https://github.com/nicksanders/gws）
gws auth login
# 勾选 Gmail 相关权限
```

## License

MIT
