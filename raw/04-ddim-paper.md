---
id: S4
title: "Denoising Diffusion Implicit Models (DDIM)"
authors: Jiaming Song, Chenlin Meng, Stefano Ermon
published: 2020-10-06 (arXiv 2010.02502)
url: https://arxiv.org/abs/2010.02502
retrieved: 2026-11-16（從 arXiv API 抓摘要）
type: 論文摘要
---

# S4　DDIM 論文（Song et al., 2020）

## 原文摘錄（摘要）
> "Denoising diffusion probabilistic models (DDPMs) have achieved high quality image generation without adversarial training, yet they require simulating a Markov chain for many steps to produce a sample."

> "we present denoising diffusion implicit models (DDIMs), a more efficient class of iterative implicit probabilistic models with the same training procedure as DDPMs."

> "DDIMs can produce high quality samples ... faster in terms of wall-clock time compared to DDPMs"

（中間的倍數原文是 LaTeX：`$10 \times$ to $50 \times$`，也就是 10～50 倍。）

## 我的筆記
- DDIM 不用重新訓練（跟 DDPM 同樣的訓練方式），只是換一種取樣方法。
- 速度快 10～50 倍，可以用計算量換品質。
