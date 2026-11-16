---
title: 擴散模型 LLM Wiki — 索引
type: index
updated: 2026-11-16
---

# 擴散模型（Diffusion Model）LLM Wiki — 索引

> 這是我用 Karpathy 的 LLM Wiki 架構整理的知識庫，主題是「擴散模型是怎麼生成圖片的？」。
> AI 回答問題或做簡報前，**先讀這一頁**，再點進需要的頁面。每一句事實後面都標了來源編號 [S1]～[S8]。

## 總覽
- [[overview|總覽：擴散模型是怎麼生成圖片的？]]：一頁看懂整體流程（先讀這頁）
- [[timeline|發展時間軸]]：2015 → 2022 的重要論文
- [[glossary|名詞表]]：新手會卡住的名詞

## 概念頁（concepts）
- [[concepts/plain-language|白話版：給完全新手的擴散模型]]：不用數學，簡報就是照這頁做的（先讀這頁）
- [[concepts/forward-process|前向過程]]：一步一步加雜訊，T = 1000
- [[concepts/reverse-process|反向過程]]：從雜訊一步一步還原
- [[concepts/noise-schedule|雜訊排程]]：β 從 0.0001 到 0.02
- [[concepts/training-objective|訓練目標]]：預測雜訊 + MSE
- [[concepts/unet-backbone|U-Net 骨幹]]：負責去雜訊的網路
- [[concepts/sampling-speed|取樣加速]]：為什麼慢、DDIM 等加速法
- [[concepts/latent-diffusion|Latent Diffusion]]：Stable Diffusion 的基礎
- [[concepts/text-conditioning|文字條件與 CFG]]：怎麼讓它照文字畫
- [[concepts/stable-diffusion-pipeline|Stable Diffusion 的三個零件]]：VAE＋U-Net＋CLIP，512→64

## 比較頁（comparisons）
- [[comparisons/diffusion-vs-gan-vae|擴散模型 vs GAN vs VAE]]
- [[comparisons/ddpm-vs-ddim|DDPM vs DDIM]]

## 來源摘要（sources）
- **S1**　[[sources/s1-ddpm|DDPM 論文（Ho et al., 2020）]]（論文）
- **S2**　[[sources/s2-lilian-weng|Lilian Weng：What are Diffusion Models?]]（部落格）
- **S3**　[[sources/s3-hf-annotated|Hugging Face：The Annotated Diffusion Model]]（部落格＋程式）
- **S4**　[[sources/s4-ddim|DDIM 論文（Song et al., 2020）]]（論文）
- **S5**　[[sources/s5-latent-diffusion|Latent Diffusion 論文（Rombach et al., 2022）]]（論文）
- **S6**　[[sources/s6-cfg|Classifier-Free Guidance 論文]]（論文）
- **S7**　[[sources/s7-wikipedia|Wikipedia：Diffusion model]]（百科）
- **S8**　[[sources/s8-hf-stable-diffusion|Hugging Face：Stable Diffusion with Diffusers]]（部落格＋程式）

## 維護紀錄
- [[log|wiki 維護紀錄（log.md）]]：每次 ingest／query／lint 都記在這裡
