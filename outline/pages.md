# 逐頁內容（由大綱展開；產生簡報時只讀這份）

格式：`{{顯示文字||wiki頁||wiki原文片段}}` 表示這句話的出處。沒有標記的句子只能是提問、比喻或過場，不能放新的事實。

## 1 | 擴散模型是怎麼生成圖片的？
wiki: overview
visual: cover
~ 一份給新手的 10 分鐘入門
~ 用我自己整理的 LLM Wiki（8 個來源）做成

## 2 | 一句話原理
wiki: overview
visual: one-line
- {{先學會「把雜訊一點一點擦掉」||overview||先學會「把雜訊一點一點擦掉」}}
- {{生成時從一張純雜訊開始，一步一步擦成一張圖||overview||生成時就從一張純雜訊開始，一步一步擦成一張圖}}
- 想像成：把一張被雪花雜訊蓋滿的電視畫面，慢慢調回清楚的影像

## 3 | 兩個過程
wiki: overview
visual: two-process
- {{擴散模型由前向過程和反向過程組成||overview||由兩個部分組成：前向擴散過程（forward diffusion process）和反向取樣過程}}
- 前向：{{每一步加一點高斯雜訊，加到最後變成純雜訊||overview||每一步加一點高斯雜訊，加到最後變成純雜訊}}，{{這個過程是固定的，不用學||overview||這個過程是固定的，不用學}}
- 反向：{{訓練神經網路從純雜訊一步一步把雜訊拿掉||overview||訓練一個神經網路，從純雜訊開始一步一步把雜訊拿掉}}

## 4 | 前向過程：一步一步加雜訊
wiki: concepts/forward-process
visual: noise-strip
- 從真圖片 x₀ 出發，得到 x₁、x₂……{{一直到 x_T||concepts/forward-process||一直到 x_T}}
- {{DDPM 的總步數是 T = 1000||concepts/forward-process||T = 1000}}
- 小技巧：{{可以用公式直接算出任意第 t 步的 x_t||concepts/forward-process||可以用公式直接算出任意第 t 步的 x_t}}，訓練時不用真的一步一步加
- 名字由來：{{靈感來自非平衡熱力學||concepts/forward-process||靈感來自非平衡熱力學}}，就像墨水在水裡擴散

## 5 | 雜訊排程：每一步加多少？
wiki: concepts/noise-schedule
visual: schedule
- {{每一步加多少雜訊由 β_t 控制||concepts/noise-schedule||由一組 β_t 控制}}
- {{DDPM 用 linear schedule：β 從 0.0001 增加到 0.02||concepts/noise-schedule||β 從 **0.0001** 線性增加到 **0.02**}}
- {{也可以用 cosine 等其他排程||concepts/noise-schedule||排程可以是 linear、quadratic、cosine 等}}
- 一開始加一點點，後面越加越多

## 6 | 反向過程：從雜訊還原成圖片
wiki: concepts/reverse-process
visual: reverse-strip
- {{反向過程是要學的那一半||concepts/reverse-process||反向過程是**要學的**那一半}}
- {{生成時先隨機抽一張純雜訊，再重複套用去雜訊網路||concepts/reverse-process||先隨機抽一張純雜訊，然後重複套用去雜訊網路}}
- {{每一步網路都會拿到目前的 x_t 和步數 t||concepts/reverse-process||每一步網路都會拿到「目前這張圖 x_t」和「現在是第幾步 t」}}
- 為什麼分很多步？{{每一步只要去掉一點點雜訊，問題就變簡單||concepts/reverse-process||每一步只要去掉一點點雜訊，問題就變簡單了}}

## 7 | 訓練時到底在學什麼？
wiki: concepts/training-objective
visual: train-loop
- 程式自己加雜訊，所以知道「標準答案」
- {{網路看 x_t 和 t，預測加進去的雜訊||concepts/training-objective||讓網路看 x_t 和 t，**預測加進去的雜訊**}}
- {{損失 = 真雜訊和預測雜訊的均方誤差（MSE）||concepts/training-objective||用真雜訊和預測雜訊的 **均方誤差（MSE）** 當損失}}
- {{Ho 等人發現簡化版損失效果更好||concepts/training-objective||用一個忽略加權項的「簡化目標」訓練，效果反而更好}}

## 8 | 誰在猜雜訊？U-Net
wiki: concepts/unet-backbone
visual: unet
- {{去雜訊的網路叫 backbone，通常是 U-Net 或 Transformer||concepts/unet-backbone||通常是 **U-Net 或 Transformer**}}
- {{U-Net 先把輸入縮小，再放大回來||concepts/unet-backbone||U-Net 先把輸入縮小（downsample），再放大回來（upsample）}}
- {{中間有 residual 連線||concepts/unet-backbone||中間有 residual 連線}}，{{也加了 attention||concepts/unet-backbone||卷積層之間也加了 attention 模組}}
- {{時間步 t 會轉成向量餵進網路||concepts/unet-backbone||時間步 t 會被轉成向量（time embedding）餵進網路}}

