#!/usr/bin/env python3
"""
memory-store — 外部持久化记忆层
读写 /root/chainup-pm-workspace/references/product-delivery/delivery-repo-template/memory-store.json

用法:
  python3 memory_store.py read                    # 读取全部有效条目
  python3 memory_store.py add <key> <value> <type> [scope] [ttl_days]
  python3 memory_store.py update <key> <new_value>
  python3 memory_store.py delete <key>
  python3 memory_store.py expire                   # 清理过期条目
  python3 memory_store.py migrate                  # 从 Hermes memory 迁移
"""
import json, sys, uuid, os
from datetime import datetime, timedelta, timezone

STORE_PATH = os.path.expanduser(
    "/root/chainup-pm-workspace/references/product-delivery/delivery-repo-template/memory-store.json"
)

VALID_TYPES = {"correction", "rule", "pointer", "fact"}
VALID_SCOPES = {"global"}

def load_store():
    if os.path.exists(STORE_PATH):
        with open(STORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"version": 1, "lastUpdated": datetime.now(timezone.utc).isoformat(), "entries": []}

def save_store(store):
    store["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

def now():
    return datetime.now(timezone.utc)

def make_entry(key, value, etype, scope="global", ttl_days=30):
    created = now()
    if etype == "correction" or ttl_days == 0:
        expires = None  # 永久保留
    else:
        expires = (created + timedelta(days=ttl_days)).isoformat()
    return {
        "id": str(uuid.uuid4())[:8],
        "type": etype,
        "scope": scope,
        "key": key,
        "value": value,
        "createdAt": created.isoformat(),
        "expiresAt": expires
    }

def read():
    store = load_store()
    now_iso = now().isoformat()
    valid = [e for e in store["entries"] if not e.get("expiresAt") or e["expiresAt"] > now_iso]
    # 只输出关键字段
    for e in valid:
        print(f"[{e['type']:10}] {e['scope']:12} {e['key']}")
        val = e['value'][:120]
        print(f"  → {val}")
        if e.get("expiresAt"):
            print(f"  过期: {e['expiresAt']}")
    print(f"\n有效条目: {len(valid)} / 总计: {len(store['entries'])}")
    return valid

def add(key, value, etype, scope="global", ttl_days=30):
    if etype not in VALID_TYPES:
        print(f"错误: type 必须是 {VALID_TYPES}")
        return
    store = load_store()
    # 去重：同 key + scope 的覆盖
    store["entries"] = [e for e in store["entries"] if not (e["key"] == key and e["scope"] == scope)]
    entry = make_entry(key, value, etype, scope, ttl_days)
    store["entries"].append(entry)
    save_store(store)
    print(f"已添加: {key} ({etype}, scope={scope})")

def update(key, new_value):
    store = load_store()
    found = False
    for e in store["entries"]:
        if e["key"] == key:
            e["value"] = new_value
            found = True
    if found:
        save_store(store)
        print(f"已更新: {key}")
    else:
        print(f"未找到: {key}")

def delete(key):
    store = load_store()
    before = len(store["entries"])
    store["entries"] = [e for e in store["entries"] if e["key"] != key]
    after = len(store["entries"])
    save_store(store)
    print(f"已删除: {key} (移除 {before - after} 条)")

def expire():
    store = load_store()
    now_iso = now().isoformat()
    before = len(store["entries"])
    store["entries"] = [e for e in store["entries"] if not e.get("expiresAt") or e["expiresAt"] > now_iso or e["type"] == "correction"]
    after = len(store["entries"])
    save_store(store)
    print(f"已清理: 移除 {before - after} 条过期条目, 剩余 {after}")

def migrate():
    """迁移当前 memory 中的关键条目到文件"""
    # 注意：本函数无法直接读 Hermes memory（不在同一个运行时）
    # 迁移需要在外部的会话中触发
    print("迁移流程：")
    print("1. 在 Hermes 会话中调用: memory(action='list_all') 获取全部条目")
    print("2. 复制到本脚本的 stdin: python3 memory_store.py migrate < entries.json")
    print("3. 或手工调用 add 逐条迁移")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "read":
        read()
    elif cmd == "add":
        if len(sys.argv) < 4:
            print("用法: add <key> <value> <type> [scope] [ttl_days]")
            sys.exit(1)
        key = sys.argv[2]
        value = sys.argv[3]
        etype = sys.argv[4] if len(sys.argv) > 4 else "fact"
        scope = sys.argv[5] if len(sys.argv) > 5 else "global"
        ttl = int(sys.argv[6]) if len(sys.argv) > 6 else 30
        add(key, value, etype, scope, ttl)
    elif cmd == "update":
        if len(sys.argv) < 4:
            print("用法: update <key> <new_value>")
            sys.exit(1)
        update(sys.argv[2], sys.argv[3])
    elif cmd == "delete":
        if len(sys.argv) < 3:
            print("用法: delete <key>")
            sys.exit(1)
        delete(sys.argv[2])
    elif cmd == "expire":
        expire()
    elif cmd == "migrate":
        migrate()
    else:
        print(f"未知命令: {cmd}")
