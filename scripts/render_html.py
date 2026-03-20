#!/usr/bin/env python3
"""
分子生物学知识库 - Markdown to HTML 渲染器
参考：史记知识库渲染方案
"""

import re
import sys
import markdown
from pathlib import Path

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
        .back {{ 
            color: #667eea; 
            text-decoration: none; 
            margin-bottom: 20px; 
            display: inline-block;
            padding: 10px 0;
        }}
        .back:hover {{ text-decoration: underline; }}
        
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
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: #f8f9fa;
            font-weight: 600;
            color: #667eea;
        }}
        tr:hover {{ background: #f8f9fa; }}
        
        /* 代码块 */
        pre {{
            background: #f4f4f4;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 15px 0;
        }}
        code {{
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9em;
        }}
        
        /* 引用 */
        blockquote {{
            border-left: 4px solid #667eea;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
        }}
        
        /* 实体标注样式 */
        .entity {{
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 500;
            cursor: pointer;
        }}
        .entity-molecule {{ background: #e3f2fd; color: #1976d2; }}
        .entity-process {{ background: #f3e5f5; color: #7b1fa2; }}
        .entity-enzyme {{ background: #e8f5e9; color: #388e3c; }}
        .entity-tech {{ background: #fff3e0; color: #f57c00; }}
        .entity-person {{ background: #fce4ec; color: #c2185b; }}
        .entity-concept {{ background: #e0f2f1; color: #00796b; }}
        
        /* 概念框 */
        .concept-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .concept-box h4 {{ margin-bottom: 10px; }}
        
        /* 列表 */
        ul, ol {{ margin: 15px 0 15px 30px; }}
        li {{ margin: 8px 0; }}
        
        footer {{
            text-align: center;
            padding: 40px;
            color: #999;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../" class="back">← 返回首页</a>
        <article>
            {content}
        </article>
        <footer>
            <p>分子生物学知识库 | Built with ❤️</p>
        </footer>
    </div>
</body>
</html>
'''

def parse_entities(md_content):
    """解析实体标注 <entity type="xxx">yyy</entity>"""
    type_map = {
        '分子': 'molecule',
        '过程': 'process',
        '酶': 'enzyme',
        '技术': 'tech',
        '人物': 'person',
        '复合物': 'molecule',
        '项目': 'concept',
        '概念': 'concept'
    }
    
    def replace_entity(match):
        entity_type = match.group(1)
        entity_text = match.group(2)
        css_class = type_map.get(entity_type, 'concept')
        return f'<span class="entity entity-{css_class}" title="{entity_type}">{entity_text}</span>'
    
    pattern = r'<entity type="([^"]+)">([^<]+)</entity>'
    return re.sub(pattern, replace_entity, md_content)

def parse_concepts(md_content):
    """解析概念标注 <concept id="xxx">yyy</concept>"""
    def replace_concept(match):
        concept_id = match.group(1)
        concept_text = match.group(2)
        return f'<span class="entity entity-concept" id="{concept_id}">{concept_text}</span>'
    
    pattern = r'<concept id="([^"]+)">([^<]+)</concept>'
    return re.sub(pattern, replace_concept, md_content)

def render_markdown(md_file, output_dir='docs/chapters'):
    """渲染单个Markdown文件为HTML"""
    md_path = Path(md_file)
    if not md_path.exists():
        print(f"❌ 文件不存在: {md_file}")
        return
    
    # 读取Markdown内容
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 提取标题
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else md_path.stem
    
    # 处理实体标注
    md_content = parse_entities(md_content)
    md_content = parse_concepts(md_content)
    
    # 转换为HTML
    md = markdown.Markdown(extensions=['tables', 'fenced_code'])
    html_content = md.convert(md_content)
    
    # 填充模板
    full_html = HTML_TEMPLATE.format(title=title, content=html_content)
    
    # 保存文件
    output_path = Path(output_dir) / f"{md_path.stem}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f"✅ 已生成: {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python render_html.py <markdown文件>")
        sys.exit(1)
    
    render_markdown(sys.argv[1])
