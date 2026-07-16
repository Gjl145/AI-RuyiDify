# 项目环境速查

> 最后更新: 2026-07-16
> 给任何新 AI 会话的第一份阅读材料

## 路径

| 项目 | 路径 |
|------|------|
| 项目根目录 | D:\ai\RuyiDify |
| 文档库 | D:\ai\RuyiDify\docs\ruyi-project\ |
| 密钥配置 | D:\ai\RuyiDify\key.txt (gitignore) |

## Docker

| 项目 | 值 |
|------|-----|
| 启动命令 | `cd D:\ai\RuyiDify\docker && docker compose --profile postgresql --profile weaviate up -d` |
| API 地址 | `http://localhost/v1` (Nginx:80 → api:5001) |
| Web 界面 | `http://localhost` |
| 管理员 | admin@ruyidify.local / RuyiDify2026! |
| 密码编码 | 前端 Base64 编码后发送（CLI: `echo -n "pw" \| base64`） |

## 知识库

| 项目 | 值 |
|------|-----|
| 名称 | RuyiDify课程资料 |
| ID | f759c84c-70a4-462e-9781-63c16a9fbbcc |
| 模式 | high_quality + BAAI/bge-m3 (SiliconFlow) |
| API Key | 见 key.txt |

## 模型

| 模型 | 供应商 | 用途 |
|------|--------|------|
| deepseek-v4-pro | DeepSeek | 对话生成 |
| BAAI/bge-m3 | SiliconFlow | 文本嵌入 |

## Windows 注意事项

- `make` 未安装，lint 用 ruff: `D:\ai\RuyiDify\api\.venv\Scripts\python.exe -m ruff check <file>`
- Python: D:/python/python.exe (3.12)
- WSL 已安装但未配置开发环境
- Docker Desktop 需手动启动

## 已知问题

- ApiToken 模型已修复（补 dataset_id 列）
- sites 表已修复（补 input_placeholder 列）
- 检索偶有无响应 → `docker restart docker-worker-1`
