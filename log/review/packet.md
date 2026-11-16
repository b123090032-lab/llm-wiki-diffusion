# 審查包：請你當審查員

你是審查員，不是作者。下面是一份教學簡報每一頁的文字，以及每一頁引用的 wiki 頁全文。
請**只根據這些 wiki 頁**檢查，不要用你自己的知識補充，也不要幫忙改寫：
1. 忠實度：每一頁有沒有說法和 wiki 講反、講過頭（wiki 沒說的也寫上去）、或數字對不上？
2. 覆蓋率：有沒有 wiki 裡很重要、但簡報完全沒提到的概念？
請用表格回覆：頁碼｜問題類型（講反／講過頭／數字錯／缺漏）｜簡報原句｜wiki 怎麼說。沒有問題就回「全部通過」。


## 一、簡報內容


### s1　擴散模型是怎麼生成圖片的？（引用：overview）
- 一份給新手的 10 分鐘入門
- 用我自己整理的 LLM Wiki（8 個來源）做成

### s2　一句話原理（引用：overview）
- 先學會「把雜訊一點一點擦掉」
- 生成時從一張純雜訊開始，一步一步擦成一張圖
- 想像成：把一張被雪花雜訊蓋滿的電視畫面，慢慢調回清楚的影像

### s3　兩個過程（引用：overview）
- 擴散模型由前向過程和反向過程組成
- 前向：每一步加一點高斯雜訊，加到最後變成純雜訊，這個過程是固定的，不用學
- 反向：訓練神經網路從純雜訊一步一步把雜訊拿掉

### s4　前向過程：一步一步加雜訊（引用：concepts/forward-process）
- 從真圖片 x₀ 出發，得到 x₁、x₂……一直到 x_T
- DDPM 的總步數是 T = 1000
- 小技巧：可以用公式直接算出任意第 t 步的 x_t，訓練時不用真的一步一步加
- 名字由來：靈感來自非平衡熱力學，就像墨水在水裡擴散

### s5　雜訊排程：每一步加多少？（引用：concepts/noise-schedule）
- 每一步加多少雜訊由 β_t 控制
- DDPM 用 linear schedule：β 從 0.0001 增加到 0.02
- 也可以用 cosine 等其他排程
- 一開始加一點點，後面越加越多

### s6　反向過程：從雜訊還原成圖片（引用：concepts/reverse-process）
- 反向過程是要學的那一半
- 生成時先隨機抽一張純雜訊，再重複套用去雜訊網路
- 每一步網路都會拿到目前的 x_t 和步數 t
- 為什麼分很多步？每一步只要去掉一點點雜訊，問題就變簡單

### s7　訓練時到底在學什麼？（引用：concepts/training-objective）
- 程式自己加雜訊，所以知道「標準答案」
- 網路看 x_t 和 t，預測加進去的雜訊
- 損失 = 真雜訊和預測雜訊的均方誤差（MSE）
- Ho 等人發現簡化版損失效果更好

### s8　誰在猜雜訊？U-Net（引用：concepts/unet-backbone）
- 去雜訊的網路叫 backbone，通常是 U-Net 或 Transformer
- U-Net 先把輸入縮小，再放大回來
- 中間有 residual 連線，也加了 attention
- 時間步 t 會轉成向量餵進網路

### s9　為什麼慢？怎麼變快？（引用：concepts/sampling-speed,comparisons/ddpm-vs-ddim）
- 在 2080 Ti 上，DDPM 生 5 萬張小圖約 20 小時，GAN 不到一分鐘
- DDIM 跟 DDPM 用同樣的訓練方式，只換取樣方法
- DDIM 速度快 10～50 倍
- Stable Diffusion 預設取樣 50 步，只用 15 步品質就會明顯變差

### s10　Latent Diffusion：先壓縮，再擴散（引用：concepts/latent-diffusion）
- 問題：直接在像素上做擴散，訓練常常要上百個 GPU 天
- 用預訓練的 autoencoder 把圖片壓縮成 latent
- 在 latent 上擴散，成本更低、更快
- 以 Stable Diffusion 為例：512×512 的圖會變成 64×64 的 latent

