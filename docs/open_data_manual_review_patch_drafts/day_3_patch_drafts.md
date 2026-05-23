# 人工審核結果回填 Patch 草稿 day_3

- 今日 patch 數：3
- 這不是 crawler
- 不啟動 live crawler
- 不對 source_url 發出自動請求
- 不抓個資
- 不抓私人陳情全文
- 不自動發布
- crawler_execution_allowed 永遠 false
- engineering_review_allowed 預設 false
- patch draft 不代表批准爬取

## Patch 1：嘉義市藝文場域

- result_id：open-data-manual-review-result-08
- source_url：https://data.gov.tw/en/datasets/52546
- fields_requiring_manual_input：source_opened_result, official_source_result, license_terms_result, format_result, update_cadence_result, personal_data_result, private_complaint_result, evidence_summary, reviewer_decision, reviewer_notes, reviewed_at
- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler

### source_result_patch 摘要

- source_opened_result：not_checked
- official_source_result：not_checked
- license_terms_result：not_checked
- format_result：not_checked
- update_cadence_result：not_checked
- personal_data_result：not_checked
- private_complaint_result：not_checked
- evidence_summary：
- reviewer_decision：not_decided
- reviewer_notes：
- follow_up_required：False
- follow_up_reason：
- recommended_next_action：collect_missing_evidence

### human_review_workbook_patch 摘要

- source_opened：False
- official_source_verified：False
- license_reviewed：False
- terms_reviewed：False
- format_checked：False
- sample_download_checked：False
- personal_data_checked：False
- private_complaint_checked：False
- robots_or_terms_checked：False
- review_status：not_started
- approval_gate_status：pending_manual_review
- engineering_review_allowed：False
- crawler_execution_allowed：False

### engineering_checklist_patch 摘要

- source_review_gate：not_checked
- license_review_gate：not_checked
- format_review_gate：not_checked
- personal_data_gate：not_checked
- private_complaint_gate：not_checked
- terms_gate：not_checked
- parser_design_gate：not_checked
- output_schema_gate：not_checked
- rate_limit_gate：not_checked
- rollback_plan_gate：not_checked
- logging_plan_gate：not_checked
- human_approval_gate：not_checked
- engineering_review_status：waiting_for_human_review
- engineering_review_allowed：False
- crawler_execution_allowed：False

### completion reminder

- 完成後仍需人工另開 PR 回填相關欄位
- crawler_execution_allowed 仍須維持 false
- engineering_review_allowed 仍須維持 false

## Patch 2：嘉義市公有路外停車場資訊

- result_id：open-data-manual-review-result-09
- source_url：https://data.chiayi.gov.tw/opendata/dataset/metadata?oid=d206db33-3ae7-489e-b709-5555222fb767
- fields_requiring_manual_input：source_opened_result, official_source_result, license_terms_result, format_result, update_cadence_result, personal_data_result, private_complaint_result, evidence_summary, reviewer_decision, reviewer_notes, reviewed_at
- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler

### source_result_patch 摘要

- source_opened_result：not_checked
- official_source_result：not_checked
- license_terms_result：not_checked
- format_result：not_checked
- update_cadence_result：not_checked
- personal_data_result：not_checked
- private_complaint_result：not_checked
- evidence_summary：
- reviewer_decision：not_decided
- reviewer_notes：
- follow_up_required：False
- follow_up_reason：
- recommended_next_action：collect_missing_evidence

### human_review_workbook_patch 摘要

- source_opened：False
- official_source_verified：False
- license_reviewed：False
- terms_reviewed：False
- format_checked：False
- sample_download_checked：False
- personal_data_checked：False
- private_complaint_checked：False
- robots_or_terms_checked：False
- review_status：not_started
- approval_gate_status：pending_manual_review
- engineering_review_allowed：False
- crawler_execution_allowed：False

### engineering_checklist_patch 摘要

- source_review_gate：not_checked
- license_review_gate：not_checked
- format_review_gate：not_checked
- personal_data_gate：not_checked
- private_complaint_gate：not_checked
- terms_gate：not_checked
- parser_design_gate：not_checked
- output_schema_gate：not_checked
- rate_limit_gate：not_checked
- rollback_plan_gate：not_checked
- logging_plan_gate：not_checked
- human_approval_gate：not_checked
- engineering_review_status：waiting_for_human_review
- engineering_review_allowed：False
- crawler_execution_allowed：False

### completion reminder

- 完成後仍需人工另開 PR 回填相關欄位
- crawler_execution_allowed 仍須維持 false
- engineering_review_allowed 仍須維持 false

## Patch 3：嘉義市重要環保統計資料

- result_id：open-data-manual-review-result-10
- source_url：https://data.moenv.gov.tw/dataset/detail/STAT_P_22
- fields_requiring_manual_input：source_opened_result, official_source_result, license_terms_result, format_result, update_cadence_result, personal_data_result, private_complaint_result, evidence_summary, reviewer_decision, reviewer_notes, reviewed_at
- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler

### source_result_patch 摘要

- source_opened_result：not_checked
- official_source_result：not_checked
- license_terms_result：not_checked
- format_result：not_checked
- update_cadence_result：not_checked
- personal_data_result：not_checked
- private_complaint_result：not_checked
- evidence_summary：
- reviewer_decision：not_decided
- reviewer_notes：
- follow_up_required：False
- follow_up_reason：
- recommended_next_action：collect_missing_evidence

### human_review_workbook_patch 摘要

- source_opened：False
- official_source_verified：False
- license_reviewed：False
- terms_reviewed：False
- format_checked：False
- sample_download_checked：False
- personal_data_checked：False
- private_complaint_checked：False
- robots_or_terms_checked：False
- review_status：not_started
- approval_gate_status：pending_manual_review
- engineering_review_allowed：False
- crawler_execution_allowed：False

### engineering_checklist_patch 摘要

- source_review_gate：not_checked
- license_review_gate：not_checked
- format_review_gate：not_checked
- personal_data_gate：not_checked
- private_complaint_gate：not_checked
- terms_gate：not_checked
- parser_design_gate：not_checked
- output_schema_gate：not_checked
- rate_limit_gate：not_checked
- rollback_plan_gate：not_checked
- logging_plan_gate：not_checked
- human_approval_gate：not_checked
- engineering_review_status：waiting_for_human_review
- engineering_review_allowed：False
- crawler_execution_allowed：False

### completion reminder

- 完成後仍需人工另開 PR 回填相關欄位
- crawler_execution_allowed 仍須維持 false
- engineering_review_allowed 仍須維持 false

