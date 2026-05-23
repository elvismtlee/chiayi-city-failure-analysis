# Day 1 人工審核表單草稿

- 這是 form draft，不是實際審核結果
- 這不是 crawler
- 不啟動 live crawler
- 不對 source_url 發出自動請求
- 不抓個資
- 不抓私人陳情全文
- 不自動發布
- crawler_execution_allowed 永遠 false
- engineering_review_allowed 預設 false
- form draft 不代表批准爬取
- form draft 不代表實際人工審核完成

- day_1 表單數：3

## Form 1：嘉義市兒童課後照顧服務據點

- source_url：https://data.gov.tw/dataset/95735

### reviewer_fields

- reviewer_name
- reviewed_at
- reviewer_notes
- evidence_summary
- reviewer_decision
- follow_up_required
- follow_up_reason
- recommended_next_action

### source_identity_section

- source_url
- page_title_or_dataset_title
- official_owner
- source_owner_matches
- source_identity_notes

### license_terms_section

- license_or_terms_found
- license_or_terms_summary
- license_terms_result
- license_terms_notes

### format_section

- available_format
- format_result
- downloadable_file_observed
- format_notes

### update_cadence_section

- update_cadence_observed
- update_cadence_result
- last_updated_observed
- update_notes

### risk_review_section

- personal_data_result
- personal_data_risk_observed
- private_complaint_result
- private_complaint_risk_observed
- risk_notes

### evidence_summary_section

- evidence_summary
- source_page_screenshot_note
- license_terms_screenshot_note
- format_or_download_link_note
- risk_review_note

### reviewer_decision_section

- reviewer_decision：not_decided
- allowed_values：['not_decided', 'source_verified_but_not_engineering_ready', 'needs_follow_up', 'not_suitable']
- disallowed_values：['ready_for_engineering_review_later', 'approved_for_crawling']

### follow_up_section

- follow_up_required：False
- follow_up_reason：
- recommended_next_action：collect_missing_evidence

- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, reviewer_decision_ready_for_engineering_review, review_status_completed, official_source_verified_without_manual_review

## Form 2：嘉義市社區整體照顧服務體系

- source_url：https://data.gov.tw/dataset/95733

### reviewer_fields

- reviewer_name
- reviewed_at
- reviewer_notes
- evidence_summary
- reviewer_decision
- follow_up_required
- follow_up_reason
- recommended_next_action

### source_identity_section

- source_url
- page_title_or_dataset_title
- official_owner
- source_owner_matches
- source_identity_notes

### license_terms_section

- license_or_terms_found
- license_or_terms_summary
- license_terms_result
- license_terms_notes

### format_section

- available_format
- format_result
- downloadable_file_observed
- format_notes

### update_cadence_section

- update_cadence_observed
- update_cadence_result
- last_updated_observed
- update_notes

### risk_review_section

- personal_data_result
- personal_data_risk_observed
- private_complaint_result
- private_complaint_risk_observed
- risk_notes

### evidence_summary_section

- evidence_summary
- source_page_screenshot_note
- license_terms_screenshot_note
- format_or_download_link_note
- risk_review_note

### reviewer_decision_section

- reviewer_decision：not_decided
- allowed_values：['not_decided', 'source_verified_but_not_engineering_ready', 'needs_follow_up', 'not_suitable']
- disallowed_values：['ready_for_engineering_review_later', 'approved_for_crawling']

### follow_up_section

- follow_up_required：False
- follow_up_reason：
- recommended_next_action：collect_missing_evidence

- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, reviewer_decision_ready_for_engineering_review, review_status_completed, official_source_verified_without_manual_review

## Form 3：嘉義市社區照顧關懷據點

- source_url：https://data.gov.tw/dataset/52404

### reviewer_fields

- reviewer_name
- reviewed_at
- reviewer_notes
- evidence_summary
- reviewer_decision
- follow_up_required
- follow_up_reason
- recommended_next_action

### source_identity_section

- source_url
- page_title_or_dataset_title
- official_owner
- source_owner_matches
- source_identity_notes

### license_terms_section

- license_or_terms_found
- license_or_terms_summary
- license_terms_result
- license_terms_notes

### format_section

- available_format
- format_result
- downloadable_file_observed
- format_notes

### update_cadence_section

- update_cadence_observed
- update_cadence_result
- last_updated_observed
- update_notes

### risk_review_section

- personal_data_result
- personal_data_risk_observed
- private_complaint_result
- private_complaint_risk_observed
- risk_notes

### evidence_summary_section

- evidence_summary
- source_page_screenshot_note
- license_terms_screenshot_note
- format_or_download_link_note
- risk_review_note

### reviewer_decision_section

- reviewer_decision：not_decided
- allowed_values：['not_decided', 'source_verified_but_not_engineering_ready', 'needs_follow_up', 'not_suitable']
- disallowed_values：['ready_for_engineering_review_later', 'approved_for_crawling']

### follow_up_section

- follow_up_required：False
- follow_up_reason：
- recommended_next_action：collect_missing_evidence

- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, reviewer_decision_ready_for_engineering_review, review_status_completed, official_source_verified_without_manual_review

## completion reminder

- 這份文件只示範人工審核表單欄位
- 不可據此視為真實人工審核完成
- crawler_execution_allowed 必須維持 false
- engineering_review_allowed 必須維持 false
