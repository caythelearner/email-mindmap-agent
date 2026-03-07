# 推送到 GitHub 的步骤

本地仓库已准备好，按以下步骤上传到 GitHub：

## 1. 在 GitHub 创建新仓库

1. 打开 https://github.com/new
2. Repository name 填：`email-mindmap-agent`（或你喜欢的名字）
3. 选择 **Public**
4. **不要**勾选 "Add a README"（本地已有）
5. 点击 Create repository

## 2. 关联并推送

创建完成后，GitHub 会显示命令。在项目目录下执行：

```bash
cd d:\科研\email-mindmap-agent

git remote add origin https://github.com/你的用户名/email-mindmap-agent.git
git branch -M main
git push -u origin main
```

把 `你的用户名` 换成你的 GitHub 用户名。

## 3. 更新 README 中的链接

推送成功后，编辑 README.md，把 `YOUR_USERNAME` 替换成你的 GitHub 用户名。
