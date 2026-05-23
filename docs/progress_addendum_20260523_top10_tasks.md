# 進度補充：Top 10 官方資料人工審核任務

更新時間：2026-05-23 台北時間

## 已完成

PR #157 已合併，Top 10 官方資料人工審核任務已進入 main。

已完成內容：

- `dashboard/open-data-top10-tasks.html`
- `dashboard/data/open_data_top10_review_tasks.json`
- `config/open_data_top10_review_tasks_schema.yml`
- `scripts/build_open_data_top10_review_tasks.py`

## 目前資料狀態

- total_count：10。
- P1：4。
- P2：3。
- P3：3。
- social_welfare：5。
- public_works_environment：3。
- traffic_parking：1。
- culture_events：1。
- complaints_service：0。
- high readiness：10。
- public_use_status：internal_top10_review_tasks。
- no_live_crawler：true。
- manual_review_required：true。
- no_auto_publish：true。
- no_personal_data：true。

## 使用邊界

Top 10 只是內部工作排序，不代表正式評價或結論。

這份任務清單只供人工審核，不啟動 live crawler，不抓私人陳情全文，不抓個資，不自動發布。

## 下一階段建議

建議下一包：

```text
feat/open-data-crawler-spec-drafts
```

任務方向：

- 從 Top 10 任務產生 crawler spec 草稿。
- 每筆 spec 都必須保持 crawler_execution_allowed: false。
- 只做規格草稿，不真正抓資料。
- 仍然不啟動 live crawler。
