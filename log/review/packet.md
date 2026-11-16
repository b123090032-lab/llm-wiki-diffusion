# 審查包：請你當審查員

你是審查員，不是作者。下面是一份教學簡報每一頁的文字，以及每一頁引用的 wiki 頁全文。
請**只根據這些 wiki 頁**檢查，不要用你自己的知識補充，也不要幫忙改寫：
1. 忠實度：每一頁有沒有說法和 wiki 講反、講過頭（wiki 沒說的也寫上去）、或數字對不上？
2. 覆蓋率：有沒有 wiki 裡很重要、但簡報完全沒提到的概念？
請用表格回覆：頁碼｜問題類型（講反／講過頭／數字錯／缺漏）｜簡報原句｜wiki 怎麼說。沒有問題就回「全部通過」。


## 一、簡報內容


### s1　AI 是怎麼「畫」出一張圖的？（引用：concepts/plain-language）
- 給完全新手的白話入門，大約十分鐘
- 不用會數學，只要看過電視的雪花畫面就好

### s2　你打一句話，AI 就畫出一張圖（引用：concepts/plain-language,overview）
- Stable Diffusion、DALL-E 這些產品，背後用的都是「擴散模型」
- 今天只回答一個問題：它到底是怎麼畫出來的？

### s3　第一步：把照片慢慢變成雪花（引用：concepts/plain-language,concepts/forward-process）
- 每一步在照片上加一點雜訊，最後整張變成一片雜訊
- 就像電視收訊越來越差，畫面變成一片雪花
- 這一步是固定的規則，不用學

### s4　第二步：學會把雪花擦掉（引用：concepts/plain-language,concepts/reverse-process）
- 模型要學的是反過來：從雪花開始，一點一點擦回一張圖
- 就像把影片倒著播

### s5　為什麼要分很多小步？（引用：concepts/plain-language,concepts/reverse-process）
- 每次只擦一點點，事情就變簡單
- 就像擦一片很髒的玻璃，一次擦一點，比一次擦乾淨容易
- 原始論文分成 1000 小步

### s6　它怎麼練習？像寫練習題（引用：concepts/plain-language,concepts/training-objective）
- 程式自己加雪花，所以知道正確答案
- 模型猜「被加了哪些雪花」，跟答案比，錯多少就改多少

### s7　真的畫圖時：從一片雪花開始（引用：concepts/plain-language,concepts/reverse-process）
- 先隨機產生一片雪花，再一次又一次地擦
- 擦完，就是一張新的圖

### s8　怎麼讓它照你的話畫？（引用：concepts/plain-language,concepts/text-conditioning）
- 你打的字會先轉成電腦看得懂的樣子，擦雪花時一起參考
- 有一個「聽話旋鈕」，調高會更像你打的字
- 但這是取捨：越聽話，每張圖的變化就越少

### s9　缺點：畫得很慢（引用：concepts/plain-language,concepts/sampling-speed）
- 要擦很多次，所以畫一張圖要算很多遍
- 產生 5 萬張小圖：擴散模型約 20 小時，另一種方法不到一分鐘
- 後來有人想出新畫法，不用重新練習，就快 10～50 倍

### s10　Stable Diffusion 的妙招：先壓縮再畫（引用：concepts/plain-language,concepts/latent-diffusion）
- 直接在大圖上做太花時間，訓練要用顯示卡算上百天
- 先把 512×512 的圖壓成 64×64 的精簡版，在小的上面擦，最後再還原

### s11　一張圖記住全部（引用：concepts/plain-language,overview）
- ① 把照片變成雪花（固定規則）
- ② 練習把雪花擦掉（要學的部分）
- ③ 從一片新的雪花，擦出一張新的圖

### s12　小測驗：你答得出來嗎？（引用：concepts/plain-language）
- 先想想看，再點一下答案
- Q1 第一步「把照片變成雪花」需要模型去學嗎？→ 不用，那是固定的規則
- Q2 練習的時候，模型在猜什麼？→ 被加了哪些雪花（雜訊）
- Q3 為什麼它畫圖比較慢？→ 因為要擦很多次


