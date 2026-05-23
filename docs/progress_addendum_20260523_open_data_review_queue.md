# 進度補充：官方資料 URL 人工審核佇列

更新時間：2026-05-23 台北時間

## 已完成

PR #153 已合併，官方 open data URL review queue 已進入 main。

已完成內容：

- `dashboard/open-data-review.html`
- `dashboard/data/open_data_url_review_queue.json`
- `config/open_data_url_review_queue_schema.yml`
- `scripts/build_open_data_url_review_queue.py`

## 目前資料狀態

- URL 審核佇列：29 筆。
- traffic_parking：6。
- social_welfare：6。
- culture_events：6。
- public_works_environment：6。
- complaints_service：5。
- public_use_status：internal_url_review_queue。
- url_review_status：needs_manual_url_review。
- crawler_candidate：false。
- crawler_priority：none。
- no_live_crawler：true。
- manual_review_required：true。
- no_auto_publish：true。
- no_personal_data：true。

## 下一階段

建議下一包：

```text
feat/open-data-readiness-report
```

任務方向：

- 建立 readiness score report。
- 新增 `dashboard/open-data-readiness.html`。
- 只做內部排序與人工審核。
- 不啟動 live crawler。
- 不抓私人陳情全文。
- 不抓個資。
- 不自動發布。
