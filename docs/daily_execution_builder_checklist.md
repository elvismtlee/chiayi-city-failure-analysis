# Daily Execution Builder Checklist

本文件用來審查未來 daily execution builder 與 dashboard PR。目標是把一週內容排程轉成一人團隊每天可執行的內部行動清單。

---

## 一、資料流

```text
content schedule draft
  -> daily execution list
  -> human review
  -> daily action
```

第一版只讀本地 JSON，只產生每日任務清單。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_daily_execution_list.py` |
| dashboard data | `dashboard/data/daily_execution_list.json` |
| dashboard page | `dashboard/daily-execution.html` |
| dashboard renderer | `dashboard/daily-execution.js` |
| builder test | `tests/test_build_daily_execution_list.py` |
| page test | `tests/test_daily_execution_page.py` |

---

## 三、daily_execution_list.json 必要欄位

```text
execution_id
date
generated_at
source_files
tasks
review_status
public_use_status
notes
```

每筆 tasks 至少包含：

```text
task_id
time_block
task_type
source_item_id
title
action_steps
estimated_minutes
required_materials
location_hint
review_status
risk_notes
```

---

## 四、任務規則

1. 每日任務數建議 3 到 7 項。
2. task_type 可包含 writing、filming、review、field_visit、dashboard_check。
3. action_steps 應是 list。
4. estimated_minutes 應合理。
5. required_materials 應是 list。
6. review_status 應是 `needs_daily_review`。
7. public_use_status 應是 `internal_daily_plan`。
8. notes 應提醒這是內部執行草稿。

---

## 五、Dashboard 驗收

`dashboard/daily-execution.html` 應顯示：

1. 每日執行清單。
2. 日期。
3. 總任務數。
4. 預估工時。
5. 各任務類型統計。
6. 每筆 task card。

每張 card 至少顯示：

1. `time_block`
2. `task_type`
3. `title`
4. `action_steps`
5. `estimated_minutes`
6. `required_materials`
7. `location_hint`
8. `risk_notes`

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 content schedule builder 後執行：

```bash
python scripts/build_daily_execution_list.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
daily-execution.html
```

---

## 八、測試指令

```bash
python scripts/build_daily_execution_list.py
pytest -q tests/test_build_daily_execution_list.py
pytest -q tests/test_daily_execution_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不輸出私人資料欄位。
5. 文案清楚標示內部每日執行草稿。

---

## 十、下一步

合併 daily execution builder 後，可再推進：

1. public material review dashboard。
2. weekly execution report draft。
3. printable daily action sheet。
4. daily review reminder draft。
