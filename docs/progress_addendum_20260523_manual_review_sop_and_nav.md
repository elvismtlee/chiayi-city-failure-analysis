# 進度補充：人工審核 SOP 與導覽尺寸修正

更新時間：2026-05-23 台北時間

## 已完成

PR #174 已合併，官方資料第一批人工審核 SOP 已進入 main。

PR #176 已合併，共用導覽第二排按鈕尺寸已修正。

## 新增主線內容

- `dashboard/open-data-manual-review-sop.html`
- `dashboard/data/open_data_manual_review_sop.json`
- `config/open_data_manual_review_sop_schema.yml`
- `scripts/build_open_data_manual_review_sop.py`

## SOP 資料狀態

- total_tasks：10。
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

## 導覽尺寸修正

共用 `shared-nav.js` 已確認保留：

- 第二排按鈕 height：42px。
- 第二排按鈕 min-height：42px。
- 第二排字級：16px。
- line-height：1。
- padding：0 16px。
- active selector 限定為 `.dashboard-nav-tab.active` 與 `.dashboard-nav-link.active`。
- 保留「人工審核 SOP」導覽入口。

## Health check 狀態

- `dashboard/data/dashboard_health_check.json`：status ok。
- warnings：[]。
- missing_files：[]。

## 使用邊界

人工審核 SOP 不是 crawler，不代表批准爬取。

目前仍然不啟動 live crawler，不對 source_url 發出網路請求，不抓私人陳情全文，不抓個資，不自動發布。

## 下一階段建議

建議下一包：

```text
feat/open-data-manual-review-execution-packets
```

任務方向：

- 從人工審核 SOP 與人工審核結果輸入表產生 day_1、day_2、day_3 三份人工審核工作包。
- 產生 dashboard JSON 與 Markdown 工作包文件。
- 保留 shared-nav 第二排按鈕尺寸修正。
- 預設 engineering_review_allowed: false。
- 預設 crawler_execution_allowed: false。
- 仍然不啟動 live crawler。
