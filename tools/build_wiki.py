#!/usr/bin/env python3
"""把 wiki/ 和 raw/ 裡的 Markdown 轉成可以在瀏覽器看的 HTML（不需要安裝任何套件）。
用法：python3 tools/build_wiki.py
- 支援：標題、清單、表格、引用、粗體、行內程式碼、[文字](連結)
- Obsidian 風格雙向連結 [[concepts/forward-process|前向過程]] → 轉成 HTML 連結
- 來源標記 [S1]～[S7] → 自動連到 wiki/sources/ 的摘要頁
"""
import html, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PAGE = {}  # "S1" -> "sources/s1-ddpm"
for p in glob.glob(os.path.join(ROOT, "wiki/sources/*.md")):
    name = os.path.basename(p)[:-3]
    SRC_PAGE["S" + name[1]] = "sources/" + name


def split_frontmatter(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            fm = {}
            for line in text[4:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    fm[k.strip()] = v.strip()
            return fm, text[end + 5:]
    return {}, text


def rel(from_dir, target):
    return os.path.relpath(target, from_dir).replace(os.sep, "/")


def inline(s, page_dir):
    s = html.escape(s, quote=False)
    codes = []
    def keep(m):
        codes.append(m.group(1)); return f"\x00{len(codes)-1}\x00"
    s = re.sub(r"`([^`]+)`", keep, s)
    # [[path|label]] / [[path]]
    def wl(m):
        path, _, label = m.group(1).partition("|")
        target = os.path.join(ROOT, "wiki", path + ".html")
        return f'<a class="wikilink" href="{rel(page_dir, target)}">{label or path}</a>'
    s = re.sub(r"\[\[([^\]]+)\]\]", wl, s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" style="max-width:100%">', s)
    # [text](url) ；本地 .md 連結改成 .html
    def ln(m):
        text, url = m.group(1), m.group(2)
        if not re.match(r"https?://", url) and url.endswith(".md"):
            url = url[:-3] + ".html"
        return f'<a href="{url}">{text}</a>'
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", ln, s)
    # [S1] 來源
    def cite(m):
        sid = m.group(1)
        if sid in SRC_PAGE:
            target = os.path.join(ROOT, "wiki", SRC_PAGE[sid] + ".html")
            return f'<a class="cite" href="{rel(page_dir, target)}">[{sid}]</a>'
        return f"[{sid}]"
    s = re.sub(r"\[(S\d+)\]", cite, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)
    return s


def md_to_html(body, page_dir):
    out, lines, i = [], body.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if line.startswith("```"):
            buf = []; i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i]); i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>"); continue
        m = re.match(r"^(#{1,4})\s+(.*)", line)
        if m:
            n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2), page_dir)}</h{n}>"); i += 1; continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c, page_dir)}</th>" for c in rows[0]) + "</tr></thead><tbody>"
            for r in rows[1:]:
                t += "<tr>" + "".join(f"<td>{inline(c, page_dir)}</td>" for c in r) + "</tr>"
            out.append(t + "</tbody></table>"); continue
        if line.startswith(">"):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i].lstrip("> ")); i += 1
            out.append("<blockquote>" + "<br>".join(inline(b, page_dir) for b in buf) + "</blockquote>"); continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.", line)); tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i])); i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x, page_dir)}</li>" for x in items) + f"</{tag}>"); continue
        buf = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|\s*([-*]|\d+\.)\s)", lines[i]):
            buf.append(lines[i]); i += 1
        out.append("<p>" + inline(" ".join(buf), page_dir) + "</p>")
    return "\n".join(out)


TEMPLATE = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
body{{font-family:system-ui,-apple-system,"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;max-width:820px;margin:0 auto;padding:24px 18px 60px;line-height:1.75;color:#1f2933;background:#fbfaf7}}
header{{font-size:14px;margin-bottom:18px;color:#52606d}} header a{{margin-right:12px}}
h1{{font-size:1.7em;border-bottom:3px solid #f2c94c;padding-bottom:6px}} h2{{margin-top:1.6em;color:#334e68}}
a{{color:#2563eb;text-decoration:none}} a:hover{{text-decoration:underline}}
a.wikilink{{background:#eef4ff;padding:0 4px;border-radius:4px}} a.cite{{font-size:.8em;color:#b45309;vertical-align:super}}
table{{border-collapse:collapse;width:100%;margin:12px 0;font-size:.95em;display:block;overflow-x:auto}} th,td{{border:1px solid #d9e2ec;padding:6px 10px;text-align:left}} th{{background:#f0f4f8}}
blockquote{{border-left:4px solid #f2c94c;margin:12px 0;padding:6px 14px;background:#fffbea;color:#52606d}}
code{{background:#f0f4f8;padding:1px 5px;border-radius:4px}} pre{{background:#f0f4f8;padding:12px;overflow-x:auto;border-radius:8px;font-size:.88em}} pre code{{padding:0}} .meta{{font-size:13px;color:#829ab1}}
</style></head><body>
<header><a href="{home}">🏠 Wiki 索引</a><a href="{site}">專案首頁</a><a href="{slides}">📽 教學簡報</a></header>
<main>
{body}
</main>
<p class="meta">原始 Markdown：<a href="{md_url}">{md_name}</a>｜更新：{updated}</p>
</body></html>
"""

REPO = "https://github.com/b123090032-lab/llm-wiki-diffusion/blob/main/"


def build(md_path):
    text = open(md_path, encoding="utf-8").read()
    fm, body = split_frontmatter(text)
    page_dir = os.path.dirname(md_path)
    m = re.search(r"^#\s+(.*)", body, re.M)
    title = fm.get("title") or (m.group(1) if m else os.path.basename(md_path))
    relpath = os.path.relpath(md_path, ROOT).replace(os.sep, "/")
    out = TEMPLATE.format(
        title=html.escape(title), body=md_to_html(body, page_dir),
        home=rel(page_dir, os.path.join(ROOT, "wiki/index.html")),
        site=rel(page_dir, os.path.join(ROOT, "index.html")),
        slides=rel(page_dir, os.path.join(ROOT, "slides/index.html")),
        md_url=REPO + relpath, md_name=relpath, updated=fm.get("updated", fm.get("retrieved", "")),
    )
    open(md_path[:-3] + ".html", "w", encoding="utf-8").write(out)
    return md_path[:-3] + ".html"


if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(ROOT, "wiki/**/*.md"), recursive=True))
    for d in ("raw", "docs", "log", "log/check-outputs", "outline"):
        files += sorted(glob.glob(os.path.join(ROOT, d, "*.md")))
    files += [os.path.join(ROOT, "AGENTS.md")]
    for f in files:
        build(f)
    print(f"built {len(files)} pages")
