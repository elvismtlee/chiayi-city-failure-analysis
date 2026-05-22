# Production Readiness Checklist

本文件用來審查未來 production readiness PR。目標是把目前可展示的城市故障分析與內容產出資料流，整理成可長期維護前的檢查表。

---

## 一、檢查範圍

```text
data builders
dashboard pages
JSON data outputs
workflow runs
tests
docs
review boundaries
```

---

## 二、資料產生器檢查

每個 builder 應符合：

1. 可從 repo root 執行。
2. 輸出路徑固定。
3. 必要欄位有驗證。
4. 不輸出私人資料欄位。
5. 不把 sample / draft 說成正式結論。
6. 有對應 pytest。

---

## 三、Dashboard 檢查

每個 dashboard page 應符合：

1. HTML 存在。
2. JS 存在。
3. 讀取正確 JSON。
4. 有空資料狀態。
5. 有人工審核提醒。
6. 有清楚標題。
7. 手機版基本可讀。
8. 已加入 site map 與 shared nav。

---

## 四、Workflow 檢查

Dashboard Data workflow 應符合：

1. builder 執行順序正確。
2. 新增 builder 後有納入 workflow。
3. workflow 產出的 JSON 已 commit 或可由 workflow 重新產生。
4. workflow 失敗時可從測試訊息追蹤。

---

## 五、測試檢查

測試應包含：

1. builder output schema。
2. 必要欄位。
3. 狀態欄位。
4. 敏感欄位防護。
5. dashboard page existence。
6. JS data source path。
7. nav / site map entry。
8. full pytest。

---

## 六、人工審核邊界

所有對外相關資料應標示：

1. internal draft。
2. needs human review。
3. not official conclusion。
4. manual publishing only。

---

## 七、上線前最低條件

進入 production 前，至少應完成：

1. Dashboard health check。
2. Command center overview。
3. Public material review queue。
4. Approved material archive。
5. Weekly system report。
6. n8n reminder draft integration。
7. 官方資料來源與人工覆核 SOP。

---

## 八、建議驗收指令

```bash
python scripts/build_cycc_minutes_review_queue.py
python scripts/build_cycc_minutes_reviewed_sample.py
python scripts/build_cycc_minutes_issue_candidates.py
python scripts/build_weekly_summary_draft.py
python scripts/build_policy_draft_candidates.py
pytest -q
```

未來 content pipeline 合併後，應再加入：

```bash
python scripts/build_social_post_drafts.py
python scripts/build_short_video_script_drafts.py
python scripts/build_filming_checklists.py
python scripts/build_content_schedule.py
python scripts/build_daily_execution_list.py
python scripts/build_public_material_review_queue.py
python scripts/build_approved_materials_sample.py
python scripts/build_command_center_overview.py
python scripts/build_dashboard_health_check.py
pytest -q
```

---

## 九、下一步

合併 production readiness checklist 後，可再推進：

1. weekly system report builder。
2. n8n reminder draft integration。
3. official source intake SOP。
4. production launch checklist page。
