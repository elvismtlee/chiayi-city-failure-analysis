# 官方資料人工審核工作包 day_1

- 今日任務數：3
- 預估時間：90 分鐘
- review_batch：batch_1_high_priority

## 安全提醒

- 這不是 crawler
- 不啟動 live crawler
- 不對 source_url 發出自動請求
- 不抓個資
- 不抓私人陳情全文
- 不自動發布
- crawler_execution_allowed 永遠 false
- engineering_review_allowed 預設 false

## 今日每筆任務卡

### 任務 1：嘉義市兒童課後照顧服務據點

- topic_group：social_welfare
- source_owner：嘉義市政府社會處
- source_url：https://data.gov.tw/dataset/95735
- recommended_next_action：collect_missing_evidence

#### 應填 evidence 欄位

- source_url
- page_title_or_dataset_title
- official_owner
- official_domain_or_platform
- license_or_terms_summary
- available_format
- update_cadence_observed
- personal_data_risk_observed
- private_complaint_risk_observed
- reviewer_notes
- reviewed_at

#### 應填 result 欄位

- source_opened_result
- official_source_result
- license_terms_result
- format_result
- update_cadence_result
- personal_data_result
- private_complaint_result
- evidence_summary
- reviewer_decision
- reviewer_notes
- follow_up_required
- follow_up_reason
- recommended_next_action

### 任務 2：嘉義市社區整體照顧服務體系

- topic_group：social_welfare
- source_owner：嘉義市政府社會處
- source_url：https://data.gov.tw/dataset/95733
- recommended_next_action：collect_missing_evidence

#### 應填 evidence 欄位

- source_url
- page_title_or_dataset_title
- official_owner
- official_domain_or_platform
- license_or_terms_summary
- available_format
- update_cadence_observed
- personal_data_risk_observed
- private_complaint_risk_observed
- reviewer_notes
- reviewed_at

#### 應填 result 欄位

- source_opened_result
- official_source_result
- license_terms_result
- format_result
- update_cadence_result
- personal_data_result
- private_complaint_result
- evidence_summary
- reviewer_decision
- reviewer_notes
- follow_up_required
- follow_up_reason
- recommended_next_action

### 任務 3：嘉義市社區照顧關懷據點

- topic_group：social_welfare
- source_owner：嘉義市政府社會處
- source_url：https://data.gov.tw/dataset/52404
- recommended_next_action：collect_missing_evidence

#### 應填 evidence 欄位

- source_url
- page_title_or_dataset_title
- official_owner
- official_domain_or_platform
- license_or_terms_summary
- available_format
- update_cadence_observed
- personal_data_risk_observed
- private_complaint_risk_observed
- reviewer_notes
- reviewed_at

#### 應填 result 欄位

- source_opened_result
- official_source_result
- license_terms_result
- format_result
- update_cadence_result
- personal_data_result
- private_complaint_result
- evidence_summary
- reviewer_decision
- reviewer_notes
- follow_up_required
- follow_up_reason
- recommended_next_action

## completion checklist

## 完成檢查清單

- 每筆 source_url 已人工開啟
- 每筆官方來源已人工確認
- 每筆授權或條款已人工記錄
- 每筆格式已人工確認
- 每筆更新頻率已人工記錄
- 每筆個資風險已人工確認
- 每筆私人陳情全文風險已人工確認
- 每筆 reviewer_notes 已完成
- crawler_execution_allowed 仍為 false
- engineering_review_allowed 仍為 false

## handoff next actions

- update_human_review_workbook_later
- update_engineering_checklist_later
- prepare_manual_review_summary_later
- request_follow_up_if_license_unclear
- block_item_if_risk_found

