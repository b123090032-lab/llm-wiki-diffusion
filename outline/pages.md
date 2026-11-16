# 逐頁內容（由大綱展開；產生簡報時只讀這份）

格式：`{{顯示文字||wiki頁||wiki原文片段}}` 表示這句話的出處。沒有標記的句子只能是提問、比喻或過場，不能放新的事實。
白話版規則（2026-11-16 穎回饋「太難」後加的）：每頁只講一件事、最多 3 句、不放公式和數學符號、專有名詞能不用就不用。

## 1 | AI 是怎麼「畫」出一張圖的？
wiki: concepts/plain-language
visual: cover
~ 給完全新手的白話入門，大約十分鐘
~ 不用會數學，只要看過電視的雪花畫面就好

## 2 | 你打一句話，AI 就畫出一張圖
wiki: concepts/plain-language, overview
visual: prompt
- {{Stable Diffusion、DALL-E 這些產品，背後用的都是「擴散模型」||concepts/plain-language||Stable Diffusion、DALL-E 這些打字就能出圖的產品，背後用的都是擴散模型}}
- 今天只回答一個問題：它到底是怎麼畫出來的？

## 3 | 第一步：把照片慢慢變成雪花
wiki: concepts/plain-language, concepts/forward-process
visual: noise-strip
- {{每一步在照片上加一點雜訊，最後整張變成一片雜訊||concepts/plain-language||每一步加一點雜訊，加到最後整張變成一片雜訊}}
- 就像電視收訊越來越差，畫面變成一片雪花
- {{這一步是固定的規則，不用學||concepts/plain-language||這一步是固定的規則，電腦不用學}}

## 4 | 第二步：學會把雪花擦掉
wiki: concepts/plain-language, concepts/reverse-process
visual: reverse-strip
- {{模型要學的是反過來：從雪花開始，一點一點擦回一張圖||concepts/plain-language||從一片雜訊開始，一點一點把雜訊擦掉，最後變回一張圖}}
- 就像把影片倒著播

## 5 | 為什麼要分很多小步？
wiki: concepts/plain-language, concepts/reverse-process
visual: stairs
- {{每次只擦一點點，事情就變簡單||concepts/plain-language||每一步只擦一點點，事情就變簡單}}
- 就像擦一片很髒的玻璃，一次擦一點，比一次擦乾淨容易
- {{原始論文分成 1000 小步||concepts/plain-language||原始論文把這件事分成 1000 小步}}

## 6 | 它怎麼練習？像寫練習題
wiki: concepts/plain-language, concepts/training-objective
visual: train-loop
- {{程式自己加雪花，所以知道正確答案||concepts/plain-language||程式自己在照片上加雜訊，所以知道正確答案是哪些雜訊}}
- {{模型猜「被加了哪些雪花」，跟答案比，錯多少就改多少||concepts/plain-language||模型的任務是猜出被加了哪些雜訊，再跟正確答案比，差多少就修正多少}}

## 7 | 真的畫圖時：從一片雪花開始
wiki: concepts/plain-language, concepts/reverse-process
visual: draw
- {{先隨機產生一片雪花，再一次又一次地擦||concepts/plain-language||先隨機產生一片雜訊，再讓模型一次又一次地擦}}
- {{擦完，就是一張新的圖||concepts/plain-language||擦完就是一張新的圖}}

## 8 | 怎麼讓它照你的話畫？
wiki: concepts/plain-language, concepts/text-conditioning
visual: knob
- {{你打的字會先轉成電腦看得懂的樣子，擦雪花時一起參考||concepts/plain-language||你打的字會先被轉成電腦看得懂的形式，在擦雜訊的時候一起參考}}
- {{有一個「聽話旋鈕」，調高會更像你打的字||concepts/plain-language||有一個聽話程度的旋鈕（guidance_scale），調高會更貼近你打的字}}
- {{但這是取捨：越聽話，每張圖的變化就越少||concepts/plain-language||這個旋鈕是在畫得好和每張都不一樣之間做取捨}}

## 9 | 缺點：畫得很慢
wiki: concepts/plain-language, concepts/sampling-speed
visual: speed
- {{要擦很多次，所以畫一張圖要算很多遍||concepts/plain-language||因為要擦很多次，畫一張圖要算很多遍}}
- {{產生 5 萬張小圖：擴散模型約 20 小時，另一種方法不到一分鐘||concepts/plain-language||產生 5 萬張小圖，DDPM 大約要 20 小時，GAN 不到一分鐘}}
- {{後來有人想出新畫法，不用重新練習，就快 10～50 倍||concepts/plain-language||後來有人想出新的畫法 DDIM，不用重新訓練，就能快 10～50 倍}}

## 10 | Stable Diffusion 的妙招：先壓縮再畫
wiki: concepts/plain-language, concepts/latent-diffusion
visual: latent
- {{直接在大圖上做太花時間，訓練要用顯示卡算上百天||concepts/plain-language||直接在原本大小的圖上做，訓練常常要花上百個 GPU 天（GPU 就是顯示卡）}}
- {{先把 512×512 的圖壓成 64×64 的精簡版，在小的上面擦，最後再還原||concepts/plain-language||先把 512×512 的圖壓縮成 64×64 的精簡版，在精簡版上擦雜訊，最後再還原成大圖}}

## 11 | 一張圖記住全部
wiki: concepts/plain-language, overview
visual: summary
- ① {{把照片變成雪花（固定規則）||concepts/plain-language||這一步是固定的規則，電腦不用學}}
- ② {{練習把雪花擦掉（要學的部分）||concepts/plain-language||模型真正要學的是反過來}}
- ③ {{從一片新的雪花，擦出一張新的圖||concepts/plain-language||先隨機產生一片雜訊，再讓模型一次又一次地擦，擦完就是一張新的圖}}

## 12 | 小測驗：你答得出來嗎？
wiki: concepts/plain-language
visual: quiz
~ 先想想看，再點一下答案
- Q1 第一步「把照片變成雪花」需要模型去學嗎？→ {{不用，那是固定的規則||concepts/plain-language||這一步是固定的規則，電腦不用學}}
- Q2 練習的時候，模型在猜什麼？→ {{被加了哪些雪花（雜訊）||concepts/plain-language||猜出被加了哪些雜訊}}
- Q3 為什麼它畫圖比較慢？→ {{因為要擦很多次||concepts/plain-language||因為要擦很多次，畫一張圖要算很多遍}}
