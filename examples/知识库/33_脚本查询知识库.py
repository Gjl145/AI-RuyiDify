"""用 Python 脚本查询 Dify 知识库 — 检索 + LLM 回答

配置方式（优先级从高到低）：
  1. 环境变量 DIFY_API_BASE_URL、DS_API_KEY、APP_API_KEY、DS_ID
  2. 项目根目录 key.txt（格式：KEY=VALUE，每行一个）
"""

import os
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEY_FILE = ROOT / "key.txt"


def _load_key(key_name: str, env_name: str, default: str = "") -> str:
    val = os.getenv(env_name)
    if val:
        return val
    if KEY_FILE.exists():
        for line in KEY_FILE.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == key_name:
                    return v.strip()
    if default:
        return default
    raise RuntimeError(f"未找到 {key_name}，请设置环境变量 {env_name} 或在 key.txt 中配置")


API_BASE = _load_key("DIFY_API_BASE_URL", "DIFY_API_BASE_URL", "http://localhost:12010/v1")
DS_API_KEY = _load_key("DS_API_KEY", "DS_API_KEY")
APP_API_KEY = _load_key("APP_API_KEY", "APP_API_KEY")
DS_ID = _load_key("DS_ID", "DS_ID")


def query_knowledge_base(question: str) -> dict:
    """第一步：检索知识库，返回相关分段"""
    url = f"{API_BASE}/datasets/{DS_ID}/retrieve"
    headers = {"Authorization": f"Bearer {DS_API_KEY}", "Content-Type": "application/json"}
    data = {
        "query": question,
        "retrieval_model": {
            "search_method": "semantic_search",
            "top_k": 5,
            "score_threshold_enabled": False,
            "reranking_enable": False,
        },
    }
    resp = requests.post(url, headers=headers, json=data, timeout=60)
    resp.raise_for_status()
    return resp.json()


def ask_ai_with_context(question: str) -> dict:
    """第二步：把检索结果交给 LLM 生成回答"""
    url = f"{API_BASE}/chat-messages"
    headers = {"Authorization": f"Bearer {APP_API_KEY}", "Content-Type": "application/json"}
    data = {
        "query": question,
        "inputs": {},
        "response_mode": "blocking",
        "user": "script-user",
        "conversation_id": "",
    }
    resp = requests.post(url, headers=headers, json=data, timeout=180)
    resp.raise_for_status()
    return resp.json()


def main():
    questions = [
        "Dify支持多少种文档类型，主流的有哪些",
        "Dify知识库有多少个接口",
    ]
    for q in questions:
        print(f"\n{'=' * 60}")
        print(f"Q: {q}")
        result = query_knowledge_base(q)
        records = result.get("records", [])
        print(f"\n检索命中 {len(records)} 个分段:")
        for i, r in enumerate(records[:3], 1):
            content = r["segment"]["content"][:100].replace("\n", " ")
            print(f"  [{i}] score={r['score']:.3f} | {content}...")
        ai_result = ask_ai_with_context(q)
        answer = ai_result.get("answer", "")
        print(f"\nAI 回答:\n{answer}")


if __name__ == "__main__":
    main()
