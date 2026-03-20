#!/usr/bin/env python3
"""
分子生物学知识库 - 增强版渲染器
支持12类实体标注体系和知识图谱
"""

import re
import json
import markdown
from pathlib import Path
from collections import defaultdict

# 12类实体定义（来自SKILL_03a）
ENTITY_TYPES = {
    '@': {'name': '基因', 'class': 'gene', 'color': '#e3f2fd', 'text': '#1976d2'},
    '#': {'name': '蛋白', 'class': 'protein', 'color': '#f3e5f5', 'text': '#7b1fa2'},
    '$': {'name': '细胞结构', 'class': 'structure', 'color': '#e8f5e9', 'text': '#388e3c'},
    '%': {'name': '分子过程', 'class': 'process', 'color': '#fff3e0', 'text': '#f57c00'},
    '&': {'name': '技术方法', 'class': 'technique', 'color': '#fce4ec', 'text': '#c2185b'},
    '*': {'name': '代谢物', 'class': 'metabolite', 'color': '#e0f2f1', 'text': '#00796b'},
    '=': {'name': '试剂材料', 'class': 'reagent', 'color': '#f5f5f5', 'text': '#616161'},
    '!': {'name': '条件参数', 'class': 'condition', 'color': '#fff8e1', 'text': '#f9a825'},
    '>': {'name': '文献来源', 'class': 'reference', 'color': '#efebe9', 'text': '#5d4037'},
    '<': {'name': '核心概念', 'class': 'concept', 'color': '#e8eaf6', 'text': '#3f51b5'},
    '+': {'name': '疾病表型', 'class': 'disease', 'color': '#ffebee', 'text': '#c62828'},
    ':': {'name': '数值数据', 'class': 'data', 'color': '#e0f7fa', 'text': '#00838f'},
}

# HTML模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | 分子生物学知识库</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.8;
            color: #333;
            background: #f5f7fa;
        }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}
        .back {{ color: #667eea; text-decoration: none; margin-bottom: 20px; display: inline-block; padding: 10px 0; }}
        .back:hover {{ text-decoration: underline; }}
        
        /* 导航栏 */
        .nav {{
            background: white;
            border-radius: 12px;
            padding: 15px 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .nav a {{ color: #667eea; text-decoration: none; font-size: 0.9rem; }}
        .nav a:hover {{ text-decoration: underline; }}
        
        /* 文章内容 */
        article {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        h1 {{ color: #667eea; margin-bottom: 30px; font-size: 2rem; }}
        h2 {{ color: #764ba2; margin: 30px 0 15px; font-size: 1.5rem; }}
        h3 {{ color: #555; margin: 20px 0 10px; font-size: 1.2rem; }}
        p {{ margin-bottom: 15px; }}
        
        /* 表格 */
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
        th {{ background: #f8f9fa; font-weight: 600; color: #667eea; }}
        tr:hover {{ background: #f8f9fa; }}
        
        /* 代码块 */
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 8px; overflow-x: auto; margin: 15px 0; }}
        code {{ font-family: 'Consolas', 'Monaco', monospace; font-size: 0.9em; }}
        
        /* 引用 */
        blockquote {{ border-left: 4px solid #667eea; padding-left: 20px; margin: 20px 0; color: #666; font-style: italic; }}
        
        /* 12类实体标注样式 */
        .entity {{
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .entity:hover {{
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            transform: translateY(-1px);
        }}
        {entity_styles}
        
        /* 实体图例 */
        .legend {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
            font-size: 0.85rem;
        }}
        .legend-title {{ font-weight: 600; margin-bottom: 10px; color: #555; }}
        .legend-items {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .legend-item {{ display: flex; align-items: center; gap: 5px; }}
        .legend-color {{ width: 12px; height: 12px; border-radius: 3px; }}
        
        /* 知识卡片 */
        .knowledge-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .knowledge-card h4 {{ margin-bottom: 10px; }}
        
        footer {{ text-align: center; padding: 40px; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../" class="back">← 返回首页</a>
        
        <div class="nav">
            <a href="../kg/entities/index.html">🔬 实体索引</a>
            <a href="../kg/concepts/index.html">💡 概念图谱</a>
            <a href="../kg/relations/index.html">🔗 关系网络</a>
        </div>
        
        <article>
            {legend}
            {content}
        </article>
        
        <footer>
            <p>分子生物学知识库 | Built with ❤️</p>
        </footer>
    </div>
    
    <script>
        // 实体点击交互
        document.querySelectorAll('.entity').forEach(el => {{
            el.addEventListener('click', function() {{
                const entityName = this.textContent;
                const entityType = this.className.split(' ')[1];
                console.log('Entity clicked:', entityName, entityType);
                // 未来可添加跳转到实体详情页
            }});
        }});
    </script>
</body>
</html>
'''

def parse_entities_v2(md_content):
    """解析12类实体标注 〖TYPE内容〗"""
    entities_found = defaultdict(list)
    
    def replace_entity(match):
        marker = match.group(1)
        content = match.group(2)
        
        if marker not in ENTITY_TYPES:
            return match.group(0)
        
        entity_info = ENTITY_TYPES[marker]
        entities_found[entity_info['name']].append(content)
        
        # 处理消歧语法：内容|规范名
        if '|' in content:
            display_name, canonical_name = content.split('|', 1)
        else:
            display_name = content
            canonical_name = content
        
        return f'<span class="entity entity-{entity_info["class"]}" title="类型：{entity_info["name"]}，规范名：{canonical_name}">{display_name}</span>'
    
    # 匹配 〖TYPE内容〗格式
    pattern = r'〖([@#$%&*!=><+:])([^〗]+)〗'
    result = re.sub(pattern, replace_entity, md_content)
    
    return result, dict(entities_found)

def generate_entity_styles():
    """生成实体样式CSS"""
    styles = []
    for marker, info in ENTITY_TYPES.items():
        styles.append(f'''
        .entity-{info['class']} {{
            background: {info['color']};
            color: {info['text']};
        }}''')
    return '\n'.join(styles)

def generate_legend():
    """生成实体图例HTML"""
    items = []
    for marker, info in ENTITY_TYPES.items():
        items.append(f'''
        <div class="legend-item">
            <span class="legend-color" style="background: {info['color']}"></span>
            <span>{marker} {info['name']}</span>
        </div>''')
    
    return f'''
    <div class="legend">
        <div class="legend-title">📋 实体标注图例</div>
        <div class="legend-items">
            {''.join(items)}
        </div>
    </div>
    '''

def render_markdown_v2(md_file, output_dir='docs/chapters'):
    """渲染增强版Markdown为HTML"""
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"❌ 文件不存在: {md_file}")
        return
    
    # 读取
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 提取标题
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem
    
    # 解析实体标注
    md_content, entities_found = parse_entities_v2(md_content)
    
    # 转换为HTML
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    html_content = md.convert(md_content)
    
    # 生成样式和图例
    entity_styles = generate_entity_styles()
    legend = generate_legend()
    
    # 填充模板
    full_html = HTML_TEMPLATE.format(
        title=title,
        entity_styles=entity_styles,
        legend=legend,
        content=html_content
    )
    
    # 保存文件
    output_path = Path(output_dir) / f"{md_path.stem}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    # 保存实体统计
    stats_path = Path(output_dir) / f"{md_path.stem}_entities.json"
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(entities_found, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已生成: {output_path}")
    print(f"📊 实体统计: {dict(entities_found)}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("用法: python render_v2.py <markdown文件>")
        sys.exit(1)
    
    render_markdown_v2(sys.argv[1])
