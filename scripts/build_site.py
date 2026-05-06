#!/usr/bin/env python3
"""Build the static Molecular Biology knowledge base from source data.

Sources kept as canonical:
- content/chapters/*.md
- kg/entities/*.json
- kg/relations/*.json
- content/skills/*.md

Generated site targets:
- index.html
- chapters/*.html
- kg/entities/*.html + index.html
- kg/concepts/index.html
- skills/*.html + index.html
- search/index.html + search/search-index.json
- docs/ mirror for compatibility with older links
"""
from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import quote

try:
    import markdown  # type: ignore
except Exception:  # pragma: no cover
    markdown = None

ROOT = Path(__file__).resolve().parents[1]
SITE_TITLE = "分子生物学知识库"

ENTITY_TYPE_CLASS = {
    "分子": "molecule",
    "酶": "enzyme",
    "蛋白": "protein",
    "蛋白质": "protein",
    "过程": "process",
    "技术": "technique",
    "复合物": "complex",
    "核心理论": "concept",
    "调控元件": "regulatory",
    "调控单元": "regulatory",
    "机制": "mechanism",
}

CSS = """
/* ===== molbio-kb v3 - Modern Documentation Style ===== */
:root{--bg:#fafbfc;--card:#fff;--ink:#1a1a2e;--ink2:#444;--mu:#777;--line:#e2e8f0;--p:#2563eb;--a:#7c3aed;--g:#059669;--o:#ea580c;--hdr:linear-gradient(135deg,#1e40af,#3b82f6,#6366f1)}
html{scroll-behavior:smooth;font-size:20px}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*{animation-duration:.01ms!important;transition-duration:.01ms!important}}
body{font-family:"Noto Serif SC","Source Han Serif SC","Songti SC",Georgia,serif;line-height:2.2;max-width:960px;margin:0 auto;padding:28px 24px;background:var(--bg);color:var(--ink)}
a{color:var(--p);text-decoration:none;transition:color .15s}
a:hover{text-decoration:underline;color:#1d4ed8}

/* ===== Header ===== */
.top{background:var(--hdr);color:#fff;padding:16px 0;margin-bottom:32px;position:sticky;top:0;z-index:100;border-radius:0 0 14px 14px;box-shadow:0 4px 24px rgba(30,64,175,.12)}
.top .wrap{max-width:960px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}
.brand{font-size:1.2rem;font-weight:700;display:flex;align-items:center;gap:8px}
.brand .icon{font-size:1.4rem}
.nav{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.nav a{color:rgba(255,255,255,.88);text-decoration:none;padding:6px 14px;border-radius:8px;font-size:.8rem;transition:all .2s;border:1px solid rgba(255,255,255,.18);font-family:-apple-system,BlinkMacSystemFont,sans-serif}
.nav a:hover{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.35);color:#fff;text-decoration:none}
.settings-toggle{background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:8px;padding:6px 10px;font-size:.9rem;cursor:pointer;transition:all .2s;color:#fff;line-height:1;margin-left:2px}
.settings-toggle:hover{background:rgba(255,255,255,.22)}

/* ===== Stats ===== */
.stats{display:flex;gap:40px;margin:16px 0 28px;flex-wrap:wrap;font-size:.95rem;color:var(--mu)}
.stat .num{font-weight:800;color:var(--p);font-size:1.4rem;letter-spacing:-.5px}

/* ===== Home sections ===== */
.section{margin:32px 0}
.section h2{font-size:1.2rem;border-bottom:2px solid #e2e8f0;padding-bottom:10px;margin-bottom:16px;color:var(--ink);font-weight:700}
.section .subsection{margin:10px 0;font-size:1rem;color:var(--ink2);line-height:2.2}
.section .subsection a{color:var(--ink2);font-weight:500}
.section .subsection a:hover{color:var(--p)}

/* ===== Chapter nav ===== */
.chapter-nav{display:flex;justify-content:center;align-items:center;gap:16px;padding:12px 0;margin:8px 0 24px}
.chapter-nav a{padding:10px 22px;background:#fff;color:#555;text-decoration:none;border:2px solid #e2e8f0;border-radius:10px;font-size:.85rem;transition:all .2s;font-family:-apple-system,BlinkMacSystemFont,sans-serif;box-shadow:0 2px 6px rgba(0,0,0,.03);font-weight:500}
.chapter-nav a:hover{background:#eff6ff;border-color:var(--p);color:var(--p);box-shadow:0 4px 12px rgba(37,99,235,.08)}
.chapter-nav .nav-home{color:#fff;background:var(--p);border-color:var(--p);font-weight:600}
.chapter-nav .nav-home:hover{background:#1d4ed8}

/* ===== Purple Numbers ===== */
.pn{font-size:.7rem;color:#7c3aed;margin-right:10px;cursor:pointer;text-decoration:none;font-family:-apple-system,BlinkMacSystemFont,sans-serif;font-weight:600;opacity:.75;vertical-align:top;position:relative;top:-2px}
.pn:hover{opacity:1;color:#6d28d9}

/* ===== Entity highlighting ===== */
.entity{font-weight:500;cursor:pointer;transition:all .15s;font-size:1.02rem}
.entity.molecule{color:#1d4ed8;text-decoration:underline;text-decoration-color:#1d4ed870;text-underline-offset:4px;text-decoration-thickness:1.5px}
.entity.enzyme{color:#059669;text-decoration:underline;text-decoration-color:#05966970;text-underline-offset:4px;text-decoration-thickness:1.5px}
.entity.protein{color:#be185d;text-decoration:underline;text-decoration-color:#be185d70;text-underline-offset:4px;text-decoration-thickness:1.5px}
.entity.process{color:#c2410c;text-decoration:underline wavy;text-decoration-color:#c2410c70;text-underline-offset:4px}
.entity.technique{color:#4f46e5;text-decoration:underline dashed;text-decoration-color:#4f46e570;text-underline-offset:4px}
.entity.complex{color:#7c3aed;text-decoration:underline double;text-decoration-color:#7c3aed70;text-underline-offset:4px}
.entity.concept,.entity.core-theory{color:#b45309;font-weight:600;background:linear-gradient(transparent 60%,#fed7aa 60%)}
.entity.regulatory{color:#be185d;text-decoration:underline;text-decoration-color:#be185d70;text-underline-offset:4px;text-decoration-thickness:1.5px}
.entity.mechanism{color:#0d9488;text-decoration:underline wavy;text-decoration-color:#0d948870;text-underline-offset:4px}
.hide-entities .entity{color:inherit!important;text-decoration:none!important;font-weight:inherit!important;background:none!important;cursor:text}

/* ===== Article ===== */
.article{margin:24px 0}
.article h2{font-size:1.2rem;margin:40px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0;color:var(--ink);font-weight:700}
.article h3{font-size:1.1rem;margin:28px 0 12px;color:var(--ink2);font-weight:600}
.article p{margin:1.2em 0;font-size:1.02rem}
.article ul,.article ol{margin:12px 0 12px 1.5em;font-size:1rem}
.article li{margin:6px 0;line-height:2}
.article table{width:100%;border-collapse:collapse;margin:28px 0;font-size:.85rem;border:1px solid #e2e8f0;border-radius:10px;overflow:hidden}
.article th{background:#eff6ff;padding:14px 18px;text-align:left;font-weight:600;font-size:.8rem;border-bottom:2px solid #bfdbfe;color:var(--p);text-transform:uppercase;letter-spacing:.3px}
.article td{padding:14px 18px;border-bottom:1px solid #e2e8f0;background:#fff}
.article tr:nth-child(even) td{background:#fafbfc}
.article tr:hover td{background:#eff6ff}
.article code{background:#eff6ff;padding:3px 8px;border-radius:5px;font-size:.85em;font-family:'SF Mono','Fira Code',monospace;color:var(--p)}
.article pre{background:#1e293b;color:#e2e8f0;padding:20px 24px;border-radius:12px;overflow:auto;font-size:.8rem;line-height:1.8;margin:24px 0}
.article blockquote{border-left:4px solid #bfdbfe;margin:24px 0;padding:12px 24px;color:var(--ink2);background:#eff6ff;border-radius:0 10px 10px 0}
.article hr{border:none;height:1px;background:linear-gradient(90deg,transparent,#cbd5e1,transparent);margin:36px 0}

/* ===== Entity detail ===== */
.entity-detail-header{display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:28px}
.entity-detail-header h1{margin:0;border-bottom:none;font-size:1.5rem}
.entity-category-pill{display:inline-block;padding:5px 16px;border-radius:8px;font-size:.8rem;font-weight:500}
.ec-molecule{background:#dbeafe;color:#1d4ed8}
.ec-enzyme{background:#d1fae5;color:#059669}
.ec-protein{background:#fce7f3;color:#be185d}
.ec-process{background:#ffedd5;color:#c2410c}
.ec-technique{background:#e0e7ff;color:#4f46e5}
.ec-complex{background:#ede9fe;color:#7c3aed}
.ec-concept{background:#fef3c7;color:#b45309}
.ec-regulatory{background:#fce7f3;color:#be185d}
.ec-mechanism{background:#ccfbf1;color:#0d9488}

/* ===== Grid / Cards ===== */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px}
.card{background:var(--card);border:1px solid #e2e8f0;border-radius:12px;padding:26px;transition:box-shadow .2s,transform .15s;box-shadow:0 1px 4px rgba(0,0,0,.03);overflow:hidden;position:relative}
.card:hover{box-shadow:0 6px 24px rgba(0,0,0,.07);transform:translateY(-2px)}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:4px;background:var(--hdr);opacity:0;transition:opacity .2s}
.card:hover::before{opacity:1}
.card h2,.card h3{margin:0 0 10px;font-size:1.1rem;font-weight:700}
.card .icon{font-size:1.3rem;margin-bottom:10px;display:block}

/* ===== Chapter page title ===== */
.chapter-title{font-size:1.5rem;font-weight:800;color:var(--ink);margin:0 0 28px;padding-bottom:14px;border-bottom:3px solid var(--p);display:flex;align-items:center;gap:12px}
.chapter-title .ch-num{background:var(--hdr);color:#fff;padding:4px 16px;border-radius:8px;font-size:1rem;font-weight:700;font-family:-apple-system,BlinkMacSystemFont,sans-serif}

/* ===== Concept graph ===== */
.graph{background:var(--card);border:1px solid #e2e8f0;border-radius:12px;padding:28px;margin:28px 0;overflow:auto}
.graph svg{display:block;margin:0 auto;max-width:100%}

/* ===== Pills / Badges ===== */
.pill{display:inline-block;border:1px solid #e2e8f0;border-radius:10px;padding:6px 14px;background:var(--card);margin:3px;font-size:.9rem;transition:all .15s;color:var(--ink2);box-shadow:0 1px 2px rgba(0,0,0,.02)}
.pill:hover{border-color:var(--p);color:var(--p);text-decoration:none;box-shadow:0 2px 8px rgba(37,99,235,.08)}
.badge{display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border-radius:8px;font-size:.75rem;font-weight:500}
.badge-blue{background:#eff6ff;color:var(--p)}
.searchbox{width:100%;font-size:.95rem;border:2px solid #e2e8f0;border-radius:10px;padding:14px 18px;background:var(--card);color:var(--ink);outline:none;transition:border-color .2s}
.searchbox:focus{border-color:var(--p);box-shadow:0 0 0 4px rgba(37,99,235,.08)}
.result{padding:18px 0;border-bottom:1px solid #e2e8f0}
.result:last-child{border-bottom:none}
.crumb{margin:0 0 20px;font-size:.85rem;color:var(--mu)}
.muted{color:var(--mu)}
.section-divider{height:1px;background:#e2e8f0;margin:40px 0}
.tag{display:inline-block;font-size:.7rem;border-radius:5px;padding:3px 9px;margin:2px;font-weight:500;font-family:-apple-system,BlinkMacSystemFont,sans-serif}
.tag.p{background:#eff6ff;color:var(--p)}
.tag.a{background:#f5f3ff;color:var(--a)}
.tag.g{background:#ecfdf5;color:var(--g)}
.list{padding-left:1.4em;font-size:1rem;line-height:2.4}
.list li{margin:3px 0}
.warn{background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:16px 20px;color:#9a3412;font-size:.9rem}
.ok{background:#ecfdf3;border:1px solid #bbf7d0;border-radius:8px;padding:16px 20px;color:#065f46;font-size:.9rem}
.footer{margin-top:64px;padding:32px 0;text-align:center;color:var(--mu);font-size:.8rem;border-top:1px solid #e2e8f0}
.footer a{color:var(--p)}

/* ===== Responsive ===== */
@media(max-width:768px){body{padding:20px 16px;font-size:18px}.brand{font-size:1rem}.chapter-title{font-size:1.3rem}.article h2{font-size:1.1rem}.grid{grid-template-columns:1fr}.stats{gap:20px}.chapter-nav{gap:8px}.chapter-nav a{font-size:.75rem;padding:8px 14px}}

/* ===== Dark mode (manual) ===== */
html.dark body{background:#0f172a;color:#e2e0d0}
html.dark .top{background:linear-gradient(135deg,#0f172a,#1e293b,#1e3a5f)}
html.dark .card{background:#1e293b;border-color:#334155}
html.dark .card::before{opacity:1}
html.dark .article th{background:#1e3a5f;border-color:#334155;color:#93c5fd}
html.dark .article td{background:#1e293b;border-color:#334155}
html.dark .article tr:nth-child(even) td{background:#1a2332}
html.dark .article tr:hover td{background:#1e3a5f}
html.dark .section h2,.article h2{border-color:#334155}
html.dark .searchbox{background:#1e293b;border-color:#334155;color:#e2e0d0}
html.dark .pill{background:#1e293b;border-color:#334155}
html.dark .chapter-nav a{background:#1e293b;border-color:#334155;color:#aaa}
html.dark .chapter-nav a:hover{background:#334155;color:#e2e0d0}
html.dark .graph{background:#1e293b;border-color:#334155}
html.dark .footer{border-color:#334155}
html.dark .chapter-title{border-color:#334155}
html.dark .entity.concept{background:linear-gradient(transparent 60%,#78350f 60%)}
"""

