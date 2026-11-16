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
"cover": '''<svg viewBox="0 0 400 120" class="vis"><defs><filter id="n"><feTurbulence baseFrequency=".9" numOctaves="2"/><feColorMatrix type="saturate" values="0"/></filter></defs>
<rect x="10" y="10" width="100" height="100" rx="10" filter="url(#n)"/><text x="160" y="68" font-size="30" fill="#1f2a44">→ → →</text>
<rect x="290" y="10" width="100" height="100" rx="10" fill="#f2c94c"/><circle cx="340" cy="48" r="18" fill="#fff"/><path d="M300 100 L330 70 L350 88 L370 66 L390 100Z" fill="#334e68"/></svg>''',
"one-line": '''<svg viewBox="0 0 400 60" class="vis"><text x="0" y="40" font-size="26">🌫️ 雜訊</text><text x="140" y="40" font-size="26">— 擦 擦 擦 →</text><text x="310" y="40" font-size="26">🖼️ 圖</text></svg>''',
"two-process": '''<svg viewBox="0 0 420 130" class="vis"><rect x="5" y="40" width="80" height="50" rx="8" fill="#f2c94c"/><text x="22" y="72" font-size="16">真圖片</text>
<rect x="335" y="40" width="80" height="50" rx="8" fill="#9aa5b1"/><text x="352" y="72" font-size="16">純雜訊</text>
<path d="M90 50 C200 0 230 0 330 50" stroke="#c0392b" stroke-width="3" fill="none" marker-end="url(#a)"/><text x="150" y="22" font-size="14" fill="#c0392b">前向：加雜訊（固定）</text>
<path d="M330 82 C230 132 200 132 90 82" stroke="#2563eb" stroke-width="3" fill="none" marker-end="url(#b)"/><text x="150" y="124" font-size="14" fill="#2563eb">反向：去雜訊（要學）</text>
<defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#c0392b"/></marker><marker id="b" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#2563eb"/></marker></defs></svg>''',
"noise-strip": "STRIP:fwd", "reverse-strip": "STRIP:rev",
"schedule": '''<svg viewBox="0 0 400 140" class="vis"><line x1="40" y1="120" x2="390" y2="120" stroke="#333"/><line x1="40" y1="120" x2="40" y2="10" stroke="#333"/>
<line x1="40" y1="118" x2="380" y2="20" stroke="#c0392b" stroke-width="3"/><text x="45" y="112" font-size="12">β₁ = 0.0001</text><text x="300" y="18" font-size="12">β_T = 0.02</text><text x="180" y="137" font-size="12">步數 t →</text></svg>''',
"train-loop": '''<svg viewBox="0 0 420 110" class="vis"><g font-size="13"><rect x="0" y="35" width="80" height="40" rx="6" fill="#f2c94c"/><text x="12" y="60">真圖 x₀</text>
<text x="88" y="60">＋雜訊 ε →</text><rect x="165" y="35" width="70" height="40" rx="6" fill="#9aa5b1"/><text x="182" y="60">x_t</text>
<text x="240" y="60">→ U-Net →</text><rect x="315" y="35" width="100" height="40" rx="6" fill="#bfdbfe"/><text x="322" y="60">猜的雜訊 ε̂</text>
<text x="150" y="102" fill="#c0392b">損失 = MSE(ε, ε̂)</text></g></svg>''',
"unet": '''<svg viewBox="0 0 400 140" class="vis"><g fill="#bfdbfe" stroke="#2563eb"><rect x="20" y="10" width="40" height="110"/><rect x="80" y="35" width="40" height="70"/><rect x="140" y="55" width="40" height="30"/>
<rect x="200" y="55" width="40" height="30" fill="#f2c94c"/><rect x="260" y="35" width="40" height="70"/><rect x="320" y="10" width="40" height="110"/></g>
<g stroke="#c0392b" stroke-dasharray="4"><line x1="60" y1="15" x2="320" y2="15"/><line x1="120" y1="40" x2="260" y2="40"/></g><text x="150" y="135" font-size="12">縮小 → 放大（虛線 = skip 連線）</text></svg>''',
"speed": '''<svg viewBox="0 0 400 110" class="vis"><g font-size="13"><text x="0" y="30">DDPM</text><rect x="60" y="15" width="320" height="22" fill="#c0392b"/><text x="300" y="31" fill="#fff">~20 小時</text>
<text x="0" y="80">GAN</text><rect x="60" y="65" width="4" height="22" fill="#2563eb"/><text x="70" y="81">&lt; 1 分鐘</text></g><text x="60" y="105" font-size="11" fill="#52606d">5 萬張 32×32，2080 Ti</text></svg>''',
"latent": '''<svg viewBox="0 0 420 100" class="vis"><g font-size="13"><rect x="0" y="20" width="70" height="60" fill="#f2c94c"/><text x="12" y="55">圖片</text><text x="75" y="55">encoder→</text>
<rect x="150" y="35" width="40" height="30" fill="#bfdbfe"/><text x="152" y="55">latent</text><text x="195" y="55">擴散/去雜訊</text><text x="275" y="55">decoder→</text>
<rect x="350" y="20" width="70" height="60" fill="#f2c94c"/><text x="362" y="55">新圖</text></g></svg>''',
"cfg": '''<svg viewBox="0 0 400 100" class="vis"><g font-size="13"><text x="0" y="25">有文字的預測</text><text x="0" y="75">沒文字的預測</text><text x="120" y="52">→ 把差異放大 →</text>
<text x="240" y="52">更貼近提示詞</text></g><text x="240" y="75" font-size="11" fill="#c0392b">放太大：多樣性變少</text></svg>''',
"compare": '''<svg viewBox="0 0 400 90" class="vis"><g font-size="14"><text x="10" y="30">GAN</text><text x="150" y="30">VAE</text><text x="280" y="30">Diffusion</text>
<text x="10" y="60">快、不穩</text><text x="150" y="60">快、替代損失</text><text x="280" y="60">穩、但慢</text></g></svg>''',
"timeline": '''<svg viewBox="0 0 420 80" class="vis"><line x1="10" y1="40" x2="410" y2="40" stroke="#334e68" stroke-width="3"/><g font-size="12">
<circle cx="30" cy="40" r="6" fill="#f2c94c"/><text x="15" y="25">2015</text><circle cx="160" cy="40" r="6" fill="#f2c94c"/><text x="145" y="25">2020</text>
<circle cx="270" cy="40" r="6" fill="#f2c94c"/><text x="255" y="25">2021</text><circle cx="380" cy="40" r="6" fill="#f2c94c"/><text x="365" y="25">2022</text></g></svg>''',
"quiz": '''<svg viewBox="0 0 400 60" class="vis"><text x="150" y="45" font-size="40">❓❓❓</text></svg>''',
"summary": '''<svg viewBox="0 0 400 60" class="vis"><text x="40" y="40" font-size="20">加雜訊 → 學去雜訊 → 生成</text></svg>''',
}


