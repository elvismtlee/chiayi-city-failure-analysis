# Weekly Summary Builder Checklist

本文件用來審查未來 weekly summary draft builder 與 dashboard PR。目標是把 reviewed issue candidates 轉成內部週報草稿，而不是自動發布或正式結論。

---

## 一、預期資料流

```text
cycc_minutes_issue_candidates.json
  -> weekly_summary_draft.json
  -> weekly summary dashboard
  -> human policy review
  -> public material draft
```

第一版可以只使用會議紀錄議題候選資料；後續再加入影音、座標與 1999 資料。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_weekly_summary_draft.py` |
| dashboard data | `dashboard/data/weekly_summary_draft.json` |
| dashboard page | `dashboard/weekly-summary.html` |
| dashboard renderer | `dashboard/weekly-summary.js` |
| builder test | `tests/test_build_weekly_summary_draft.py` |
| page test | `tests/test_weekly_summary_page.py` |

---

## 三、weekly_summary_draft.json 必要欄位

```text
summary_id
week_start
week_end
generated_at
source_files
total_candidates
department_summary
keyword_summary
top_issues
needs_review
suggested_policy_topics
public_use_status
notes
```

驗收重點：

1. `summary_id` 穩定。
2. `source_files` 應列出輸入資料。
3. `total_candidates` 應等於輸入候選數。
4. `department_summary` 應可統計局處。
5. `keyword_summary` 應可統計關鍵字。
6. `top_issues` 應來自 candidates，不可憑空生成。
7. `public_use_status` 應標示 internal draft。
8. `notes` 應提醒需人工確認。

---

## 四、top_issues 必要欄位

```text
issue_id
issue_title
department
issue_keywords
issue_summary
source_count
source_urls
review_status
confidence_level
recommended_follow_up
```

---

## 五、Dashboard 驗收

`dashboard/weekly-summary.html` 應顯示：

1. 週報草稿標題。
2. 週期起訖。
3. 總候選數。
4. 涉及局處數。
5. 高頻關鍵字。
6. top issues。
7. suggested policy topics。
8. needs review 清單。

頁面文案必須提醒：

1. 這是內部草稿。
2. 不是正式結論。
3. 對外使用前需人工審核。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 issue candidates builder 之後執行：

```bash
python scripts/build_weekly_summary_draft.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
weekly-summary.html
```

---

## 八、測試指令

```bash
python scripts/build_weekly_summary_draft.py
pytest -q tests/test_build_weekly_summary_draft.py
pytest -q tests/test_weekly_summary_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不自動發布。
5. 不寄出訊息。
6. 不輸出私人資料欄位。
7. 文案清楚標示內部草稿。

---

## 十、下一步

合併 weekly summary builder 後，可再推進：

1. 社群文案草稿 builder。
2. 政策提案草稿 builder。
3. n8n 每週人工審核通知。
4. dashboard review funnel。
