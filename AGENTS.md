# AGENTS.md — 擴散模型 LLM Wiki ＋ 教學簡報 工作手冊

> 給 AI agent（Antigravity / Gemini、Claude Code、Codex…）看的規則。**每次開新對話，先讀完這份再動手。**
> `CLAUDE.md` 和 `GEMINI.md` 只寫一句「請讀 AGENTS.md」，規則只維護這一份。

## 1. 專案目的
1. 用 Karpathy 的 LLM Wiki 架構，整理一個主題知識庫：**擴散模型（Diffusion Model）是怎麼生成圖片的？**
2. 用這個 wiki 當**唯一的知識來源**，產生一份教新手的 HTML 教學簡報。
3. 簡報裡每個重點都要追得到 wiki 頁，wiki 每句事實都要追得到 raw 來源。

## 2. 資料夾結構
```
raw/              原始來源（不可修改）：01-*.md … 每個檔案有 id、url、retrieved、英文原文摘錄、我的筆記
wiki/             AI 維護的 wiki（Obsidian 也能直接開）
  index.md        目錄：所有頁面＋一句話說明（查詢時先讀這頁）
  log.md          append-only 維護紀錄：## [日期] ingest|query|lint | 標題
  overview.md     總覽；timeline.md 時間軸；glossary.md 名詞表
  sources/        每個來源一頁摘要（s1-ddpm.md …）
  concepts/       概念頁（forward-process.md …）
  comparisons/    比較頁
outline/          outline.md 大綱（人類確認關卡）、pages.md 逐頁內容
slides/           index.html 簡報（自動產生，不要手改）、style.md 風格規格
docs/             workflow.md / workflow.svg 流程圖、requirements.md 需求、reflection.md 反思
log/              run-YYYY-MM-DD.md 執行紀錄、check-outputs/ 每次檢查的原始輸出
tools/            build_wiki.py、make_slides.py、check.py
index.html        專案首頁（連到 wiki 和簡報）
```

## 3. 寫作規則
- 內文用**繁體中文**，專有名詞保留英文（DDPM、U-Net、latent、CFG）。
- 檔名用英文小寫加連字號（`noise-schedule.md`）；來源頁用 `s編號-簡稱.md`。
- 每頁開頭有 frontmatter：`title`、`type`（concept / comparison / source / overview / glossary / index / log）、`sources`、`updated`。
- **每一句事實後面標來源** `[S1]`～`[S8]`；frontmatter 的 `sources` 要跟內文實際用到的一致。
- 頁面之間用 Obsidian 雙向連結：`[[concepts/forward-process|前向過程]]`。每頁最後有「相關頁面」。
- 表格裡不要用 `[[頁面|文字]]`（直線會切壞表格），要用連結就改成清單。
- 新頁面一定要加進 `wiki/index.md`，而且至少要有一頁連過來（不能有孤兒頁）。
- 比喻、白話說明可以不標來源，但**不能夾帶新的事實或數字**。
- 不要把 API key、密碼、個資放進專案（會公開在 GitHub 上）。

## 4. 工作流程（詳見 docs/workflow.md 的圖）
### A. 新增一個來源（ingest）
1. 把來源存成 `raw/0N-簡稱.md`：id、title、authors、published、url、retrieved、英文原文摘錄（`> "..."`，數學式用 `...` 省略）、中文筆記。
2. 寫 `wiki/sources/sN-簡稱.md` 摘要，列出「這篇更新了哪些頁面」。
3. 更新相關的 concepts / comparisons / overview / timeline / glossary，必要時開新概念頁。
4. 更新 `wiki/index.md`，在 `wiki/log.md` 加一筆 `## [日期] ingest | 標題`。
5. 跑 `python3 tools/check.py wiki`，通過才算完成；再跑 `python3 tools/build_wiki.py` 產生網頁。

### B. 用 wiki 做簡報（query）
1. **寫大綱** `outline/outline.md`：對象、目標、頁數，每頁一行「標題｜重點｜用到的 wiki 頁」。
2. **停下來給人確認大綱**（唯一的人工關卡）。不滿意就改大綱，不要往下做。
3. **寫逐頁內容** `outline/pages.md`：只能用 wiki 的內容。格式：
   ```
   ## 4 | 標題
   wiki: concepts/forward-process
   visual: noise-strip
   - {{顯示文字||wiki頁||從那頁 wiki 複製的原文片段}}
   ~ 跟主題無關的說明（例如簡報長度），不算事實
   ```
4. **跑提前檢查** `python3 tools/check.py pages`。
   - 「找不到原文」→ 回第 3 步修那一句（每輪只修報告列出的問題，**最多 3 輪**，還不過就停下來問人）。
   - 「wiki 沒有這個事實」→ **回 A. 新增來源**，不准自己編。
   - 「沒標出處的數字」→ 補出處或刪掉。
5. **產生簡報** `python3 tools/make_slides.py`（照 `slides/style.md`，不要手改 slides/index.html）。
6. **跑簡報檢查** `python3 tools/check.py all`（wiki＋pages＋slides＋links 全部要通過）。
7. **人工抽查**：看「重點 ↔ 原文」對照表，確認原文真的支持那句話（程式只能檢查原文存在）。
8. 在 `log/run-日期.md` 記下這次每個節點發生什麼事、哪裡失敗、怎麼修，原始輸出存到 `log/check-outputs/`。

### C. 發布
1. **先確認 `python3 tools/check.py all` 的結束碼是 0**（不要接 `| tee` 又接 `&& git commit`，tee 會吃掉錯誤碼；要存輸出請先 `set -o pipefail`），才 `git add -A && git commit`，push 到 GitHub（repo 要是 public）。
2. Settings → Pages → Deploy from branch → `main` / root。
3. 等 Pages 建好，用 curl 確認 `index.html`、`wiki/index.html`、`slides/index.html` 和每一頁 wiki 都是 HTTP 200。
4. 再實際打開（或截圖）看 wiki 索引和簡報前幾頁有沒有跑版——200 不代表畫面是對的。

## 5. 怎樣才算完成
- [ ] `python3 tools/check.py all` 顯示「通過 ✅」
- [ ] raw/ 至少 5 個來源，都有網址
- [ ] 簡報每一頁頁尾都有「📚 Wiki 出處」連結
- [ ] `log/run-*.md` 有這次的執行紀錄（含失敗和修正）
- [ ] 線上網址都能打開

## 6. 簡報風格（摘要，完整見 slides/style.md）
米白底、深藍字、黃色重點；每頁最多 4 個重點＋一個簡單圖示；← → / 空白鍵 / 手機滑動換頁；單一 HTML 檔、不連外部資源。
