# 簡報大綱（人類確認關卡）

- 主題：AI 是怎麼「畫」出一張圖的？（擴散模型白話入門）
- 對象：**完全沒基礎的新手**（沒學過程式的高中生也要看得懂）
- 目標：看完 12 頁，能用自己的話講出「把照片變成雪花 → 練習把雪花擦掉 → 從新的雪花擦出新的圖」，並知道它的缺點是慢。
- 長度：約 10 分鐘，12 頁
- 規則：**只能用 wiki/ 的內容**（主要是 concepts/plain-language 白話版）；每頁標出用到哪幾頁 wiki；數字一定要有出處；不放公式和數學符號；每頁只講一件事。

| 頁 | 標題 | 要講的重點 | 用到的 wiki 頁 |
|---|---|---|---|
| 1 | 封面 | AI 是怎麼畫圖的 | concepts/plain-language |
| 2 | 你打一句話，AI 就畫出圖 | 這些產品背後都是擴散模型 | concepts/plain-language, overview |
| 3 | 第一步：照片變雪花 | 一步一步加雜訊；固定規則不用學 | concepts/plain-language, concepts/forward-process |
| 4 | 第二步：學會擦掉雪花 | 反過來，一點一點擦回圖 | concepts/plain-language, concepts/reverse-process |
| 5 | 為什麼分很多小步 | 每次擦一點比較簡單；1000 小步 | concepts/plain-language, concepts/reverse-process |
| 6 | 怎麼練習 | 自己加雪花所以有答案；猜雪花、對答案 | concepts/plain-language, concepts/training-objective |
| 7 | 真的畫圖時 | 從隨機雪花開始擦 | concepts/plain-language, concepts/reverse-process |
| 8 | 照你的話畫 | 文字一起參考；聽話旋鈕的取捨 | concepts/plain-language, concepts/text-conditioning |
| 9 | 缺點：很慢 | 要擦很多次；20 小時 vs 不到一分鐘；新畫法快 10～50 倍 | concepts/plain-language, concepts/sampling-speed |
| 10 | 先壓縮再畫 | 512×512 壓成 64×64 再擦 | concepts/plain-language, concepts/latent-diffusion |
| 11 | 一張圖記住全部 | 三步驟總結 | concepts/plain-language, overview |
| 12 | 小測驗 | 3 題，點一下看答案 | concepts/plain-language |

## 確認紀錄
- 2026-11-16：第一版大綱定案為 15 頁（之後才寫逐頁內容）。
- 2026-11-16：穎看完第一版說「簡報太難、看不懂，要更簡單」。退回「寫大綱」重做：改成 12 頁白話版，拿掉公式、雜訊排程、U-Net、時間軸、GAN／VAE 比較；新增 wiki 白話頁 concepts/plain-language（每句仍有來源）。第一版內容留在 git 歷史（commit c73539f）。