### s11　怎麼讓它「照著文字畫」？（引用：concepts/text-conditioning）
- 文字先經過 text encoder，再透過 cross-attention 影響去雜訊網路
- CFG：同一個模型同時學「有條件」和「無條件」
- 訓練時隨機把文字丟掉
- guidance 調越大越貼近提示詞，但太大圖會比較單調

### s12　跟 GAN、VAE 比一比（引用：comparisons/diffusion-vs-gan-vae）
- 三種模型都是把簡單的雜訊轉成資料
- GAN 訓練可能不穩、多樣性較低
- DDPM 不用對抗式訓練就能做出高品質圖片
- 代價：生成要很多步，比較慢

### s13　發展時間軸（引用：timeline）
- 2015：擴散模型首次被提出
- 2020-06：DDPM（FID 3.17）；2020-10：DDIM
- 2021-12：Latent Diffusion
- 2022：Classifier-Free Guidance 論文上 arXiv

### s14　小測驗：你答得出來嗎？（引用：overview,concepts/training-objective,concepts/text-conditioning）
- Q1 前向過程需要訓練嗎？→ 不用，它是固定的
- Q2 網路訓練時在猜什麼？→ 加進去的雜訊
- Q3 CFG 調太大會怎樣？→ 更貼近提示詞，但圖會比較單調

### s15　總結＋延伸閱讀（引用：index,concepts/stable-diffusion-pipeline）
- 加雜訊（固定）→ 學去雜訊（訓練）→ 從雜訊生成（取樣）
- Stable Diffusion = VAE + U-Net + CLIP 文字編碼器
- 想看更多：打開我的 Wiki 索引，每一頁都有原始來源


## 二、引用到的 wiki 頁全文


---
### wiki/overview.md

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
- [[concepts/noise-schedule|雜訊排程]]
- [[comparisons/ddpm-vs-ddim|DDPM vs DDIM]]
- [[timeline|發展時間軸]]
- [[glossary|名詞表]]


---
### wiki/concepts/forward-process.md

---
title: 前向過程（Forward Process）：一步一步加雜訊
type: concept
sources: [S1, S2, S3, S7]
updated: 2026-11-16
---

# 前向過程（Forward Process）

## 在做什麼
從一張真實圖片 x₀ 開始，每一步加一點高斯雜訊（Gaussian noise），得到 x₁、x₂……一直到 x_T [S2]。步數越多，圖片越看不出原本的樣子，最後接近純高斯雜訊 [S2]。

- 這個過程是**固定的、事先定義好的**，不需要訓練 [S3]。
- DDPM 用的總步數是 **T = 1000** [S3]。
- 每一步加多少雜訊由 [[concepts/noise-schedule|雜訊排程]] β_t 決定 [S2]。

## 一個重要的小技巧：可以直接跳到第 t 步
前向過程有一個好性質：不用真的一步一步加，可以用公式直接算出任意第 t 步的 x_t（closed form，用 reparameterization trick）[S2]。這讓訓練時可以隨機挑一個 t 來練，效率高很多。→ [[concepts/training-objective|訓練目標]]

## 白話比喻
像一滴墨水滴進水裡慢慢擴散開來，最後整杯水都變成均勻的顏色。擴散模型的名字就是從這裡來的，靈感來自非平衡熱力學 [S1][S7]。

## 相關頁面
- [[concepts/reverse-process|反向過程]]：前向的「倒帶」
- [[overview|總覽]]


---
### wiki/concepts/noise-schedule.md

---
title: 雜訊排程（Noise / Variance Schedule）
type: concept
sources: [S2, S3]
updated: 2026-11-16
---

# 雜訊排程（Variance Schedule）

前向過程每一步加多少雜訊，由一組 β_t 控制，β_t 介於 0 和 1 之間 [S2]。

- β_t 不是固定值，每一步都不一樣，所以叫「排程」，有點像學習率排程 [S3]。
- 排程可以是 linear、quadratic、cosine 等 [S3]。
- DDPM 原本用 **linear schedule**：β 從 **0.0001** 線性增加到 **0.02** [S3]。

## 白話
一開始只加一點點雜訊，後面越加越多。這樣前幾步圖片還保留很多細節，最後才完全變成雜訊。

