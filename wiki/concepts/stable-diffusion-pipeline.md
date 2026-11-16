---
title: Stable Diffusion 的三個零件
type: concept
sources: [S5, S8]
updated: 2026-11-16
---

# Stable Diffusion 的三個零件

Stable Diffusion 是一種 text-to-image 的 latent diffusion model，由 CompVis、Stability AI 和 LAION 的研究人員做出來，用 512×512 的圖片訓練 [S8]。

## 三個零件
1. **Autoencoder（VAE）**：encoder 把圖片壓成 latent，decoder 再把 latent 還原成圖片 [S8]。
2. **U-Net**：在 latent 上一步一步預測雜訊、去雜訊，並透過 cross-attention 讀文字 [S8]。
3. **文字編碼器**：用現成訓練好的 CLIP 文字編碼器，不重新訓練 [S8]。

## 數字感
- VAE 的縮小倍率是 8：512×512 的圖會變成 64×64（4 個通道）的 latent [S8]。
- 預設取樣 50 步；只用 15 步品質會明顯變差 [S8]。

## 跟論文的關係
Latent Diffusion 論文提出「在預訓練 autoencoder 的 latent space 做擴散」和「用 cross-attention 接文字」這兩個想法 [S5]，Stable Diffusion 就是照這個架構做出來的產品 [S8]。

## 相關頁面
- [[concepts/latent-diffusion|Latent Diffusion]]
- [[concepts/text-conditioning|文字條件與 CFG]]
- [[sources/s8-hf-stable-diffusion|S8 HF Stable Diffusion 部落格]]
