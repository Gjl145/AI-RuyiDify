"""上传文档到 Dify 知识库 — 自动删除同名文档后上传

配置来源: 项目根目录 key.txt
"""

import json
import os
import time
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
KEY_FILE = ROOT / "key.txt"


def _load_key(name: str, default: str = "") -> str:
    val = os.getenv(name)
    if val:
        return val
    if KEY_FILE.exists():
        for line in KEY_FILE.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                if k.strip() == name:
                    return v.strip()
    if default:
        return default
    raise RuntimeError(f"未找到 {name}")


API_BASE = _load_key("DIFY_API_BASE_URL", "http://localhost:12010/v1")
API_KEY = _load_key("DS_API_KEY")
DS_ID = _load_key("DS_ID")
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 要上传的文件
FILE_PATH = ROOT / "docs" / "ruyi-project" / "Dify学习资料大全.docx"
FILE_NAME = "Dify学习资料大全.docx"


def find_documents_by_name(name: str) -> list[dict]:
    """查找知识库中同名文档"""
    url = f"{API_BASE}/datasets/{DS_ID}/documents"
    resp = requests.get(url, headers=HEADERS, params={"page": 1, "limit": 100, "keyword": name}, timeout=30)
    resp.raise_for_status()
    return [d for d in resp.json().get("data", []) if d["name"] == name]


def delete_document(doc_id: str):
    """删除文档"""
    url = f"{API_BASE}/datasets/{DS_ID}/documents/{doc_id}"
    resp = requests.delete(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    print(f"  已删除: {doc_id}")


def upload_document(file_path: Path) -> str:
    """上传文档，返回 batch 号"""
    url = f"{API_BASE}/datasets/{DS_ID}/document/create-by-file"
    config = {
        "indexing_technique": "high_quality",
        "process_rule": {"mode": "automatic"},
    }
    with file_path.open("rb") as f:
        resp = requests.post(
            url,
            headers=HEADERS,
            files={"file": (file_path.name, f)},
            data={"data": json.dumps(config)},
            timeout=120,
        )
    resp.raise_for_status()
    result = resp.json()
    batch = result.get("batch", "")
    doc_id = result.get("document", {}).get("id", "")
    print(f"  上传成功: {doc_id}  batch={batch}")
    return batch


def wait_indexing(batch: str, timeout: int = 120):
    """轮询等待索引完成"""
    url = f"{API_BASE}/datasets/{DS_ID}/documents/{batch}/indexing-status"
    start = time.time()
    data_key = "data"  # Dify returns {"data": [...]}
    while time.time() - start < timeout:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        info = (payload.get(data_key) or [{}])[0]
        status = info.get("indexing_status", "unknown")
        completed = info.get("completed_segments", 0)
        total = info.get("total_segments", 0)
        print(f"  状态: {status} ({completed}/{total})")
        if status == "completed":
            return
        if status == "error":
            raise RuntimeError(f"索引失败: {info.get('error', 'unknown')}")
        time.sleep(5)
    raise TimeoutError("索引超时")


def main():
    if not FILE_PATH.exists():
        raise FileNotFoundError(f"文件不存在: {FILE_PATH}")

    print(f"知识库: {DS_ID}")
    print(f"文件: {FILE_PATH}\n")

    # 1. 删除同名文档
    existing = find_documents_by_name(FILE_NAME)
    if existing:
        print(f"发现 {len(existing)} 个同名文档，正在删除...")
        for doc in existing:
            delete_document(doc["id"])
    else:
        print("无同名文档")

    # 2. 上传
    print(f"\n上传 {FILE_NAME} ...")
    batch = upload_document(FILE_PATH)

    # 3. 等待索引
    print("\n等待索引完成...")
    wait_indexing(batch)

    print("\n完成 — 文档已可检索")


if __name__ == "__main__":
    main()
