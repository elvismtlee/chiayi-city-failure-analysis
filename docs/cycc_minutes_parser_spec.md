# 嘉義市議會會議紀錄 PDF / HTML 解析規格

本文件推進 issue #1「建立嘉義市議會會議紀錄 crawler」的下一階段。這一版先建立解析契約、fixture 測試與人工 review 流程，不連外部 API，不寫 Google Sheet credential，不放 token，也不處理非公開資料。

---

## 一、目前 metadata crawler 已完成什麼

目前 repo 已具備 CYCC metadata crawler 的第一版基礎：

1. 可從 `config/sources.yml` 定義資料來源。
2. 可整理嘉義市議會會議紀錄與議員質詢影音 metadata。
3. 可輸出 raw CSV，包含來源 ID、標題、來源 URL、屆次、會期、日期等基礎欄位。
4. 已使用 `raw_hash` 作為去重與追蹤基礎。
5. dashboard data pipeline 已可讀取 raw CSV，並在資料不足時保留 fallback output。

下一階段不是重做 metadata crawler，而是在 metadata 指到的公開 PDF / HTML 會議紀錄上，建立可測試、可 review 的內容解析流程。

---

## 二、下一階段要解析哪些欄位

| 欄位 | 說明 | 初始來源 |
|---|---|---|
| `source_id` | 來源唯一識別 | metadata 或 fixture |
| `meeting_name` | 會議名稱 | PDF / HTML 標題或 metadata |
| `meeting_date` | 會議日期，建議 ISO `YYYY-MM-DD` | PDF / HTML 文字或 metadata |
| `councilor_name` | 發言或質詢議員姓名 | 會議紀錄段落 |
| `department` | 回應局處或相關單位 | 會議紀錄段落 |
| `agenda_item` | 議程或討論事項 | 會議紀錄段落 |
| `issue_keywords` | 議題關鍵字 list | parser 初步抽取或人工補正 |
| `source_url` | 公開來源連結 | metadata |
| `raw_text` | 原始段落文字 | PDF / HTML 解析結果 |
| `raw_hash` | 穩定 hash | 由核心欄位產生 |
| `parser_status` | 解析狀態 | parser |
| `review_status` | 人工審核狀態 | 初始 `unreviewed` |

---

## 三、PDF / HTML 兩種來源的解析策略

### HTML 來源

1. 優先讀取標題、日期、議員姓名、局處、議程、來源連結等明確欄位。
2. 若 HTML 有表格，先以表格列作為段落切分單位。
3. 若 HTML 只有純文字區塊，使用標籤文字與段落換行切分。
4. 若欄位缺漏，保留可解析內容並將 `parser_status` 標為需要 review 的狀態。

### PDF 來源

1. 第一階段只從文字層解析，不做 OCR。
2. 每頁文字保留頁碼或段落位置，方便人工回查。
3. 以會議名稱、日期、出席或質詢段落、局處回應段落作為解析錨點。
4. 若 PDF 無文字層或格式破碎，應輸出失敗原因，不假裝成功解析。

---

## 四、欄位 schema

第一版 processed record schema：

```json
{
  "source_id": "CYCC_MINUTES_FIXTURE_HTML",
  "meeting_name": "嘉義市議會第 11 屆第 3 次定期會模擬紀錄",
  "meeting_date": "2026-05-01",
  "councilor_name": "測試議員甲",
  "department": "交通處",
  "agenda_item": "市區道路安全與停車動線專案報告",
  "issue_keywords": ["道路安全", "停車動線"],
  "source_url": "https://www.cycc.gov.tw/public/minutes/sample.html",
  "raw_text": "公開會議紀錄模擬段落。",
  "raw_hash": "sha256 stable hash",
  "parser_status": "parsed_from_fixture",
  "review_status": "unreviewed"
}
```

欄位規則：

1. `issue_keywords` 必須是 list。
2. `raw_hash` 應使用穩定 hash，輸入欄位順序固定。
3. `parser_status` 不得把 fixture 或未 review 解析結果標成正式完成。
4. `review_status` 初始為 `unreviewed`，人工確認後才能改為 `reviewed`。
5. 不輸出敏感欄位，例如 `phone`、`email`、`address`、`national_id`、`id_number`、`full_address`。

---

## 五、raw data、processed data、dashboard data 資料流

```text
公開 CYCC metadata
  -> data/raw/cycc_minutes_metadata.csv
  -> PDF / HTML 內容解析
  -> data/raw/cycc_minutes_content_raw.jsonl
  -> data/processed/cycc_minutes_parsed.json
  -> 人工 review
  -> data/processed/cycc_minutes_reviewed.json
  -> dashboard/data/*
```

本 PR 只建立 fixture-only parser prototype，不新增正式 raw / processed / dashboard output。

---

## 六、不做事項

1. 不寫入 Google Sheet credential。
2. 不把 token、API key、webhook secret 或任何 credential 寫入 repo。
3. 不抓取非公開資料。
4. 不輸出個資欄位。
5. 不呼叫外部 AI API。
6. 不呼叫外部 geocoding API。
7. 不把未經人工 review 的 parser output 當成正式資料。

---

## 七、失敗處理

| 情境 | 處理方式 |
|---|---|
| 缺欄位 | 保留可解析欄位，標記 `parser_status`，送人工 review。 |
| 日期格式錯誤 | 嘗試轉為 ISO 日期；失敗時保留原文並標記需要 review。 |
| 議員姓名缺漏 | 不猜測姓名，標記 `review_status` 仍為 `unreviewed`。 |
| PDF 無法解析 | 記錄失敗原因，不輸出假段落。 |
| HTML 結構變動 | fallback 到純文字段落解析，並新增 fixture 測試覆蓋新結構。 |
| 來源 URL 失效 | 保留 metadata，標記來源需要人工確認。 |

---

## 八、人工 review 流程

1. 先確認來源 URL 是否為公開資料。
2. 比對 `meeting_name`、`meeting_date` 與原始頁面或 PDF。
3. 檢查 `councilor_name` 與 `department` 是否來自原文，不做推測。
4. 檢查 `agenda_item` 與 `issue_keywords` 是否忠實反映段落。
5. 檢查 `raw_text` 是否足以回溯上下文。
6. 若資料可用，將 `review_status` 由 `unreviewed` 改為 `reviewed`。
7. 若資料不完整，保留 `unreviewed` 或標記為需要補 metadata。
8. 若來源不公開或內容不適合使用，排除於正式 processed data。

---

## 九、PR 驗收清單

1. `pytest -q tests/test_parse_cycc_minutes_sample.py` 通過。
2. `pytest -q` 通過。
3. fixture 不含真實個資。
4. parser prototype 不連網。
5. PR 不包含 Google Sheet credential。
6. PR 不包含 token、API key 或 webhook secret。
7. parser output 不含敏感欄位。
8. 未經人工確認的 output 不得標為 `reviewed`。
9. PR 說明需標示 fixture-only、安全限制與後續銜接方式。
