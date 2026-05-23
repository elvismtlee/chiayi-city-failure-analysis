# 進度補充：人工審核工作包

更新時間：2026-05-23 台北時間

## 已完成

PR #178 已合併，官方資料人工審核工作包已進入 main。

已完成內容：

- `dashboard/open-data-manual-review-packets.html`
- `dashboard/data/open_data_manual_review_execution_packets.json`
- `config/open_data_manual_review_execution_packets_schema.yml`
- `scripts/build_open_data_manual_review_execution_packets.py`
- `docs/open_data_manual_review_packets/day_1_packet.md`
- `docs/open_data_manual_review_packets/day_2_packet.md`
- `docs/open_data_manual_review_packets/day_3_packet.md`

## 目前資料狀態

- total_tasks：10。
- packet_count：3。
- review_day：day_1 3、day_2 4、day_3 3。
- review_batch：batch_1_high_priority 3、batch_2_standard 4、batch_3_follow_up 3。
- topic_group：social_welfare 5、public_works_environment 3、traffic_parking 1、culture_events 1。
- estimated_total_minutes：285。
- engineering_review_allowed_count：0。
- crawler_execution_allowed：false。
- no_live_crawler：true。
- manual_review_required：true。
- no_auto_publish：true。
- no_personal_data：true。

## Markdown 工作包

- day_1_packet.md：3 筆，90 分鐘。
- day_2_packet.md：4 筆，120 分鐘。
- day_3_packet.md：3 筆，75 分鐘。

每份文件都明確標示：不是 crawler、不啟動 live crawler、不對 source_url 發出自動請求、不抓個資、不抓私人陳情全文、不自動發布。

## 使用邊界

人工審核工作包不是 crawler，不代表批准爬取。

目前仍然不啟動 live crawler，不對 source_url 發出網路請求，不抓私人陳情全文，不抓個資，不自動發布。

## 下一階段建議

建議下一包：

```text
feat/open-data-manual-review-result-patch-drafts
```

任務方向：

- 從人工審核工作包與人工審核結果輸入模板產生回填 Patch 草稿。
- 只產生 patch draft，不實際改審核結果。
- 預設 engineering_review_allowed: false。
- 預設 crawler_execution_allowed: false。
- 仍然不啟動 live crawler。
