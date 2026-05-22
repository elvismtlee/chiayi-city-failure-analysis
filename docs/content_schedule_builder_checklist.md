# Content Schedule Builder Checklist

本文件用來審查未來 content schedule builder 與 dashboard PR。目標是把社群草稿、短影音腳本與拍攝清單整理成一週內部執行排程，而不是自動發布。

---

## 一、預期資料流

```text
social post drafts
short video script drafts
filming checklists
  -> content schedule draft
  -> human review
  -> daily execution list
  -> manual publishing
```

第一版只讀本地 JSON，只產生排程草稿，不接任何平台 API。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_content_schedule.py` |
| dashboard data | `dashboard/data/content_schedule.json` |
| dashboard page | `dashboard/content-schedule.html` |
| dashboard renderer | `dashboard/content-schedule.js` |
| builder test | `tests/test_build_content_schedule.py` |
| page test | `tests/test_content_schedule_page.py` |

---

## 三、content_schedule.json 必要欄位

```text
schedule_id
week_start
week_end
generated_at
source_files
items
review_status
public_use_status
notes
```

每筆 items 至少包含：

```text
item_id
day
slot
content_type
source_id
title
channel_or_format
action_needed
estimated_minutes
review_status
risk_notes
```

---

## 四、排程規則

1. 每天最多安排 1 到 3 個項目。
2. content_type 可包含 social_post、short_video、filming_task。
3. estimated_minutes 應合理，一人團隊可執行。
4. review_status 應是 `needs_schedule_review`。
5. public_use_status 應是 `internal_schedule_draft`。
6. notes 應提醒這只是內部排程草稿。

---

## 五、Dashboard 驗收

`dashboard/content-schedule.html` 應顯示：

1. 一週內容排程草稿。
2. 週期起訖。
3. 總排程項目。
4. 各類型項目數。
5. 每日排程清單。
6. 需要人工審核項目。

頁面必須提醒：

1. 這是內部排程草稿。
2. 不是自動發布排程。
3. 發布前需人工確認。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 social / video / filming builders 後執行：

```bash
python scripts/build_content_schedule.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
content-schedule.html
```

---

## 八、測試指令

```bash
python scripts/build_content_schedule.py
pytest -q tests/test_build_content_schedule.py
pytest -q tests/test_content_schedule_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不自動發布。
5. 不呼叫平台 API。
6. 不寄出訊息。
7. 不輸出私人資料欄位。
8. 文案清楚標示內部排程草稿。

---

## 十、下一步

合併 content schedule builder 後，可再推進：

1. daily execution checklist。
2. public material review dashboard。
3. n8n 每週人工審核通知。
4. printable daily action sheet。
