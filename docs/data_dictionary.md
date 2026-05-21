# 資料欄位字典 v1

本文件定義本專案主要資料表與 JSON 的欄位標準。

---

## 1. cycc_minutes_metadata.csv

嘉義市議會會議紀錄 metadata。

| 欄位 | 類型 | 說明 |
|---|---|---|
| source | string | 資料來源名稱 |
| source_url | string | 原始頁面 URL |
| title | string | 會議紀錄標題 |
| date | date/string | 會議日期 |
| term | string | 屆次 |
| session | string | 會期 |
| meeting_type | string | 會議類型 |
| file_url | string | 附件或全文 URL |
| crawled_at | datetime | 抓取時間 |

---

## 2. cycc_question_video_metadata.csv

嘉義市議員質詢影音 metadata。

| 欄位 | 類型 | 說明 |
|---|---|---|
| source | string | 資料來源名稱 |
| source_url | string | 原始頁面 URL |
| title | string | 影音標題 |
| date | date/string | 質詢日期 |
| councilor_name | string | 議員姓名 |
| term | string | 屆次 |
| session | string | 會期 |
| video_url | string | 影音連結 |
| crawled_at | datetime | 抓取時間 |

---

## 3. dashboard_summary.json

首頁 KPI 與資料狀態。

| 欄位 | 類型 | 說明 |
|---|---|---|
| updated_at | datetime/string | 更新時間 |
| total_cases | number | 案件或資料總數 |
| top_issue | string | 主要議題 |
| total_hotspots | number | 熱點數 |
| total_questions | number | 議員質詢 metadata 數 |
| data_status | string | mock / processed / verified |
| notes | string | 補充說明 |

---

## 4. issue_ranking.json

議題排行。

| 欄位 | 類型 | 說明 |
|---|---|---|
| issue | string | 議題名稱 |
| issue_code | string | 議題分類 code |
| count | number | 件數 |
| percent | number | 比例 |
| trend | string | up / down / stable / spike |
| summary | string | 簡短說明 |

---

## 5. hotspots.json

城市故障熱點。

| 欄位 | 類型 | 說明 |
|---|---|---|
| name | string | 熱點名稱 |
| district | string | 行政區 |
| category | string | 議題類別 |
| score | number | 城市故障分數 |
| department | string | 可能相關局處 |
| action | string | 建議行動 |
| lat | number/null | 緯度 |
| lng | number/null | 經度 |
| source | string | 資料來源 |

---

## 6. ai_issue_summary.json

AI 城市觀察摘要。

| 欄位 | 類型 | 說明 |
|---|---|---|
| updated_at | datetime/string | 更新時間 |
| summary_title | string | 摘要標題 |
| summary | string | 摘要內容 |
| top_findings | array | 重點發現 |
| recommended_actions | array | 建議行動 |
| data_status | string | mock / processed / verified |

---

## 7. issue_trends.json

議題趨勢。

| 欄位 | 類型 | 說明 |
|---|---|---|
| issue | string | 議題名稱 |
| issue_code | string | 議題 code |
| trend | string | up / down / stable / spike |
| change_percent | number | 變化百分比 |
| district | string | 區域 |
| summary | string | 趨勢說明 |
| recommended_action | string | 建議行動 |

---

## 8. data_sources.json

資料來源狀態。

| 欄位 | 類型 | 說明 |
|---|---|---|
| source_name | string | 資料來源名稱 |
| source_type | string | 官方資料 / 開放資料 / 使用者回報 / prototype |
| status | string | planned / crawling / processed / verified / published |
| latest_update | string | 最近更新時間 |
| record_count | number | 筆數 |
| source_url | string | 來源網址 |
| notes | string | 資料限制 |

---

## 9. reports_index.json

城市週報列表。

| 欄位 | 類型 | 說明 |
|---|---|---|
| report_id | string | 週報 ID |
| title | string | 週報標題 |
| week_start | date/string | 週期開始 |
| week_end | date/string | 週期結束 |
| top_issue | string | 本週主要議題 |
| summary | string | 摘要 |
| report_url | string | 週報連結 |

---

## 欄位命名原則

1. 使用 snake_case。
2. 時間欄位用 `updated_at`、`created_at`、`crawled_at`。
3. 來源欄位保留 `source` 或 `source_url`。
4. 對外顯示名稱與內部 code 分開。
5. 若資料不明，使用 null，不要填入誤導性資料。

---

## 資料狀態

| status | 說明 |
|---|---|
| mock | 原型假資料 |
| raw | 原始抓取資料 |
| processed | 已處理資料 |
| verified | 已人工檢查 |
| published | 已公開發布 |
