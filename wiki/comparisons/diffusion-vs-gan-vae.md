---
title: 比較：擴散模型 vs GAN vs VAE
type: comparison
sources: [S2, S3, S4]
updated: 2026-11-16
---

# 擴散模型 vs GAN vs VAE

| | GAN | VAE | 擴散模型 |
|---|---|---|---|
| 訓練方式 | 對抗式訓練（生成器 vs 判別器） | 用替代損失（surrogate loss） | 固定的加雜訊流程 + 學去雜訊 |
| 常見問題 | 訓練可能不穩、多樣性較低 [S2] | 依賴替代損失 [S2] | 生成要很多步，慢 [S3] |
| 生成速度 | 快（一次前向） | 快 | 慢，要很多步 [S2] |

- 共同點：都是把簡單分布的雜訊轉換成資料樣本 [S3]。
- 擴散模型的 latent 跟原始資料一樣大（高維度），這點跟 VAE 不同 [S2]。
- DDPM 不用對抗式訓練就能做出高品質圖片 [S4]。

## 相關頁面
- [[overview|總覽]]
- [[concepts/sampling-speed|取樣加速]]
