# Day 1 人工審核填寫範例

- 這是 sample，不是實際審核結果
- 這不是 crawler
- 不啟動 live crawler
- 不對 source_url 發出自動請求
- 不抓個資
- 不抓私人陳情全文
- 不自動發布
- crawler_execution_allowed 永遠 false
- engineering_review_allowed 預設 false
- sample 不代表批准爬取
- sample 不代表實際人工審核完成

- day_1 任務數：3

## Sample 1：嘉義市兒童課後照顧服務據點

- source_url：https://data.gov.tw/dataset/95735
- sample_evidence_summary：這是填寫範例，不代表已完成實際人工審核。
- sample_reviewer_notes：範例：請在實際人工審核後，填入來源頁標題、授權摘要、格式觀察、個資風險與私人陳情全文風險。
- fields_not_changed：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, review_status, approval_gate_status, engineering_review_status
- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, reviewer_decision_ready_for_engineering_review, review_status_completed, official_source_verified_without_manual_review

## Sample 2：嘉義市社區整體照顧服務體系

- source_url：https://data.gov.tw/dataset/95733
- sample_evidence_summary：這是填寫範例，不代表已完成實際人工審核。
- sample_reviewer_notes：範例：請在實際人工審核後，填入來源頁標題、授權摘要、格式觀察、個資風險與私人陳情全文風險。
- fields_not_changed：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, review_status, approval_gate_status, engineering_review_status
- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, reviewer_decision_ready_for_engineering_review, review_status_completed, official_source_verified_without_manual_review

## Sample 3：嘉義市社區照顧關懷據點

- source_url：https://data.gov.tw/dataset/52404
- sample_evidence_summary：這是填寫範例，不代表已完成實際人工審核。
- sample_reviewer_notes：範例：請在實際人工審核後，填入來源頁標題、授權摘要、格式觀察、個資風險與私人陳情全文風險。
- fields_not_changed：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, review_status, approval_gate_status, engineering_review_status
- blocked_fields：crawler_execution_allowed, engineering_review_allowed, approved_for_crawling, live_crawler, reviewer_decision_ready_for_engineering_review, review_status_completed, official_source_verified_without_manual_review

## completion reminder

- 這份文件只示範欄位如何填寫
- 不可據此視為真實人工審核完成
- crawler_execution_allowed 必須維持 false
- engineering_review_allowed 必須維持 false
