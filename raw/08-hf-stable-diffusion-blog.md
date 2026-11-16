---
id: S8
title: "Stable Diffusion with 🧨 Diffusers"
authors: Suraj Patil, Pedro Cuenca, Nathan Lambert, Patrick von Platen（Hugging Face）
published: 2022-08-22
url: https://huggingface.co/blog/stable_diffusion
retrieved: 2026-11-16（簡報檢查發現「沒出處的數字」後補抓的來源）
type: 技術部落格（附程式）
---

# S8　Hugging Face：Stable Diffusion with Diffusers

## 原文摘錄
> "Stable Diffusion is a text-to-image latent diffusion model created by the researchers and engineers from CompVis , Stability AI and LAION ."

> "It is trained on 512x512 images from a subset of the LAION-5B database."

> "There are three main components in latent diffusion. An autoencoder (VAE). A U-Net . A text-encoder, e.g. CLIP's Text Encoder ."

> "the autoencoder used in Stable Diffusion has a reduction factor of 8. This means that an image of shape (3, 512, 512) becomes (4, 64, 64) in latent space"

> "Stable Diffusion does not train the text-encoder during training and simply uses an CLIP's already trained text encoder"

> "Stable Diffusion works quite well with a relatively small number of steps, so we recommend using the default number of inference steps of 50 ."

> "This shows that using only 15 denoising steps has significantly degraded the quality of the generation result."

> "guidance_scale is a way to increase the adherence to the"

## 我的筆記
- Stable Diffusion = 一種 latent diffusion model，三個零件：VAE、U-Net、文字編碼器（CLIP）。
- 512×512 的圖會被壓成 64×64（4 個通道）的 latent，縮小倍率 8。
- 文字編碼器用現成訓練好的 CLIP，不重新訓練。
- 預設取樣 50 步；只用 15 步品質會明顯變差。
- guidance_scale 就是 CFG 強度，越大越貼近提示詞。
