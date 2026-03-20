#!/usr/bin/env python3
"""
批量生成所有章节HTML
"""

import subprocess
from pathlib import Path

def generate_all():
    """生成所有章节的HTML"""
    chapters_dir = Path('chapters')
    
    if not chapters_dir.exists():
        print("❌ chapters/ 目录不存在")
        return
    
    md_files = sorted(chapters_dir.glob('*.md'))
    
    if not md_files:
        print("❌ 没有找到Markdown文件")
        return
    
    print(f"📝 找到 {len(md_files)} 个章节文件")
    print("=" * 50)
    
    for md_file in md_files:
        subprocess.run(['python3', 'scripts/render_html.py', str(md_file)])
    
    print("=" * 50)
    print("✅ 全部生成完成！")
    print("📁 输出目录: docs/chapters/")

if __name__ == '__main__':
    generate_all()