def strip(direction):
    cells = []
    for i in range(6):
        k = i if direction == "fwd" else 5 - i
        cells.append(f'<div class="cell" style="--n:{k/5:.2f}"><span>{"x"+["₀","₁","₂","…","…","_T"][i] if direction=="fwd" else ["x_T","…","…","x₂","x₁","x₀"][i]}</span></div>')
    return '<div class="strip">' + "".join(cells) + "</div>"


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
        cls = "slide cover" if i == 0 else "slide"
        secs.append(f'''<section class="{cls}" id="s{s["num"]}" data-wiki="{",".join(s["wiki"])}">
<div class="num">{s["num"]} / {len(slides)}</div><h2>{E(s["title"])}</h2>
<div class="body"><ul>{lis}</ul><div class="visual">{v}</div></div>
<footer class="src">📚 Wiki 出處：{foot}</footer></section>''')
    return TEMPLATE.replace("{{SLIDES}}", "\n".join(secs))


TEMPLATE = r'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>擴散模型是怎麼生成圖片的？｜教學簡報</title>
<style>
:root{--bg:#fbfaf7;--ink:#1f2a44;--hi:#f2c94c;--muted:#52606d}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#e9e6df;font-family:system-ui,-apple-system,"Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;color:var(--ink);overflow:hidden}
.deck{position:relative;width:100vw;height:100vh;height:100dvh}
.slide{position:absolute;inset:0;margin:auto;width:min(96vw,calc(96vh*16/9));height:min(54vw,96vh);background:var(--bg);border-radius:18px;box-shadow:0 10px 40px #0002;padding:3.2% 4.5% 2%;display:none;flex-direction:column;font-size:min(2.1vw,3.7vh)}
.slide.active{display:flex;animation:fade .35s}@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1}}
.num{font-size:.7em;color:var(--muted)}h2{margin:.2em 0 .5em;font-size:1.9em;border-left:.25em solid var(--hi);padding-left:.4em}
.body{flex:1;display:flex;gap:4%;align-items:center;min-height:0}.body ul{flex:1;margin:0;padding-left:1.1em;line-height:1.55}.body li{margin:.45em 0}
.visual{flex:1.15;display:flex;justify-content:center;align-items:center}.vis{width:100%;max-height:42vh}.vis text{font-family:inherit;fill:var(--ink)}
.claim{background:linear-gradient(transparent 62%,#f2c94c88 0);cursor:help}
footer.src{font-size:.62em;color:var(--muted);border-top:1px dashed #cbd2d9;padding-top:.5em}footer.src a{color:#2563eb}
.cover h2{font-size:2.4em;border:none;padding:0}.cover .body{flex-direction:column;align-items:flex-start}.cover .visual{width:60%;align-self:center}.cover li.meta{list-style:none;margin-left:-1.1em;color:var(--muted)}
.strip{display:flex;gap:4%;width:100%}.cell{flex:1;aspect-ratio:1;border-radius:8px;position:relative;overflow:hidden;background:linear-gradient(135deg,#f2c94c,#e67e22 60%,#2563eb)}
.cell::after{content:"";position:absolute;inset:0;opacity:var(--n);background:repeating-conic-gradient(#888 0 25%,#ddd 0 50%,#444 0 75%,#bbb 0) 0 0/6px 6px}
.cell span{position:absolute;bottom:2px;left:4px;z-index:1;font-size:.7em;color:#fff;text-shadow:0 0 3px #000}
.nav{position:fixed;right:14px;bottom:12px;display:flex;gap:8px;z-index:5}.nav button{font-size:18px;width:44px;height:44px;border-radius:50%;border:none;background:var(--ink);color:#fff;opacity:.75}
.progress{position:fixed;left:0;top:0;height:4px;background:var(--hi);z-index:5;transition:width .3s}
.home{position:fixed;left:14px;bottom:16px;font-size:13px;z-index:5}.home a{color:var(--ink)}
@media (max-aspect-ratio:1/1){.slide{width:94vw;height:calc(100dvh - 84px);top:12px;bottom:auto;font-size:4.2vw;overflow-y:auto;padding:5% 5% 3%}.body{flex-direction:column;align-items:stretch;justify-content:center;gap:1.4em}.body ul{flex:none}.visual{flex:none}.vis{max-height:30vh}h2{font-size:1.45em}.cover .visual{width:100%}.home{bottom:24px}}
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
go((parseInt(location.hash.slice(1))||1)-1);
</script></body></html>'''

if __name__ == "__main__":
    md = open(os.path.join(ROOT, "outline/pages.md"), encoding="utf-8").read()
    slides = parse(md)
    open(os.path.join(ROOT, "slides/index.html"), "w", encoding="utf-8").write(render(slides))
    print(f"slides/index.html：{len(slides)} 頁")
