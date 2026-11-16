# 白話版簡報：簡報文字 ↔ wiki 原文 對照表（2026-11-16 重做後）

給人工抽查用：程式只能確認右欄的原文存在，這張表用來看左欄有沒有講過頭。

| 頁 | 簡報文字 | wiki 頁 | wiki 原文 |
|---|---|---|---|
| 2 | Stable Diffusion、DALL-E 這些產品，背後用的都是「擴散模型」 | concepts/plain-language | Stable Diffusion、DALL-E 這些打字就能出圖的產品，背後用的都是擴散模型 |
| 3 | 每一步在照片上加一點雜訊，最後整張變成一片雜訊 | concepts/plain-language | 每一步加一點雜訊，加到最後整張變成一片雜訊 |
| 3 | 這一步是固定的規則，不用學 | concepts/plain-language | 這一步是固定的規則，電腦不用學 |
| 4 | 模型要學的是反過來：從雪花開始，一點一點擦回一張圖 | concepts/plain-language | 從一片雜訊開始，一點一點把雜訊擦掉，最後變回一張圖 |
| 5 | 每次只擦一點點，事情就變簡單 | concepts/plain-language | 每一步只擦一點點，事情就變簡單 |
| 5 | 原始論文分成 1000 小步 | concepts/plain-language | 原始論文把這件事分成 1000 小步 |
| 6 | 程式自己加雪花，所以知道正確答案 | concepts/plain-language | 程式自己在照片上加雜訊，所以知道正確答案是哪些雜訊 |
| 6 | 模型猜「被加了哪些雪花」，跟答案比，錯多少就改多少 | concepts/plain-language | 模型的任務是猜出被加了哪些雜訊，再跟正確答案比，差多少就修正多少 |
| 7 | 先隨機產生一片雪花，再一次又一次地擦 | concepts/plain-language | 先隨機產生一片雜訊，再讓模型一次又一次地擦 |
| 7 | 擦完，就是一張新的圖 | concepts/plain-language | 擦完就是一張新的圖 |
| 8 | 你打的字會先轉成電腦看得懂的樣子，擦雪花時一起參考 | concepts/plain-language | 你打的字會先被轉成電腦看得懂的形式，在擦雜訊的時候一起參考 |
| 8 | 有一個「聽話旋鈕」，調高會更像你打的字 | concepts/plain-language | 有一個聽話程度的旋鈕（guidance_scale），調高會更貼近你打的字 |
| 8 | 但這是取捨：越聽話，每張圖的變化就越少 | concepts/plain-language | 這個旋鈕是在畫得好和每張都不一樣之間做取捨 |
| 9 | 要擦很多次，所以畫一張圖要算很多遍 | concepts/plain-language | 因為要擦很多次，畫一張圖要算很多遍 |
| 9 | 產生 5 萬張小圖：擴散模型約 20 小時，另一種方法不到一分鐘 | concepts/plain-language | 產生 5 萬張小圖，DDPM 大約要 20 小時，GAN 不到一分鐘 |
| 9 | 後來有人想出新畫法，不用重新練習，就快 10～50 倍 | concepts/plain-language | 後來有人想出新的畫法 DDIM，不用重新訓練，就能快 10～50 倍 |
| 10 | 直接在大圖上做太花時間，訓練要用顯示卡算上百天 | concepts/plain-language | 直接在原本大小的圖上做，訓練常常要花上百個 GPU 天（GPU 就是顯示卡） |
| 10 | 先把 512×512 的圖壓成 64×64 的精簡版，在小的上面擦，最後再還原 | concepts/plain-language | 先把 512×512 的圖壓縮成 64×64 的精簡版，在精簡版上擦雜訊，最後再還原成大圖 |
| 11 | 把照片變成雪花（固定規則） | concepts/plain-language | 這一步是固定的規則，電腦不用學 |
| 11 | 練習把雪花擦掉（要學的部分） | concepts/plain-language | 模型真正要學的是反過來 |
| 11 | 從一片新的雪花，擦出一張新的圖 | concepts/plain-language | 先隨機產生一片雜訊，再讓模型一次又一次地擦，擦完就是一張新的圖 |
| 12 | 不用，那是固定的規則 | concepts/plain-language | 這一步是固定的規則，電腦不用學 |
| 12 | 被加了哪些雪花（雜訊） | concepts/plain-language | 猜出被加了哪些雜訊 |
| 12 | 因為要擦很多次 | concepts/plain-language | 因為要擦很多次，畫一張圖要算很多遍 |
