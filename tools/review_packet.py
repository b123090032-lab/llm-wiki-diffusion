#!/usr/bin/env python3
"""產生 AI 審查用的「審查包」log/review/packet.md：只放簡報每頁的文字和它引用的 wiki 頁。
用法：python3 tools/review_packet.py
把 packet.md 整份貼到一個「新的」AI 對話（不要用寫簡報的那個對話），請它照最上面的指示審查。
"""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT = """# 審查包：請你當審查員

你是審查員，不是作者。下面是一份教學簡報每一頁的文字，以及每一頁引用的 wiki 頁全文。
請**只根據這些 wiki 頁**檢查，不要用你自己的知識補充，也不要幫忙改寫：
1. 忠實度：每一頁有沒有說法和 wiki 講反、講過頭（wiki 沒說的也寫上去）、或數字對不上？
2. 覆蓋率：有沒有 wiki 裡很重要、但簡報完全沒提到的概念？
請用表格回覆：頁碼｜問題類型（講反／講過頭／數字錯／缺漏）｜簡報原句｜wiki 怎麼說。沒有問題就回「全部通過」。
"""

def main():
    t = open(os.path.join(ROOT, "slides/index.html"), encoding="utf-8").read()
    out, used = [PROMPT, "\n## 一、簡報內容\n"], []
    for sid, wiki, body in re.findall(r'<section class="[^"]*" id="(s\d+)" data-wiki="([^"]*)">(.*?)</section>', t, re.S):
        title = re.search(r"<h2>(.*?)</h2>", body).group(1)
        items = [re.sub(r"<[^>]+>", "", li) for li in re.findall(r"<li[^>]*>(.*?)</li>", body, re.S)]
        out.append(f"\n### {sid}　{html.unescape(title)}（引用：{wiki}）\n" + "\n".join(f"- {html.unescape(x)}" for x in items))
        used += [w for w in wiki.split(",") if w and w not in used]
    out.append("\n\n## 二、引用到的 wiki 頁全文\n")
    for w in used:
        out.append(f"\n---\n### wiki/{w}.md\n\n" + open(os.path.join(ROOT, "wiki", w + ".md"), encoding="utf-8").read())
    os.makedirs(os.path.join(ROOT, "log/review"), exist_ok=True)
    open(os.path.join(ROOT, "log/review/packet.md"), "w", encoding="utf-8").write("\n".join(out))
    print(f"log/review/packet.md：{len(used)} 個 wiki 頁")

if __name__ == "__main__":
    main()
