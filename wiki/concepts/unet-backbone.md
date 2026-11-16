---
title: U-Net 骨幹（Backbone）
type: concept
sources: [S3, S5, S7]
updated: 2026-11-16
---

# U-Net 骨幹

負責去雜訊的網路叫做 backbone，通常是 **U-Net 或 Transformer** [S7]。

## DDPM 用的 U-Net
- DDPM 的作者選了 U-Net（Ronneberger et al., 2015 提出）[S3]。
- U-Net 先把輸入縮小（downsample），再放大回來（upsample）[S3]。
- 中間有 residual 連線，讓梯度比較好傳 [S3]。
- 卷積層之間也加了 attention 模組 [S3]。
- 時間步 t 會被轉成向量（time embedding）餵進網路，讓它知道現在雜訊有多重 [S3]。

## 加上文字以後
Latent Diffusion 在 U-Net 裡加入 **cross-attention** 層，讓文字等條件可以影響生成 [S5]。→ [[concepts/text-conditioning|文字條件與 CFG]]

## 相關頁面
- [[concepts/training-objective|訓練目標]]
- [[concepts/latent-diffusion|Latent Diffusion]]
