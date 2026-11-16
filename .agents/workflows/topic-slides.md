---
description: 用 wiki 的內容產生一份教學 HTML 簡報（graph 大流程＋每格裡的 loop）
---

# /topic-slides

> Antigravity 的 workflow 檔。在對話裡輸入 `/topic-slides 主題` 就會照這份跑。完整規則在 AGENTS.md，流程圖在 docs/workflow.md。

## Loop 規格（五件事）
- 🎯 **目標**：只用 `wiki/` 的內容，產出一份教新手的 HTML 簡報 `slides/index.html`。
- 🚧 **限制**：不能用 wiki 以外的知識；不能手改 `slides/index.html`（只能改 `outline/pages.md` 再重新產生）；不能改 `raw/`。
- ✅ **完成標準**（全部由腳本判斷，不是 AI 說了算）：
  - `python3 tools/check.py all` 結束碼是 0：每頁有出處、引用的 wiki 頁存在、每個重點的原文找得到、數字都有出處、8–15 頁、8 個來源都有被用到、桌機和手機渲染後沒有溢出、連結沒斷。
  - 審查（新對話，只給 `log/review/packet.md`）沒有「講反」「講過頭」。
- 🛑 **停止條件**：全部通過就停；**同一格最多改 3 輪**還不過就停下來問人；一開始如果跟主題相關的 wiki 頁少於 3 頁，直接停下，先回去補資料，不要用自己的知識硬湊。
- ⏰ **觸發**：輸入 `/topic-slides`；或 wiki 新增來源（`wiki/log.md` 多了 ingest）之後重新跑一次。

## Graph（大流程，錯在哪一關就退回哪一關）
| 節點 | 只能看 | 產出 | 檢查關卡（一關＝一支腳本／一個人） | 失敗時退回 |
|---|---|---|---|---|
| 寫大綱 | wiki/index.md＋相關頁 | outline/outline.md | 人工確認大綱 | 寫大綱 |
| 逐頁內容 | 大綱＋大綱指定的 wiki 頁 | outline/pages.md | `check.py pages` | 原文對不上 → 只修那頁；wiki 沒有 → 回 ingest 補來源 |
| 產生簡報 | 已通過的 pages.md | slides/index.html | `check.py slides`、`check.py render`、`check.py links` | 版面溢出 → 回逐頁內容縮短；格式錯 → 重新產生 |
| 審查 | 簡報＋引用的 wiki 頁（審查包） | 審查意見 | 新對話的 AI 審查／人工抽查 | 講反、講過頭 → 只修那頁 |
| 交件 | — | git commit、Pages | curl 200＋截圖看畫面 | 404、跑版 → 產生簡報 |

## 每一格裡面還是 loop
- 逐頁內容：寫一頁 → `check.py pages` → 只修報告列的問題，最多 3 輪。
- 產生簡報：產生 HTML → `check.py render`（桌機 1280×720、手機 390×844）→ 修版面 → 再檢查。

## 步驟
1. 讀 AGENTS.md、wiki/index.md，列出跟主題相關的 wiki 頁；少於 3 頁就停。
2. 寫 outline/outline.md，**停下來給人確認**。
3. 寫 outline/pages.md → `python3 tools/check.py pages`（loop，最多 3 輪）。
4. `python3 tools/make_slides.py` → `python3 tools/check.py all`（loop，最多 3 輪）。
5. `python3 tools/review_packet.py` 產生審查包，開**新對話**只貼審查包請 AI 審查（不要叫寫的人審自己的作品）。
6. 把每一關的結果記到 log/run-日期.md，原始輸出放 log/check-outputs/，通過才 commit、push。
