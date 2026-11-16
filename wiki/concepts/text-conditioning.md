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
