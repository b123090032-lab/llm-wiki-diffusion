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
