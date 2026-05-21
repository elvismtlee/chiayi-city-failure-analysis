# 嘉義市 12 年城市故障分析資料庫

本專案用來建立「嘉義市 12 年城市故障分析資料庫」，整合嘉義市民 1999 / 陳情資料、嘉義市議會會議紀錄、議員質詢影音、地方生活議題與地理熱點，形成可分析、可追蹤、可視覺化的城市治理資料系統。

## 專案核心

科技分析城市問題，文化理解地方生活，幸福改善市民日常。

## 第一階段目標

1. 建立資料表欄位標準
2. 盤點官方公開資料來源
3. 建立 Python crawler / parser 架構
4. 建立議題分類字典
5. 建立 Google Sheet / Looker Studio / HTML dashboard 對接骨架
6. 建立 n8n 每週自動更新與週報流程

## 資料來源方向

- 嘉義市議會會議紀錄
- 嘉義市議員質詢影音
- 嘉義市政府 1999 / 線上陳情相關公開資訊
- 政府資料開放平台
- 嘉義市政府各局處公開資料
- 地方新聞與公告

## 資料表

主要資料表包含：

- `1999陳情案件`
- `議員質詢`
- `資料源盤點`
- `議題分類字典`
- `地理熱點`
- `投訴質詢對照`
- `儀表板指標`

## 專案結構

```text
chiayi-city-failure-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
├── docs/
│   ├── data_schema.md
│   ├── source_inventory.md
│   ├── n8n_workflows.md
│   └── dashboard_spec.md
├── src/
│   ├── crawlers/
│   ├── parsers/
│   ├── classifiers/
│   └── utils/
├── dashboard/
│   └── index.html
└── tests/
```

## 開發狀態

目前為 v0.1 專案骨架階段。

下一步：

1. 確認資料來源網址與可爬欄位
2. 建立第一批 sample data
3. 撰寫嘉義市議會會議紀錄 crawler
4. 撰寫議題分類器
5. 接 Google Sheet / n8n 自動更新
