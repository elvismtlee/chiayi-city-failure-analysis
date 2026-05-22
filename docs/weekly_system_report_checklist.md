# Weekly System Report Checklist

本文件用來審查未來 weekly system report builder 與 dashboard PR。目標是把 dashboard 健康檢查、總控台狀態、資料產出流程與人工審核 backlog，整理成每週內部系統報告。

---

## 一、資料流

```text
command center overview
dashboard health check
review queues
approved materials
  -> weekly system report
```

第一版只讀本地 JSON，只產生每週內部報告，不對外發布。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_weekly_system_report.py` |
| data | `dashboard/data/weekly_system_report.json` |
| page | `dashboard/weekly-system-report.html` |
| renderer | `dashboard/weekly-system-report.js` |
| builder test | `tests/test_build_weekly_system_report.py` |
| page test | `tests/test_weekly_system_report_page.py` |

---

## 三、weekly_system_report.json 必要欄位

```text
report_id
week_start
week_end
generated_at
source_files
system_status
pipeline_summary
review_backlog_summary
completed_outputs
warnings
recommended_next_actions
public_use_status
notes
```

---

## 四、欄位規則

1. `report_id` 必須穩定。
2. `source_files` 應列出使用到的 JSON。
3. `system_status` 可為 `ok`、`needs_attention`、`incomplete`。
4. `pipeline_summary` 應彙整主要資料流狀態。
5. `review_backlog_summary` 應統計需要人工審核的項目。
6. `completed_outputs` 應列出已產出的 dashboard data。
7. `warnings` 應列出缺檔、空檔或仍為草稿的提醒。
8. `recommended_next_actions` 應是 list。
9. `public_use_status` 應為 `internal_weekly_system_report`。
10. `notes` 應提醒這是內部系統報告。

---

## 五、Dashboard 驗收

`dashboard/weekly-system-report.html` 應顯示：

1. 每週系統報告。
2. 週期起訖。
3. system_status。
4. pipeline_summary。
5. review_backlog_summary。
6. completed_outputs。
7. warnings。
8. recommended_next_actions。

頁面必須提醒：

1. 這是內部系統報告。
2. 不是對外宣傳內容。
3. 不代表資料已完成人工審核。

---

## 六、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
weekly-system-report.html
```

---

## 七、測試指令

```bash
python scripts/build_weekly_system_report.py
pytest -q tests/test_build_weekly_system_report.py
pytest -q tests/test_weekly_system_report_page.py
pytest -q
```

---

## 八、合併條件

1. Python Tests 成功。
2. 只讀本地 JSON。
3. 不自動發布。
4. 不呼叫外部 API。
5. 報告清楚標示內部用途。
6. warnings 能提醒資料仍需人工審核。

---

## 九、下一步

合併 weekly system report 後，可再推進：

1. production launch checklist page。
2. official source intake SOP。
3. reminder draft integration。
4. monthly progress archive。