## 二、引用到的 wiki 頁全文


---
### wiki/concepts/plain-language.md

---
title: 白話版：給完全新手的擴散模型
type: concept
sources: [S1, S2, S3, S4, S5, S6, S7, S8]
updated: 2026-11-16
---

# 白話版：給完全新手的擴散模型

> 這頁是因為「簡報太難、看不懂」的回饋才新增的。內容全部來自其他 wiki 頁和原始來源，只是把話講白；每一句後面仍然標來源。最下面的比喻是我自己加的，用來幫助理解，不是來源的說法。

## 打字就能出圖的產品，用的就是它
- Stable Diffusion、DALL-E 這些打字就能出圖的產品，背後用的都是擴散模型 [S7]。
- 它們會再加上看懂文字的零件，讓圖照著你打的字來畫 [S7]。

## 第一步：把照片一點一點弄花
- 拿一張真的照片，每一步加一點雜訊，加到最後整張變成一片雜訊 [S3]。
- 這一步是固定的規則，電腦不用學 [S3]。
- 原始論文把這件事分成 1000 小步 [S3]。

## 第二步：學會把雜訊擦掉
- 模型真正要學的是反過來：從一片雜訊開始，一點一點把雜訊擦掉，最後變回一張圖 [S3]。
- 分成很多小步，是因為每一步只擦一點點，事情就變簡單 [S3]。

## 怎麼練習
- 練習時，程式自己在照片上加雜訊，所以知道正確答案是哪些雜訊 [S3]。
- 模型的任務是猜出被加了哪些雜訊，再跟正確答案比，差多少就修正多少 [S3]。

## 真的要畫圖時
- 先隨機產生一片雜訊，再讓模型一次又一次地擦，擦完就是一張新的圖 [S7]。

## 怎麼讓它照你的話畫
- 你打的字會先被轉成電腦看得懂的形式，在擦雜訊的時候一起參考 [S5][S7]。
- 有一個聽話程度的旋鈕（guidance_scale），調高會更貼近你打的字 [S8]。
- 這個旋鈕是在畫得好和每張都不一樣之間做取捨 [S6]。

## 缺點：很慢
- 因為要擦很多次，畫一張圖要算很多遍，這幾乎是它唯一的大缺點 [S3]。
- 舉例：用同一張顯示卡產生 5 萬張小圖，DDPM 大約要 20 小時，GAN 不到一分鐘 [S2]。
- 後來有人想出新的畫法 DDIM，不用重新訓練，就能快 10～50 倍 [S4]。

## Stable Diffusion 的妙招：先壓縮再畫
- 直接在原本大小的圖上做，訓練常常要花上百個 GPU 天（GPU 就是顯示卡）[S5]。
- Stable Diffusion 先把 512×512 的圖壓縮成 64×64 的精簡版，在精簡版上擦雜訊，最後再還原成大圖 [S8]。

## 名字的由來
- 「擴散」這個名字，靈感來自物理學裡的熱力學 [S1]。

## 比喻（我自己加的，不是來源的說法）
加雜訊就像電視收訊越來越差，畫面變成一片雪花；模型學的是反過來，把雪花一點一點擦掉。練習的方式像寫練習題：老師自己灑雪花，所以知道答案，學生負責猜。分很多小步，就像擦一片很髒的玻璃，一次擦一點，比一次擦乾淨容易。「擴散」這兩個字，可以想成一滴墨水在水裡慢慢散開。

## 相關頁面
- [[overview|總覽]]：比較完整的版本
- [[concepts/forward-process|前向過程]]、[[concepts/reverse-process|反向過程]]、[[concepts/training-objective|訓練目標]]
- [[concepts/text-conditioning|文字條件與 CFG]]、[[concepts/sampling-speed|取樣加速]]、[[concepts/latent-diffusion|Latent Diffusion]]


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
- [[concepts/plain-language|白話版（給完全新手）]]
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
