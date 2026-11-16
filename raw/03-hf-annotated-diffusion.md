---
id: S3
title: "The Annotated Diffusion Model"
authors: Niels Rogge, Kashif Rasul（Hugging Face）
published: 2022-06-07
url: https://huggingface.co/blog/annotated-diffusion
retrieved: 2026-11-16
type: 技術部落格（附 PyTorch 程式）
---

# S3　Hugging Face：The Annotated Diffusion Model

## 原文摘錄
> "a fixed (or predefined) forward diffusion process ... of our choosing, that gradually adds Gaussian noise to an image, until you end up with pure noise"

> "a learned reverse denoising diffusion process ... where a neural network is trained to gradually denoise an image starting from pure noise, until you end up with an actual image."

> "(the DDPM authors use ... T= 1000)"

> "we take a random sample ... from the real unknown and possibily complex data distribution"

> "we sample a noise level ... uniformly between ... (i.e., a random time step)"

> "The neural network is optimized using a simple mean squared error (MSE) between the true and the predicted Gaussian noise."

> "In terms of architecture, the DDPM authors went for a U-Net, introduced by (Ronneberger et al., 2015)"

> "We set the forward process variances to constants increasing linearly from"（引用 DDPM 原文；後面的數字是數學式，見下一行程式碼）

> "beta_start = 0.0001"

> "beta_end = 0.02"

> "the main (perhaps only) disadvantage of diffusion models is that they require multiple forward passes to generate an image"

## 我的筆記
- 兩個過程：固定的前向 q、要學的反向 p_θ。
- DDPM 用 T = 1000 步。
- 神經網路學的是「預測加進去的雜訊」，損失函數就是真雜訊和預測雜訊的 MSE。
- 網路架構是 U-Net（先縮小再放大，有 skip/residual 連線），並且把時間步 t 當成輸入。
- 雜訊排程（variance schedule）β 從 0.0001 線性增加到 0.02；也有 cosine 等其他排程。
