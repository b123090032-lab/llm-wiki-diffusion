---
title: wiki 維護紀錄（log.md）
type: log
updated: 2026-11-16
---

# wiki 維護紀錄（append-only）

> 照 Karpathy 建議的格式：每筆以 `## [日期] 動作 | 標題` 開頭，可以用 `grep "^## \[" wiki/log.md` 快速看最近做了什麼。
> 完整的流程執行紀錄（含檢查失敗與修正）在 [log/run-2026-11-16.md](../log/run-2026-11-16.md)。

## [2026-11-16] ingest | S1～S7 共 7 個來源
- 新增 raw/01～07，每個來源都有網址、讀取日期、英文原文摘錄和我的中文筆記。
- 新增 sources/ 7 頁摘要、concepts/ 8 頁、comparisons/ 2 頁、overview、timeline、glossary、index。

## [2026-11-16] lint | 第一次 wiki 檢查
- `python3 tools/check.py wiki` 抓到 4 個錯誤：index 連到還沒建立的 log 頁；overview、glossary、forward-process 三頁的 frontmatter `sources` 跟內文實際引用不一致。另外 training-objective 有 2 行步驟沒有來源。
- 修正：建立本頁；補齊 frontmatter；在 raw/03 補上「隨機抽 t」的原文摘錄，讓訓練步驟每一行都有來源。

## [2026-11-16] query | 產生教學簡報（第一次檢查失敗）
- 用 wiki 產生 15 頁簡報後跑 `python3 tools/check.py slides`：45 個標了出處的重點都在 wiki 找得到，但抓到 5 個「沒標出處的數字」。
- 其中 2 個是我憑印象寫的事實：「Stable Diffusion 通常只要 20～50 步」「512×512 壓成 64×64」，wiki 裡沒有。

## [2026-11-16] ingest | S8 Hugging Face：Stable Diffusion with Diffusers
- 為了上面兩個數字回到「取得資料」補抓 S8。結果發現我的印象不準：官方建議的預設是 **50 步**（不是 20～50），15 步品質就會明顯變差。
- 新增 concepts/stable-diffusion-pipeline；更新 latent-diffusion、sampling-speed、text-conditioning、index。

## [2026-11-16] lint | 發布後發現 index 表格跑版
- 線上截圖看到「來源摘要」表格跑版：表格裡 `[[頁面|文字]]` 的直線被當成欄位分隔。
- 修正：改成清單；`check.py wiki` 新增「表格裡不能有帶直線的雙向連結」規則。
