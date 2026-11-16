#!/usr/bin/env python3
"""LLM Wiki + 教學簡報 的自動檢查（不用安裝套件）。
用法：
  python3 tools/check.py wiki     # 檢查 wiki：連結、孤兒頁、來源標記、frontmatter
  python3 tools/check.py pages    # 【提前的檢查】產生簡報前，先檢查大綱和逐頁內容
  python3 tools/check.py slides   # 檢查簡報：每頁都有 wiki 出處、每個重點都找得到原文
  python3 tools/check.py render   # 用 headless Chrome 實際渲染，檢查桌機／手機每頁有沒有溢出
  python3 tools/check.py links    # 檢查所有 HTML 裡的本地連結都存在
  python3 tools/check.py all      # 全部
有任何錯誤就 exit 1，並印出要退回哪個關卡。
"""
import glob, html, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.join(ROOT, "wiki")
errors, warns = [], []


def err(node, msg):
    errors.append(f"[退回：{node}] {msg}")


def read(p):
    return open(p, encoding="utf-8").read()


def wiki_pages():
    return {os.path.relpath(p, W)[:-3].replace(os.sep, "/"): p for p in glob.glob(os.path.join(W, "**/*.md"), recursive=True)}


def norm(s):
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    s = s.replace("**", "").replace("`", "")
    return re.sub(r"\s+", "", s)


# ---------------- wiki ----------------
def check_wiki():
    pages = wiki_pages()
    raw_ids = {"S" + os.path.basename(p)[:2].lstrip("0"): p for p in glob.glob(os.path.join(ROOT, "raw/*.md"))}
    inbound = {k: 0 for k in pages}
    for name, path in pages.items():
        text = read(path)
        text_nocode = re.sub(r"`[^`]*`", "", text)  # 行內程式碼裡的 [[...]] 是範例，不算連結
        for link in re.findall(r"\[\[([^\]|]+)", text_nocode):
            if link not in pages:
                err("整理 Wiki", f"{name}.md 連到不存在的頁面 [[{link}]]")
            elif link != name:
                inbound[link] += 1
        for line in text.splitlines():
            if line.startswith("|") and re.search(r"\[\[[^\]]*\|[^\]]*\]\]", line):
                err("整理 Wiki", f"{name}.md 的表格裡用了 [[頁面|文字]]，直線會把表格切壞：{line[:40]}")
        cites = set(re.findall(r"\[(S\d+)\]", text))
        for c in cites:
            if c not in raw_ids:
                err("取得資料", f"{name}.md 引用了 [{c}]，但 raw/ 裡沒有這個來源")
        m = re.search(r"^sources:\s*\[(.*?)\]", text, re.M)
        declared = set(x.strip() for x in m.group(1).split(",")) if m else set()
        kind = re.search(r"^type:\s*(\w+)", text, re.M)
        kind = kind.group(1) if kind else ""
        if kind in ("concept", "comparison", "overview", "glossary"):
            if not cites:
                err("整理 Wiki", f"{name}.md 沒有任何來源標記 [Sx]")
            if declared != cites:
                err("整理 Wiki", f"{name}.md frontmatter sources={sorted(declared)} 跟內文實際引用 {sorted(cites)} 不一致")
            # 每個條列句子都要有來源（表格列、相關頁面區除外）
            body = text.split("## 相關頁面")[0]
            for line in body.splitlines():
                s = line.strip()
                if re.match(r"^([-*]|\d+\.)\s", s) and "[[" not in s and not re.search(r"\[S\d+\]", s) and len(s) > 25:
                    warns.append(f"{name}.md 這行沒有來源：{s[:40]}…")
    index_text = read(pages["index"])
    for name in pages:
        if name in ("index",):
            continue
        if f"[[{name}" not in index_text:
            err("整理 Wiki", f"{name}.md 沒有列在 index.md（孤兒頁）")
        if inbound[name] == 0 and name != "log":
            err("整理 Wiki", f"{name}.md 沒有任何頁面連過來")
    for sid, p in raw_ids.items():
        t = read(p)
        if not re.search(r"^url:\s*https?://", t, re.M):
            err("取得資料", f"{os.path.basename(p)} 沒有來源網址")
    if len(raw_ids) < 5:
        err("取得資料", f"來源只有 {len(raw_ids)} 個，作業要求至少 5 個")
    print(f"wiki：{len(pages)} 頁，{len(raw_ids)} 個來源")


