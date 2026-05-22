# Crawler Permission Review Checklist

本文件用來審查未來 crawler / fetcher PR。目標是在任何正式公開資料擷取功能上線前，先確認資料來源、使用條款、頻率、欄位與人工覆核邊界。

---

## 一、適用範圍

```text
public web pages
open data downloads
council records
public complaint records
city project pages
budget or procurement pages
```

第一版應優先使用人工下載、本地 fixture 或小量公開測試資料，不直接大量爬取。

---

## 二、來源權限檢查

每個來源開始自動擷取前，至少確認：

1. 來源是否公開。
2. 是否有 robots.txt 或使用條款限制。
3. 是否允許自動化存取。
4. 是否需要授權或 API key。
5. 是否含個資或敏感欄位。
6. 是否可用人工下載替代。
7. 是否需要降低頻率或分批處理。

---

## 三、建議登記欄位

每個 crawler 設定至少包含：

```text
crawler_id
source_id
source_name
source_url
allowed_access_method
rate_limit_notes
robots_or_terms_reviewed
contains_personal_data_hint
storage_path
review_status
risk_notes
recommended_next_step
```

---

## 四、狀態建議

```text
needs_permission_review
permission_reviewed
manual_download_only
api_required
not_allowed
disabled_until_reviewed
```

---

## 五、不可做事項

1. 不繞過登入、驗證碼、付費牆或技術限制。
2. 不高頻率請求造成來源網站負擔。
3. 不下載非必要的大量資料。
4. 不收集非必要個資。
5. 不把未審核資料直接對外發布。
6. 不把 crawler 失敗當成資料不存在。
7. 不把自動解析結果當正式結論。

---

## 六、Crawler PR 驗收

未來 crawler PR 至少要有：

1. 權限或使用條款備註。
2. 頻率限制說明。
3. timeout 與錯誤處理。
4. user agent 說明。
5. 本地 fixture 測試。
6. 不含 credential。
7. 不把 secrets 寫入 repo。
8. output 進入人工 review queue。

---

## 七、測試建議

```bash
pytest -q tests/test_crawler_permission_review.py
pytest -q
```

測試至少涵蓋：

1. 沒有 credential 或 token 字串。
2. 沒有硬編碼密碼。
3. 有 timeout。
4. 有錯誤處理。
5. 有人工審核狀態。
6. 有 rate limit 或 politeness 設定。
7. fixture 測試不連網。

---

## 八、合併條件

1. Python Tests 成功。
2. 權限審核清楚。
3. 頻率限制清楚。
4. 不繞過限制。
5. 不輸出私人資料欄位。
6. 不自動發布。
7. 對外使用前需人工覆核。

---

## 九、下一步

合併本 checklist 後，可再推進：

1. crawler permission registry sample。
2. source-specific fixture parser。
3. manual download SOP。
4. official data update cadence checklist。
