# Source Update Cadence Checklist

本文件用來規劃正式公開資料來源的更新頻率、人工確認節點與過期資料提醒。目標是避免 dashboard 使用過期資料、未審核資料或未確認來源狀態的資料。

---

## 一、適用範圍

```text
source registry
manual downloads
parser fixtures
parser outputs
review queues
dashboards
weekly system reports
```

本 checklist 不建立自動爬蟲，只規劃更新節奏與人工確認流程。

---

## 二、來源更新頻率分類

每個 source 應標示建議更新頻率：

```text
daily
weekly
monthly
quarterly
annual
event_based
manual_only
unknown
```

---

## 三、來源更新紀錄必要欄位

未來若建立 update registry，每筆至少包含：

```text
source_id
source_name
expected_update_frequency
last_checked_at
last_updated_at
last_reviewed_at
next_check_due
update_status
review_status
staleness_warning
notes
```

---

## 四、狀態規則

`update_status` 可包含：

```text
up_to_date
check_due
stale
source_unavailable
manual_review_needed
unknown
```

`review_status` 可包含：

```text
needs_update_review
update_reviewed
needs_source_review
internal_only
```

---

## 五、staleness 規則建議

1. daily 來源：超過 3 天未確認，標示 `check_due`。
2. weekly 來源：超過 14 天未確認，標示 `check_due`。
3. monthly 來源：超過 45 天未確認，標示 `check_due`。
4. quarterly 來源：超過 120 天未確認，標示 `check_due`。
5. annual 來源：超過 400 天未確認，標示 `check_due`。
6. manual_only 或 unknown 來源：dashboard 應明確顯示人工確認需求。

---

## 六、Dashboard 顯示要求

任何對外前的內部 dashboard 若使用正式來源資料，應顯示：

1. source_name。
2. last_checked_at。
3. last_reviewed_at。
4. update_status。
5. staleness_warning。
6. public_use_status。

頁面必須提醒：

1. 這是內部資料狀態提醒。
2. 不代表資料已完成最新官方確認。
3. 對外使用前需人工確認來源與日期。

---

## 七、不可做事項

1. 不把過期資料當最新狀態。
2. 不把來源無法連線解讀為事件不存在。
3. 不自動覆蓋人工審核資料。
4. 不在未審核前自動發布新資料分析。
5. 不忽略來源授權與使用條款。

---

## 八、測試建議

未來若新增 update cadence builder，測試至少涵蓋：

1. 可讀取 source registry。
2. 可產生 update status summary。
3. 缺少 last_checked_at 不 crash。
4. stale / check_due 規則正確。
5. warnings 是 list。
6. public_use_status 是 internal_source_update_status。
7. dashboard 顯示人工確認提醒。

---

## 九、建議測試指令

```bash
python scripts/build_source_update_status.py
pytest -q tests/test_build_source_update_status.py
pytest -q tests/test_source_update_status_page.py
pytest -q
```

---

## 十、合併條件

1. Python Tests 成功。
2. 不自動連外。
3. 不自動下載。
4. 不自動發布。
5. 過期資料提醒清楚。
6. 來源更新狀態需人工確認。

---

## 十一、下一步

合併本 checklist 後，可再推進：

1. source update status builder。
2. source update dashboard。
3. monthly source audit report。
4. official source maintenance runbook。