# ---------------- slides ----------------
class SlideParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.slides = []; self.cur = None; self.claim = None; self.in_foot = False; self.depth = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "section" and "slide" in a.get("class", ""):
            self.cur = {"id": a.get("id", "?"), "wiki": [x.strip() for x in a.get("data-wiki", "").split(",") if x.strip()], "claims": [], "foot": [], "text": ""}
            self.slides.append(self.cur)
        if self.cur is None:
            return
        if tag == "li":
            self.li = {"cls": a.get("class", ""), "free": ""}
            self.cur.setdefault("lis", []).append(self.li)
        if tag == "span" and "claim" in a.get("class", ""):
            self.claim = {"src": a.get("data-src", ""), "quote": a.get("data-quote", ""), "text": ""}
            self.cur["claims"].append(self.claim)
        if tag == "footer" and "src" in a.get("class", ""):
            self.in_foot = True
        if tag == "a" and self.in_foot:
            self.cur["foot"].append(a.get("href", ""))
    def handle_endtag(self, tag):
        if tag == "span" and self.claim is not None:
            self.claim = None
        if tag == "footer":
            self.in_foot = False
        if tag == "li":
            self.li = None
    def handle_data(self, d):
        if self.claim is not None:
            self.claim["text"] += d
        elif getattr(self, "li", None) is not None:
            self.li["free"] += d


def check_slides():
    path = os.path.join(ROOT, "slides/index.html")
    if not os.path.exists(path):
        err("產生簡報", "slides/index.html 不存在"); return
    p = SlideParser(); p.feed(read(path))
    pages = wiki_pages()
    n_claims = 0
    for s in p.slides:
        sid = s["id"]
        if not s["wiki"]:
            err("逐頁內容", f"投影片 {sid} 沒有標 data-wiki（不知道內容從哪一頁 wiki 來）")
        for w in s["wiki"]:
            if w not in pages:
                err("逐頁內容", f"投影片 {sid} 標的 wiki 頁 {w} 不存在")
            if not any(h.endswith(f"wiki/{w}.html") for h in s["foot"]):
                err("產生簡報", f"投影片 {sid} 的頁尾沒有附上 {w} 的連結")
        for c in s["claims"]:
            n_claims += 1
            src = c["src"]
            if src not in pages:
                err("逐頁內容", f"投影片 {sid} 的重點「{c['text'][:20]}」指向不存在的 wiki 頁 {src}"); continue
            if src not in s["wiki"]:
                err("產生簡報", f"投影片 {sid} 的重點用了 {src}，但頁尾沒列這一頁")
            if not c["quote"]:
                err("逐頁內容", f"投影片 {sid} 的重點「{c['text'][:20]}」沒有 data-quote"); continue
            if norm(c["quote"]) not in norm(read(pages[src])):
                err("查詢 Wiki", f"投影片 {sid} 的重點「{c['text'][:24]}」在 {src}.md 找不到「{c['quote']}」→ 可能是 AI 自己加的內容")
        # 沒有標出處的句子裡如果有數字，很可能是 AI 自己補的事實
        for li in s.get("lis", []):
            if "meta" in li["cls"]:
                continue
            free = re.sub(r"Q\d", "", li["free"])
            if re.search(r"\d", free):
                err("逐頁內容", f"投影片 {sid} 有沒標出處的數字：「{li['free'].strip()[:40]}」")
    if not 8 <= len(p.slides) <= 15:
        err("寫大綱", f"簡報有 {len(p.slides)} 頁，規格是 8–15 頁")
    # 覆蓋率：簡報引用到的 wiki 頁，追回去用到了幾個來源
    used = set()
    for s in p.slides:
        for w in s["wiki"]:
            if w in pages:
                used |= set(re.findall(r"\[(S\d+)\]", read(pages[w])))
    allsrc = {"S" + os.path.basename(x)[:2].lstrip("0") for x in glob.glob(os.path.join(ROOT, "raw/*.md"))}
    missing = sorted(allsrc - used)
    if missing:
        err("寫大綱", f"簡報引用的 wiki 頁沒有用到這些來源：{missing}（覆蓋率不足）")
    print(f"coverage：簡報間接用到 {len(used & allsrc)}/{len(allsrc)} 個來源")
    print(f"slides：{len(p.slides)} 頁，{n_claims} 個重點已比對")


