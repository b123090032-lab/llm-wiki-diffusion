---
title: Latent Diffusion：Stable Diffusion 背後的關鍵
type: concept
sources: [S2, S5, S7, S8]
updated: 2026-11-16
---

# Latent Diffusion（LDM）

## 遇到的問題
直接在像素上做擴散非常貴：訓練強的擴散模型常常要花上百個 GPU 天，生成時也要一步一步算 [S5]。

## 解法：先壓縮，再擴散
1. 用一個**預訓練好的 autoencoder**，把圖片壓縮成比較小的 latent [S5]。
2. 擴散和去雜訊都在 latent 上做，訓練成本更低、生成更快 [S2]。
3. 最後再用 decoder 把 latent 還原成圖片 [S2]。

以 Stable Diffusion 為例：VAE 縮小倍率是 8，512×512 的圖會變成 64×64 的 latent [S8]。

背後的想法：圖片大部分的資料量都花在人眼感受的細節上，就算大幅壓縮，語意和構圖還是保留得住 [S2]。

## 文字怎麼進來
在 U-Net 裡加 **cross-attention**，就能用文字、bounding box 等當條件來生成 [S5]。→ [[concepts/text-conditioning|文字條件與 CFG]]

## 跟 Stable Diffusion 的關係
Stable Diffusion 這類商業產品，就是把擴散模型和文字編碼器、cross-attention 模組結合起來 [S7]。

## 相關頁面
- [[concepts/unet-backbone|U-Net 骨幹]]
- [[concepts/stable-diffusion-pipeline|Stable Diffusion 的三個零件]]
- [[sources/s5-latent-diffusion|S5 Latent Diffusion 論文]]