@dataclass
class Page:
    title: str
    path: Path
    kind: str
    text: str


def clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def slug_filename(name: str) -> str:
    return f"{name}.html"


def title_from_md(md: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", md, re.M)
    return m.group(1).strip() if m else fallback


def md_to_html(md_text: str) -> str:
    # Convert custom entity/concept tags before Markdown rendering.
    md_text = re.sub(
        r"<entity\s+type=\"([^\"]+)\">(.*?)</entity>",
        lambda m: f'<span class="entity {ENTITY_TYPE_CLASS.get(m.group(1), "entity-generic")}" title="{html.escape(m.group(1))}">{html.escape(m.group(2))}</span>',
        md_text,
        flags=re.S,
    )
    md_text = re.sub(
        r"<concept\s+id=\"([^\"]+)\">(.*?)</concept>",
        lambda m: f'<span class="entity concept" title="概念：{html.escape(m.group(1))}">{html.escape(m.group(2))}</span>',
        md_text,
        flags=re.S,
    )
    # Legacy 〖@实体〗 syntax.
    md_text = re.sub(r"〖([@#$%&*!=><+:])([^〗]+)〗", lambda m: f'<span class="entity">{html.escape(m.group(2).split("|",1)[0])}</span>', md_text)
    if markdown:
        return markdown.markdown(md_text, extensions=["tables", "fenced_code", "toc"])
    # Minimal fallback.
    lines = []
    for line in md_text.splitlines():
        if line.startswith("# "):
            lines.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            lines.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.strip():
            lines.append(f"<p>{html.escape(line)}</p>")
    return "\n".join(lines)


def rel(from_file: Path, to_file: str | Path) -> str:
    target_text = str(to_file)
    if target_text.startswith(("http://", "https://", "mailto:", "tel:")):
        return target_text
    relative = Path(__import__("os").path.relpath(ROOT / to_file, (ROOT / from_file).parent)).as_posix()
    return "/".join(quote(part) for part in relative.split("/"))


def layout(title: str, body: str, out_path: Path, description: str = "", hero_stats: str = "", is_chapter: bool = False) -> str:
    nav_items = [
        ("🧬 首页", "index.html"),
        ("📖 章节", "chapters/index.html"),
        ("🏷️ 实体", "kg/entities/index.html"),
        ("🔗 图谱", "kg/concepts/index.html"),
        ("🔍 搜索", "search/index.html"),
    ]
    nav = "".join(f'<a href="{rel(out_path, href)}">{label}</a>' for label, href in nav_items)
    nav += '<button class="settings-toggle" onclick="toggleEntities()" title="开关实体高亮">⚙️</button><button class="settings-toggle" onclick="toggleDark()" title="明暗切换" style="font-size:.85rem">🌓</button>'
    toggle_script = '''<script>
(function(){var bk="molbio-hide-entities";var dk="molbio-dark";var s=localStorage.getItem(bk);if(s==="1"){document.documentElement.classList.add("hide-entities")};var d=localStorage.getItem(dk);if(d==="1"){document.documentElement.classList.add("dark")}})();
function toggleEntities(){var c=document.documentElement.classList;c.toggle("hide-entities");localStorage.setItem("molbio-hide-entities",c.contains("hide-entities")?"1":"0")}
function toggleDark(){var c=document.documentElement.classList;c.toggle("dark");localStorage.setItem("molbio-dark",c.contains("dark")?"1":"0")}
</script>'''
    return f'''<!doctype html>
<html lang="zh-CN" class="{'hide-entities' if False else ''}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | {SITE_TITLE}</title><meta name="description" content="{html.escape(description or SITE_TITLE)}">
<style>{CSS}</style></head><body>
<header class="top"><div class="wrap">
<span class="brand"><span class="icon">🧬</span>{SITE_TITLE}</span>
<nav class="nav">{nav}</nav>
</div></header>
<main>{body}</main>
<footer class="footer"><p>Molecular Biology Knowledge Base · <a href="https://github.com/xzx0015/molbio-kb">GitHub</a></p></footer>
{toggle_script}
</body></html>'''


def write_page(path: Path, title: str, body: str, pages: list[Page], kind: str, text: str = "", hero_stats: str = "") -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(layout(title, body, path, clean_text(text)[:160], hero_stats=hero_stats), encoding="utf-8")
    pages.append(Page(title=title, path=path, kind=kind, text=clean_text(text or body)))


def load_entities() -> dict[str, dict[str, Any]]:
    entities: dict[str, dict[str, Any]] = {}
    for fp in sorted((ROOT / "kg/entities").glob("*.json")):
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"WARN invalid json {fp}: {e}")
            continue
        name = data.get("name") or fp.stem
        entities[name] = data
    return entities


