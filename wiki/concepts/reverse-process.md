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
