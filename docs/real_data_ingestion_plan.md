# 真實資料匯入基礎計畫

本文件說明目前 dashboard 資料狀態，以及從 prototype / fixture data 進入真實公開資料爬蟲的工程步驟。

## 一、目前狀態

目前 dashboard 主要用於驗證資料欄位結構、dashboard 呈現方式、內部人工審核流程、內容產出與公開前審核流程、health check 與 CI 保護。

目前資料不得宣稱為完整 12 年真實資料庫。

## 二、本 PR 新增內容

- `config/real_data_sources.yml`：定義真實資料來源 manifest。所有來源預設 `crawl_enabled: false`。
- `scripts/plan_real_data_ingestion.py`：讀取 manifest，檢查每個來源是否可爬，產出內部 plan。
- `tests/test_real_data_ingestion_plan.py`：確認尚未人工審核前不會啟用 crawler。

## 三、資料來源優先順序

### 1. 嘉義市議會公開資料

用途：會議紀錄、議程、質詢 metadata、可公開引用的議事資訊。

下一步：人工確認嘉義市議會公開資料 URL，確認格式後建立 source-specific crawler。

### 2. 嘉義市 1999 或市民陳情公開統計

用途：申訴類別、局處統計、時間趨勢、地點或行政區彙整資料。

限制：優先使用公開統計資料，不匯入私人陳情全文，不匯入電話、email、私人地址、身分證字號等個資。

### 3. 嘉義市政府開放資料

用途：交通、停車、公共工程、長照、兒少、治安、環境、商圈、文化活動。

## 四、安全原則

1. 只抓公開來源。
2. 不抓登入後資料。
3. 不繞過防爬限制。
4. 不收集私人個資。
5. 不把原型資料稱為真實統計。
6. 不自動公開發布。
7. 所有對外內容都需人工 review。

## 五、建議下一個 PR

下一個 PR 可做：

```text
feat/cycc-public-records-crawler
```

建議內容：先建立 `scripts/crawl_cycc_public_records.py`，只抓公開 metadata，產出 `data/raw/cycc_meetings/source_index.json`，並加測試確認 parser 可處理 fixture HTML / PDF metadata。
