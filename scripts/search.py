#!/usr/bin/env python3
"""
molbio-kb 知识库快速检索工具
支持关键词搜索、章节查询、概念检索
"""

import os
import re
import json
import argparse
from pathlib import Path

# Get the directory where the script is located
SCRIPT_DIR = Path(__file__).parent.resolve()
# The knowledge base root is one level up from scripts
KB_DIR = SCRIPT_DIR.parent
RAW_DIR = KB_DIR / "docs" / "raw"

def search_keyword(keyword, textbooks=None, context_lines=3):
    """
    搜索关键词
    
    Args:
        keyword: 搜索关键词
        textbooks: 指定教材列表（None 表示全部）
        context_lines: 显示上下文行数
    """
    results = []
    
    # 获取要搜索的文件
    if textbooks:
        files = [RAW_DIR / f"{t}.md" for t in textbooks]
        files = [f for f in files if f.exists()]
    else:
        files = list(RAW_DIR.glob("*.md"))
        files = [f for f in files if not f.name.endswith('_meta.json') and not f.name.endswith('_ocr.txt')]
    
    print(f"📚 搜索关键词：{keyword}")
    print(f"📁 搜索范围：{len(files)} 个文件")
    print("-" * 60)
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if keyword.lower() in line.lower():
                    # 显示上下文
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    
                    context = '\n'.join(lines[start:end])
                    
                    results.append({
                        'file': file_path.name,
                        'line_num': i + 1,
                        'content': context
                    })
        except Exception as e:
            print(f"⚠️  读取文件失败：{file_path} - {e}")
    
    # 显示结果
    if results:
        print(f"\n✅ 找到 {len(results)} 条结果:\n")
        for i, result in enumerate(results[:20], 1):  # 限制显示 20 条
            print(f"[{i}] 📄 {result['file']} (第{result['line_num']}行)")
            print(f"    {result['content'][:200]}...")
            print()
        
        if len(results) > 20:
            print(f"... 还有 {len(results) - 20} 条结果，请缩小搜索范围")
    else:
        print("\n❌ 未找到相关内容")
    
    return results

def list_chapters(textbook=None):
    """列出教材章节"""
    
    if textbook:
        files = [RAW_DIR / f"{textbook}.md"]
    else:
        files = list(RAW_DIR.glob("*.md"))
        files = [f for f in files if not f.name.endswith('_meta.json')]
    
    print(f"📖 教材章节列表:\n")
    
    for file_path in files:
        if not file_path.exists():
            continue
            
        print(f"\n{'='*60}")
        print(f"📘 {file_path.stem}")
        print(f"{'='*60}")
        
        content = file_path.read_text(encoding='utf-8')
        
        # 提取目录
        in_toc = False
        chapters = []
        
        for line in content.split('\n'):
            if '## Table of Contents' in line:
                in_toc = True
                continue
            elif in_toc:
                if line.strip().startswith('---'):
                    break
                if line.strip() and any(c.isdigit() for c in line):
                    chapters.append(line.strip())
        
        if chapters:
            for ch in chapters[:15]:  # 显示前 15 章
                print(f"  {ch}")
            if len(chapters) > 15:
                print(f"  ... 还有 {len(chapters) - 15} 章")

def show_stats():
    """显示知识库统计信息"""
    
    print("📊 molbio-kb 知识库统计\n")
    print("=" * 60)
    
    # 统计文件
    md_files = list(RAW_DIR.glob("*.md"))
    md_files = [f for f in md_files if not f.name.endswith('_meta.json')]
    
    print(f"📁 已处理教材：{len(md_files)} 本")
    
    total_lines = 0
    total_chars = 0
    
    for file_path in md_files:
        content = file_path.read_text(encoding='utf-8')
        total_lines += len(content.split('\n'))
        total_chars += len(content)
    
    print(f"📄 总行数：{total_lines:,}")
    print(f"📝 总字符：{total_chars:,}")
    print()
    
    # 显示每本教材
    print("📚 教材详情:")
    print("-" * 60)
    
    for file_path in sorted(md_files):
        content = file_path.read_text(encoding='utf-8')
        lines = len(content.split('\n'))
        chars = len(content)
        
        # 尝试读取元数据
        meta_file = file_path.parent / f"{file_path.stem}_meta.json"
        chapters = "?"
        if meta_file.exists():
            try:
                meta = json.loads(meta_file.read_text(encoding='utf-8'))
                chapters = len(meta.get('chapters', []))
            except:
                pass
        
        print(f"  {file_path.stem}")
        print(f"    行数：{lines:,} | 字符：{chars:,} | 章节：{chapters}")
    
    print()
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='molbio-kb 知识库检索工具')
    parser.add_argument('action', choices=['search', 'chapters', 'stats'],
                       help='操作类型：search(搜索) | chapters(章节) | stats(统计)')
    parser.add_argument('-k', '--keyword', help='搜索关键词')
    parser.add_argument('-t', '--textbook', help='指定教材')
    parser.add_argument('-c', '--context', type=int, default=3,
                       help='搜索上下文行数（默认：3）')
    
    args = parser.parse_args()
    
    if args.action == 'search':
        if not args.keyword:
            print("❌ 搜索需要提供关键词 (-k)")
            return
        textbooks = [args.textbook] if args.textbook else None
        search_keyword(args.keyword, textbooks, args.context)
    
    elif args.action == 'chapters':
        textbook = args.textbook
        list_chapters(textbook)
    
    elif args.action == 'stats':
        show_stats()

if __name__ == '__main__':
    main()
