#!/usr/bin/env python3
"""
molbio-kb 健康检查脚本（lint）

检查项：
  1. 孤立实体 — 0 入链（无其他实体引用它）
  2. 弱定义 — 定义 < 60 字或缺失
  3. 缺 importance 字段
  4. 全 related 类型关系（缺乏 is-a/part-of/regulates 等类型化关系）
  5. 章节实体覆盖度 — 实体非常少的章节
  6. 实体名含特殊字符（路径安全）

用法:
  python3 scripts/lint_wiki.py              # 全部检查
  python3 scripts/lint_wiki.py --orphans    # 只看孤立实体
  python3 scripts/lint_wiki.py --weak       # 只看弱定义
  python3 scripts/lint_wiki.py --summary    # 仅摘要
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict

REPO = Path(__file__).resolve().parent.parent
ENTITIES_DIR = REPO / "kg/entities"
LINKS_FILE = REPO / "kg/relations/concept-links.json"
CHAPTERS_DIR = REPO / "content/chapters"


def load_entities():
    """加载所有实体，返回 {name: data}"""
    entities = {}
    for f in sorted(ENTITIES_DIR.glob("*.json")):
        d = json.loads(f.read_text())
        entities[d["name"]] = d
    return entities


def load_links():
    if not LINKS_FILE.exists():
        return []
    return json.loads(LINKS_FILE.read_text()).get("links", [])


def check_orphans(entities, links):
    """检查孤立实体：无入链"""
    inbound = Counter()
    for link in links:
        target = link.get("target", "")
        if target in entities:
            inbound[target] += 1

    # 也从 relatedEntities 收集入链
    for name, data in entities.items():
        for rel in data.get("relatedEntities", []):
            if rel in entities:
                inbound[rel] += 1

    orphans = sorted(
        [name for name in entities if inbound.get(name, 0) == 0]
    )
    return orphans


def check_weak_definitions(entities):
    """检查弱定义：< 60 字或缺失"""
    weak = []
    for name, data in entities.items():
        d = data.get("definition", "")
        if not d or len(d) < 60:
            weak.append((name, len(d) if d else 0))
    return sorted(weak, key=lambda x: x[1])


def check_missing_importance(entities):
    """检查缺失 importance 字段"""
    missing = []
    for name, data in entities.items():
        imp = data.get("importance")
        if imp is None or imp == "":
            missing.append(name)
    return sorted(missing)


def check_relation_types(links):
    """检查关系类型分布"""
    types = Counter(l.get("type", "related") for l in links)
    total = len(links)
    if total == 0:
        return types, "⚠️ 无关系数据"

    typed_count = sum(n for t, n in types.items() if t != "related")
    if typed_count == 0 and total > 0:
        return types, "⚠️ 所有关系均为 'related' 类型，缺乏 is-a/part-of/regulates 等类型化关系"
    return types, None


def check_chapter_coverage(entities):
    """检查章节实体覆盖度"""
    ch_count = Counter()
    for data in entities.values():
        ch = data.get("chapter", "未归类")
        ch_count[ch] += 1

    low = [(ch, n) for ch, n in ch_count.items() if n < 5]
    return ch_count, low


def check_path_safety(entities):
    """检查实体名中的路径不友好字符"""
    unsafe = []
    for name in entities:
        if "/" in name:
            unsafe.append((name, "含 /"))
    return unsafe


def format_summary(entities, links, orphans, weak, missing_imp, rel_types,
                   ch_count, low_chapters, unsafe_names):
    """生成摘要报告"""
    lines = []
    lines.append("=" * 55)
    lines.append("  molbio-kb 健康检查报告")
    lines.append("=" * 55)
    lines.append(f"  实体总数:     {len(entities)}")
    lines.append(f"  关系总数:     {len(links)}")
    lines.append(f"  章节数:       {len([f for f in CHAPTERS_DIR.glob('*.md') if f.name[0].isdigit()])}")
    lines.append("")
    lines.append("  --- 问题统计 ---")
    lines.append(f"  🔴 孤立实体:   {len(orphans)} (0 入链)")
    lines.append(f"  🟡 弱定义:     {len(weak)} (< 60 字)")
    lines.append(f"  🟡 缺 importance: {len(missing_imp)}")
    lines.append(f"  🟠 路径不安全: {len(unsafe_names)}")
    lines.append(f"  🟠 低覆盖章节: {len(low_chapters)} (< 5 实体)")
    lines.append("")

    rel_warning = check_relation_types(links)[1]
    if rel_warning:
        lines.append(f"  {rel_warning}")
    lines.append("")

    lines.append("  --- 关系类型 ---")
    for t, n in rel_types.most_common():
        lines.append(f"  {t}: {n}")
    lines.append("")

    lines.append("  --- 章节覆盖 ---")
    for ch, n in sorted(ch_count.items()):
        flag = " ⚠️" if (ch, n) in low_chapters else ""
        lines.append(f"  {ch}: {n}{flag}")

    return "\n".join(lines)


def main():
    args = set(sys.argv[1:])
    summary_only = "--summary" in args

    entities = load_entities()
    links = load_links()

    orphans = check_orphans(entities, links)
    weak = check_weak_definitions(entities)
    missing_imp = check_missing_importance(entities)
    rel_types, rel_warning = check_relation_types(links)
    ch_count, low_chapters = check_chapter_coverage(entities)
    unsafe_names = check_path_safety(entities)

    # 摘要
    print(format_summary(entities, links, orphans, weak, missing_imp,
                         rel_types, ch_count, low_chapters, unsafe_names))

    if summary_only:
        return

    # 详细输出
    if "--orphans" in args or not any(a.startswith("--") for a in args):
        if orphans:
            print(f"\n🔴 孤立实体 ({len(orphans)}):")
            for name in orphans:
                cat = entities[name].get("category", "")
                print(f"  [{cat}] {name}")
        else:
            print("\n✅ 无孤立实体")

    if "--weak" in args or not any(a.startswith("--") for a in args):
        if weak:
            print(f"\n🟡 弱定义 ({len(weak)}):")
            for name, n in weak:
                print(f"  {name} ({n} 字)")
        else:
            print("\n✅ 无弱定义")

    if not any(a.startswith("--") for a in args):
        if missing_imp:
            print(f"\n🟡 缺 importance 字段 ({len(missing_imp)}):")
            for name in missing_imp[:20]:
                print(f"  {name}")
            if len(missing_imp) > 20:
                print(f"  ... 及其他 {len(missing_imp)-20} 个")
        else:
            print("\n✅ importance 字段完整")

        if unsafe_names:
            print(f"\n🟠 路径不安全 ({len(unsafe_names)}):")
            for name, reason in unsafe_names:
                print(f"  {name}: {reason}")


if __name__ == "__main__":
    main()
