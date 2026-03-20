#!/usr/bin/env python3
"""
Extract structure from scanned PDFs using OCR
For molbio-kb knowledge base
"""

import fitz
import os
import re
import json
from pathlib import Path

def extract_text_with_ocr(pdf_path, output_dir, max_pages=50):
    """Extract text from scanned PDF using OCR"""
    import subprocess
    import tempfile
    
    doc = fitz.open(pdf_path)
    pdf_name = Path(pdf_path).stem
    
    print(f"Processing {pdf_name} ({len(doc)} pages)")
    
    # Create temp directory for images
    with tempfile.TemporaryDirectory() as tmpdir:
        all_text = []
        
        # Process first max_pages pages
        for page_num in range(min(max_pages, len(doc))):
            page = doc[page_num]
            
            # Render page to image
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR
            img_path = os.path.join(tmpdir, f"page_{page_num:04d}.png")
            pix.save(img_path)
            
            # OCR the image
            txt_path = os.path.join(tmpdir, f"page_{page_num:04d}")
            try:
                result = subprocess.run(
                    ['tesseract', img_path, txt_path, '-l', 'chi_sim+eng'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                # Read OCR result
                with open(txt_path + '.txt', 'r', encoding='utf-8') as f:
                    text = f.read()
                    if text.strip():
                        all_text.append(f"<!-- Page {page_num + 1} -->\n{text}")
            except Exception as e:
                print(f"  OCR failed for page {page_num + 1}: {e}")
                continue
            
            if (page_num + 1) % 10 == 0:
                print(f"  Processed {page_num + 1} pages...")
        
        doc.close()
        
        # Save extracted text
        full_text = '\n\n'.join(all_text)
        output_path = Path(output_dir) / f"{pdf_name}_ocr.txt"
        output_path.write_text(full_text, encoding='utf-8')
        print(f"✓ Saved: {output_path}")
        
        return output_path

def detect_chapters_from_text(text):
    """Detect chapter structure from OCR text"""
    chapters = []
    
    # Chinese chapter patterns
    patterns = [
        r'第[一二三四五六七八九十\d]+章\s*[\u4e00-\u9fff]+',
        r'第\d+章\s+[\u4e00-\u9fff]+',
        r'Chapter\s+\d+[\s:]+[A-Za-z\s]+',
    ]
    
    lines = text.split('\n')
    current_chapter = None
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 3:
            continue
            
        # Check for chapter headers
        for pattern in patterns:
            if re.search(pattern, line):
                if current_chapter and current_chapter['content']:
                    chapters.append(current_chapter)
                current_chapter = {
                    'title': line[:100],
                    'content': []
                }
                break
        else:
            if current_chapter:
                current_chapter['content'].append(line)
    
    if current_chapter and current_chapter['content']:
        chapters.append(current_chapter)
    
    return chapters

def create_markdown_from_ocr(ocr_file, output_dir):
    """Create structured markdown from OCR text"""
    text = Path(ocr_file).read_text(encoding='utf-8')
    pdf_name = Path(ocr_file).stem.replace('_ocr', '')
    
    # Detect chapters
    chapters = detect_chapters_from_text(text)
    
    # Create markdown
    md_content = f"""---
source: {pdf_name}.pdf
date_extracted: 2026-03-19
extraction_method: OCR
chapters_detected: {len(chapters)}
---

# {pdf_name}

## Table of Contents

"""
    
    for i, ch in enumerate(chapters[:20], 1):  # Limit to first 20 chapters
        md_content += f"{i}. {ch['title']}\n"
    
    md_content += "\n---\n\n"
    
    # Add chapter content (first 50 lines per chapter)
    for ch in chapters[:10]:  # First 10 chapters
        md_content += f"## {ch['title']}\n\n"
        content_text = '\n'.join(ch['content'][:50])
        md_content += content_text + "\n\n"
    
    # Save markdown
    output_path = Path(output_dir) / f"{pdf_name}.md"
    output_path.write_text(md_content, encoding='utf-8')
    print(f"✓ Created: {output_path}")
    
    # Save metadata
    meta = {
        'source': pdf_name + '.pdf',
        'extraction': 'OCR',
        'chapters': [{'title': ch['title'], 'lines': len(ch['content'])} for ch in chapters]
    }
    meta_path = Path(output_dir) / f"{pdf_name}_meta.json"
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return output_path

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python extract_pdf_structure.py <pdf_path> <output_dir> [max_pages]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    max_pages = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Extract OCR text
    ocr_file = extract_text_with_ocr(pdf_path, output_dir, max_pages)
    
    # Create markdown
    create_markdown_from_ocr(ocr_file, output_dir)
