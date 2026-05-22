# CYCC Public Records Crawler

本文件定義下一個真實資料 PR 的最小範圍：只抓嘉義市議會公開資料的 metadata，不碰 1999 私人陳情全文，不抓個資，不自動公開發布。

## 範圍

本 PR 只處理：

- 嘉義市議會會議紀錄 metadata
- 嘉義市議會議員質詢影音 metadata

本 PR 不處理：

- 1999 私人陳情全文
- 非公開檔案
- PDF 全文解析
- 自動摘要
- 自動社群發布
- 自動寄信

## 主要檔案

- `config/cycc_public_records.yml`
- `scripts/crawl_cycc_public_records.py`
- `src/crawlers/cycc_metadata_crawler.py`
- `tests/test_crawl_cycc_public_records.py`

## 安全邊界

1. 只允許 `cycc.gov.tw` 與 `cycc.digital.th.gov.tw` 公開網址。
2. 只允許 metadata crawler。
3. 不建立 1999 或陳情全文匯入。
4. 不儲存 phone、email、address、donor、volunteer 等個資或敏感資料。
5. `manual_review_required` 必須維持 `true`。
6. `no_auto_publish` 必須維持 `true`。

## 執行方式

```bash
python scripts/crawl_cycc_public_records.py
```

預期輸出：

- `data/raw/cycc_minutes_metadata.csv`
- `data/raw/cycc_question_video_metadata.csv`
- `data/processed/cycc_public_records_crawl_report.json`

## 下一步

這一版合併後，下一個擴充可做：

1. `cycc_minutes` 詳細頁 parser
2. agenda metadata crawler
3. official source registry / intake queue
4. PDF / DOC metadata normalization

但仍不應碰 1999 私人陳情全文。
