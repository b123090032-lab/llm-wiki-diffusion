---
title: 雜訊排程（Noise / Variance Schedule）
type: concept
sources: [S2, S3]
updated: 2026-11-16
---

# 雜訊排程（Variance Schedule）

前向過程每一步加多少雜訊，由一組 β_t 控制，β_t 介於 0 和 1 之間 [S2]。

- β_t 不是固定值，每一步都不一樣，所以叫「排程」，有點像學習率排程 [S3]。
- 排程可以是 linear、quadratic、cosine 等 [S3]。
- DDPM 原本用 **linear schedule**：β 從 **0.0001** 線性增加到 **0.02** [S3]。

## 白話
一開始只加一點點雜訊，後面越加越多。這樣前幾步圖片還保留很多細節，最後才完全變成雜訊。

## 相關頁面
- [[concepts/forward-process|前向過程]]
- [[sources/s3-hf-annotated|S3 The Annotated Diffusion Model]]
