"""不登录 Dify 界面，直接用 API 查看知识库里的内容

配置方式（优先级从高到低）：
  1. 环境变量 DIFY_API_BASE_URL、DS_API_KEY、DS_ID
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
API_KEY = _load_key("DS_API_KEY", "DS_API_KEY")
DS_ID = _load_key("DS_ID", "DS_ID")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}


def list_documents():
    """列出知识库下所有文档"""
    url = f"{API_BASE}/datasets/{DS_ID}/documents"
    params = {"page": 1, "limit": 50}
    resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    docs = data.get("data", [])
    print(f"知识库共有 {data.get('total', 0)} 个文档:\n")
    for doc in docs:
        print(f"  [{doc['indexing_status']}] {doc['name']}")
        print(f"       ID: {doc['id']}  来源: {doc['data_source_type']}")
    return docs


def list_segments(document_id: str, doc_name: str):
    """列出某个文档的所有分段"""
    url = f"{API_BASE}/datasets/{DS_ID}/documents/{document_id}/segments"
    all_segments = []
    page = 1
    while True:
        resp = requests.get(url, headers=HEADERS, params={"page": page, "limit": 50}, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        segments = data.get("data", [])
        all_segments.extend(segments)
        if not data.get("has_more"):
            break
        page += 1
    print(f"\n{'─' * 60}")
    print(f"文档: {doc_name}  共 {len(all_segments)} 个分段")
    print(f"{'─' * 60}")
    for seg in all_segments:
        pos = seg.get("position", "?")
        word_count = seg.get("word_count", "?")
        enabled = "启用" if seg.get("enabled") else "禁用"
        content = seg.get("content", "").strip()
        print(f"\n 分段 #{pos}  [{word_count}字] 状态:{enabled}")
        print(f" {content[:200]}")
        if len(content) > 200:
            print(f" ...(共{len(content)}字符)")
    return all_segments


if __name__ == "__main__":
    docs = list_documents()
    for doc in docs:
        list_segments(doc["id"], doc["name"])
