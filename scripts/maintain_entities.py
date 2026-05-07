#!/usr/bin/env python3
"""
molbio-kb 实体维护工具
- scan: 扫描章节，找出缺失和弱定义实体
- dedup: 检测重复/相似实体
- stats: 实体覆盖统计
"""
import json, re, pathlib, sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTITIES_DIR = ROOT / "kg/entities"
CHAPTERS_DIR = ROOT / "content/chapters"

def load_entities():
    entities = {}
    for fp in sorted(ENTITIES_DIR.glob("*.json")):
        try:
            d = json.loads(fp.read_text(encoding="utf-8"))
            entities[d.get("name", fp.stem)] = d
        except:
            pass
    return entities

def extract_terms(text):
    """Extract bold terms from markdown."""
    terms = set()
    for m in re.finditer(r'\*\*([^*\n]{2,80}?)\*\*', text):
        t = m.group(1).strip().rstrip('：:，,。.')
        if t and not t.startswith('<') and not re.match(r'^\d', t):
            terms.add(t)
    return terms

# Walk all existing entity names
JUNK = {"起始","延伸","终止","补充","机制","优势","位点","关键差异",
        "关键特征","实验证明","生物学意义","结构特征","功能位点","全酶",
        "核心酶","简并性","通用性","连续性","方向性","不重叠性","关键参数",
        "分析流程","技术原理","临床意义","独特之处","发明者","反应体系",
        "培养条件","调控方式","调控模式","调控过程","调控因子","调控元件",
        "增强子特征","转录因子结构","转录因子结构域","常见DNA结合域",
        "乳糖操纵子的双重调控","双重调控","原核生物特点","关键蛋白","关键酶",
        "常用酶","常用荧光染料","识别序列特点","DNA提取原理","DNA沉淀",
        "RNA提取注意事项","蛋白质去除","细胞裂解","A位","P位","E位",
        "前导链","后随链","半不连续复制","起始合成","闭合复合物形成",
        "开放复合物形成","大亚基结合","小亚基识别mRNA","氨酰-tRNA进入A位",
        "空载tRNA释放","肽键形成","核糖体移位","起始密码子识别","扫描机制",
        "校对机制","终止过程","终止信号","剪接过程","剪接模式","S期检查点",
        "情况1","情况2","全基因组NER vs 转录偶联NER","深度学习应用",
        "核小体与转录","密码子特点","5'帽识别","1. 起始","2. 延伸","3. 终止",
        "起始tRNA进入","延伸循环","衰减效率","衰减作用","密码子特点"}

def scan():
    entities = load_entities()
    entity_names = set(entities.keys())
    
    # Per-chapter coverage
    chapters = {}
    for md in sorted(CHAPTERS_DIR.glob("*.md")):
        raw = md.read_text(encoding="utf-8")
        terms = extract_terms(raw)
        clean_terms = {t for t in terms if t not in JUNK and len(t) >= 3}
        
        covered = clean_terms & entity_names
        missing = clean_terms - entity_names
        
        chapters[md.stem] = {
            "total": len(clean_terms),
            "covered": len(covered),
            "missing": sorted(missing)
        }
    
    # Weak definitions
    weak = []
    for name, d in entities.items():
        df = d.get("definition", "")
        if len(df) < 60:
            weak.append((name, len(df)))
    
    # Duplicates
    name_norm = {}
    dups = []
    for name in sorted(entity_names):
        n = name.replace(" ", "").replace(" ", "").lower()
        if n in name_norm:
            dups.append((name_norm[n], name))
        else:
            name_norm[n] = name
    
    # Category stats
    cats = Counter(d.get("category", "未分类") for d in entities.values())
    
    return chapters, weak, dups, cats

def report():
    chapters, weak, dups, cats = scan()
    
    print("=" * 60)
    print("📊 实体维护报告")
    print(f"   总实体: {sum(cats.values())}")
    print(f"   分类: {dict(cats.most_common())}")
    print()
    
    print("=" * 60)
    print("📖 章节覆盖率")
    for ch, info in chapters.items():
        pct = info["covered"]/info["total"]*100 if info["total"] else 0
        bar = "█" * int(pct/10) + "░" * (10-int(pct/10))
        print(f"   {ch}: [{bar}] {info['covered']}/{info['total']} ({pct:.0f}%)")
        if info["missing"]:
            print(f"      缺失: {', '.join(info['missing'][:8])}")
    
    print()
    print("=" * 60)
    print(f"⚠️  弱定义实体 ({len(weak)}):")
    for name, length in sorted(weak, key=lambda x: x[1]):
        print(f"   - {name} ({length}字)")
    
    print()
    print("=" * 60)
    print(f"🔀 疑似重复 ({len(dups)}):")
    for a, b in dups:
        print(f"   - \"{a}\" ↔ \"{b}\"")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        report()
    else:
        report()
