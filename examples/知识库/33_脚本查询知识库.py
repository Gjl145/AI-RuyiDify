"""用 Python 脚本查询 Dify 知识库 — 检索 + LLM 回答"""
import requests

# 配置
API_BASE = "http://localhost/v1"
DS_API_KEY = "ds-OuFGPk1qgB0RtmQM2WrdDCb4"     # 知识库 API Key
APP_API_KEY = "app-kzqVORHstTM1u9TwsZN7t4pG"     # 聊天应用 API Key
DS_ID = "f759c84c-70a4-462e-9781-63c16a9fbbcc"

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
        print(f"\n{'='*60}")
        print(f"Q: {q}")

        # 方式一：纯检索（只看命中了哪些分段）
        result = query_knowledge_base(q)
        records = result.get("records", [])
        print(f"\n检索命中 {len(records)} 个分段:")
        for i, r in enumerate(records[:3], 1):
            content = r["segment"]["content"][:100].replace("\n", " ")
            print(f"  [{i}] score={r['score']:.3f} | {content}...")

        # 方式二：检索 + LLM 回答
        ai_result = ask_ai_with_context(q)
        answer = ai_result.get("answer", "")
        print(f"\nAI 回答:\n{answer}")


if __name__ == "__main__":
    main()