## 相關頁面
- [[concepts/forward-process|前向過程]]
- [[sources/s3-hf-annotated|S3 The Annotated Diffusion Model]]


---
### wiki/concepts/reverse-process.md

---
title: 反向過程（Reverse Process）：從雜訊還原成圖片
type: concept
sources: [S2, S3, S7]
updated: 2026-11-16
---

# 反向過程（Reverse Process）

## 在做什麼
反向過程是**要學的**那一半：訓練一個神經網路，從純雜訊開始一步一步去雜訊，最後得到一張真的圖片 [S3]。

- 前向是「加雜訊」，反向是「把擴散倒過來」，從雜訊中建構出想要的資料樣本 [S2]。
- 生成新圖片時：先隨機抽一張純雜訊，然後重複套用去雜訊網路 [S7]。
- 每一步網路都會拿到「目前這張圖 x_t」和「現在是第幾步 t」[S3]。→ [[concepts/unet-backbone|U-Net 骨幹]]

## 為什麼不一步就去完？
一次要從雜訊直接變出一張圖太難；拆成很多小步驟，每一步只要去掉一點點雜訊，問題就變簡單了。代價是生成需要很多次網路運算，比較慢 [S3]。→ [[concepts/sampling-speed|取樣加速]]

## 相關頁面
- [[concepts/forward-process|前向過程]]
- [[concepts/training-objective|訓練目標]]：網路到底在學什麼
- [[concepts/text-conditioning|文字條件與 CFG]]：怎麼讓它照文字畫


---
### wiki/concepts/training-objective.md

---
title: 訓練目標：讓網路猜「加了什麼雜訊」
type: concept
sources: [S2, S3]
updated: 2026-11-16
---

# 訓練目標（Training Objective）

## 一次訓練步驟在做什麼
1. 從資料集拿一張真圖片 x₀ [S3]。
2. 隨機挑一個步數 t，再抽一個真的高斯雜訊 ε [S3]。
3. 用 [[concepts/forward-process|前向過程]] 的公式直接算出加了雜訊的 x_t [S2]。
4. 讓網路看 x_t 和 t，**預測加進去的雜訊** [S3]。
5. 用真雜訊和預測雜訊的 **均方誤差（MSE）** 當損失 [S3]。

## 簡化版損失
Ho et al.（2020）發現，用一個忽略加權項的「簡化目標」訓練，效果反而更好 [S2]。這就是現在大家常說的「預測雜訊 + MSE」。

## 白話
就像做「找出照片上被灑了哪些沙子」的練習題：老師（程式）自己灑沙子，所以知道標準答案，學生（網路）負責猜。猜得越準，之後就越會把沙子撥掉。

## 相關頁面
- [[concepts/unet-backbone|U-Net 骨幹]]：負責猜雜訊的那個網路
- [[sources/s1-ddpm|S1 DDPM]]


---
### wiki/concepts/unet-backbone.md

---
title: U-Net 骨幹（Backbone）
type: concept
sources: [S3, S5, S7]
updated: 2026-11-16
---

# U-Net 骨幹

負責去雜訊的網路叫做 backbone，通常是 **U-Net 或 Transformer** [S7]。

## DDPM 用的 U-Net
- DDPM 的作者選了 U-Net（Ronneberger et al., 2015 提出）[S3]。
- U-Net 先把輸入縮小（downsample），再放大回來（upsample）[S3]。
- 中間有 residual 連線，讓梯度比較好傳 [S3]。
- 卷積層之間也加了 attention 模組 [S3]。
- 時間步 t 會被轉成向量（time embedding）餵進網路，讓它知道現在雜訊有多重 [S3]。

## 加上文字以後
Latent Diffusion 在 U-Net 裡加入 **cross-attention** 層，讓文字等條件可以影響生成 [S5]。→ [[concepts/text-conditioning|文字條件與 CFG]]

## 相關頁面
- [[concepts/training-objective|訓練目標]]
- [[concepts/latent-diffusion|Latent Diffusion]]


---
### wiki/concepts/sampling-speed.md

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


---
### wiki/comparisons/ddpm-vs-ddim.md

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


