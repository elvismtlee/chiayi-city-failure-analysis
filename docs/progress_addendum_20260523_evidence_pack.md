# 進度補充：官方資料人工審核證據包

更新時間：2026-05-23 台北時間

## 已完成

PR #169 已合併，官方資料人工審核證據包 Evidence Pack 已進入 main。

PR #170 已合併，Evidence Pack 的 dashboard health check stale warning 已修正。

已完成內容：

- `dashboard/open-data-review-evidence.html`
- `dashboard/data/open_data_review_evidence_pack.json`
- `config/open_data_review_evidence_pack_schema.yml`
- `scripts/build_open_data_review_evidence_pack.py`
- `tests/test_health_check_evidence_pack_status.py`

## 目前資料狀態

- total_count：10。
- evidence_status：not_started 10。
- review_day：day_1 3、day_2 4、day_3 3。
- review_batch：batch_1_high_priority 3、batch_2_standard 4、batch_3_follow_up 3。
- engineering_review_allowed_count：0。
- crawler_execution_allowed：false。
- no_live_crawler：true。
- manual_review_required：true。
- no_auto_publish：true。
- no_personal_data：true。

## Health check 狀態

- `dashboard/data/open_data_review_evidence_pack.json`：valid_json true。
- invalid_json_files：[]。
- warnings：[]。
- status：ok。

## 使用邊界

Evidence Pack 不是 crawler，不代表批准爬取。

目前仍然不啟動 live crawler，不對 source_url 發出網路請求，不抓私人陳情全文，不抓個資，不自動發布。

## 下一階段建議

建議下一包：

```text
feat/open-data-manual-review-result-template
```

任務方向：

- 從 10 筆 Evidence Pack 產生人工審核結果輸入模板。
- 預設 reviewer_name 空白。
- 預設 reviewer_decision: not_decided。
- 預設 engineering_review_allowed: false。
- 預設 crawler_execution_allowed: false。
- 仍然不啟動 live crawler。