def entity_href(name: str, entities: dict[str, dict[str, Any]], from_path: Path) -> str:
    if name in entities:
        return rel(from_path, Path("kg/entities") / slug_filename(name))
    nospace = name.replace(" ", "")
    for n in entities:
        if n.replace(" ", "") == nospace:
            return rel(from_path, Path("kg/entities") / slug_filename(n))
    return rel(from_path, "kg/entities/index.html") + f"?q={quote(name)}"


def build_chapters(pages: list[Page]) -> list[dict[str, str]]:
    # Collect all markdown files, grouped by chapter number prefix
    from collections import defaultdict
    md_files = sorted((ROOT / "content/chapters").glob("*.md"))
    groups = defaultdict(list)
    for md in md_files:
        prefix = md.stem[:2]
        groups[prefix].append(md)
    
    ch_names = ["", "绪论", "分子基础与复制", "信息传递与转录", "翻译与表达调控",
                "原核表达调控与基因组维持", "分子生物学技术与真核表达调控", "实验技术", "组学前沿"]
    
    # Build ONE merged page per chapter (8 chapters total)
    sorted_prefixes = sorted(groups)
    all_chapters = []
    
    for pi, prefix in enumerate(sorted_prefixes):
        subs = groups[prefix]
        ch_num = int(prefix)
        ch_name = ch_names[ch_num] if ch_num < len(ch_names) else f"第{ch_num}章"
        out = Path("chapters") / f"ch{ch_num:02d}_{ch_name}.html"
        
        # Concatenate all sub-chapter markdown content with section breaks
        merged_md = ""
        merged_text = ""
        for mi, md in enumerate(subs):
            raw = md.read_text(encoding="utf-8")
            if mi > 0:
                merged_md += "\n\n---\n\n"
            # Demote ALL # headings to ## (chapter title is already in HTML h1)
            raw_fixed = re.sub(r'^#\s+', '## ', raw, flags=re.M)
            merged_md += raw_fixed
            merged_text += clean_text(raw) + " "
        
        all_chapters.append({"title": ch_name, "stem": f"ch{ch_num:02d}_{ch_name}", "out": out.as_posix(), "text": clean_text(merged_text), "prefix": prefix})
        
        # Chapter nav (prev/home/next)
        prev_link = ""
        next_link = ""
        if pi > 0:
            prev_prefix = sorted_prefixes[pi-1]
            prev_name = ch_names[int(prev_prefix)] if int(prev_prefix) < len(ch_names) else f"第{int(prev_prefix)}章"
            prev_link = f'<a href="{rel(out, Path("chapters") / f"ch{int(prev_prefix):02d}_{prev_name}.html")}">← 上一章</a>'
        if pi < len(sorted_prefixes) - 1:
            next_prefix = sorted_prefixes[pi+1]
            next_name = ch_names[int(next_prefix)] if int(next_prefix) < len(ch_names) else f"第{int(next_prefix)}章"
            next_link = f'<a href="{rel(out, Path("chapters") / f"ch{int(next_prefix):02d}_{next_name}.html")}">下一章 →</a>'
        chapter_nav = f'<nav class="chapter-nav">{prev_link}<a href="{rel(out, "index.html")}" class="nav-home">🏠 首页</a>{next_link}</nav>'
        
        # Build HTML with purple numbers
        html_body = md_to_html(merged_md)
        pn_counter = [0]
        def add_pn(m):
            pn_counter[0] += 1
            return f'<p><a class="pn" id="pn-{pn_counter[0]}" href="#pn-{pn_counter[0]}">{pn_counter[0]}</a>'
        html_body = re.sub(r'<p>', add_pn, html_body)
        
        body = f'{chapter_nav}<div class="chapter-title"><span class="ch-num">第{ch_num}章</span>{ch_name}</div><div class="article">{html_body}</div>{chapter_nav}'
        write_page(out, ch_name, body, pages, "chapter", merged_text)
    
    # Chapter index page – one card per chapter (clean, no sub-list)
    idx = Path("chapters/index.html")
    chapter_cards = []
    for prefix in sorted_prefixes:
        ch_num = int(prefix)
        ch_name = ch_names[ch_num] if ch_num < len(ch_names) else f"第{ch_num}章"
        out_ch = Path("chapters") / f"ch{ch_num:02d}_{ch_name}.html"
        chapter_cards.append(f'<div class="card chapter"><span class="icon">📄</span><h2>第{ch_num}章：{html.escape(ch_name)}</h2><p><a href="{rel(idx, out_ch)}">阅读本章 →</a></p></div>')
    
    body = f'<h1>📖 课程章节</h1><p class="muted">共 <b>{len(groups)}</b> 章。</p><div class="section-divider"></div><div class="grid">{"".join(chapter_cards)}</div>'
    write_page(idx, "课程章节", body, pages, "index", "课程章节")
    return all_chapters