## 9 | 為什麼慢？怎麼變快？
wiki: concepts/sampling-speed, comparisons/ddpm-vs-ddim
visual: speed
- {{在 2080 Ti 上，DDPM 生 5 萬張小圖約 20 小時，GAN 不到一分鐘||concepts/sampling-speed||DDPM 產生 5 萬張 32×32 的圖大約要 20 小時，GAN 不到一分鐘}}
- {{DDIM 跟 DDPM 用同樣的訓練方式，只換取樣方法||concepts/sampling-speed||跟 DDPM 用**同樣的訓練方式**，只換取樣方法}}
- {{DDIM 速度快 10～50 倍||comparisons/ddpm-vs-ddim||快 10～50 倍}}
- {{Stable Diffusion 預設取樣 50 步，只用 15 步品質就會明顯變差||concepts/sampling-speed||Stable Diffusion 預設取樣 50 步，但只用 15 步品質會明顯變差}}

## 10 | Latent Diffusion：先壓縮，再擴散
wiki: concepts/latent-diffusion
visual: latent
- 問題：{{直接在像素上做擴散，訓練常常要上百個 GPU 天||concepts/latent-diffusion||訓練強的擴散模型常常要花上百個 GPU 天}}
- {{用預訓練的 autoencoder 把圖片壓縮成 latent||concepts/latent-diffusion||把圖片壓縮成比較小的 latent}}
- {{在 latent 上擴散，成本更低、更快||concepts/latent-diffusion||擴散和去雜訊都在 latent 上做，訓練成本更低、生成更快}}
- {{以 Stable Diffusion 為例：512×512 的圖會變成 64×64 的 latent||concepts/latent-diffusion||512×512 的圖會變成 64×64 的 latent}}

## 11 | 怎麼讓它「照著文字畫」？
wiki: concepts/text-conditioning
visual: cfg
- {{文字先經過 text encoder，再透過 cross-attention 影響去雜訊網路||concepts/text-conditioning||文字會先經過文字編碼器（text encoder），再透過 cross-attention 影響去雜訊的網路}}
- {{CFG：同一個模型同時學「有條件」和「無條件」||concepts/text-conditioning||同一個模型同時學「有條件」和「無條件」}}
- {{訓練時隨機把文字丟掉||concepts/text-conditioning||訓練時隨機把條件（例如文字）丟掉}}
- {{guidance 調越大越貼近提示詞，但太大圖會比較單調||concepts/text-conditioning||放太大，圖就會比較單調}}

## 12 | 跟 GAN、VAE 比一比
wiki: comparisons/diffusion-vs-gan-vae
visual: compare
- {{三種模型都是把簡單的雜訊轉成資料||comparisons/diffusion-vs-gan-vae||都是把簡單分布的雜訊轉換成資料樣本}}
- {{GAN 訓練可能不穩、多樣性較低||comparisons/diffusion-vs-gan-vae||訓練可能不穩、多樣性較低}}
- {{DDPM 不用對抗式訓練就能做出高品質圖片||comparisons/diffusion-vs-gan-vae||DDPM 不用對抗式訓練就能做出高品質圖片}}
- 代價：{{生成要很多步，比較慢||comparisons/diffusion-vs-gan-vae||生成要很多步，慢}}

## 13 | 發展時間軸
wiki: timeline
visual: timeline
- {{2015：擴散模型首次被提出||timeline||2015 | 擴散模型首次被提出}}
- {{2020-06：DDPM（FID 3.17）||timeline||DDPM：CIFAR10 FID 3.17}}；{{2020-10：DDIM||timeline||DDIM：取樣快 10～50 倍}}
- {{2021-12：Latent Diffusion||timeline||Latent Diffusion：在 latent space 做擴散}}
- {{2022：Classifier-Free Guidance 論文上 arXiv||timeline||Classifier-Free Guidance 論文上 arXiv}}

## 14 | 小測驗：你答得出來嗎？
wiki: overview, concepts/training-objective, concepts/text-conditioning
visual: quiz
- Q1 前向過程需要訓練嗎？→ {{不用，它是固定的||overview||這個過程是固定的，不用學}}
- Q2 網路訓練時在猜什麼？→ {{加進去的雜訊||concepts/training-objective||預測加進去的雜訊}}
- Q3 CFG 調太大會怎樣？→ {{更貼近提示詞，但圖會比較單調||concepts/text-conditioning||讓圖更貼近提示詞；放太大，圖就會比較單調}}

## 15 | 總結＋延伸閱讀
wiki: index, concepts/stable-diffusion-pipeline
visual: summary
- 加雜訊（固定）→ 學去雜訊（訓練）→ 從雜訊生成（取樣）
- Stable Diffusion = {{VAE||concepts/stable-diffusion-pipeline||**Autoencoder（VAE）**：encoder 把圖片壓成 latent}} + {{U-Net||concepts/stable-diffusion-pipeline||**U-Net**：在 latent 上一步一步預測雜訊}} + {{CLIP 文字編碼器||concepts/stable-diffusion-pipeline||用現成訓練好的 CLIP 文字編碼器}}
- 想看更多：打開我的 Wiki 索引，每一頁都有原始來源
