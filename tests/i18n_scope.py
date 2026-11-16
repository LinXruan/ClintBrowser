#!/usr/bin/env python3
"""按批次统计需要翻译的字符串 key。

用法：
    python tests/i18n_scope.py B3              # 打印 B3 全部 key + 状态
    python tests/i18n_scope.py B3 --missing    # 只打印未翻译的
    python tests/i18n_scope.py --all --stat    # 各批覆盖率
    python tests/i18n_scope.py --all --unassigned   # 找出未归类的 key
"""
import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "app/src/main/res/values/strings.xml"

SCOPE = {
    "B1": ["pref", "app", "language", "look", "misc", "menu", "action", "popup",
           "address", "link", "search", "suggestion", "suggestions", "open", "clear",
           "choose", "create", "check", "hide", "view", "skip", "remember", "restart",
           "install", "default", "exit", "back", "forward", "share", "next", "get",
           "use", "close", "no", "reader", "toast", "content", "select", "preview",
           "date", "shortcut", "settings", "home", "downloading", "refresh"],
    "B2": ["accent", "custom", "surface", "theme", "color", "frameless"],
    "B3": ["download", "downloads", "mega", "redownload"],
    "B4": ["tab", "tabs", "homepage", "bookmarks", "history", "incognito",
           "nested", "strip", "new", "delete_inactive"],
    "B5": ["media", "image", "document", "camera", "mic", "location", "voice",
           "notification", "clipboard", "background", "screenshot", "battery"],
    "B6": ["website", "quiver", "filter", "cookies", "additional", "privacy", "do",
           "webrtc", "global", "block", "ssl", "http", "https", "site"],
    "B7": ["user", "js", "translation", "data", "engine", "desktop", "autofill",
           "speed", "beta", "update", "crash", "profiles", "measurement", "browser",
           "clint", "google", "javascript", "web", "delete_data"],
    "B8": ["backup", "restore", "about", "support", "setup", "debug", "rerun"],
}

BATCHES = list(SCOPE)


def batch_of(name: str):
    """最长前缀命中；同长取靠前批次，保证归类稳定。"""
    best = None
    for batch in BATCHES:
        for p in SCOPE[batch]:
            if name == p or name.startswith(p + "_"):
                score = (len(p), -BATCHES.index(batch))
                if best is None or score > best[0]:
                    best = (score, batch)
    return best[1] if best else None


def load_keys(path: Path):
    """返回 [(key, tag)]，保持文件顺序。"""
    if not path.exists():
        return []
    out = []
    for el in ET.parse(path).getroot():
        if el.tag not in ("string", "plurals"):
            continue
        if el.get("translatable", "true") == "false":
            continue
        out.append((el.get("name"), el.tag))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("batch", nargs="?", help="B1..B8")
    ap.add_argument("--locale", default="zh")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--stat", action="store_true")
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--unassigned", action="store_true")
    args = ap.parse_args()

    src = [(k, t) for k, t in load_keys(SRC) if t == "string"]
    plurals = {b: 0 for b in BATCHES}
    for key, tag in load_keys(SRC):
        if tag == "plurals":
            b = batch_of(key)
            if b:
                plurals[b] += 1
    done = {k for k, _ in load_keys(ROOT / f"app/src/main/res/values-{args.locale}/strings.xml")}

    groups = {b: [] for b in BATCHES}
    unassigned = []
    for key, _ in src:
        b = batch_of(key)
        (groups[b] if b else unassigned).append(key)

    if args.unassigned:
        print(f"未归类 {len(unassigned)} 条")
        for k in unassigned:
            print(k)
        return 0 if not unassigned else 1

    if args.batch and args.stat and not args.all:
        b = args.batch.upper()
        if b not in groups:
            ap.error(f"未知批次 {b}，可选 {', '.join(BATCHES)}")
        hit = sum(1 for k in groups[b] if k in done)
        more = f"  + {plurals[b]} 组复数" if plurals[b] else ""
        print(f"{b} {hit}/{len(groups[b])} {hit * 100 // max(len(groups[b]), 1)}%{more}")
        return 0 if hit == len(groups[b]) else 1

    if args.all or args.stat:
        total = 0
        for b in BATCHES:
            hit = sum(1 for k in groups[b] if k in done)
            total += len(groups[b])
            more = f"  + {plurals[b]} 组复数" if plurals[b] else ""
            print(f"{b} {hit}/{len(groups[b])} {hit * 100 // max(len(groups[b]), 1)}%{more}")
        hit = sum(1 for k in groups_sum(groups) if k in done)
        print(f"-- 合计 {hit}/{total} {hit * 100 // max(total, 1)}%")
        if unassigned:
            print(f"[WARN] 未归类 {len(unassigned)} 条，用 --unassigned 查看")
        pending = total - hit
        return 0 if pending == 0 and not unassigned else 1

    if not args.batch:
        ap.error("需要批次名，或 --all / --stat")

    batch = args.batch.upper()
    if batch not in groups:
        ap.error(f"未知批次 {batch}，可选 {', '.join(BATCHES)}")

    keys = groups[batch]
    shown = 0
    for k in keys:
        if args.missing and k in done:
            continue
        print(f"{'[x]' if k in done else '[ ]'} {k}")
        shown += 1
    hit = sum(1 for k in keys if k in done)
    print(f"-- {batch} {hit}/{len(keys)} {hit * 100 // max(len(keys), 1)}%  列出 {shown} 条")
    return 0 if hit == len(keys) else 1


def groups_sum(groups):
    out = []
    for b in BATCHES:
        out.extend(groups[b])
    return out


if __name__ == "__main__":
    sys.exit(main())