def build_entities(pages: list[Page], entities: dict[str, dict[str, Any]]) -> None:
    for name, data in entities.items():
        out = Path("kg/entities") / slug_filename(name)
        concepts = data.get("keyConcepts") or []
        concept_html = "".join(f'<li><b>{html.escape(str(c.get("term", "")))}</b>：{html.escape(str(c.get("definition", "")))}</li>' if isinstance(c, dict) else f'<li>{html.escape(str(c))}</li>' for c in concepts)
        points = "".join(f'<li>{html.escape(str(x))}</li>' for x in data.get("keyPoints", []) or [])
        related = "".join(f'<a class="pill" href="{entity_href(str(x), entities, out)}">{html.escape(str(x))}</a>' for x in data.get("relatedEntities", []) or [])
        refs = "".join(f'<li>{html.escape(str(x))}</li>' for x in data.get("references", []) or [])
        structure = data.get("structure") or {}
        structure_html = ""
        if isinstance(structure, dict) and structure:
            links = []
            for k in ["pdbUrl", "alphafoldUrl", "imageUrl"]:
                if structure.get(k):
                    links.append(f'<a class="pill" href="{html.escape(str(structure[k]))}">{html.escape(k)}</a>')
            structure_html = f'<h2>结构信息</h2><p>{html.escape(str(structure.get("description", "")))}</p><p>{"".join(links)}</p>'
        body = f'''<div class="crumb"><a href="{rel(out, "index.html")}">首页</a> / <a href="{rel(out, "kg/entities/index.html")}">实体索引</a></div>
<article class="article"><h1>{html.escape(name)} <span class="tag">{html.escape(str(data.get("category", "未分类")))}</span></h1>
<p class="muted">{html.escape(str(data.get("nameEn", "")))} · {html.escape(str(data.get("chapter", "")))}</p>
<h2>定义</h2><p>{html.escape(str(data.get("definition", "暂无定义。")))}</p>
<h2>关键概念</h2><ul>{concept_html or "<li>暂无</li>"}</ul>
<h2>要点</h2><ul>{points or "<li>暂无</li>"}</ul>
<h2>相关实体</h2><p>{related or "暂无"}</p>{structure_html}
<h2>参考</h2><ul>{refs or "<li>暂无</li>"}</ul></article>'''
        write_page(out, name, body, pages, "entity", json.dumps(data, ensure_ascii=False))
    groups: dict[str, list[str]] = {}
    for n, d in entities.items():
        groups.setdefault(str(d.get("category", "未分类")), []).append(n)
    sections = []
    idx = Path("kg/entities/index.html")
    for cat, names in sorted(groups.items()):
        links = "".join(f'<li><a href="{rel(idx, Path("kg/entities") / slug_filename(n))}">{html.escape(n)}</a></li>' for n in sorted(names))
        sections.append(f'<div class="card entity"><h2 style="font-size:18px">{html.escape(cat)} <span class="badge badge-blue">{len(names)}</span></h2><ul class="list" style="font-size:16px;line-height:2">{links}</ul></div>')
    body = f'<h1>🏷️ 实体索引</h1><p class="muted">由 <code>kg/entities/*.json</code> 自动生成，共 <b>{len(entities)}</b> 个结构化实体。</p><div class="section-divider"></div><div class="grid">{"".join(sections)}</div>'
    write_page(idx, "实体索引", body, pages, "index", "实体索引")


