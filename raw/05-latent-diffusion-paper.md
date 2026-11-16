---
id: S5
title: "High-Resolution Image Synthesis with Latent Diffusion Models"
authors: Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser, Björn Ommer
published: 2021-12-20 (arXiv 2112.10752；CVPR 2022)
url: https://arxiv.org/abs/2112.10752
retrieved: 2026-11-16（從 arXiv API 抓摘要）
type: 論文摘要
---

# S5　Latent Diffusion 論文（Rombach et al., 2022）——Stable Diffusion 的基礎

## 原文摘錄（摘要）
> "since these models typically operate directly in pixel space, optimization of powerful DMs often consumes hundreds of GPU days and inference is expensive due to sequential evaluations."

> "we apply them in the latent space of powerful pretrained autoencoders."

> "By introducing cross-attention layers into the model architecture, we turn diffusion models into powerful and flexible generators for general conditioning inputs such as text or bounding boxes"

## 我的筆記
- 問題：直接在像素上做擴散很貴（訓練要上百個 GPU 天）。
- 解法：先用預訓練的 autoencoder 把圖片壓到 latent space，在那裡做擴散，最後再解碼回圖片。
- 文字條件透過 cross-attention 加進 U-Net，這就是「輸入一句話生成圖片」的關鍵。