# ---------------- pages（提前的檢查：產生 HTML 之前先查逐頁內容） ----------------
def check_pages():
    pages = wiki_pages()
    outline = read(os.path.join(ROOT, "outline/outline.md"))
    for row in re.findall(r"^\|\s*\d+\s*\|.*\|\s*([^|]+?)\s*\|\s*$", outline, re.M):
        for w in [x.strip() for x in row.split(",")]:
            if w not in pages:
                err("寫大綱", f"outline.md 用到不存在的 wiki 頁 {w}")
    md = read(os.path.join(ROOT, "outline/pages.md"))
    n = 0
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        sid = "s" + lines[0].split("|")[0].strip()
        wl = []
        for l in lines[1:]:
            if l.startswith("wiki:"):
                wl = [x.strip() for x in l[5:].split(",")]
        for w in wl:
            if w not in pages:
                err("逐頁內容", f"{sid} 標的 wiki 頁 {w} 不存在")
        for l in lines[1:]:
            if not l.startswith("- "):
                continue
            for shown, src, quote in re.findall(r"\{\{(.+?)\|\|(.+?)\|\|(.+?)\}\}", l):
                n += 1
                if src not in pages:
                    err("逐頁內容", f"{sid}「{shown[:20]}」指向不存在的 wiki 頁 {src}")
                elif norm(quote) not in norm(read(pages[src])):
                    err("查詢 Wiki", f"{sid}「{shown[:24]}」在 {src}.md 找不到「{quote}」→ 回 wiki 查，wiki 沒有就回『取得資料』")
                if src not in wl:
                    err("逐頁內容", f"{sid} 用了 {src} 但 wiki: 那行沒列")
            free = re.sub(r"\{\{.+?\}\}", "", l[2:])
            free = re.sub(r"Q\d", "", free)
            if re.search(r"\d", free):
                err("逐頁內容", f"{sid} 有沒標出處的數字：「{l[2:42]}」")
    print(f"pages：逐頁內容 {n} 個重點已比對")


# ---------------- render（渲染後有沒有溢出） ----------------
def check_render():
    import json, shutil, subprocess
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        warns.append("找不到 Chrome，跳過渲染檢查"); return
    url = "file://" + os.path.join(ROOT, "slides/index.html") + "?check=1"
    for name, size in (("桌機", "1280,720"), ("手機", "390,844")):
        out = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-sandbox", f"--window-size={size}",
                              "--virtual-time-budget=3000", "--dump-dom", url], capture_output=True, text=True, timeout=60).stdout
        m = re.search(r'<pre id="render-report">(.*?)</pre>', out, re.S)
        if not m:
            err("產生簡報", f"{name}渲染檢查拿不到結果"); continue
        rep = json.loads(html.unescape(m.group(1)))
        bad = [x["slide"] for x in rep["slides"] if x["overflow"]]
        if bad:
            err("產生簡報", f"{name}（{size}）第 {bad} 頁內容超出投影片範圍（溢出）")
        print(f"render：{name} {size} 檢查 {len(rep['slides'])} 頁，溢出 {len(bad)} 頁")


# ---------------- links ----------------
class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = []
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ("href", "src") and v:
                self.links.append(v)


def check_links():
    files = [p for p in glob.glob(os.path.join(ROOT, "**/*.html"), recursive=True) if "/.git/" not in p]
    n = 0
    for f in files:
        lp = LinkParser(); lp.feed(read(f))
        for l in lp.links:
            if re.match(r"^(https?:|mailto:|#|data:|javascript:)", l):
                continue
            n += 1
            target = os.path.normpath(os.path.join(os.path.dirname(f), l.split("#")[0]))
            if not os.path.exists(target):
                node = "產生簡報" if "/slides/" in f else "整理 Wiki"
                err(node, f"{os.path.relpath(f, ROOT)} 的連結 {l} 指到不存在的檔案")
    print(f"links：{len(files)} 個 HTML、{n} 個本地連結")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("wiki", "all"): check_wiki()
    if mode in ("pages", "all"): check_pages()
    if mode in ("slides", "all"): check_slides()
    if mode in ("render", "all"): check_render()
    if mode in ("links", "all"): check_links()
    for w in warns: print("⚠️ ", w)
    for e in errors: print("❌", e)
    print("結果：", "通過 ✅" if not errors else f"{len(errors)} 個錯誤")
    sys.exit(1 if errors else 0)
