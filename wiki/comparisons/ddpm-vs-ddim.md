---
title: 比較：DDPM vs DDIM
type: comparison
sources: [S1, S3, S4]
updated: 2026-11-16
---

# DDPM vs DDIM

| | DDPM（2020） | DDIM（2020） |
|---|---|---|
| 訓練 | 預測雜訊 + MSE [S3] | **跟 DDPM 一樣**，不用重練 [S4] |
| 取樣 | 照馬可夫鏈一步一步走，很多步 [S4] | 非馬可夫的反向過程，可以少走很多步 [S4] |
| 速度 | 慢 | 快 10～50 倍 [S4] |
| 代表成果 | CIFAR10 FID 3.17 [S1] | 可以用計算量換品質 [S4] |

重點：DDIM 是「換一種取樣方法」，不是換一個模型，所以同一個訓練好的模型可以直接拿來用 [S4]。

## 相關頁面
- [[concepts/sampling-speed|取樣加速]]
- [[sources/s4-ddim|S4 DDIM 論文]]
