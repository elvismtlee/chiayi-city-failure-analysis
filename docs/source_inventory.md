# 嘉義城市故障資料來源盤點 v1

更新日期：2026-05-21

本文件整理「嘉義市 12 年城市故障分析資料庫」可能使用的資料來源。

---

## 目的

在正式大量爬取資料前，先建立資料來源盤點，避免：

1. 不清楚來源是否合法公開。
2. crawler 抓錯資料。
3. 把個資或敏感內容公開。
4. 不知道資料更新頻率。
5. 無法追溯原始資料。

---

## 1. 嘉義市議會全球資訊網

首頁：<https://www.cycc.gov.tw/Default.aspx>

可用入口：

- 會議紀錄檢索
- 議決案檢索
- 本屆議事錄
- 議員質詢影音專區
- 議事日程表
- 新聞資料
- 公告訊息

優先級：最高

用途：

- 建立議員質詢資料表
- 建立會議紀錄資料表
- 建立議題 / 局處 / 議員對照
- 形成投訴 vs 質詢對照分析

### 1.1 會議紀錄

| 項目 | 內容 |
|---|---|
| source_name | 嘉義市議會會議紀錄 |
| source_type | 官方公開資料 |
| data_type | metadata / file / text |
| priority | high |
| risk | low |
| access_method | crawler |
| notes | 第一階段先抓 metadata，後續再做全文解析。 |

### 1.2 議員質詢影音

| 項目 | 內容 |
|---|---|
| source_name | 嘉義市議員質詢影音 |
| source_type | 官方公開資料 |
| data_type | metadata / video link |
| priority | high |
| risk | medium |
| access_method | crawler |
| notes | 先做 metadata，不直接下載影音。若要語音轉文字需另行規劃。 |

---

## 2. 嘉義市政府

首頁：<https://www.chiayi.gov.tw/>

待盤點：

- 1999 服務資訊
- 線上陳情系統
- 市政信箱
- 各局處公告
- 施政成果
- 統計資訊

優先級：高

注意：1999 或陳情逐案明細可能未完整公開，需用公開資料、資訊公開申請或統計報告補足。

### 2.1 1999 / 陳情案件

| 項目 | 內容 |
|---|---|
| source_name | 嘉義市政府 1999 / 陳情案件 |
| source_type | 官方資料 / 待確認 |
| data_type | case data |
| priority | very_high |
| risk | high |
| access_method | unknown |
| notes | 需確認是否公開、是否有個資、是否可再利用。 |

### 2.2 市府公開統計

| 項目 | 內容 |
|---|---|
| source_name | 嘉義市政府公開統計 |
| source_type | 官方公開資料 |
| data_type | statistical data |
| priority | medium |
| risk | low |
| access_method | crawler / manual_download |
| notes | 可補充人口、交通、區域背景資料。 |

---

## 3. 政府資料開放平台

首頁：<https://data.gov.tw/>

搜尋關鍵字：

- 嘉義市 1999
- 嘉義市 陳情
- 嘉義市 交通
- 嘉義市 道路
- 嘉義市 環保
- 嘉義市 路燈
- 嘉義市 公園
- 嘉義市 停車

優先級：高

用途：

- 補足 CSV / JSON / API 資料
- 與議會質詢資料交叉比對
- 建立交通、道路、環境與公共設施背景資料

| 項目 | 內容 |
|---|---|
| source_name | 政府資料開放平台 |
| source_type | 開放資料 |
| data_type | CSV / JSON / API |
| priority | high |
| risk | low |
| access_method | api / manual_download |
| notes | 需確認授權、更新頻率與欄位。 |

---

## 4. 地方回報資料

### 4.1 城市故障回報表單

| 項目 | 內容 |
|---|---|
| source_name | 城市故障回報表單 |
| source_type | 使用者回報 |
| possible_url | https://www.chiayi2026.com/ |
| data_type | form submission |
| priority | high |
| risk | high |
| access_method | WordPress / SureForms / Google Sheet |
| notes | 必須去識別化後才能公開。 |

### 4.2 西區意見牆

| 項目 | 內容 |
|---|---|
| source_name | 西區意見牆 |
| source_type | 使用者回報 / 意見徵集 |
| possible_url | https://www.chiayi2026.com/ |
| data_type | form submission / text |
| priority | medium |
| risk | high |
| access_method | WordPress / SureForms / Google Sheet |
| notes | 不稱為民調，不公開個資。 |

---

## 5. 地方新聞與公開資訊

用途：

- 議題補充
- 年度事件脈絡
- 熱點驗證

注意：新聞只能作為輔助資料，正式分析仍以官方資料為主。

| 項目 | 內容 |
|---|---|
| source_name | 地方新聞與公開資訊 |
| source_type | 新聞 / 公開資訊 |
| data_type | text / url |
| priority | low |
| risk | medium |
| access_method | manual_review |
| notes | 不直接作為統計主來源，避免新聞偏誤。 |

---

## 6. 補充地理資料

### 6.1 地標與 POI

| 項目 | 內容 |
|---|---|
| source_name | 嘉義市地標 / POI seed list |
| source_type | 人工整理 / 開放資料 |
| data_type | location index |
| priority | medium |
| risk | low |
| access_method | manual_seed / open_data |
| notes | 用於地點標準化與熱點地圖。 |

### 6.2 行政區與里界

| 項目 | 內容 |
|---|---|
| source_name | 嘉義市行政區 / 里界 GeoJSON |
| source_type | 開放資料 / 待確認 |
| data_type | GeoJSON |
| priority | medium |
| risk | low |
| access_method | open_data / manual_download |
| notes | 用於地圖 layer 與里別統計。 |

---

## 優先接入順序

```text
1. 嘉義市議會會議紀錄 metadata
2. 嘉義市議員質詢影音 metadata
3. 政府資料開放平台嘉義市資料
4. 1999 / 陳情資料來源盤點
5. 地標 seed list
6. 城市故障回報去識別化資料
7. 里界 / 路段 GeoJSON
```

---

## 每個資料來源都應記錄

```json
{
  "source_name": "",
  "source_type": "",
  "source_url": "",
  "access_method": "crawler / api / manual_download / form",
  "update_frequency": "unknown",
  "license_or_terms": "unknown",
  "contains_personal_data": false,
  "risk_level": "low / medium / high",
  "status": "planned"
}
```

---

## 注意事項

1. 來源不明的資料不可放進正式 dashboard。
2. 可能含個資的資料不可直接公開。
3. 影音資料先做 metadata，不要直接下載大量影音。
4. crawler 應尊重網站負載，不做高頻請求。
5. 所有資料應保留 source_url 與 crawled_at。
6. 新聞只能作為輔助脈絡，不應作為主要統計依據。
7. 使用者回報資料必須先去識別化再公開。
