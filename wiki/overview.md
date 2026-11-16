---
title: 總覽：擴散模型是怎麼生成圖片的？
type: overview
sources: [S1, S2, S3, S4, S7]
updated: 2026-11-16
---

# 總覽：擴散模型是怎麼生成圖片的？

一句話版本：**先學會「把雜訊一點一點擦掉」，生成時就從一張純雜訊開始，一步一步擦成一張圖。**

## 兩個過程
擴散模型（Diffusion Model）由兩個部分組成：前向擴散過程（forward diffusion process）和反向取樣過程（reverse sampling process）[S7]。

1. **前向過程：加雜訊**。拿一張真的圖片，每一步加一點高斯雜訊，加到最後變成純雜訊。這個過程是固定的，不用學 [S3]。→ [[concepts/forward-process|前向過程]]
2. **反向過程：去雜訊**。訓練一個神經網路，從純雜訊開始一步一步把雜訊拿掉，最後得到一張真的圖片 [S3]。→ [[concepts/reverse-process|反向過程]]

## 訓練的時候到底在學什麼？
網路學的是「這張圖裡被加了什麼雜訊」，用真雜訊和預測雜訊的均方誤差（MSE）當損失 [S3]。→ [[concepts/training-objective|訓練目標]]

負責去雜訊的網路叫 backbone，通常是 U-Net 或 Transformer [S7]。→ [[concepts/unet-backbone|U-Net 骨幹]]

## 為什麼現在這麼紅？
- 2020 年的 DDPM 在 CIFAR10 上拿到 FID 3.17，畫質追上 GAN [S1]。→ [[sources/s1-ddpm|S1 DDPM]]
- 跟 GAN 相比，不需要對抗式訓練，訓練比較穩 [S2][S4]。→ [[comparisons/diffusion-vs-gan-vae|擴散 vs GAN／VAE]]
- Stable Diffusion、DALL-E 等商業產品都是以擴散模型為基礎，再加上文字編碼器和 cross-attention [S7]。→ [[concepts/latent-diffusion|Latent Diffusion]]、[[concepts/text-conditioning|文字條件與 CFG]]

## 缺點
生成時要跑很多步，所以很慢 [S3]。→ [[concepts/sampling-speed|取樣加速]]

## 延伸閱讀
- [[concepts/plain-language|白話版（給完全新手）]]
- [[concepts/noise-schedule|雜訊排程]]
- [[comparisons/ddpm-vs-ddim|DDPM vs DDIM]]
- [[timeline|發展時間軸]]
- [[glossary|名詞表]]
