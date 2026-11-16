---
id: S2
title: "What are Diffusion Models?"
authors: Lilian Weng（Lil'Log）
published: 2021-07-11（之後多次更新，最後一次 2024-04-13）
url: https://lilianweng.github.io/posts/2021-07-11-diffusion-models/
retrieved: 2026-11-16
type: 技術部落格
---

# S2　Lilian Weng：What are Diffusion Models?

## 原文摘錄
> "They define a Markov chain of diffusion steps to slowly add random noise to data and then learn to reverse the diffusion process to construct desired data samples from the noise."

> "GAN models are known for potentially unstable training and less diversity in generation due to their adversarial training nature."

> "Empirically, Ho et al. (2020) found that training the diffusion model works better with a simplified objective that ignores the weighting term"

> "For example, it takes around 20 hours to sample 50k images of size 32 × 32 from a DDPM, but less than a minute to do so from a GAN on an Nvidia 2080 Ti GPU."（引用 Song et al. 2020）

> "Latent diffusion model (LDM; Rombach & Blattmann, et al. 2022) runs the diffusion process in the latent space instead of pixel space, making training cost lower and inference speed faster."

> "a conditional diffusion model ... is trained on paired data ... where the conditioning information ... gets discarded periodically at random such that the model knows how to generate images unconditionally as well"

## 我的筆記
- 前向（加雜訊）是固定的馬可夫鏈；反向（去雜訊）是要學的。
- 前向過程可以直接一步算出任意第 t 步的 x_t（closed form），訓練時不用真的一步一步加。
- 跟 GAN 比：GAN 訓練不穩、多樣性較低；擴散模型生成很慢（要跑很多步）。
- 加速方法：跳步取樣（strided）、DDIM、蒸餾（progressive distillation）。
- Latent Diffusion：先用 autoencoder 壓縮成 latent，再在 latent 上做擴散。
- Classifier-free guidance：訓練時隨機丟掉條件 y，取樣時把「有條件」和「無條件」的預測組合起來。
