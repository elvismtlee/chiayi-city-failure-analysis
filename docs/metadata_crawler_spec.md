# Metadata Crawler 規格 v1

本文件定義第一階段 crawler 的目標：先抓 metadata，不急著解析全文。

## 為什麼先抓 metadata？

1. 最穩定
2. 最容易測試
3. 最快建立資料庫雛形
4. 可先支援 dashboard
5. 後續再接 PDF parser / transcript / AI 摘要

---

## 來源一：嘉義市議會會議紀錄檢索

設定來源：`config/sources.yml > sources.cycc.targets.minutes`

### 輸出檔案

```text
data/raw/cycc_minutes_metadata.csv
```

### 欄位

| 欄位 | 說明 |
|---|---|
| source_id | 固定為 CYCC_MINUTES |
| title | 會議紀錄標題 |
| department | 公告單位 |
| views | 點閱數 |
| updated_at | 更新時間 |
| detail_url | 詳細頁連結 |
| file_url | PDF 或附件連結，若無則空白 |
| crawled_at | crawler 執行時間 |
| raw_hash | 原始資料 hash，用於去重 |

---

## 來源二：議員質詢影音專區

設定來源：`config/sources.yml > sources.cycc.targets.question_videos`

### 輸出檔案

```text
data/raw/cycc_question_video_metadata.csv
```

### 欄位

| 欄位 | 說明 |
|---|---|
| source_id | 固定為 CYCC_QUESTION_VIDEO |
| councilor_name | 議員姓名 |
| council_term | 屆次 |
| session_name | 會期 |
| video_title | 影音標題 |
| video_url | 影音連結 |
| meeting_date | 會議日期，若無法解析則空白 |
| topic_guess | 從標題初步判斷議題 |
| crawled_at | crawler 執行時間 |
| raw_hash | 原始資料 hash，用於去重 |

---

## 去重規則

每筆資料建立 `raw_hash`：

```text
hash(title + detail_url + updated_at)
```

或：

```text
hash(video_title + video_url + councilor_name)
```

---

## 第一階段驗收標準

crawler 必須能做到：

1. 讀取 `config/sources.yml`
2. 送出 HTTP request
3. 解析列表 metadata
4. 輸出 CSV
5. 重跑不產生重複資料
6. pytest 通過
7. GitHub Actions 通過

---

## 不在第一階段做的事

以下先不做：

- PDF 全文解析
- 影音轉文字
- AI 長文摘要
- 地理座標轉換
- 自動發文

這些等 metadata 穩定後再做。
