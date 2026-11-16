# 簡報大綱（人類確認關卡）

- 主題：擴散模型（Diffusion Model）是怎麼生成圖片的？
- 對象：沒學過生成模型的新手（例如剛修這門課的同學、高中生）
- 目標：看完 15 頁，能用自己的話講出「加雜訊 → 學去雜訊 → 從雜訊生成」，並知道 Stable Diffusion 多做了哪兩件事（latent、文字條件）。
- 長度：約 10 分鐘，15 頁
- 規則：**只能用 wiki/ 的內容**；每頁標出用到哪幾頁 wiki；數字一定要有出處。

| 頁 | 標題 | 要講的重點 | 用到的 wiki 頁 |
|---|---|---|---|
| 1 | 封面 | 主題、一句話原理 | overview |
| 2 | 一句話原理 | 先學擦雜訊，再從雜訊擦出圖 | overview |
| 3 | 兩個過程 | 前向（加雜訊、固定）／反向（去雜訊、要學） | overview |
| 4 | 前向過程 | 每步加一點高斯雜訊、T = 1000、可直接跳到第 t 步 | concepts/forward-process |
| 5 | 雜訊排程 | β 從 0.0001 線性增加到 0.02 | concepts/noise-schedule |
| 6 | 反向過程 | 從純雜訊開始一步步去雜訊；為什麼要分很多步 | concepts/reverse-process |
| 7 | 訓練在學什麼 | 預測加進去的雜訊、MSE、簡化損失 | concepts/training-objective |
| 8 | U-Net 骨幹 | 先縮小再放大、residual、attention、time embedding | concepts/unet-backbone |
| 9 | 為什麼慢？怎麼變快？ | 20 小時 vs 1 分鐘；DDIM 快 10～50 倍 | concepts/sampling-speed, comparisons/ddpm-vs-ddim |
| 10 | Latent Diffusion | 先壓縮再擴散，Stable Diffusion 的基礎 | concepts/latent-diffusion |
| 11 | 照著文字畫 | cross-attention、CFG 的品質／多樣性取捨 | concepts/text-conditioning |
| 12 | 跟 GAN、VAE 比 | 訓練穩定度、速度 | comparisons/diffusion-vs-gan-vae |
| 13 | 時間軸 | 2015 → 2022 | timeline |
| 14 | 小測驗 | 3 題 | overview, concepts/training-objective, concepts/text-conditioning |
| 15 | 總結＋延伸閱讀 | 三句話總結、去哪裡看更多 | index |

## 確認紀錄
- 2026-11-16：大綱定案為 15 頁，之後才開始寫逐頁內容（outline/pages.md）。
