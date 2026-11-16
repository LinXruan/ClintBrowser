#!/usr/bin/env python3
"""校验某语种 strings.xml 与英文源文件的一致性。

用法：
    python tools/check_i18n.py --locale zh
    python tools/check_i18n.py --locale zh --allow-missing     # 分批阶段
    python tools/check_i18n.py --locale zh --report-missing
"""
import argparse
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "app/src/main/res"
SRC = RES / "values/strings.xml"

POS_RE = re.compile(r"%(\d+)\$[sd]")
RAW_RE = re.compile(r"%(?!%)(?:\d+\$)?[sd]")

# 允许保留英文的术语（禁译清单 + 术语表里的保留项）
ALLOW_EN = ("Quiver Guard", "MEGA", "Cookie", "Bergamot", "URL", "MIME",
            "GPL", "Clint", "ClintBrowser", "Material You", "DuckDuckGo",
            "Brave", "Google", "QA")

# 出现即提示可能漏译的英文词（大小写敏感，只报前 20 条）
SUSPECT = ("Tab", "Tabs", "Incognito", "Bookmark", "History", "Homepage",
           "Download", "Settings", "Cancel", "Delete", "Save", "Search",
           "Enable", "Disable", "Clear", "Close", "Retry", "Copy", "Paste")


def text_of(el):
    return "".join(el.itertext())


def load(path, label):
    if not path.exists():
        print(f"[FAIL] {label} 不存在：{path}")
        sys.exit(1)
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        print(f"[FAIL] {label} XML 无法解析：{e}")
        sys.exit(1)
    except Exception as e:  # noqa: BLE001
        print(f"[FAIL] {label} 解析失败：{e}")
        sys.exit(1)
    if root.tag != "resources":
        print(f"[FAIL] {label} 根节点是 <{root.tag}>，应为 <resources>")
        sys.exit(1)
    strings, plurals = {}, {}
    for el in root:
        if el.tag not in ("string", "plurals"):
            continue
        if el.get("translatable", "true") == "false":   # 禁译项（如 custom_theme_preview_*）不进 zh
            continue
        if el.tag == "string":
            strings[el.get("name")] = text_of(el)
        elif el.tag == "plurals":
            plurals[el.get("name")] = {
                item.get("quantity"): text_of(item) for item in el
            }
    return strings, plurals


def strip_allowed(text):
    for word in ALLOW_EN:
        text = text.replace(word, "")
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--locale", required=True)
    ap.add_argument("--allow-missing", action="store_true")
    ap.add_argument("--report-missing", action="store_true")
    args = ap.parse_args()

    src_s, src_p = load(SRC, "源文件")
    trg_path = RES / f"values-{args.locale}/strings.xml"
    trg_s, trg_p = load(trg_path, f"values-{args.locale}")

    fails, warns = [], []

    # 1 已在 load() 内校验
    # 2 key 集合
    missing_s = [k for k in src_s if k not in trg_s]
    missing_p = [k for k in src_p if k not in trg_p]
    extra = [k for k in trg_s if k not in src_s] + [k for k in trg_p if k not in src_p]
    for k in extra:
        fails.append(f"多余 key：{k}")
    if not args.allow_missing:
        for k in missing_s + missing_p:
            fails.append(f"缺少 key：{k}")

    # 3 复数 quantity
    for key, items in trg_p.items():
        bad = [q for q in items if q != "other"]
        if bad:
            fails.append(f"复数 quantity 非法 {key}：{bad}")
        if "other" not in items:
            fails.append(f"复数缺少 other：{key}")

    # 4 位置占位符
    for key in src_s:
        if key not in trg_s:
            continue
        a = sorted(POS_RE.findall(src_s[key]))
        b = sorted(POS_RE.findall(trg_s[key]))
        if a != b:
            fails.append(f"占位符不匹配 {key}：src={a} {args.locale}={b}")
    for key in src_p:
        if key not in trg_p or "other" not in trg_p[key]:
            continue
        a = sorted(POS_RE.findall(src_p[key].get("other", "")))
        b = sorted(POS_RE.findall(trg_p[key]["other"]))
        if a != b:
            fails.append(f"复数占位符不匹配 {key}：src={a} {args.locale}={b}")

    # 5 非位置占位符
    for key in src_s:
        if key not in trg_s:
            continue
        a = sorted(RAW_RE.findall(src_s[key]))
        b = sorted(RAW_RE.findall(trg_s[key]))
        if a != b:
            fails.append(f"非位置占位符数量不一致 {key}：src={a} {args.locale}={b}")
    for key in src_p:
        if key not in trg_p or "other" not in trg_p[key]:
            continue
        a = sorted(RAW_RE.findall(src_p[key].get("other", "")))
        b = sorted(RAW_RE.findall(trg_p[key]["other"]))
        if a != b:
            fails.append(f"复数非位置占位符不一致 {key}：src={a} {args.locale}={b}")

    # 6 值不以 @ / ? 开头
    for key, val in trg_s.items():
        if val[:1] in ("@", "?"):
            fails.append(f"值不能以 {val[:1]} 开头：{key}")
        if val.strip() == "":
            fails.append(f"空值：{key}")

    # 7 单引号转义
    for key, val in trg_s.items():
        for i, ch in enumerate(val):
            if ch == "'" and (i == 0 or val[i - 1] != "\\"):
                fails.append(f"单引号未转义：{key}")
                break

    # 8 长度
    for key, val in trg_s.items():
        if key in src_s and src_s[key]:
            ratio = len(val) / max(len(src_s[key]), 1)
            if ratio > 1.6:
                warns.append(f"长度 {ratio:.1f}x：{key}")

    # 9 术语抽查
    hits = 0
    for key, val in trg_s.items():
        rest = strip_allowed(val)
        for word in SUSPECT:
            if re.search(rf"\b{word}\b", rest):
                warns.append(f"疑似未译「{word}」：{key}")
                hits += 1
                break
        if hits >= 20:
            break

    done_s = len(src_s) - len(missing_s)
    done_p = len(src_p) - len(missing_p)
    status = "OK" if not fails else "FAIL"
    print(f"[{status}]   strings {done_s}/{len(src_s)}  plurals {done_p}/{len(src_p)}")
    if args.report_missing and (missing_s or missing_p):
        sys.path.insert(0, str(ROOT / "tools"))
        try:
            from i18n_scope import batch_of
        except ImportError:
            batch_of = lambda _k: None
        groups = {}
        for key in missing_s + missing_p:
            groups.setdefault(batch_of(key) or "UNASSIGNED", []).append(key)
        print("-- 未译 key --")
        for batch in sorted(groups):
            print(f"[{batch}] {len(groups[batch])} 条")
            for key in groups[batch]:
                print(f"    {key}")
    for w in warns:
        print(f"[WARN] {w}")
    for f in fails:
        print(f"[FAIL] {f}")
    if fails:
        print(f"-- {len(fails)} 项失败")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())