---
### wiki/concepts/latent-diffusion.md

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


---
### wiki/concepts/text-conditioning.md

---
title: 文字條件與 Classifier-Free Guidance（CFG）
type: concept
sources: [S2, S5, S6, S7, S8]
updated: 2026-11-16
---

# 文字條件與 CFG

## 讓模型「照文字畫」
- 文字會先經過文字編碼器（text encoder），再透過 cross-attention 影響去雜訊的網路 [S5][S7]。
- Stable Diffusion 直接用訓練好的 CLIP 文字編碼器，不重新訓練 [S8]。
- 程式裡的 guidance_scale 參數就是用來加強「貼近提示詞」的程度 [S8]。

## Classifier Guidance（舊方法）
要另外訓練一個圖片分類器，用它的梯度把生成結果「推」向指定類別 [S6]。

## Classifier-Free Guidance（CFG）
- 不需要分類器：**同一個模型同時學「有條件」和「無條件」** 的生成 [S6]。
- 做法：訓練時隨機把條件（例如文字）丟掉，讓模型也學會無條件生成 [S2]。
- 生成時把兩種預測組合起來 [S6]。
- 調整 guidance 強度，就是在**品質**和**多樣性**之間取捨 [S6]。

## 白話
CFG 就像問兩次：「照這句話畫會怎樣？」和「隨便畫會怎樣？」，然後把差異放大，讓圖更貼近提示詞；放太大，圖就會比較單調。

## 相關頁面
- [[concepts/latent-diffusion|Latent Diffusion]]
- [[sources/s6-cfg|S6 CFG 論文]]


---
### wiki/comparisons/diffusion-vs-gan-vae.md

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


---
### wiki/timeline.md

---
title: 發展時間軸
type: overview
sources: [S1, S2, S4, S5, S6, S7]
updated: 2026-11-16
---

# 發展時間軸

| 時間 | 事件 | 來源 |
|---|---|---|
| 2015 | 擴散模型首次被提出（Sohl-Dickstein et al.） | [S7] |
| 2019 | NCSN（Song & Ermon）：用不同程度的雜訊訓練 score network | [S2] |
| 2020-06 | DDPM：CIFAR10 FID 3.17 | [S1] |
| 2020-10 | DDIM：取樣快 10～50 倍 | [S4] |
| 2021-12 | Latent Diffusion：在 latent space 做擴散 | [S5] |
| 2022-07 | Classifier-Free Guidance 論文上 arXiv（之前已在 NeurIPS 2021 workshop 發表） | [S6][S2] |

## 相關頁面
- [[overview|總覽]]


---
### wiki/index.md

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


---
### wiki/concepts/stable-diffusion-pipeline.md

---
title: Stable Diffusion 的三個零件
type: concept
sources: [S5, S8]
updated: 2026-11-16
---

# Stable Diffusion 的三個零件

Stable Diffusion 是一種 text-to-image 的 latent diffusion model，由 CompVis、Stability AI 和 LAION 的研究人員做出來，用 512×512 的圖片訓練 [S8]。

## 三個零件
1. **Autoencoder（VAE）**：encoder 把圖片壓成 latent，decoder 再把 latent 還原成圖片 [S8]。
2. **U-Net**：在 latent 上一步一步預測雜訊、去雜訊，並透過 cross-attention 讀文字 [S8]。
3. **文字編碼器**：用現成訓練好的 CLIP 文字編碼器，不重新訓練 [S8]。

## 數字感
- VAE 的縮小倍率是 8：512×512 的圖會變成 64×64（4 個通道）的 latent [S8]。
- 預設取樣 50 步；只用 15 步品質會明顯變差 [S8]。

## 跟論文的關係
Latent Diffusion 論文提出「在預訓練 autoencoder 的 latent space 做擴散」和「用 cross-attention 接文字」這兩個想法 [S5]，Stable Diffusion 就是照這個架構做出來的產品 [S8]。

## 相關頁面
- [[concepts/latent-diffusion|Latent Diffusion]]
- [[concepts/text-conditioning|文字條件與 CFG]]
- [[sources/s8-hf-stable-diffusion|S8 HF Stable Diffusion 部落格]]
