---
title: 取樣加速：為什麼慢、怎麼變快
type: concept
sources: [S2, S3, S4, S8]
updated: 2026-11-16
---

# 取樣加速

## 為什麼慢
- 擴散模型生成一張圖要做很多次網路前向運算，這幾乎是它唯一的主要缺點 [S3]。
- 一個例子：在 Nvidia 2080 Ti 上，用 DDPM 產生 5 萬張 32×32 的圖大約要 20 小時，GAN 不到一分鐘 [S2]。

## 怎麼變快
1. **跳步取樣（strided sampling）**：不用每一步都走，每隔幾步更新一次，把 T 步縮成 S 步 [S2]。
2. **DDIM**：跟 DDPM 用**同樣的訓練方式**，只換取樣方法，速度快 **10～50 倍** [S4]。→ [[comparisons/ddpm-vs-ddim|DDPM vs DDIM]]
3. **蒸餾（Progressive Distillation）**：訓練一個學生模型，每一輪把取樣步數減半 [S2]。
4. **少走幾步**：Stable Diffusion 預設取樣 50 步，但只用 15 步品質會明顯變差，所以步數是在速度和品質之間取捨 [S8]。
5. **在 latent space 做擴散**：資料變小，算得更快 [S2]。→ [[concepts/latent-diffusion|Latent Diffusion]]

## 相關頁面
- [[concepts/reverse-process|反向過程]]
