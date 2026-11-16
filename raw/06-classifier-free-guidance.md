---
id: S6
title: "Classifier-Free Diffusion Guidance"
authors: Jonathan Ho, Tim Salimans
published: 2022-07-26 (arXiv 2207.12598；NeurIPS 2021 workshop)
url: https://arxiv.org/abs/2207.12598
retrieved: 2026-11-16（從 arXiv API 抓摘要）
type: 論文摘要
---

# S6　Classifier-Free Guidance 論文（Ho & Salimans）

## 原文摘錄（摘要）
> "Classifier guidance ... requires training an image classifier separate from the diffusion model."

> "we jointly train a conditional and an unconditional diffusion model, and we combine the resulting conditional and unconditional score estimates to attain a trade-off between sample quality and diversity"

## 我的筆記
- 舊方法 classifier guidance 要多訓練一個分類器。
- CFG 不需要分類器：同一個模型同時學「有條件」和「無條件」。
- 調整 guidance 強度 = 在「品質／貼近提示詞」和「多樣性」之間取捨。
