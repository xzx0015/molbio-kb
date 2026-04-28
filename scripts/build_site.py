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
:root{--bg:#f6f8fb;--card:#fff;--ink:#1f2937;--muted:#667085;--line:#e5e7eb;--primary:#355cde;--accent:#764ba2;--soft:#eef2ff}
*{box-sizing:border-box}body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans SC",Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.75}.wrap{max-width:1120px;margin:0 auto;padding:24px}.top{background:linear-gradient(135deg,#355cde,#764ba2);color:white}.top .wrap{padding-top:34px;padding-bottom:34px}.brand{font-size:28px;font-weight:800;margin:0}.subtitle{opacity:.9;margin:8px 0 0}.nav{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px}.nav a{color:white;text-decoration:none;border:1px solid rgba(255,255,255,.35);padding:7px 12px;border-radius:999px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px;box-shadow:0 8px 24px rgba(16,24,40,.04)}.card h2,.card h3{margin-top:0}.muted{color:var(--muted)}a{color:var(--primary);text-decoration:none}a:hover{text-decoration:underline}.article{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:30px;box-shadow:0 8px 24px rgba(16,24,40,.05)}.article h1{color:var(--primary);line-height:1.25}.article h2{border-bottom:1px solid var(--line);padding-bottom:6px;margin-top:30px}.article table{width:100%;border-collapse:collapse;margin:16px 0}.article th,.article td{border-bottom:1px solid var(--line);padding:8px;text-align:left}.article th{background:#f9fafb}.article code{background:#f3f4f6;padding:2px 5px;border-radius:5px}.article pre{background:#111827;color:#f9fafb;padding:14px;border-radius:12px;overflow:auto}.crumb{margin:16px 0;color:var(--muted)}.entity{display:inline-block;padding:1px 7px;border-radius:999px;background:var(--soft);font-weight:600}.tag{display:inline-block;font-size:12px;border-radius:999px;background:#eef2ff;color:#3730a3;padding:2px 8px;margin:2px}.list{padding-left:1.2em}.searchbox{width:100%;font-size:16px;border:1px solid var(--line);border-radius:14px;padding:12px 14px;background:white}.result{padding:14px 0;border-bottom:1px solid var(--line)}.footer{padding:28px;text-align:center;color:var(--muted)}.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:4px 10px;background:white;margin:3px}.warn{background:#fff7ed;border-color:#fed7aa}.ok{background:#ecfdf3;border-color:#bbf7d0}@media(max-width:640px){.wrap{padding:16px}.article{padding:20px}.brand{font-size:24px}}
""".strip()

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


def layout(title: str, body: str, out_path: Path, description: str = "") -> str:
    nav_items = [
        ("首页", "index.html"),
        ("课程章节", "chapters/index.html"),
        ("实体索引", "kg/entities/index.html"),
        ("概念图谱", "kg/concepts/index.html"),
        ("搜索", "search/index.html"),
        ("构建方法", "skills/index.html"),
    ]
    nav = "".join(f'<a href="{rel(out_path, href)}">{label}</a>' for label, href in nav_items)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | {SITE_TITLE}</title><meta name="description" content="{html.escape(description or SITE_TITLE)}">
<style>{CSS}</style></head><body>
<header class="top"><div class="wrap"><h1 class="brand">🧬 {SITE_TITLE}</h1><p class="subtitle">Molecular Biology KB · 统一生成的课程章节、实体索引、概念关系与搜索入口</p><nav class="nav">{nav}</nav></div></header>
<main class="wrap">{body}</main><footer class="footer">Built for molecular biology teaching · Generated by scripts/build_site.py</footer>
</body></html>'''


def write_page(path: Path, title: str, body: str, pages: list[Page], kind: str, text: str = "") -> None:
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(layout(title, body, path, clean_text(text)[:160]), encoding="utf-8")
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
    chapters = []
    for md in sorted((ROOT / "content/chapters").glob("*.md")):
        raw = md.read_text(encoding="utf-8")
        title = title_from_md(raw, md.stem)
        out = Path("chapters") / f"{md.stem}.html"
        chapters.append({"title": title, "stem": md.stem, "out": out.as_posix(), "text": clean_text(raw)})
        body = f'<div class="crumb"><a href="{rel(out, "index.html")}">首页</a> / <a href="{rel(out, "chapters/index.html")}">课程章节</a></div><article class="article">{md_to_html(raw)}</article>'
        write_page(out, title, body, pages, "chapter", raw)
    cards = "".join(f'<div class="card"><h3><a href="{rel(Path("chapters/index.html"), c["out"])}">{html.escape(c["title"])}</a></h3><p class="muted">{html.escape(c["text"][:130])}...</p></div>' for c in chapters)
    body = f'<h1>课程章节</h1><p class="muted">由 <code>content/chapters/*.md</code> 自动生成，共 {len(chapters)} 章。</p><div class="grid">{cards}</div>'
    write_page(Path("chapters/index.html"), "课程章节", body, pages, "index", "课程章节")
    return chapters


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
        sections.append(f'<div class="card"><h2>{html.escape(cat)} <span class="tag">{len(names)}</span></h2><ul class="list">{links}</ul></div>')
    body = f'<h1>实体索引</h1><p class="muted">由 <code>kg/entities/*.json</code> 自动生成，共 {len(entities)} 个结构化实体。</p><div class="grid">{"".join(sections)}</div>'
    write_page(idx, "实体索引", body, pages, "index", "实体索引")


def build_concepts(pages: list[Page], entities: dict[str, dict[str, Any]]) -> None:
    rel_file = ROOT / "kg/relations/concept-links.json"
    data = json.loads(rel_file.read_text(encoding="utf-8")) if rel_file.exists() else {"nodes": [], "links": []}
    out = Path("kg/concepts/index.html")
    nodes = data.get("nodes", [])
    links = data.get("links", [])
    node_html = "".join(f'<a class="pill" href="{entity_href(str(n.get("name") or n.get("id")), entities, out)}">{html.escape(str(n.get("name") or n.get("id")))}</a>' for n in nodes if isinstance(n, dict))
    link_rows = "".join(f'<tr><td>{html.escape(str(l.get("source")))}</td><td>{html.escape(str(l.get("type")))}</td><td>{html.escape(str(l.get("target")))}</td><td>{html.escape(str(l.get("description", "")))}</td></tr>' for l in links if isinstance(l, dict))
    body = f'''<h1>概念图谱</h1><p class="muted">由 <code>kg/relations/concept-links.json</code> 自动生成：{len(nodes)} 个节点，{len(links)} 条关系。</p>
<div class="card"><h2>核心节点</h2><p>{node_html}</p></div>
<article class="article"><h2>关系表</h2><table><thead><tr><th>源</th><th>关系</th><th>目标</th><th>说明</th></tr></thead><tbody>{link_rows}</tbody></table></article>'''
    write_page(out, "概念图谱", body, pages, "concept", json.dumps(data, ensure_ascii=False))


def build_skills(pages: list[Page]) -> None:
    skills = []
    for md in sorted((ROOT / "content/skills").glob("*.md")):
        raw = md.read_text(encoding="utf-8")
        title = title_from_md(raw, md.stem)
        out = Path("skills") / f"{md.stem}.html"
        body = f'<div class="crumb"><a href="{rel(out, "index.html")}">首页</a> / <a href="{rel(out, "skills/index.html")}">构建方法</a></div><article class="article">{md_to_html(raw)}</article>'
        write_page(out, title, body, pages, "skill", raw)
        skills.append((title, out, clean_text(raw)))
    idx = Path("skills/index.html")
    cards = "".join(f'<div class="card"><h3><a href="{rel(idx, p)}">{html.escape(t)}</a></h3><p class="muted">{html.escape(txt[:120])}...</p></div>' for t, p, txt in skills)
    write_page(idx, "构建方法", f'<h1>构建方法</h1><p class="muted">保留并发布 <code>content/skills/*.md</code>，共 {len(skills)} 个流程文档。</p><div class="grid">{cards}</div>', pages, "index", "构建方法")


def build_search(pages: list[Page]) -> None:
    idx_data = [{"title": p.title, "url": p.path.as_posix(), "kind": p.kind, "text": p.text[:2000]} for p in pages]
    (ROOT / "search").mkdir(exist_ok=True)
    (ROOT / "search/search-index.json").write_text(json.dumps(idx_data, ensure_ascii=False, indent=2), encoding="utf-8")
    out = Path("search/index.html")
    body = f'''<h1>站内搜索</h1><p class="muted">索引 {len(idx_data)} 个页面，离线可用。</p><input id="q" class="searchbox" placeholder="输入关键词，例如 DNA复制、PCR、转录因子..." autofocus><div id="results"></div>
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
    chapter_links = "".join(f'<li><a href="{rel(out, c["out"])}">{html.escape(c["title"])}</a></li>' for c in chapters[:8])
    entity_links = "".join(f'<a class="pill" href="{rel(out, Path("kg/entities") / slug_filename(n))}">{html.escape(n)}</a>' for n in sorted(entities)[:24])
    body = f'''<section class="grid">
<div class="card"><h2>课程章节</h2><p class="muted">统一从 Markdown 源生成，链接稳定。</p><ul>{chapter_links}</ul><p><a href="{rel(out, "chapters/index.html")}">查看全部章节 →</a></p></div>
<div class="card"><h2>实体索引</h2><p class="muted">从 JSON 实体数据生成，当前 {len(entities)} 个实体。</p><p>{entity_links}</p><p><a href="{rel(out, "kg/entities/index.html")}">查看实体索引 →</a></p></div>
<div class="card"><h2>概念图谱</h2><p class="muted">展示中心法则、复制、转录、翻译、调控和实验技术之间的关系。</p><p><a href="{rel(out, "kg/concepts/index.html")}">进入概念图谱 →</a></p></div>
<div class="card"><h2>站内搜索</h2><p class="muted">搜索章节、实体、构建方法文档。</p><p><a href="{rel(out, "search/index.html")}">打开搜索 →</a></p></div>
</section>'''
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
