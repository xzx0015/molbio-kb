#!/usr/bin/env python3
"""
批量生成实体详情页
"""

import json
from pathlib import Path

# 实体数据
ENTITIES = {
    "DNA": {
        "type": "基因/分子",
        "type_color": "#e3f2fd",
        "type_text": "#1976d2",
        "desc": "脱氧核糖核酸，遗传信息的载体",
        "definition": "DNA（Deoxyribonucleic Acid，脱氧核糖核酸）是生物体内存储遗传信息的生物大分子。它由两条反向平行的多核苷酸链组成双螺旋结构，通过碱基互补配对（A-T，G-C）连接在一起。",
        "related": ["RNA", "蛋白质", "DNA复制", "转录", "基因", "核苷酸", "染色体", "DNA聚合酶"],
        "chapters": [
            ("01", "绪论", "中心法则与DNA"),
            ("02", "分子基础", "DNA双螺旋结构"),
            ("03", "信息传递", "DNA复制机制"),
            ("05", "基因组维持", "DNA损伤与修复"),
        ],
        "features": [
            "双螺旋结构：由Watson和Crick于1953年发现",
            "碱基配对：A与T配对（2个氢键），G与C配对（3个氢键）",
            "半保留复制：复制时两条链分开，各作为模板合成新链",
            "方向性：5'→3'方向合成",
            "稳定性：脱氧核糖比核糖更稳定，适合长期存储遗传信息"
        ]
    },
    "RNA": {
        "type": "基因/分子",
        "type_color": "#e3f2fd",
        "type_text": "#1976d2",
        "desc": "核糖核酸，参与蛋白质合成",
        "definition": "RNA（Ribonucleic Acid，核糖核酸）是由核糖核苷酸组成的单链核酸分子。与DNA相比，RNA的糖是核糖而非脱氧核糖，碱基为A、U、G、C（用尿嘧啶U代替胸腺嘧啶T）。",
        "related": ["DNA", "蛋白质", "转录", "翻译", "mRNA", "tRNA", "rRNA", "核糖体"],
        "chapters": [
            ("01", "绪论", "中心法则与RNA"),
            ("02", "分子基础", "RNA结构与功能"),
            ("03", "信息传递", "转录与RNA加工"),
        ],
        "features": [
            "单链结构：通常以单链形式存在，可形成局部双链",
            "核糖：2'位有羟基，使RNA更易被水解",
            "尿嘧啶：用U代替T，与A配对",
            "多功能：mRNA传递信息、tRNA转运氨基酸、rRNA组成核糖体",
            "催化功能：某些RNA具有酶活性（核酶）"
        ]
    },
    "蛋白质": {
        "type": "蛋白质",
        "type_color": "#f3e5f5",
        "type_text": "#7b1fa2",
        "desc": "生命活动的主要执行者",
        "definition": "蛋白质是由氨基酸通过肽键连接形成的大分子。它们是生命活动的主要执行者，具有催化（酶）、结构支撑、运输、免疫、信号传导等多种功能。",
        "related": ["DNA", "RNA", "翻译", "氨基酸", "酶", "核糖体", "tRNA", "遗传密码"],
        "chapters": [
            ("01", "绪论", "中心法则与蛋白质"),
            ("02", "分子基础", "蛋白质结构"),
            ("03", "信息传递", "翻译过程"),
        ],
        "features": [
            "氨基酸组成：由20种标准氨基酸组成",
            "四级结构：一级（序列）、二级（局部折叠）、三级（三维结构）、四级（多亚基）",
            "多样性：结构和功能的多样性",
            "酶：绝大多数酶是蛋白质",
            "动态性：可折叠、修饰、降解"
        ]
    },
    "PCR": {
        "type": "技术方法",
        "type_color": "#fff3e0",
        "type_text": "#f57c00",
        "desc": "聚合酶链式反应，体外扩增DNA",
        "definition": "PCR（Polymerase Chain Reaction，聚合酶链式反应）是一种在体外快速扩增特定DNA片段的技术。通过反复循环的变性-退火-延伸步骤，可在数小时内将目标DNA扩增数百万倍。",
        "related": ["DNA", "DNA聚合酶", "引物", "Taq酶", "DNA复制", "测序", "基因克隆"],
        "chapters": [
            ("06", "分子生物学技术", "PCR技术原理与应用"),
        ],
        "features": [
            "三步循环：变性（95°C）→ 退火（50-65°C）→ 延伸（72°C）",
            "指数扩增：n个循环后扩增2ⁿ倍",
            "关键组分：模板DNA、引物、DNA聚合酶、dNTPs、缓冲液",
            "Taq酶：耐热DNA聚合酶，来自嗜热菌Thermus aquaticus",
            "应用广泛：基因检测、克隆、测序、法医鉴定、医学诊断"
        ]
    },
    "CRISPR-Cas9": {
        "type": "技术方法",
        "type_color": "#fff3e0",
        "type_text": "#f57c00",
        "desc": "基因编辑技术",
        "definition": "CRISPR-Cas9是一种革命性的基因编辑技术，源于细菌的适应性免疫系统。通过sgRNA引导Cas9蛋白识别并切割特定DNA序列，可实现基因的敲除、插入或替换。",
        "related": ["DNA", "基因", "Cas9蛋白", "sgRNA", "DNA修复", "基因治疗", "逆转录"],
        "chapters": [
            ("06", "分子生物学技术", "CRISPR-Cas9基因编辑"),
        ],
        "features": [
            "组成：Cas9蛋白（切割）+ sgRNA（引导）",
            "机制：sgRNA识别靶序列（需PAM: NGG），Cas9切割DNA双链",
            "修复途径：NHEJ（敲除）或 HDR（精确编辑）",
            "发现者：Jennifer Doudna和Emmanuelle Charpentier（2020诺贝尔奖）",
            "应用：基因治疗、作物改良、功能研究"
        ]
    },
    "DNA复制": {
        "type": "分子过程",
        "type_color": "#e8f5e9",
        "type_text": "#388e3c",
        "desc": "DNA双链的精确拷贝",
        "definition": "DNA复制是以亲代DNA为模板合成子代DNA的过程。遵循半保留复制原则，即每个子代DNA分子包含一条亲代链和一条新合成链。",
        "related": ["DNA", "DNA聚合酶", "引物酶", "解旋酶", "半保留复制", "冈崎片段", "中心法则"],
        "chapters": [
            ("01", "绪论", "中心法则"),
            ("03", "信息传递", "DNA复制机制"),
        ],
        "features": [
            "半保留复制：Meselson-Stahl实验证实",
            "半不连续：前导链连续合成，后随链不连续（冈崎片段）",
            "多酶参与：解旋酶、SSB、引物酶、DNA聚合酶、连接酶",
            "高保真：错误率约10⁻⁹，依赖校对功能",
            "起始点：从复制起点（Origin）开始"
        ]
    },
    "转录": {
        "type": "分子过程",
        "type_color": "#e8f5e9",
        "type_text": "#388e3c",
        "desc": "DNA到RNA的信息传递",
        "definition": "转录是以DNA为模板合成RNA的过程。RNA聚合酶识别启动子序列，沿DNA模板链合成互补的RNA链，将遗传信息从DNA传递到RNA。",
        "related": ["DNA", "RNA", "RNA聚合酶", "启动子", "翻译", "中心法则", "基因调控"],
        "chapters": [
            ("01", "绪论", "中心法则"),
            ("03", "信息传递", "转录过程"),
            ("04", "表达调控", "转录调控"),
        ],
        "features": [
            "模板：DNA的一条链（模板链）",
            "酶：RNA聚合酶（原核1种，真核3种）",
            "三阶段：起始（启动子识别）→ 延伸 → 终止",
            "不需要引物：与DNA复制不同",
            "加工：真核mRNA需加帽、加尾、剪接"
        ]
    },
    "翻译": {
        "type": "分子过程",
        "type_color": "#e8f5e9",
        "type_text": "#388e3c",
        "desc": "RNA到蛋白质的信息传递",
        "definition": "翻译是以mRNA为模板合成蛋白质的过程。核糖体读取mRNA上的遗传密码，tRNA携带相应氨基酸，通过肽键连接形成多肽链。",
        "related": ["RNA", "蛋白质", "mRNA", "tRNA", "rRNA", "核糖体", "遗传密码", "中心法则"],
        "chapters": [
            ("01", "绪论", "中心法则"),
            ("03", "信息传递", "翻译过程"),
        ],
        "features": [
            "场所：核糖体（rRNA + 蛋白质）",
            "密码子：三联体密码子编码氨基酸",
            "tRNA：携带氨基酸，反密码子识别密码子",
            "三阶段：起始 → 延伸 → 终止",
            "方向：mRNA 5'→3'，多肽 N端→C端"
        ]
    },
}

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | 实体详情</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f7fa;
        }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        .back {{ color: #667eea; text-decoration: none; margin-bottom: 20px; display: inline-block; padding: 10px 0; }}
        
        .entity-header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .entity-type {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85rem;
            margin-bottom: 15px;
            background: {type_color};
            color: {type_text};
        }}
        .entity-name {{
            font-size: 2rem;
            color: #667eea;
            margin-bottom: 15px;
        }}
        .entity-desc {{
            color: #666;
            font-size: 1.1rem;
        }}
        
        .section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .section h2 {{
            color: #764ba2;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }}
        
        .related-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .related-tag {{
            background: #f0f0f0;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            color: #333;
            transition: all 0.2s;
        }}
        .related-tag:hover {{
            background: #667eea;
            color: white;
        }}
        
        .chapter-link {{
            display: block;
            padding: 12px 15px;
            background: #f8f9fa;
            border-radius: 8px;
            margin-bottom: 10px;
            text-decoration: none;
            color: #333;
            transition: all 0.2s;
        }}
        .chapter-link:hover {{
            background: #667eea;
            color: white;
        }}
        
        footer {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back">← 返回实体索引</a>
        
        <div class="entity-header">
            <span class="entity-type">{type}</span>
            <h1 class="entity-name">{name}</h1>
            <p class="entity-desc">{desc}</p>
        </div>
        
        <div class="section">
            <h2>📖 定义</h2>
            <p>{definition}</p>
        </div>
        
        <div class="section">
            <h2>🔗 关联实体</h2>
            <div class="related-list">
                {related_links}
            </div>
        </div>
        
        <div class="section">
            <h2>📚 出现章节</h2>
            {chapter_links}
        </div>
        
        <div class="section">
            <h2>🧬 关键特性</h2>
            <ul>
                {features_list}
            </ul>
        </div>
        
        <footer>
            <p>分子生物学知识库</p>
        </footer>
    </div>
</body>
</html>
'''

def generate_entity_page(name, data):
    """生成单个实体详情页"""
    # 处理关联实体链接
    related_links = "\n                ".join([
        f'<a href="{r}.html" class="related-tag">{r}</a>'
        for r in data.get("related", [])
    ])
    
    # 处理章节链接
    chapter_links = "\n            ".join([
        f'<a href="../../chapters/{c[0]}_{c[1]}.html" class="chapter-link">📖 第{c[0]}章：{c[1]} - {c[2]}</a>'
        for c in data.get("chapters", [])
    ])
    
    # 处理特性列表
    features_list = "\n                ".join([
        f'<li><strong>{f.split("：")[0]}</strong>：{f.split("：")[1] if "：" in f else ""}</li>'
        for f in data.get("features", [])
    ])
    
    html = HTML_TEMPLATE.format(
        name=name,
        type=data["type"],
        type_color=data["type_color"],
        type_text=data["type_text"],
        desc=data["desc"],
        definition=data["definition"],
        related_links=related_links,
        chapter_links=chapter_links,
        features_list=features_list
    )
    
    return html

def generate_all_entities():
    """生成所有实体详情页"""
    output_dir = Path("kg/entities")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📝 生成 {len(ENTITIES)} 个实体详情页...")
    print("=" * 50)
    
    for name, data in ENTITIES.items():
        html = generate_entity_page(name, data)
        output_file = output_dir / f"{name}.html"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ {name}.html")
    
    print("=" * 50)
    print(f"✅ 全部生成完成！")
    print(f"📁 输出目录: {output_dir}")

if __name__ == '__main__':
    generate_all_entities()
