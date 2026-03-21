#!/usr/bin/env python3
"""
生成实体 HTML 页面脚本
读取 JSON 实体文件，生成美观的 HTML 展示页面
"""

import json
import os
from pathlib import Path
from urllib.parse import quote

# HTML 模板
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} | 分子生物学知识库</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        
        .header {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .back {{ color: #667eea; text-decoration: none; display: inline-block; margin-bottom: 15px; }}
        .back:hover {{ text-decoration: underline; }}
        h1 {{ color: #667eea; margin-bottom: 10px; }}
        .subtitle {{ color: #999; font-size: 0.9em; }}
        .meta {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        .tag {{
            background: #667eea;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
        }}
        .chapter-tag {{ background: #28a745; }}
        
        .section {{
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            color: #764ba2;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .section p {{ color: #555; line-height: 1.8; }}
        
        .concept-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 15px;
        }}
        .concept-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #667eea;
        }}
        .concept-card h4 {{ color: #333; margin-bottom: 8px; font-size: 1em; }}
        .concept-card p {{ color: #666; font-size: 0.9em; line-height: 1.5; }}
        
        .key-points {{ list-style: none; padding: 0; }}
        .key-points li {{
            padding: 12px 15px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 3px solid #667eea;
            color: #555;
        }}
        
        .relation-list {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .relation-tag {{
            background: #e9ecef;
            color: #495057;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            transition: all 0.3s;
        }}
        .relation-tag:hover {{ background: #667eea; color: white; }}
        
        .references {{ list-style: none; padding: 0; }}
        .references li {{
            padding: 10px 15px;
            margin: 8px 0;
            background: #f8f9fa;
            border-radius: 8px;
            color: #666;
            font-size: 0.9em;
            border-left: 3px solid #28a745;
        }}
        
        .structure-box {{
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
            border-radius: 12px;
            padding: 20px;
            margin-top: 15px;
        }}
        .structure-box h4 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        .structure-img {{
            width: 100%;
            max-width: 400px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin: 10px 0;
        }}
        .structure-links {{
            display: flex;
            gap: 10px;
            margin-top: 10px;
        }}
        .structure-link {{
            background: #667eea;
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            text-decoration: none;
            font-size: 0.85em;
        }}
        .structure-link:hover {{ background: #5a6fd6; }}
        
        footer {{ text-align: center; color: white; padding: 20px; opacity: 0.8; }}
        
        @media (max-width: 768px) {{ .concept-grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="index.html" class="back">← 返回实体索引</a>
            <h1>{name}</h1>
            <p class="subtitle">{nameEn} | {chapter}</p>
            <div class="meta">
                <span class="tag">{category}</span>
                <span class="tag chapter-tag">{chapter}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>📖 定义</h2>
            <p>{definition}</p>
        </div>
        
        <div class="section">
            <h2>🔑 关键概念</h2>
            <div class="concept-grid">{concepts}</div>
        </div>
        
        <div class="section">
            <h2>📌 核心知识点</h2>
            <ul class="key-points">{keyPoints}</ul>
        </div>
        
        <div class="section">
            <h2>🔗 关联实体</h2>
            <div class="relation-list">{relations}</div>
        </div>
        
        {structure}
        
        <div class="section">
            <h2>📚 参考文献</h2>
            <ul class="references">{references}</ul>
        </div>
        
        <footer><p>© 2026 分子生物学知识库</p></footer>
    </div>
</body>
</html>
'''

def generate_concepts_html(concepts):
    if not concepts:
        return '<p>暂无关键概念</p>'
    html = ''
    for concept in concepts:
        html += f'<div class="concept-card"><h4>{concept.get("term", "")}</h4><p>{concept.get("definition", "")}</p></div>'
    return html

def generate_keypoints_html(key_points):
    if not key_points:
        return '<li>暂无核心知识点</li>'
    return '\n'.join([f'<li>{point}</li>' for point in key_points])

def generate_relations_html(relations):
    if not relations:
        return '<span style="color: #999;">暂无关联实体</span>'
    html = ''
    for rel in relations:
        encoded_rel = quote(rel, safe='')
        html += f'<a href="{encoded_rel}.html" class="relation-tag">{rel}</a>'
    return html

def generate_references_html(references):
    if not references:
        return '<li>暂无参考文献</li>'
    return '\n'.join([f'<li>{ref}</li>' for ref in references])

def generate_structure_html(structure):
    if not structure:
        return ''
    
    pdb_id = structure.get('pdbId', '')
    pdb_url = structure.get('pdbUrl', '')
    alphafold_url = structure.get('alphafoldUrl', '')
    description = structure.get('description', '')
    image_url = structure.get('imageUrl', '')
    
    html = '<div class="section">\n'
    html += '<h2>🧬 蛋白质结构</h2>\n'
    html += '<div class="structure-box">\n'
    html += f'<h4>📷 {description}</h4>\n'
    
    if image_url:
        html += f'<img src="{image_url}" alt="蛋白质结构" class="structure-img" onerror="this.style.display=\'none\'">\n'
    
    html += '<div class="structure-links">\n'
    if pdb_url:
        html += f'<a href="{pdb_url}" target="_blank" class="structure-link">🔗 PDB 数据库</a>\n'
    if alphafold_url:
        html += f'<a href="{alphafold_url}" target="_blank" class="structure-link">🔗 AlphaFold</a>\n'
    html += '</div>\n'
    html += '</div>\n'
    html += '</div>\n'
    
    return html

def generate_entity_page(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    concepts_html = generate_concepts_html(data.get('keyConcepts', []))
    keypoints_html = generate_keypoints_html(data.get('keyPoints', []))
    relations_html = generate_relations_html(data.get('relatedEntities', []))
    references_html = generate_references_html(data.get('references', []))
    structure_html = generate_structure_html(data.get('structure'))
    
    html = HTML_TEMPLATE.format(
        name=data.get('name', ''),
        nameEn=data.get('nameEn', ''),
        chapter=data.get('chapter', ''),
        category=data.get('category', ''),
        definition=data.get('definition', ''),
        concepts=concepts_html,
        keyPoints=keypoints_html,
        relations=relations_html,
        references=references_html,
        structure=structure_html
    )
    
    output_file = json_file.parent / (json_file.stem + '.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 生成: {output_file.name}")

def main():
    entities_dir = Path(__file__).parent.parent / 'kg' / 'entities'
    
    json_files = list(entities_dir.glob('*.json'))
    print(f"找到 {len(json_files)} 个 JSON 实体文件")
    print("开始生成 HTML 页面...\n")
    
    for json_file in json_files:
        try:
            generate_entity_page(json_file)
        except Exception as e:
            print(f"❌ 错误 {json_file.name}: {e}")
    
    print("\n✅ 全部生成完成！")

if __name__ == '__main__':
    main()
