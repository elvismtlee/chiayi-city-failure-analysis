# 方法論頁規格 v1

本文件定義 `dashboard/methodology.html` 的頁面內容與資料結構。

---

## 頁面定位

```text
分析方法與城市故障分數說明頁
```

用途是讓使用者理解本平台如何進行：

- 議題分類
- 熱點判定
- 城市故障分數
- 趨勢分析
- AI 摘要
- 議員與局處分析

---

## 建議網址

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/methodology.html
```

---

## 頁面主要區塊

### 1. 分析流程

```text
資料來源
→ crawler
→ raw CSV
→ processed CSV
→ JSON
→ dashboard
→ AI 摘要與週報
```

---

### 2. 議題分類方法

使用城市故障分類字典：

- 交通
- 道路
- 人行
- 環境
- 公共安全
- 水利排水
- 市場商圈
- 公園休憩
- 教育學區
- 社福高齡
- 文化觀光
- 行政服務
- 其他

---

### 3. 城市故障分數

公式：

```text
城市故障分數 =
案件量分數
+ 重複率分數
+ 處理時間分數
+ 質詢落差分數
+ 趨勢升高分數
```

---

### 4. 趨勢分析

趨勢類型：

- up
- down
- stable
- spike

時間範圍：

- 7 天
- 30 天
- 90 天
- 半年
- 一年
- 12 年

---

### 5. AI 摘要方法

AI 摘要只用於：

- 整理
- 分類
- 摘要
- 趨勢提示
- 建議追蹤方向

AI 摘要不應用於：

- 無來源指控
- 人身攻擊
- 絕對化結論
- 個人評分
- 支持度推論

---

### 6. 資料限制

必須說明：

1. 資料來源可能不完整。
2. crawler metadata 不等於全文內容。
3. 樣本資料不代表完整趨勢。
4. 統計分析需標示更新時間。
5. 任何正式引用應回到原始來源查證。

---

## 導覽關係

`methodology.html` 應與下列頁面互相連結：

- index.html
- insights.html
- sources.html
- reports.html
