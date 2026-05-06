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
:root{--p:#1d4ed8;--p2:#2563eb;--a:#7c3aed;--a2:#8b5cf6;--g:#059669;--o:#ea580c;--r:#dc2626;--bg:#f8fafc;--bg2:#f1f5f9;--card:#fff;--ink:#0f172a;--ink2:#334155;--mu:#64748b;--line:#e2e8f0;--line2:#cbd5e1;--soft:#eff6ff;--softa:#f5f3ff;--softg:#ecfdf5;--softo:#fff7ed;--rad:12px;--sh:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);--shm:0 4px 12px rgba(0,0,0,.08);}
*,::before,::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth;font-size:16px}
body{font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC',sans-serif;background:var(--bg);color:var(--ink);line-height:1.7;-webkit-font-smoothing:antialiased}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.top{background:linear-gradient(135deg,#1e3a8a 0%,#1d4ed8 30%,#7c3aed 70%,#a855f7 100%);color:#fff;position:relative;overflow:hidden}
.top::before{content:'';position:absolute;inset:0;background:url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Ccircle cx='30' cy='30' r='1.5'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");pointer-events:none}
.top .wrap{position:relative;padding-top:40px;padding-bottom:36px}
.brand{font-size:32px;font-weight:800;letter-spacing:-.5px;display:flex;align-items:center;gap:10px}
.brand .icon{font-size:36px}
.subtitle{opacity:.85;margin:6px 0 0;font-size:15px;font-weight:400;max-width:600px}
.nav{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}
.nav a{color:#fff;text-decoration:none;border:1px solid rgba(255,255,255,.25);padding:6px 14px;border-radius:999px;font-size:14px;transition:all .2s;backdrop-filter:blur(4px)}
.nav a:hover{background:rgba(255,255,255,.15);border-color:rgba(255,255,255,.5);text-decoration:none}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:22px 24px;box-shadow:var(--sh);transition:box-shadow .2s,transform .15s;position:relative;overflow:hidden}
.card:hover{box-shadow:var(--shm);transform:translateY(-2px)}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--p);opacity:0;transition:opacity .2s}
.card:hover::before{opacity:1}
.card h2,.card h3{margin:0 0 8px;font-size:17px;font-weight:700;color:var(--ink)}
.card .icon{font-size:24px;margin-bottom:10px;display:block}
.card.chapter::before{background:var(--p)}
.card.entity::before{background:var(--a)}
.card.concept::before{background:var(--g)}
.card.search::before{background:var(--o)}
.card.skill::before{background:var(--a2)}
.stats{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:16px;margin:24px 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:var(--rad);padding:20px;text-align:center;box-shadow:var(--sh);transition:box-shadow .2s,transform .15s}
.stat:hover{box-shadow:var(--shm);transform:translateY(-2px)}
.stat .num{font-size:36px;font-weight:800;background:linear-gradient(135deg,var(--p),var(--a));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.stat .label{color:var(--mu);font-size:13px;margin-top:4px;text-transform:uppercase;letter-spacing:.5px}
.muted{color:var(--mu)}
a{color:var(--p);text-decoration:none;transition:color .15s}
a:hover{color:var(--p2);text-decoration:none}
.article{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:32px 36px;box-shadow:var(--sh)}
.article h1{font-size:26px;font-weight:800;color:var(--ink);margin-bottom:8px;line-height:1.3}
.article h2{font-size:20px;font-weight:700;margin:32px 0 12px;padding-bottom:8px;border-bottom:2px solid var(--soft);color:var(--ink)}
.article h3{font-size:17px;font-weight:600;margin:20px 0 8px;color:var(--ink2)}
.article p{margin:10px 0;color:var(--ink2)}
.article ul,.article ol{margin:8px 0 8px 20px}
.article li{margin:4px 0;color:var(--ink2)}
.article table{width:100%;border-collapse:collapse;margin:20px 0;font-size:14px;border-radius:8px;overflow:hidden;border:1px solid var(--line)}
.article th{background:linear-gradient(135deg,#1e3a8a,#1d4ed8);color:#fff;padding:12px 14px;text-align:left;font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.5px}
.article td{padding:10px 14px;border-bottom:1px solid var(--line);background:#fff}
.article tr:nth-child(even) td{background:var(--bg2)}
.article tr:hover td{background:var(--soft)}
.article code{background:var(--soft);padding:2px 6px;border-radius:4px;font-size:.9em;color:var(--p);font-family:'SF Mono','Fira Code','Cascadia Code',monospace}
.article pre{background:#1e293b;color:#e2e8f0;padding:16px 20px;border-radius:10px;overflow:auto;font-size:13px;line-height:1.6;margin:16px 0}
.article blockquote{border-left:4px solid var(--p);margin:16px 0;padding:12px 20px;background:var(--soft);border-radius:0 8px 8px 0;color:var(--ink2)}
.crumb{margin:0 0 20px;font-size:14px;color:var(--mu)}
.crumb a{color:var(--mu)}
.crumb a:hover{color:var(--p)}
.entity{display:inline-block;padding:3px 10px;border-radius:999px;font-weight:600;font-size:13px;margin:2px;transition:all .15s}
.entity:hover{transform:scale(1.05)}
.entity.molecule,.entity.molecule{background:#dbeafe;color:#1e40af}
.entity.enzyme{background:#dcfce7;color:#166534}
.entity.protein{background:#fce7f3;color:#9d174d}
.entity.process{background:#fef3c7;color:#92400e}
.entity.technique{background:#e0e7ff;color:#3730a3}
.entity.complex{background:#f3e8ff;color:#6b21a8}
.entity.concept,.entity.core-theory{background:#ffedd5;color:#9a3412}
.entity.regulatory{background:#fce7f3;color:#9d174d}
.entity.mechanism{background:#d1fae5;color:#065f46}
.tag{display:inline-block;font-size:11px;border-radius:999px;padding:2px 8px;margin:2px;font-weight:500}
.tag.p{background:var(--soft);color:var(--p)}
.tag.a{background:var(--softa);color:var(--a)}
.tag.g{background:var(--softg);color:var(--g)}
.list{padding-left:1.2em}
.searchbox{width:100%;font-size:16px;border:2px solid var(--line);border-radius:12px;padding:14px 18px;background:var(--card);color:var(--ink);transition:border-color .2s;outline:none}
.searchbox:focus{border-color:var(--p);box-shadow:0 0 0 3px rgba(29,78,216,.1)}
.result{padding:16px 0;border-bottom:1px solid var(--line)}
.result:last-child{border-bottom:none}
.footer{margin-top:60px;padding:32px 0;text-align:center;color:var(--mu);font-size:13px;border-top:1px solid var(--line)}
.footer a{color:var(--p)}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:5px 12px;background:var(--card);margin:3px;font-size:14px;transition:all .15s;text-decoration:none;color:var(--ink2)}
.pill:hover{border-color:var(--p);color:var(--p);box-shadow:0 2px 8px rgba(29,78,216,.1);text-decoration:none}
.pill.active{background:var(--p);color:#fff;border-color:var(--p)}
.warn{background:#fff7ed;border:1px solid #fed7aa;border-radius:8px;padding:12px 16px;color:#9a3412}
.ok{background:#ecfdf3;border:1px solid #bbf7d0;border-radius:8px;padding:12px 16px;color:#065f46}
.info{background:var(--soft);border:1px solid #bfdbfe;border-radius:8px;padding:12px 16px;color:var(--p)}
.hero-stats{display:flex;gap:32px;margin-top:14px;flex-wrap:wrap}
.hero-stat{display:flex;align-items:baseline;gap:6px}
.hero-stat .hs-num{font-size:24px;font-weight:800;opacity:.95}
.hero-stat .hs-label{font-size:13px;opacity:.7}
.graph{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:28px;margin:24px 0;box-shadow:var(--sh);min-height:400px;position:relative;overflow:auto}
.graph svg{display:block;margin:0 auto;max-width:100%}
.section-divider{height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent);margin:40px 0}
.badge{display:inline-flex;align-items:center;gap:5px;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600}
.badge-blue{background:var(--soft);color:var(--p)}
.badge-purple{background:var(--softa);color:var(--a)}
.badge-green{background:var(--softg);color:var(--g)}
.badge-orange{background:var(--softo);color:var(--o)}
.entity-detail-header{display:flex;align-items:flex-start;gap:16px;flex-wrap:wrap;margin-bottom:24px}
.entity-detail-header h1{margin:0}
.entity-category-pill{display:inline-block;padding:4px 14px;border-radius:999px;font-size:13px;font-weight:600}
.ec-molecule{background:#dbeafe;color:#1e40af}
.ec-enzyme{background:#dcfce7;color:#166534}
.ec-protein{background:#fce7f3;color:#9d174d}
.ec-process{background:#fef3c7;color:#92400e}
.ec-technique{background:#e0e7ff;color:#3730a3}
.ec-complex{background:#f3e8ff;color:#6b21a8}
.ec-concept{background:#ffedd5;color:#9a3412}
.ec-regulatory{background:#fce7f3;color:#9d174d}
.ec-mechanism{background:#d1fae5;color:#065f46}
@media(max-width:768px){.wrap{padding:0 16px}.top .wrap{padding-top:28px;padding-bottom:24px}.brand{font-size:24px}.article{padding:20px;border-radius:10px}.grid{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}.hero-stats{gap:16px}.nav{gap:6px}.nav a{font-size:13px;padding:5px 10px}}
@media(prefers-color-scheme:dark){:root{--bg:#0f172a;--bg2:#1e293b;--card:#1e293b;--ink:#f1f5f9;--ink2:#cbd5e1;--mu:#94a3b8;--line:#334155;--line2:#475569;--soft:#1e3a5f;--softa:#2d1b69;--softg:#064e3b;--softo:#431407;--sh:0 1px 3px rgba(0,0,0,.3);--shm:0 4px 12px rgba(0,0,0,.4)}.article td{background:#1e293b}.article tr:nth-child(even) td{background:var(--bg2)}.article tr:hover td{background:var(--soft)}.searchbox{background:var(--bg)}.pill{background:var(--bg)}.entity.molecule,.entity.molecule{background:#1e3a5f;color:#93c5fd}.entity.enzyme{background:#064e3b;color:#6ee7b7}.entity.protein{background:#4a1942;color:#f9a8d4}.entity.process{background:#451a03;color:#fcd34d}.entity.technique{background:#1e3a5f;color:#a5b4fc}.entity.complex{background:#2d1b69;color:#c4b5fd}.article th{background:linear-gradient(135deg,#1e3a8a,#1d4ed8)}}
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


def layout(title: str, body: str, out_path: Path, description: str = "", hero_stats: str = "") -> str:
    nav_items = [
        ("🧬 首页", "index.html"),
        ("📖 课程章节", "chapters/index.html"),
        ("🏷️ 实体索引", "kg/entities/index.html"),
        ("🔗 概念图谱", "kg/concepts/index.html"),
        ("🔍 搜索", "search/index.html"),
    ]
    nav = "".join(f'<a href="{rel(out_path, href)}">{label}</a>' for label, href in nav_items)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | {SITE_TITLE}</title><meta name="description" content="{html.escape(description or SITE_TITLE)}">
<style>{CSS}</style></head><body>
<header class="top"><div class="wrap"><h1 class="brand"><span class="icon">🧬</span> {SITE_TITLE}</h1><p class="subtitle">Molecular Biology Knowledge Base · 课程章节 · 实体索引 · 概念图谱 · 搜索</p>{hero_stats}<nav class="nav">{nav}</nav></div></header>
<main class="wrap">{body}</main><footer class="footer"><p>Built for molecular biology teaching · Generated by <code>scripts/build_site.py</code></p><p style="margin-top:6px"><a href="https://github.com/xzx0015/molbio-kb">GitHub</a></p></footer>
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
        prefix = md.stem[:2]  # "01", "02", etc.
        groups[prefix].append(md)
    
    # Build individual pages for each md file
    all_chapters = []
    for md in md_files:
        raw = md.read_text(encoding="utf-8")
        title = title_from_md(raw, md.stem)
        out = Path("chapters") / f"{md.stem}.html"
        all_chapters.append({"title": title, "stem": md.stem, "out": out.as_posix(), "text": clean_text(raw), "prefix": md.stem[:2]})
        body = f'<div class="crumb"><a href="{rel(out, "index.html")}">首页</a> / <a href="{rel(out, "chapters/index.html")}">课程章节</a></div><div class="section-divider"></div><article class="article">{md_to_html(raw)}</article>'
        write_page(out, title, body, pages, "chapter", raw)
    
    # Build chapter index: one card per chapter number, with sub-sections listed
    idx = Path("chapters/index.html")
    chapter_cards = []
    for prefix in sorted(groups):
        subs = groups[prefix]
        # Use the first sub as the main chapter title base
        main_title = None
        sub_list_parts = []
        for md in subs:
            raw = md.read_text(encoding="utf-8")
            t = title_from_md(raw, md.stem)
            if main_title is None:
                main_title = t
            out = Path("chapters") / f"{md.stem}.html"
            sub_list_parts.append(f'<li><a href="{rel(idx, out)}">{html.escape(t)}</a></li>')
        ch_num = int(prefix)
        ch_names = ["", "绪论", "分子基础与复制", "信息传递与转录", "翻译与表达调控", "原核与基因组维持", "技术与真核调控", "实验技术", "组学前沿"]
        ch_name = ch_names[ch_num] if ch_num < len(ch_names) else (main_title or f"第{ch_num}章")
        chapter_cards.append(f'''<div class="card chapter"><span class="icon">📄</span><h2>第{ch_num}章：{html.escape(ch_name)}</h2><ul class="list" style="font-size:15px">{"".join(sub_list_parts)}</ul></div>''')
    
    body = f'<h1>📖 课程章节</h1><p class="muted">由 <code>content/chapters/*.md</code> 自动生成，共 <b>{len(groups)}</b> 章。</p><div class="section-divider"></div><div class="grid">{"".join(chapter_cards)}</div>'
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
    
    chapter_links = "".join(f'<li><a href="{rel(out, c["out"])}">{html.escape(c["title"])}</a></li>' for c in chapters[:8])
    entity_pills = "".join(f'<a class="pill" href="{rel(out, Path("kg/entities") / slug_filename(n))}">{html.escape(n)}</a>' for n in sorted(entities)[:24])
    
    # Count unique chapters (by prefix)
    ch_prefixes = set(md.stem[:2] for md in (ROOT / "content/chapters").glob("*.md"))
    ch_count = len(ch_prefixes)
    hero_stats = f'''<div class="hero-stats"><div class="hero-stat"><span class="hs-num">{ch_count}</span><span class="hs-label">课程章节</span></div><div class="hero-stat"><span class="hs-num">{len(entities)}</span><span class="hs-label">知识实体</span></div><div class="hero-stat"><span class="hs-num">{node_count}</span><span class="hs-label">概念节点</span></div><div class="hero-stat"><span class="hs-num">{rel_count}</span><span class="hs-label">语义关系</span></div></div>'''
    body = f'''<div class="stats">
<div class="stat"><div class="num">{ch_count}</div><div class="label">课程章节</div></div>
<div class="stat"><div class="num">{len(entities)}</div><div class="label">知识实体</div></div>
<div class="stat"><div class="num">{node_count}</div><div class="label">概念节点</div></div>
<div class="stat"><div class="num">{rel_count}</div><div class="label">语义关系</div></div>
</div>
<section class="grid">
<div class="card chapter"><span class="icon">📖</span><h2>课程章节</h2><p class="muted">统一从 Markdown 源生成，共 {ch_count} 章。</p><ul>{chapter_links}</ul><p><a href="{rel(out, "chapters/index.html")}">查看全部章节 →</a></p></div>
<div class="card entity"><span class="icon">🏷️</span><h2>实体索引</h2><p class="muted">从 JSON 实体数据生成，{len(entities)} 个实体覆盖 {len(cats)} 个类别。</p><p style="margin:8px 0">{cat_html}</p><p>{entity_pills}</p><p><a href="{rel(out, "kg/entities/index.html")}">查看实体索引 →</a></p></div>
<div class="card concept"><span class="icon">🔗</span><h2>概念图谱</h2><p class="muted">{node_count} 个节点 · {rel_count} 条关系，展示中心法则、复制、转录、翻译、调控与实验技术之间的关系。</p><p><a href="{rel(out, "kg/concepts/index.html")}">进入概念图谱 →</a></p></div>
<div class="card search"><span class="icon">🔍</span><h2>站内搜索</h2><p class="muted">搜索章节、实体、概念，离线可用。</p><p><a href="{rel(out, "search/index.html")}">打开搜索 →</a></p></div>
</section>'''
    write_page(out, SITE_TITLE, body, pages, "home", SITE_TITLE, hero_stats=hero_stats)


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
