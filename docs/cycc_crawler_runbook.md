# 嘉義市議會公開資料 Crawler 執行手冊

本手冊用於手動執行嘉義市議會公開資料 metadata crawler，並檢查輸出是否可以進入內部 dashboard。

## 一、目前定位

此 crawler 只處理公開 metadata，用來建立第一批真實公開資料來源索引。

目前允許範圍：

- 嘉義市議會會議紀錄 metadata
- 嘉義市議會議員質詢影音 metadata
- 來源網址、標題、日期、點閱數、檔案連結或詳情連結

目前不做：

- 不抓非公開資料
- 不抓私人陳情全文
- 不做個人資料彙整
- 不自動發布到公開網站
- 不自動產生競選文案

## 二、執行前檢查

先確認 config 維持安全邊界：

```bash
python -m pytest tests/test_crawl_cycc_public_records.py
```

必須確認：

- `manual_review_required` 是 `true`
- `no_auto_publish` 是 `true`
- `crawl_scope` 是 `metadata_only`
- 來源只限嘉義市議會公開網域

## 三、手動執行 crawler

```bash
python scripts/crawl_cycc_public_records.py
```

預期輸出：

```text
data/raw/cycc_minutes_metadata.csv
data/raw/cycc_question_video_metadata.csv
data/processed/cycc_public_records_crawl_report.json
```

## 四、輸出檢查

執行後先檢查報告：

```bash
python -m json.tool data/processed/cycc_public_records_crawl_report.json
```

必須確認：

- `public_use_status` 是 `internal_crawl_report`
- `manual_review_required` 是 `true`
- `no_auto_publish` 是 `true`
- `crawl_scope` 是 `metadata_only`
- `output_files` 有列出 CSV 檔案
- `record_count` 大於 0 才能進入下一步人工審核

## 五、人工審核清單

提交 crawler 輸出前，人工抽查至少 10 筆資料：

1. 標題是否正常顯示。
2. 連結是否仍指向嘉義市議會公開網域。
3. 日期欄位是否合理。
4. 點閱數欄位是否被誤判為其他數字。
5. 是否出現 phone、email、完整地址或其他個資欄位。
6. 是否出現非公開內容。
7. 是否有大量重複列。

## 六、接入 dashboard 條件

只有符合以下條件，才可把輸出 commit 到 repo 並接入 dashboard：

- 測試通過。
- 人工抽查通過。
- 資料只含公開 metadata。
- 來源與抓取時間清楚。
- 頁面仍標示 internal / manual review。

## 七、下一個工程步驟

第一批輸出通過後，下一個 PR 可以做：

```text
feat/cycc-crawl-output-dashboard
```

目標：

- 將 `cycc_public_records_crawl_report.json` 複製到 `dashboard/data/`
- 在資料來源頁顯示實際抓取筆數
- 顯示最近抓取時間
- 仍標示「內部 metadata，人工審核後才能對外引用」
