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
/* ===== molbio-kb — Mintlify-inspired design ===== */
:root{--brand:#18E299;--brand-deep:#0fa76e;--brand-light:#d4fae8;--ink:#0d0d0d;--ink2:#333;--mu:#666;--mu2:#888;--line:rgba(0,0,0,0.05);--line2:rgba(0,0,0,0.08);--bg:#fff;--warm:#fafafa;--rad:16px;--rad-lg:24px;--rad-pill:9999px}
html{scroll-behavior:smooth;font-size:18px}
*{box-sizing:border-box}
body{font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,'Noto Sans SC',sans-serif;line-height:1.7;max-width:1200px;margin:0 auto;padding:0;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}

/* ===== Header ===== */
.top{position:sticky;top:0;z-index:100;background:rgba(255,255,255,.85);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line);padding:0}
.top .wrap{max-width:1200px;margin:0 auto;padding:14px 32px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{font-size:1.1rem;font-weight:600;color:var(--ink);display:flex;align-items:center;gap:8px;letter-spacing:-.3px}
.brand .icon{font-size:1.3rem}
.nav{display:flex;gap:4px;align-items:center}
.nav a{color:var(--ink);text-decoration:none;padding:6px 14px;border-radius:8px;font-size:.85rem;font-weight:500;transition:all .15s;border:1px solid transparent}
.nav a:hover{color:var(--brand);background:transparent;text-decoration:none}
.settings-toggle{background:transparent;border:1px solid var(--line);border-radius:8px;padding:6px 10px;font-size:.85rem;cursor:pointer;transition:all .15s;color:var(--mu);line-height:1}
.settings-toggle:hover{background:var(--warm);border-color:var(--line2);color:var(--ink)}

/* ===== Hero section on home ===== */
.hero{padding:80px 32px 64px;text-align:center;background:linear-gradient(180deg,rgba(24,226,153,.06) 0%,rgba(255,255,255,0) 70%)}
.hero h1{font-size:2.8rem;font-weight:600;color:var(--ink);margin:0 0 12px;letter-spacing:-1.2px;line-height:1.15}
.hero p{font-size:1.1rem;color:var(--mu);max-width:600px;margin:0 auto 28px;line-height:1.6}

/* ===== Home sections ===== */
.section{margin:0;padding:48px 32px}
.section:nth-child(even){background:var(--warm)}
.section h2{font-size:1.1rem;font-weight:600;color:var(--ink);margin:0 0 16px;letter-spacing:-.3px;display:flex;align-items:center;gap:8px}
.section h2::after{content:'';flex:1;height:1px;background:var(--line)}
.section .subsection{margin:6px 0;font-size:1rem;color:var(--ink2);line-height:2}
.section .subsection a{color:var(--ink);font-weight:500}
.section .subsection a:hover{color:var(--brand)}

/* ===== Chapter nav ===== */
.chapter-nav{display:flex;justify-content:center;align-items:center;gap:12px;padding:12px 32px;margin:0}
.chapter-nav a{padding:8px 18px;background:var(--bg);color:var(--ink2);text-decoration:none;border:1px solid var(--line);border-radius:var(--rad-pill);font-size:.85rem;font-weight:500;transition:all .15s}
.chapter-nav a:hover{background:var(--warm);border-color:var(--line2);color:var(--ink)}
.chapter-nav .nav-home{background:var(--ink);color:#fff;border-color:var(--ink)}
.chapter-nav .nav-home:hover{background:#1a1a1a;color:#fff}

/* ===== Purple Numbers ===== */
.pn{font-size:.7rem;color:var(--brand-deep);margin-right:8px;cursor:pointer;text-decoration:none;font-weight:600;opacity:.7;font-family:'Geist Mono',ui-monospace,monospace}
.pn:hover{opacity:1}

/* ===== Entity highlighting ===== */
.entity{font-weight:500;cursor:pointer;transition:all .1s;padding:1px 0}
.entity.molecule{color:#2563eb;text-decoration:underline;text-decoration-color:#2563eb50;text-underline-offset:4px}
.entity.enzyme{color:var(--brand-deep);text-decoration:underline;text-decoration-color:var(--brand-deep);text-underline-offset:4px;text-decoration-thickness:1.5px}
.entity.protein{color:#db2777;text-decoration:underline;text-decoration-color:#db277750;text-underline-offset:4px}
.entity.process{color:#ea580c;text-decoration:underline wavy;text-decoration-color:#ea580c60;text-underline-offset:4px}
.entity.technique{color:#6366f1;text-decoration:underline dashed;text-decoration-color:#6366f160;text-underline-offset:4px}
.entity.complex{color:#7c3aed;text-decoration:underline double;text-decoration-color:#7c3aed60;text-underline-offset:4px}
.entity.concept,.entity.core-theory{color:#b45309;font-weight:600;background:linear-gradient(transparent 60%,#fed7aa 60%)}
.entity.regulatory{color:#db2777;text-decoration:underline;text-decoration-color:#db277750;text-underline-offset:4px}
.entity.mechanism{color:var(--brand-deep);text-decoration:underline wavy;text-decoration-color:var(--brand-deep);text-underline-offset:4px}
.hide-entities .entity{color:inherit!important;text-decoration:none!important;font-weight:inherit!important;background:none!important;cursor:text}

/* ===== Article / content ===== */
.article{max-width:800px;margin:0 auto;padding:32px 0}
.article h2{font-size:1.3rem;font-weight:600;margin:48px 0 16px;color:var(--ink);letter-spacing:-.3px}
.article h3{font-size:1.1rem;font-weight:600;margin:32px 0 12px;color:var(--ink2)}
.article p{margin:1em 0;font-size:1rem;line-height:1.8}
.article ul,.article ol{margin:12px 0 12px 1.5em;font-size:1rem;line-height:1.9}
.article li{margin:4px 0}
.article table{width:100%;border-collapse:collapse;margin:32px 0;font-size:.85rem;border:1px solid var(--line);border-radius:var(--rad);overflow:hidden}
.article th{background:var(--warm);padding:14px 18px;text-align:left;font-weight:600;font-size:.8rem;border-bottom:1px solid var(--line2);color:var(--ink2)}
.article td{padding:14px 18px;border-bottom:1px solid var(--line);background:var(--bg)}
.article tr:nth-child(even) td{background:var(--warm)}
.article code{background:var(--brand-light);padding:2px 8px;border-radius:4px;font-size:.85em;font-family:'Geist Mono',ui-monospace,monospace;color:var(--brand-deep)}
.article pre{background:var(--ink);color:#e8e8e8;padding:20px 24px;border-radius:var(--rad);overflow:auto;font-size:.8rem;line-height:1.7;margin:24px 0}
.article blockquote{border-left:3px solid var(--brand);margin:24px 0;padding:8px 20px;color:var(--ink2);background:var(--warm);border-radius:0 8px 8px 0}
.article hr{border:none;height:1px;background:var(--line);margin:40px 0}

/* ===== Chapter title ===== */
.chapter-title{font-size:1.6rem;font-weight:600;color:var(--ink);margin:0;padding:40px 32px 20px;letter-spacing:-.5px;display:flex;align-items:center;gap:12px;max-width:800px;margin-left:auto;margin-right:auto}
.chapter-title .ch-num{background:var(--brand);color:var(--ink);padding:4px 16px;border-radius:var(--rad-pill);font-size:.85rem;font-weight:600}

/* ===== Entity detail ===== */
.entity-detail-header{display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:28px;max-width:800px;margin-left:auto;margin-right:auto;padding:0 32px}
.entity-detail-header h1{margin:0;font-size:1.5rem;font-weight:600;letter-spacing:-.4px}
.entity-category-pill{display:inline-block;padding:5px 16px;border-radius:var(--rad-pill);font-size:.8rem;font-weight:500}
.ec-molecule{background:#dbeafe;color:#2563eb}
.ec-enzyme{background:var(--brand-light);color:var(--brand-deep)}
.ec-protein{background:#fce7f3;color:#db2777}
.ec-process{background:#ffedd5;color:#ea580c}
.ec-technique{background:#e0e7ff;color:#6366f1}
.ec-complex{background:#ede9fe;color:#7c3aed}
.ec-concept{background:#fef3c7;color:#b45309}
.ec-regulatory{background:#fce7f3;color:#db2777}
.ec-mechanism{background:var(--brand-light);color:var(--brand-deep)}

/* ===== Grid / Cards ===== */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px;padding:0 32px;max-width:1200px;margin:0 auto}
.card{background:var(--bg);border:1px solid var(--line);border-radius:var(--rad);padding:28px;transition:box-shadow .2s,border-color .2s}
.card:hover{border-color:var(--line2);box-shadow:0 2px 16px rgba(0,0,0,.03)}
.card h2,.card h3{margin:0 0 10px;font-size:1.05rem;font-weight:600;color:var(--ink);letter-spacing:-.2px}
.card .icon{font-size:1.2rem;margin-bottom:10px;display:block}

/* ===== Concept graph ===== */
.graph{background:var(--bg);border:1px solid var(--line);border-radius:var(--rad);padding:28px;margin:28px 32px;overflow:auto}
.graph svg{display:block;margin:0 auto;max-width:100%}

/* ===== Pills / Badges ===== */
.pill{display:inline-block;border:1px solid var(--line);border-radius:var(--rad-pill);padding:6px 16px;background:var(--bg);margin:4px;font-size:.85rem;transition:all .15s;color:var(--ink2)}
.pill:hover{border-color:var(--brand);color:var(--brand-deep);text-decoration:none;background:var(--brand-light)}
.badge{display:inline-flex;align-items:center;gap:4px;padding:4px 12px;border-radius:var(--rad-pill);font-size:.75rem;font-weight:500}
.badge-blue{background:#eff6ff;color:#2563eb}
.searchbox{width:100%;max-width:400px;font-size:.9rem;border:1px solid var(--line);border-radius:var(--rad-pill);padding:10px 18px;background:var(--bg);color:var(--ink);outline:none;transition:all .15s}
.searchbox:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(24,226,153,.12)}
.result{padding:18px 0;border-bottom:1px solid var(--line)}
.result:last-child{border-bottom:none}

/* ===== Utilities ===== */
.crumb{margin:0 0 20px;font-size:.85rem;color:var(--mu);padding:0 32px}
.muted{color:var(--mu)}
.section-divider{height:1px;background:var(--line);margin:0}
.tag{display:inline-block;font-size:.7rem;border-radius:4px;padding:2px 8px;margin:2px;font-weight:500}
.tag.p{background:#eff6ff;color:#2563eb}
.tag.a{background:#f5f3ff;color:var(--a,--7c3aed)}
.list{padding-left:1.4em;font-size:.95rem;line-height:2.2}
.list li{margin:3px 0}
.footer{margin-top:64px;padding:32px;text-align:center;color:var(--mu);font-size:.8rem;border-top:1px solid var(--line)}
.footer a{color:var(--ink)}

/* ===== Dark mode ===== */
html.dark body{background:#0d0d0d;color:#ededed}
html.dark .top{background:rgba(13,13,13,.85);border-color:rgba(255,255,255,.08)}
html.dark .section:nth-child(even){background:#141414}
html.dark .card{background:#141414;border-color:rgba(255,255,255,.08)}
html.dark .card:hover{border-color:rgba(255,255,255,.12)}
html.dark .article th{background:#1a1a1a;border-color:rgba(255,255,255,.08)}
html.dark .article td{background:#0d0d0d;border-color:rgba(255,255,255,.05)}
html.dark .article tr:nth-child(even) td{background:#111}
html.dark .searchbox{background:#141414;border-color:rgba(255,255,255,.08);color:#ededed}
html.dark .pill{background:#141414;border-color:rgba(255,255,255,.08)}
html.dark .chapter-nav a{background:#141414;border-color:rgba(255,255,255,.08);color:#a0a0a0}
html.dark .chapter-nav a:hover{background:#1a1a1a;color:#ededed}
html.dark .graph{background:#141414;border-color:rgba(255,255,255,.08)}
html.dark .footer{border-color:rgba(255,255,255,.08)}
html.dark .hero{background:linear-gradient(180deg,rgba(24,226,153,.04) 0%,rgba(13,13,13,0) 70%)}
html.dark .brand{color:#ededed}
html.dark .nav a{color:#a0a0a0}
html.dark .nav a:hover{color:var(--brand)}
html.dark .article h2,.dark .article h3,.dark .section h2{color:#ededed}

/* ===== Responsive ===== */
@media(max-width:768px){
  html{font-size:16px}
  .hero{padding:40px 20px 32px}
  .hero h1{font-size:2rem;letter-spacing:-.8px}
  .section{padding:32px 20px}
  .grid{grid-template-columns:1fr;padding:0 20px}
  .chapter-title{padding:24px 20px 16px;font-size:1.3rem}
  .article{max-width:100%}
}
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
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@400;500;600;700&display=swap" rel="stylesheet">
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
    
    body = f'<h1>📖 课程章节</h1><div class="section-divider"></div><div class="grid">{"".join(chapter_cards)}</div>'
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
    body = f'<h1>🏷️ 实体索引</h1><div class="section-divider"></div><div class="grid">{"".join(sections)}</div>'
    write_page(idx, "实体索引", body, pages, "index", "实体索引")


def build_concepts(pages: list[Page], entities: dict[str, dict[str, Any]]) -> None:
    rel_file = ROOT / "kg/relations/concept-links.json"
    data = json.loads(rel_file.read_text(encoding="utf-8")) if rel_file.exists() else {"nodes": [], "links": []}
    out = Path("kg/concepts/index.html")
    nodes = data.get("nodes", [])
    links = data.get("links", [])
    relation_types = data.get("relationTypes", {})
    
    cat_colors = {
        "核心理论": "#1d4ed8", "分子": "#2563eb", "蛋白质": "#db2777", "酶": "#059669",
        "过程": "#ea580c", "技术": "#6366f1", "复合物": "#7c3aed", "调控": "#db2777",
        "机制": "#0891b2", "基因组": "#7c3aed", "概念": "#64748b"
    }
    
    # Build node map for hrefs
    node_links = {}
    for n in nodes:
        if isinstance(n, dict):
            name = n.get("name", n.get("id", ""))
            node_links[name] = entity_href(str(name), entities, out)
    
    # JSON data embedded for D3
    graph_json = json.dumps(data, ensure_ascii=False)
    n_cats = len(set(n.get("category","") for n in nodes if isinstance(n, dict)))
    hrefs_dict = {n.get("name", n.get("id","")): entity_href(str(n.get("name", n.get("id",""))), entities, out) for n in nodes if isinstance(n, dict)}
    hrefs_json = json.dumps(hrefs_dict, ensure_ascii=False)
    
    # Render graph.js from template
    template = (ROOT / "kg/concepts/graph.template.js").read_text(encoding="utf-8")
    graph_js = template.replace("{GRAPH_DATA}", graph_json).replace("{HREFS_JSON}", hrefs_json)
    (ROOT / "kg/concepts/graph.js").write_text(graph_js, encoding="utf-8")
    (ROOT / "docs/kg/concepts").mkdir(parents=True, exist_ok=True)
    (ROOT / "docs/kg/concepts/graph.js").write_text(graph_js, encoding="utf-8")
    
    body = f"""<h1>🌐 概念图谱</h1>
<div class="section-divider"></div>
<div id="graph-container" style="width:100%;height:80vh;min-height:600px;background:var(--warm);border-radius:var(--rad);overflow:hidden;position:relative">
  <div id="tooltip" style="position:absolute;padding:6px 14px;background:rgba(0,0,0,.82);color:#fff;border-radius:8px;font-size:.85rem;pointer-events:none;display:none;z-index:10;white-space:nowrap"></div>
  <div style="position:absolute;bottom:16px;right:16px;display:flex;gap:8px;z-index:5">
    <button onclick="zoomIn()" style="background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 12px;cursor:pointer;font-size:1.1rem">+</button>
    <button onclick="zoomOut()" style="background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:6px 12px;cursor:pointer;font-size:1.1rem">−</button>
  </div>
</div>
<div class="section-divider"></div>
<div class="card" style="margin:16px 32px"><p style="font-size:.9rem;color:var(--mu)">💡 悬停高亮关联 | 双击跳转实体 | 拖拽节点 | 滚轮缩放</p></div>
<div class="card" style="margin:8px 32px">
  <p style="font-weight:600;margin-bottom:8px">🔗 关系图例</p>
  <p style="display:flex;gap:16px;flex-wrap:wrap;font-size:.85rem">
    <span><span style="display:inline-block;width:18px;height:3px;background:#667eea;vertical-align:middle;margin-right:4px;border-radius:2px"></span>是一种</span>
    <span><span style="display:inline-block;width:18px;height:3px;background:#764ba2;vertical-align:middle;margin-right:4px;border-radius:2px"></span>组成</span>
    <span><span style="display:inline-block;width:18px;height:3px;background:#e74c3c;vertical-align:middle;margin-right:4px;border-radius:2px"></span>调控</span>
    <span><span style="display:inline-block;width:18px;height:3px;background:#27ae60;vertical-align:middle;margin-right:4px;border-radius:2px"></span>催化</span>
    <span><span style="display:inline-block;width:18px;height:3px;background:#f39c12;vertical-align:middle;margin-right:4px;border-radius:2px"></span>参与</span>
    <span><span style="display:inline-block;width:18px;height:3px;background:#95a5a6;vertical-align:middle;margin-right:4px;border-radius:2px"></span>相关</span>
  </p>
</div>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script src="graph.js"></script>
<div class="section-divider"></div>
<h2 style="padding:0 32px">📊 统计</h2>
<div class="card" style="margin:16px 32px"><p><b>{len(nodes)}</b> 个节点 · <b>{len(links)}</b> 条关系 · <b>{n_cats}</b> 个类别</p></div>"""
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
    body = f'''<div class="hero"><h1>分子生物学知识库</h1><p>课程章节 · 知识实体 · 概念图谱 · 全文搜索 — 为分子生物学教学打造的开放知识体系</p></div>
<div class="section"><h2>📖 课程章节</h2>{chapter_links}</div>
<div class="section"><h2>🏷️ 知识实体</h2><p class="subsection">{entity_pills}</p><p class="subsection">{cat_html}</p><p><a href="{rel(out, "kg/entities/index.html")}">查看全部实体 →</a></p></div>
<div class="section"><h2>🔗 概念图谱</h2><p class="subsection">展示中心法则、复制、转录、翻译、调控与实验技术之间的关系。</p><p><a href="{rel(out, "kg/concepts/index.html")}">进入概念图谱 →</a></p></div>
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
