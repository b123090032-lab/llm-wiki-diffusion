# 擴散模型 LLM Wiki ＋ 教學簡報

生成式AI：文字與圖像生成的原理與實務｜第十週作業

- 🌐 專案首頁：https://b123090032-lab.github.io/llm-wiki-diffusion/
- 📽 教學簡報：https://b123090032-lab.github.io/llm-wiki-diffusion/slides/
- 📚 Wiki 索引：https://b123090032-lab.github.io/llm-wiki-diffusion/wiki/index.html （也可以直接在 GitHub 看 [wiki/index.md](wiki/index.md)，或用 Obsidian 打開 `wiki/` 資料夾）
- 🔁 流程圖：[docs/workflow.md](docs/workflow.md)
- 🧾 執行紀錄：[log/run-2026-11-16.md](log/run-2026-11-16.md)
- 🤖 AI 工作手冊：[AGENTS.md](AGENTS.md)

## 怎麼重跑
```
python3 tools/build_wiki.py     # wiki/raw/docs 的 Markdown → HTML
python3 tools/check.py pages    # 產生簡報前先檢查逐頁內容
python3 tools/make_slides.py    # outline/pages.md → slides/index.html
python3 tools/check.py all      # 全部檢查
```
只用 Python 標準函式庫，不用安裝套件。
