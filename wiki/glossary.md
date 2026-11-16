---
title: 名詞表
type: glossary
sources: [S2, S3, S4, S5, S6, S7]
updated: 2026-11-16
---

# 名詞表

- **Diffusion Model（擴散模型）**：先學去雜訊，再從雜訊生成資料的生成模型 [S7]。→ [[overview|總覽]]
- **Forward process（前向過程）**：固定地一步步加高斯雜訊 [S3]。→ [[concepts/forward-process|前向過程]]
- **Reverse process（反向過程）**：學出來的去雜訊過程 [S3]。→ [[concepts/reverse-process|反向過程]]
- **β_t / Variance schedule**：每一步加多少雜訊 [S2]。→ [[concepts/noise-schedule|雜訊排程]]
- **Backbone**：負責去雜訊的網路，通常是 U-Net 或 Transformer [S7]。→ [[concepts/unet-backbone|U-Net 骨幹]]
- **Latent space**：autoencoder 壓縮後的小空間 [S5]。→ [[concepts/latent-diffusion|Latent Diffusion]]
- **Cross-attention**：把文字等條件接進 U-Net 的方法 [S5]。
- **CFG（Classifier-Free Guidance）**：結合有條件和無條件預測，調整貼近提示詞的程度 [S6]。→ [[concepts/text-conditioning|文字條件與 CFG]]
- **DDIM**：更快的取樣方法 [S4]。→ [[comparisons/ddpm-vs-ddim|DDPM vs DDIM]]
