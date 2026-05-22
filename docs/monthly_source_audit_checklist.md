# Monthly Source Audit Checklist

本文件用來規劃每月正式資料來源盤點。目標是定期確認來源是否仍可用、資料是否過期、人工覆核是否完成，以及 dashboard 是否清楚標示資料狀態。

---

## 一、適用範圍

```text
source registry
manual download records
source update status
parser fixtures
parser outputs
review queues
dashboards
weekly system reports
```

本 checklist 不建立自動發布流程，只建立每月內部盤點規格。

---

## 二、每月盤點目標

每月應確認：

1. 來源清單是否仍有效。
2. 來源網址是否仍可人工開啟。
3. 來源使用條款是否有變更。
4. 最新資料日期是否已更新。
5. parser fixture 是否仍代表主要格式。
6. review queue 是否有長期未處理項目。
7. dashboard 是否有缺檔或過期提醒。
8. 對外使用前是否仍需人工確認。

---

## 三、月度稽核報告欄位

未來若建立 monthly source audit report，每份報告至少包含：

```text
audit_id
audit_month
generated_at
source_count
sources_checked
sources_stale
sources_missing_review
sources_with_terms_warning
fixture_status_summary
parser_status_summary
review_backlog_summary
recommended_next_actions
public_use_status
notes
```

---

## 四、狀態建議

`audit_status` 可包含：

```text
ok
needs_attention
source_review_required
parser_review_required
stale_sources_found
```

`public_use_status` 應為：

```text
internal_monthly_source_audit
```

---

## 五、每月人工檢查清單

1. 檢查 source registry 是否有 unknown frequency。
2. 檢查 source update status 是否有 stale 或 check_due。
3. 檢查 manual downloads 是否有未覆核資料。
4. 檢查 parser fixtures 是否有未去識別資料。
5. 檢查 parser output 是否仍為 internal parser output。
6. 檢查 dashboard 是否清楚標示內部用途。
7. 檢查公開引用前是否需要更新來源日期。
8. 檢查是否有需要移除或重新製作的 fixture。

---

## 六、不可做事項

1. 不把月度稽核報告當對外宣傳內容。
2. 不把 stale source 當最新資料。
3. 不因來源無法連線就推論事件不存在。
4. 不自動覆蓋人工覆核結果。
5. 不自動發布新的分析結論。
6. 不忽略授權、個資與使用條款。

---

## 七、測試建議

未來若新增 monthly source audit builder，測試至少涵蓋：

1. 可讀取 source registry 或缺檔時產生 warning。
2. 可讀取 source update status 或缺檔時產生 warning。
3. recommended_next_actions 是 list。
4. warnings 是 list。
5. public_use_status 是 internal_monthly_source_audit。
6. 缺檔不 crash。
7. 報告標示內部用途與人工確認需求。

---

## 八、建議測試指令

```bash
python scripts/build_monthly_source_audit.py
pytest -q tests/test_build_monthly_source_audit.py
pytest -q tests/test_monthly_source_audit_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. 不自動連外。
3. 不自動下載。
4. 不自動發布。
5. 缺檔時輸出 warning。
6. 月度稽核結果清楚標示內部用途。
7. 對外使用前需人工確認。

---

## 十、下一步

合併本 checklist 後，可再推進：

1. monthly source audit builder。
2. monthly source audit dashboard。
3. source maintenance runbook。
4. official source risk register。
