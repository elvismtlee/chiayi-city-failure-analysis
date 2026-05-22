# Command Center Overview Checklist

本文件用來審查未來 command center overview dashboard PR。目標是把城市故障分析資料庫、會議紀錄流程、內容產出流程與人工審核流程，彙整成一個總控頁，方便一人團隊每天快速掌握狀態。

---

## 一、預期資料流

```text
issue candidates
weekly summary
policy drafts
social drafts
video scripts
filming checklists
content schedule
daily execution
public review
approved materials
  -> command center overview
```

第一版只讀本地 JSON，只顯示狀態，不自動發布或修改資料。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_command_center_overview.py` |
| dashboard data | `dashboard/data/command_center_overview.json` |
| dashboard page | `dashboard/command-center.html` |
| dashboard renderer | `dashboard/command-center.js` |
| builder test | `tests/test_build_command_center_overview.py` |
| page test | `tests/test_command_center_page.py` |

---

## 三、command_center_overview.json 必要欄位

```text
overview_id
generated_at
source_files
pipeline_status
key_counts
review_backlog
next_actions
warnings
public_use_status
notes
```

---

## 四、pipeline_status 建議欄位

```text
minutes_review
issue_candidates
weekly_summary
policy_drafts
social_drafts
video_scripts
filming_checklists
content_schedule
daily_execution
public_review
approved_materials
```

每個 pipeline item 至少包含：

```text
name
status
record_count
source_file
last_updated_hint
next_step
```

---

## 五、Dashboard 驗收

`dashboard/command-center.html` 應顯示：

1. 競選資料總控台。
2. 各資料流狀態。
3. key counts。
4. review backlog。
5. next actions。
6. warnings。
7. 各 dashboard 入口連結。

頁面必須提醒：

1. 本頁是內部作戰總覽。
2. 顯示的是 sample / draft / internal review 狀態。
3. 對外使用前仍需人工確認。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在所有 builder 後執行：

```bash
python scripts/build_command_center_overview.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
command-center.html
```

建議把 command center 放在 nav 前段，但不要大幅重排既有頁面。

---

## 八、測試指令

```bash
python scripts/build_command_center_overview.py
pytest -q tests/test_build_command_center_overview.py
pytest -q tests/test_command_center_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不自動發布。
5. 不呼叫平台 API。
6. 不輸出私人資料欄位。
7. 頁面清楚標示內部總覽。
8. warnings 能提醒缺檔或資料仍為草稿。
9. 所有輸出標示 `internal dashboard / needs human review / manual publishing only`。
10. 不把 dashboard 說成民調或支持度調查。

---

## 十、下一步

合併 command center overview 後，可再推進：

1. one-person daily operations page。
2. weekly report archive。
3. n8n reminder draft integration。
4. dashboard health check summary。
