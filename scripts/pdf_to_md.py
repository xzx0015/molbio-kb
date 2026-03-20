#!/usr/bin/env python3
"""
PDF to Markdown Converter for molbio-kb
Converts molecular biology textbooks to structured Markdown
"""

import sys
import os
import re
import json
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF using available tools"""
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        text_content = []
        
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            if text.strip():
                text_content.append(f"<!-- Page {page_num} -->\n{text}")
        
        doc.close()
        return '\n\n'.join(text_content)
    except Exception as e:
        print(f"PyMuPDF failed: {e}")
        # Fallback to pdftotext
        import subprocess
        result = subprocess.run(['pdftotext', '-layout', pdf_path, '-'], 
                              capture_output=True, text=True)
        return result.stdout

def clean_text(text):
    """Clean extracted text"""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove page numbers (standalone numbers)
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    # Remove header/footer patterns
    text = re.sub(r'第[一二三四五六七八九十\d]+章.*?\n', '\n', text)
    return text.strip()

def detect_chapters(text):
    """Detect chapter structure from text"""
    chapters = []
    
    # Chinese chapter patterns
    chapter_patterns = [
        r'第[一二三四五六七八九十\d]+章\s*[\u4e00-\u9fff]+',  # 第一章 XXX
        r'Chapter\s+\d+[\s:]+[A-Za-z\s]+',  # Chapter 1: XXX
        r'^\d+\.\d+\s+',  # 1.1 XXX
    ]
    
    lines = text.split('\n')
    current_chapter = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for chapter headers
        for pattern in chapter_patterns:
            if re.match(pattern, line):
                if current_chapter:
                    chapters.append(current_chapter)
                current_chapter = {
                    'title': line,
                    'content': []
                }
                break
        else:
            if current_chapter:
                current_chapter['content'].append(line)
    
    if current_chapter:
        chapters.append(current_chapter)
    
    return chapters

def convert_pdf_to_md(pdf_path, output_dir):
    """Convert PDF to structured Markdown"""
    pdf_name = Path(pdf_path).stem
    print(f"Processing: {pdf_name}")
    
    # Extract text
    raw_text = extract_text_from_pdf(pdf_path)
    cleaned_text = clean_text(raw_text)
    
    # Detect chapters
    chapters = detect_chapters(cleaned_text)
    
    # Create output
    output_path = Path(output_dir) / f"{pdf_name}.md"
    
    # Build markdown content
    md_content = f"""---
source: {pdf_name}.pdf
date_extracted: 2026-03-19
chapters_detected: {len(chapters)}
---

# {pdf_name}

## Table of Contents

"""
    
    for i, ch in enumerate(chapters, 1):
        md_content += f"{i}. {ch['title']}\n"
    
    md_content += "\n---\n\n"
    
    # Add chapter content
    for ch in chapters:
        md_content += f"## {ch['title']}\n\n"
        content_text = '\n'.join(ch['content'][:100])  # First 100 lines per chapter
        md_content += content_text + "\n\n"
    
    # Write output
    output_path.write_text(md_content, encoding='utf-8')
    print(f"✓ Created: {output_path}")
    
    # Save metadata
    meta_path = Path(output_dir) / f"{pdf_name}_meta.json"
    metadata = {
        'source': pdf_name + '.pdf',
        'chapters': [{'title': ch['title'], 'line_count': len(ch['content'])} for ch in chapters]
    }
    meta_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return output_path

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python pdf_to_md.py <pdf_path> <output_dir>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    
    convert_pdf_to_md(pdf_path, output_dir)