def build_concepts(pages: list[Page], entities: dict[str, dict[str, Any]]) -> None:
    rel_file = ROOT / "kg/relations/concept-links.json"
    data = json.loads(rel_file.read_text(encoding="utf-8")) if rel_file.exists() else {"nodes": [], "links": []}
    out = Path("kg/concepts/index.html")
    nodes = data.get("nodes", [])
    links = data.get("links", [])
    relation_types = data.get("relationTypes", {})
    
    # Category color map for nodes
    cat_colors = {
        "核心理论": "#1d4ed8", "分子": "#2563eb", "蛋白质": "#db2777", "酶": "#059669",
        "过程": "#ea580c", "技术": "#6366f1", "复合物": "#7c3aed", "调控元件": "#db2777",
        "调控单元": "#db2777", "机制": "#0891b2", "表观修饰": "#0891b2", "结构": "#7c3aed",
        "小RNA": "#2563eb", "工具": "#059669", "调控": "#db2777"
    }
    rel_colors = {
        "is-a": "#667eea", "part-of": "#764ba2", "regulates": "#e74c3c", "catalyzes": "#27ae60",
        "participates": "#f39c12", "produces": "#9b59b6", "binds": "#3498db", "inhibits": "#e67e22",
        "activates": "#2ecc71", "related": "#95a5a6"
    }
    
    # Build a visual graph using layered layout
    # Layer 0: core theory, Layer 1: molecules, Layer 2: processes, Layer 3: machinery/techniques
    node_map = {}
    for n in nodes:
        if isinstance(n, dict):
            node_map[n.get("id") or n.get("name")] = n
    
    layers = {"中心法则": 0}
    # Simple BFS layering
    for l in links:
        src = l.get("source")
        tgt = l.get("target")
        if src in layers:
            layers[tgt] = max(layers.get(tgt, 0), layers.get(src, 0) + 1)
        elif tgt in layers:
            layers[src] = max(layers.get(src, 0), layers.get(tgt, 0) - 1)
    
    for n in node_map:
        if n not in layers:
            layers[n] = 2
    
    # Group by layer
    layer_nodes = {}
    for nid, layer in layers.items():
        layer_nodes.setdefault(layer, []).append(nid)
    
    # SVG generation
    svg_width = 1100
    layer_x = {}
    for layer in sorted(layer_nodes):
        items = layer_nodes[layer]
        spacing = svg_width / (len(items) + 1)
        for i, nid in enumerate(items):
            layer_x[nid] = spacing * (i + 1)
    
    svg_height = max(100, (max(layer_nodes.keys()) + 1) * 120 + 60)
    
    svg_lines = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" style="width:100%;height:auto;font-family:system-ui,sans-serif">']
    svg_lines.append('<defs><marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="#94a3b8"/></marker></defs>')
    
    # Draw edges
    edge_used = set()
    for l in links:
        src = l.get("source")
        tgt = l.get("target")
        rtype = l.get("type", "related")
        key = (src, tgt)
        if key in edge_used:
            continue
        edge_used.add(key)
        if src in layer_x and tgt in layer_x:
            x1, x2 = layer_x[src], layer_x[tgt]
            y1 = layers.get(src, 0) * 120 + 40
            y2 = layers.get(tgt, 0) * 120 + 40
            color = rel_colors.get(rtype, "#94a3b8")
            svg_lines.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.2" stroke-opacity="0.5" marker-end="url(#arrow)"/>')
    
    # Draw nodes
    for n in nodes:
        if not isinstance(n, dict):
            continue
        nid = n.get("id") or n.get("name")
        name = n.get("name") or nid
        cat = n.get("category", "")
        color = cat_colors.get(cat, "#64748b")
        if nid in layer_x:
            x = layer_x[nid]
            y = layers.get(nid, 2) * 120 + 40
            href = entity_href(str(name), entities, out)
            # Truncate long names
            display = name if len(name) <= 5 else name
            svg_lines.append(f'<a href="{href}"><rect x="{x-42}" y="{y-15}" width="84" height="30" rx="15" fill="{color}" fill-opacity="0.9"/><text x="{x}" y="{y+5}" text-anchor="middle" fill="white" font-size="13" font-weight="600">{html.escape(display[:8])}</text></a>')
    
    svg_lines.append('</svg>')
    svg_graph = "\n".join(svg_lines)
    
    # Node pills
    node_html = "".join(f'<a class="pill" href="{entity_href(str(n.get("name") or n.get("id")), entities, out)}">{html.escape(str(n.get("name") or n.get("id")))}</a>' for n in nodes if isinstance(n, dict))
    
    # Legend for relation types
    legend_parts = []
    for k, v in relation_types.items():
        c = rel_colors.get(k, "#95a5a6")
        legend_parts.append(f'<span class="badge" style="background:{c}22;color:{c};border:1px solid {c}44">{v.get("label", k)}</span>')
    legend = "".join(legend_parts)
    
    link_rows_parts = []
    for l in links:
        if not isinstance(l, dict):
            continue
        rt = str(l.get("type"))
        rc = rel_colors.get(rt, "#95a5a6")
        link_rows_parts.append(f'<tr><td><a href="{entity_href(str(l.get("source")), entities, out)}"><b>{html.escape(str(l.get("source")))}</b></a></td><td><span class="badge" style="background:{rc}22;color:{rc};border:1px solid {rc}44">{html.escape(rt)}</span></td><td><a href="{entity_href(str(l.get("target")), entities, out)}"><b>{html.escape(str(l.get("target")))}</b></a></td><td>{html.escape(str(l.get("description", "")))}</td></tr>')
    link_rows = "".join(link_rows_parts)
    
    body = f'''<h1>概念图谱</h1><p class="muted">由 <code>kg/relations/concept-links.json</code> 自动生成：<b>{len(nodes)}</b> 个节点 · <b>{len(links)}</b> 条关系 · {len(relation_types)} 种关系类型</p>
<div class="section-divider"></div>
<h2>🌐 可视化图谱</h2>
<div class="graph">{svg_graph}</div>
<div class="section-divider"></div>
<h2>🏷️ 关系图例</h2><p style="display:flex;gap:8px;flex-wrap:wrap;margin:12px 0">{legend}</p>
<div class="section-divider"></div>
<h2>📋 所有节点</h2><div class="card"><p>{node_html}</p></div>
<div class="section-divider"></div>
<article class="article"><h2>📊 关系表</h2><table><thead><tr><th>源</th><th>关系</th><th>目标</th><th>说明</th></tr></thead><tbody>{link_rows}</tbody></table></article>'''
    write_page(out, "概念图谱", body, pages, "concept", json.dumps(data, ensure_ascii=False))


def build_skills(pages: list[Page]) -> None:
    skills = []
    for md in sorted((ROOT / "content/skills").glob("*.md")):
        raw = md.read_text(encoding="utf-8")
        title = title_from_md(raw, md.stem)
        out = Path("skills") / f"{md.stem}.html"
        body = f'<div class="crumb"><a href="{rel(out, "index.html")}">首页</a> / <a href="{rel(out, "skills/index.html")}">构建方法</a></div><div class="section-divider"></div><article class="article">{md_to_html(raw)}</article>'
        write_page(out, title, body, pages, "skill", raw)
        skills.append((title, out, clean_text(raw)))
    idx = Path("skills/index.html")
    cards = "".join(f'<div class="card skill"><span class="icon">🛠️</span><h3><a href="{rel(idx, p)}">{html.escape(t)}</a></h3><p class="muted">{html.escape(txt[:120])}...</p></div>' for t, p, txt in skills)
    write_page(idx, "构建方法", f'<h1>🛠️ 构建方法</h1><p class="muted">保留并发布 <code>content/skills/*.md</code>，共 <b>{len(skills)}</b> 个流程文档。</p><div class="section-divider"></div><div class="grid">{cards}</div>', pages, "index", "构建方法")


def build_search(pages: list[Page]) -> None:
    idx_data = [{"title": p.title, "url": p.path.as_posix(), "kind": p.kind, "text": p.text[:2000]} for p in pages]
    (ROOT / "search").mkdir(exist_ok=True)
    (ROOT / "search/search-index.json").write_text(json.dumps(idx_data, ensure_ascii=False, indent=2), encoding="utf-8")
    out = Path("search/index.html")
    body = f'''<h1>🔍 站内搜索</h1><p class="muted">索引 <b>{len(idx_data)}</b> 个页面，离线可用。</p><input id="q" class="searchbox" placeholder="输入关键词，例如 DNA复制、PCR、转录因子..." autofocus><div id="results"></div>
<script>
const INDEX_URL = 'search-index.json';
let docs=[];fetch(INDEX_URL).then(r=>r.json()).then(x=>{{docs=x;render();}});
const q=document.getElementById('q'), results=document.getElementById('results');
function score(d, term){{const hay=(d.title+' '+d.text).toLowerCase(); const t=term.toLowerCase(); return (d.title.toLowerCase().includes(t)?5:0)+(hay.includes(t)?1:0);}}
function esc(s){{return String(s).replace(/[&<>\"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));}}
function render(){{const term=q.value.trim(); let arr=term?docs.map(d=>[score(d,term),d]).filter(x=>x[0]>0).sort((a,b)=>b[0]-a[0]).slice(0,30).map(x=>x[1]):docs.slice(0,20); results.innerHTML=arr.map(d=>`<div class="result"><a href="../${{d.url}}"><b>${{esc(d.title)}}</b></a> <span class="tag">${{esc(d.kind)}}</span><p class="muted">${{esc(d.text.slice(0,160))}}...</p></div>`).join('') || '<p class="muted">没有结果</p>';}}
q.addEventListener('input',render);
</script>'''
    write_page(out, "站内搜索", body, pages, "search", "站内搜索")


def build_home(pages: list[Page], chapters: list[dict[str, str]], entities: dict[str, dict[str, Any]]) -> None:
    out = Path("index.html")
    # Count stats
    rel_file = ROOT / "kg/relations/concept-links.json"
    kg_data = json.loads(rel_file.read_text(encoding="utf-8")) if rel_file.exists() else {"nodes": [], "links": []}
    node_count = len(kg_data.get("nodes", []))
    rel_count = len(kg_data.get("links", []))
    skill_count = len(list((ROOT / "content/skills").glob("*.md")))
    
    # Category counts
    from collections import Counter
    cats = Counter(str(e.get("category", "未分类")) for e in entities.values())
    cat_html = "".join(f'<span class="badge badge-blue">{c}: {n}</span>' for c, n in cats.most_common(6))
    entity_pills = "".join(f'<a class="pill" href="{rel(out, Path("kg/entities") / slug_filename(n))}">{html.escape(n)}</a>' for n in sorted(entities)[:24])
    
    # Home page in shiji-kb style - sections with chapter + sub-links
    from collections import defaultdict
    md_files = sorted((ROOT / "content/chapters").glob("*.md"))
    groups = defaultdict(list)
    for md in md_files:
        prefix = md.stem[:2]
        groups[prefix].append(md)
    
    ch_names_list = ["", "绪论", "分子基础与复制", "信息传递与转录", "翻译与表达调控",
                "原核表达调控与基因组维持", "分子生物学技术与真核表达调控", "实验技术", "组学前沿"]
    chapter_links = ""
    for prefix in sorted(groups):
        subs = groups[prefix]
        ch_num = int(prefix)
        ch_name = ch_names_list[ch_num] if ch_num < len(ch_names_list) else f"第{ch_num}章"
        ch_file = Path("chapters") / f"ch{ch_num:02d}_{ch_name}.html"
        sub_links = ""
        for md in subs:
            raw = md.read_text(encoding="utf-8")
            t = title_from_md(raw, md.stem)
            sub_links += f'<span class="subsection">{html.escape(t)}</span> · '
        sub_links = sub_links.rstrip(" · ")
        chapter_links += f'<div class="subsection" style="margin:8px 0"><b>{ch_num:02d}</b> <a href="{rel(out, ch_file)}" style="font-weight:700;font-size:1.1rem">{html.escape(ch_name)}</a></div>'
    
    ch_count = len(groups)
    body = f'''<div class="stats"><div class="stat"><span class="num">{ch_count}章</span></div><div class="stat"><span class="num">{len(entities)}实体</span></div><div class="stat"><span class="num">{node_count}节点</span></div><div class="stat"><span class="num">{rel_count}关系</span></div></div>
<div class="section"><h2>📖 课程章节</h2>{chapter_links}</div>
<div class="section"><h2>🏷️ 知识实体</h2><p class="subsection">{entity_pills}</p><p class="subsection">{cat_html}</p><p><a href="{rel(out, "kg/entities/index.html")}">查看全部 {len(entities)} 个实体 →</a></p></div>
<div class="section"><h2>🔗 概念图谱</h2><p class="subsection">{node_count} 个节点 · {rel_count} 条关系，展示中心法则、复制、转录、翻译、调控与实验技术之间的关系。</p><p><a href="{rel(out, "kg/concepts/index.html")}">进入概念图谱 →</a></p></div>
<div class="section"><h2>🔍 站内搜索</h2><p class="subsection">全文搜索章节、实体、概念。</p><input id="q" class="searchbox" placeholder="搜索 DNA复制、PCR、转录因子..." onkeyup="if(event.key===&apos;Enter&apos;){{window.location=&apos;search/index.html?q=&apos;+encodeURIComponent(this.value)}}" style="max-width:400px"></div>'''
    write_page(out, SITE_TITLE, body, pages, "home", SITE_TITLE)


def clean_generated() -> None:
    for path in ["chapters", "search", "skills"]:
        p = ROOT / path
        if p.exists():
            shutil.rmtree(p)
    # Remove generated html from docs/chapters and docs/kg/entities, preserving md/json.
    for folder in [ROOT / "docs/chapters", ROOT / "docs/kg/entities", ROOT / "kg/entities"]:
        if folder.exists():
            for fp in folder.glob("*.html"):
                fp.unlink()
    # Remove generated concept/search indexes that are rebuilt.
    for fp in [ROOT / "kg/concepts/index.html", ROOT / "docs/index.html"]:
        if fp.exists():
            fp.unlink()


def mirror_docs() -> None:
    # Compatibility mirror for existing docs/* URLs. Only generated outputs are copied.
    for rel_dir in ["chapters", "kg/entities", "kg/concepts", "search", "skills"]:
        src = ROOT / rel_dir
        dst = ROOT / "docs" / rel_dir
        if dst.exists():
            shutil.rmtree(dst)
        if src.exists():
            shutil.copytree(src, dst)
    shutil.copy2(ROOT / "index.html", ROOT / "docs/index.html")


def main() -> None:
    clean_generated()
    pages: list[Page] = []
    entities = load_entities()
    chapters = build_chapters(pages)
    build_entities(pages, entities)
    build_concepts(pages, entities)
    build_skills(pages)
    build_home(pages, chapters, entities)
    build_search(pages)
    mirror_docs()
    print(f"Generated: {len(chapters)} chapters, {len(entities)} entities, {len(pages)} indexed pages")


if __name__ == "__main__":
    main()
