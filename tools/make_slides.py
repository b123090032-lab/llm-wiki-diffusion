#!/usr/bin/env python3
"""把 outline/pages.md（逐頁內容）變成單一檔案的 HTML 簡報 slides/index.html。
用法：python3 tools/make_slides.py
- `{{顯示文字||wiki頁||wiki原文}}` → <span class="claim" data-src=... data-quote=...>
- `~ ` 開頭的條列 = 跟主題無關的說明（例如簡報長度），不算事實
- 每頁頁尾自動附上「📚 Wiki 出處」連結
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = lambda s: html.escape(s, quote=True)

VIS = {
"cover": """<svg viewBox="0 0 400 130" class="vis"><defs><filter id="n"><feTurbulence baseFrequency=".9" numOctaves="2"/><feColorMatrix type="saturate" values="0"/></filter></defs>
<rect x="10" y="10" width="110" height="110" rx="12" filter="url(#n)"/><text x="148" y="78" font-size="34">→ 擦 →</text>
<rect x="280" y="10" width="110" height="110" rx="12" fill="#f2c94c"/><circle cx="335" cy="50" r="20" fill="#fff"/><path d="M290 110 L322 76 L344 96 L366 72 L388 110Z" fill="#334e68"/></svg>""",
"prompt": """<svg viewBox="0 0 420 140" class="vis"><rect x="5" y="45" width="170" height="50" rx="25" fill="#fff" stroke="#1f2a44" stroke-width="2"/><text x="22" y="77" font-size="18">「海邊的夕陽」</text>
<text x="190" y="80" font-size="34">→</text><rect x="245" y="10" width="170" height="120" rx="12" fill="#f9a825"/><circle cx="330" cy="72" r="24" fill="#ff7043"/><rect x="245" y="88" width="170" height="42" fill="#1e88e5"/></svg>""",
"noise-strip": "STRIP:fwd", "reverse-strip": "STRIP:rev",
"stairs": """<svg viewBox="0 0 400 150" class="vis"><path d="M20 140 H80 V115 H140 V90 H200 V65 H260 V40 H320 V15 H380" stroke="#2563eb" stroke-width="5" fill="none"/>
<text x="10" y="132" font-size="16">雪花</text><text x="335" y="40" font-size="16">清楚的圖</text><text x="110" y="35" font-size="16" fill="#c0392b">一次一小步</text></svg>""",
"train-loop": """<svg viewBox="0 0 420 150" class="vis"><g font-size="17"><rect x="0" y="20" width="110" height="50" rx="8" fill="#f2c94c"/><text x="14" y="51">照片＋雪花</text>
<text x="118" y="52">→</text><rect x="145" y="20" width="110" height="50" rx="8" fill="#bfdbfe"/><text x="160" y="51">模型猜雪花</text>
<text x="263" y="52">→</text><rect x="290" y="20" width="125" height="50" rx="8" fill="#c8e6c9"/><text x="305" y="51">對答案、修正</text>
<path d="M352 75 C352 130 60 130 55 78" stroke="#c0392b" stroke-width="2.5" fill="none" stroke-dasharray="6"/><text x="140" y="140" fill="#c0392b">重複練習很多次</text></g></svg>""",
"draw": """<svg viewBox="0 0 420 130" class="vis"><defs><filter id="n2"><feTurbulence baseFrequency=".9" numOctaves="2"/><feColorMatrix type="saturate" values="0"/></filter></defs>
<rect x="5" y="10" width="110" height="110" rx="12" filter="url(#n2)"/><text x="130" y="72" font-size="28">擦 擦 擦 →</text>
<rect x="300" y="10" width="110" height="110" rx="12" fill="#f2c94c"/><circle cx="355" cy="50" r="20" fill="#fff"/><path d="M310 110 L342 76 L364 96 L386 72 L408 110Z" fill="#334e68"/></svg>""",
"knob": """<svg viewBox="0 0 420 150" class="vis"><circle cx="80" cy="80" r="55" fill="#fff" stroke="#1f2a44" stroke-width="4"/><line x1="80" y1="80" x2="118" y2="45" stroke="#c0392b" stroke-width="6" stroke-linecap="round"/>
<text x="38" y="148" font-size="16">聽話旋鈕</text><g font-size="18"><text x="160" y="55">調低 → 比較自由、變化多</text><text x="160" y="105">調高 → 比較聽話、變化少</text></g></svg>""",
"speed": """<svg viewBox="0 0 400 120" class="vis"><g font-size="17"><text x="0" y="38">擴散模型</text><rect x="85" y="18" width="300" height="28" rx="4" fill="#c0392b"/><text x="265" y="38" fill="#fff">約 20 小時</text>
<text x="0" y="92">另一種方法</text><rect x="95" y="72" width="6" height="28" fill="#2563eb"/><text x="110" y="92">不到一分鐘</text></g></svg>""",
"latent": """<svg viewBox="0 0 420 140" class="vis"><g font-size="17"><rect x="0" y="10" width="110" height="110" fill="#f2c94c"/><text x="25" y="70">大圖</text><text x="118" y="70">壓縮→</text>
<rect x="180" y="45" width="40" height="40" fill="#bfdbfe"/><text x="172" y="110" font-size="14">在小的上面擦</text><text x="232" y="70">還原→</text>
<rect x="300" y="10" width="110" height="110" fill="#f2c94c"/><text x="325" y="70">新圖</text></g></svg>""",
"summary": """<svg viewBox="0 0 420 110" class="vis"><g font-size="18"><rect x="0" y="30" width="120" height="50" rx="8" fill="#e0e0e0"/><text x="10" y="61">① 變成雪花</text><text x="125" y="62">→</text>
<rect x="150" y="30" width="120" height="50" rx="8" fill="#bfdbfe"/><text x="160" y="61">② 練習擦掉</text><text x="275" y="62">→</text>
<rect x="300" y="30" width="120" height="50" rx="8" fill="#f2c94c"/><text x="310" y="61">③ 畫出新圖</text></g></svg>""",
"quiz": """<svg viewBox="0 0 400 70" class="vis"><text x="140" y="52" font-size="44">❓❓❓</text></svg>""",
}


def strip(direction):
    labels = ["照片", "", "", "", "", "雪花"]
    cells = []
    for i in range(6):
        k = i if direction == "fwd" else 5 - i
        lab = labels[i] if direction == "fwd" else labels[5 - i]
        cells.append(f'<div class="cell" style="--n:{k/5:.2f}"><span>{lab}</span></div>')
    arrow = "加雪花 →" if direction == "fwd" else "擦掉雪花 →"
    return '<div class="stripwrap"><div class="strip">' + "".join(cells) + f'</div><div class="arrow">{arrow}</div></div>'



def claimify(text):
    def rep(m):
        shown, src, quote = m.group(1), m.group(2).strip(), m.group(3)
        return f'<span class="claim" data-src="{E(src)}" data-quote="{E(quote)}" title="出處：wiki/{E(src)}.md">{E(shown)}</span>'
    parts, last = [], 0
    for m in re.finditer(r"\{\{(.+?)\|\|(.+?)\|\|(.+?)\}\}", text):
        parts.append(E(text[last:m.start()])); parts.append(rep(m)); last = m.end()
    parts.append(E(text[last:]))
    return "".join(parts)


def parse(md):
    slides = []
    for block in re.split(r"^## ", md, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        num, title = [x.strip() for x in lines[0].split("|", 1)]
        s = {"num": num, "title": title, "wiki": [], "visual": "", "items": []}
        for l in lines[1:]:
            if l.startswith("wiki:"): s["wiki"] = [x.strip() for x in l[5:].split(",")]
            elif l.startswith("visual:"): s["visual"] = l[7:].strip()
            elif l.startswith("- "): s["items"].append(("fact", l[2:]))
            elif l.startswith("~ "): s["items"].append(("meta", l[2:]))
        slides.append(s)
    return slides


def render(slides):
    secs = []
    for i, s in enumerate(slides):
        lis = "".join(f'<li class="{k}">{claimify(t)}</li>' for k, t in s["items"])
        v = VIS.get(s["visual"], "")
        if v.startswith("STRIP:"): v = strip(v[6:])
        foot = "、".join(f'<a href="../wiki/{w}.html" target="_blank">{w}</a>' for w in s["wiki"])
        cls = "slide cover" if i == 0 else ("slide quiz" if s["visual"] == "quiz" else "slide")
        secs.append(f'''<section class="{cls}" id="s{s["num"]}" data-wiki="{",".join(s["wiki"])}">
<div class="num">{s["num"]} / {len(slides)}</div><h2>{E(s["title"])}</h2>
<div class="body"><ul>{lis}</ul><div class="visual">{v}</div></div>
<footer class="src">📚 Wiki 出處：{foot}</footer></section>''')
    return TEMPLATE.replace("{{SLIDES}}", "\n".join(secs))


TEMPLATE = r'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>AI 是怎麼「畫」出一張圖的？｜擴散模型白話教學簡報</title>
<style>
:root{--bg:#fbfaf7;--ink:#1f2a44;--hi:#f2c94c;--muted:#52606d}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#e9e6df;font-family:system-ui,-apple-system,"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;color:var(--ink);overflow:hidden}
.deck{position:relative;width:100vw;height:100vh;height:100dvh}
.slide{position:absolute;inset:0;margin:auto;width:min(96vw,calc(96vh*16/9));height:min(54vw,96vh);background:var(--bg);border-radius:18px;box-shadow:0 10px 40px #0002;padding:3.2% 4.5% 2%;display:none;flex-direction:column;font-size:min(2.5vw,4.4vh)}
.slide.active{display:flex;animation:fade .35s}@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1}}
.num{font-size:.7em;color:var(--muted)}h2{margin:.2em 0 .5em;font-size:1.9em;border-left:.25em solid var(--hi);padding-left:.4em}
.body{flex:1;display:flex;gap:4%;align-items:center;min-height:0}.body ul{flex:1;margin:0;padding-left:1.1em;line-height:1.55}.body li{margin:.6em 0}
.visual{flex:1.45;display:flex;justify-content:center;align-items:center}.vis{width:100%;max-height:46vh}.vis text{font-family:inherit;fill:var(--ink)}
.claim{background:linear-gradient(transparent 62%,#f2c94c88 0);cursor:help}
footer.src{font-size:.62em;color:var(--muted);border-top:1px dashed #cbd2d9;padding-top:.5em}footer.src a{color:#2563eb}
.cover h2{font-size:2.4em;border:none;padding:0}.cover .body{flex-direction:column;align-items:flex-start}.cover .visual{width:60%;align-self:center}.cover li.meta{list-style:none;margin-left:-1.1em;color:var(--muted)}
.strip{display:flex;gap:4%;width:100%}.cell{flex:1;aspect-ratio:1;border-radius:8px;position:relative;overflow:hidden;background:linear-gradient(135deg,#f2c94c,#e67e22 60%,#2563eb)}
.cell::after{content:"";position:absolute;inset:0;opacity:var(--n);background:repeating-conic-gradient(#888 0 25%,#ddd 0 50%,#444 0 75%,#bbb 0) 0 0/6px 6px}
.stripwrap{width:100%}.arrow{text-align:center;font-size:.9em;color:#c0392b;margin-top:.4em}.cell span{position:absolute;bottom:2px;left:4px;z-index:1;font-size:.7em;color:#fff;text-shadow:0 0 3px #000}
.nav{position:fixed;right:14px;bottom:12px;display:flex;gap:8px;z-index:5}.nav button{font-size:18px;width:44px;height:44px;border-radius:50%;border:none;background:var(--ink);color:#fff;opacity:.75}
.progress{position:fixed;left:0;top:0;height:4px;background:var(--hi);z-index:5;transition:width .3s}
.home{position:fixed;left:14px;bottom:16px;font-size:13px;z-index:5}.home a{color:var(--ink)}
@media (max-aspect-ratio:1/1){.slide{width:94vw;height:calc(100dvh - 84px);top:12px;bottom:auto;font-size:4.2vw;overflow-y:auto;padding:5% 5% 3%}.body{flex-direction:column;align-items:stretch;justify-content:center;gap:1.4em}.body ul{flex:none}.visual{flex:none}.vis{max-height:30vh}h2{font-size:1.45em}.cover .visual{width:100%}.home{bottom:24px}}
.quiz .claim{background:#1f2a44;color:#1f2a44;border-radius:6px;padding:0 .3em;cursor:pointer}.quiz .claim.show{background:linear-gradient(transparent 62%,#f2c94c88 0);color:inherit}
@media print{html,body{overflow:visible}.slide{display:flex!important;position:relative;page-break-after:always;margin:0 auto 20px}.nav,.progress,.home{display:none}}
</style></head><body>
<div class="progress" id="bar"></div>
<main class="deck" id="deck">
{{SLIDES}}
</main>
<div class="home"><a href="../index.html">← 專案首頁</a>｜<a href="../wiki/index.html">Wiki 索引</a></div>
<div class="nav"><button id="prev" aria-label="上一頁">‹</button><button id="next" aria-label="下一頁">›</button></div>
<script>
const S=[...document.querySelectorAll('.slide')];let i=0;
function go(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,k)=>s.classList.toggle('active',k===i));document.getElementById('bar').style.width=((i+1)/S.length*100)+'%';history.replaceState(null,'','#'+(i+1));}
document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' ','Enter'].includes(e.key)){e.preventDefault();go(i+1)}else if(['ArrowLeft','PageUp','Backspace'].includes(e.key)){e.preventDefault();go(i-1)}else if(e.key==='Home')go(0);else if(e.key==='End')go(S.length-1)});
document.getElementById('next').onclick=()=>go(i+1);document.getElementById('prev').onclick=()=>go(i-1);
let x0=null;document.addEventListener('touchstart',e=>{x0=e.touches[0].clientX},{passive:true});
document.addEventListener('touchend',e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)go(i+(dx<0?1:-1));x0=null});
document.querySelectorAll('.quiz .claim').forEach(c=>c.addEventListener('click',()=>c.classList.toggle('show')));
go((parseInt(location.hash.slice(1))||1)-1);
if(location.search.includes('check')){const r=[];S.forEach((s,k)=>{go(k);const o=s.scrollHeight>s.clientHeight+2||s.scrollWidth>s.clientWidth+2;r.push({slide:k+1,overflow:o,sh:s.scrollHeight,ch:s.clientHeight});});go(0);const p=document.createElement('pre');p.id='render-report';p.textContent=JSON.stringify({w:innerWidth,h:innerHeight,slides:r});document.body.appendChild(p);}
</script></body></html>'''

if __name__ == "__main__":
    md = open(os.path.join(ROOT, "outline/pages.md"), encoding="utf-8").read()
    slides = parse(md)
    open(os.path.join(ROOT, "slides/index.html"), "w", encoding="utf-8").write(render(slides))
    print(f"slides/index.html：{len(slides)} 頁")
