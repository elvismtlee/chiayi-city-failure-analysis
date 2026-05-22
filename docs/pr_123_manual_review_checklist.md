# PR #123 人工驗收清單｜Command Center System Pipeline

更新時間：2026-05-23 02:23 Asia/Taipei

本清單用於合併 PR #123 前的人工確認。此 PR 是內部 dashboard 與人工審核流程，不是自動發布系統。

---

## 一、合併前必要狀態

| 項目 | 應達成狀態 |
|---|---|
| PR 狀態 | open、非 draft、mergeable |
| Python Tests | success |
| Dashboard Data | success |
| health check | `status: ok` 或 `ready_for_manual_review` |
| missing files | 空陣列，或僅剩明確標記為非必要的檔案 |
| 個資檢查 | 不含私人個資、捐款人資料、志工名單、私人陳情 |
| 發布行為 | 無自動發文、無自動寄信、無社群平台 API 發布 |

---

## 二、四個新工作模組檢查

### 1. 內容排程

檔案：

- `dashboard/content-schedule.html`
- `dashboard/content-schedule.js`
- `dashboard/data/content_schedule.json`
- `scripts/build_content_schedule.py`
- `tests/test_build_content_schedule.py`
- `tests/test_content_schedule_page.py`

人工確認：

- 頁面清楚標示 internal / manual review / manual publishing only。
- JSON 讀取失敗時有錯誤訊息。
- 缺欄位時不會造成整頁 crash。
- 不會自動排程到任何外部平台。

### 2. 每日執行

檔案：

- `dashboard/daily-execution.html`
- `dashboard/daily-execution.js`
- `dashboard/data/daily_execution_list.json`
- `scripts/build_daily_execution_list.py`
- `tests/test_build_daily_execution_list.py`
- `tests/test_daily_execution_page.py`

人工確認：

- 頁面是內部作戰節奏，不是對外承諾。
- 任務欄位包含 priority、task、estimated_minutes、status、related_dashboard、notes。
- 不含未公開敏感策略。

### 3. 公開審核

檔案：

- `dashboard/public-review.html`
- `dashboard/public-review.js`
- `dashboard/data/public_material_review_queue.json`
- `scripts/build_public_material_review_queue.py`
- `tests/test_build_public_material_review_queue.py`
- `tests/test_public_review_page.py`

人工確認：

- 頁面明確寫出「未通過人工審核，不可公開使用」。
- 每筆素材有 risk_level、review_status、evidence_status、required_action。
- 對外使用前必須人工確認來源、語氣、法遵與上下文。

### 4. 已核准素材

檔案：

- `dashboard/approved-materials.html`
- `dashboard/approved-materials.js`
- `dashboard/data/approved_materials_sample.json`
- `scripts/build_approved_materials_sample.py`
- `tests/test_build_approved_materials_sample.py`
- `tests/test_approved_materials_page.py`

人工確認：

- 頁面明確寫出 approved 不等於自動發布。
- 發布前仍需再次確認日期、語氣、圖片與法遵。
- 空資料可以是合法狀態，不應視為錯誤。

---

## 三、資料檔檢查

需要確認以下檔案都是 valid JSON：

- `dashboard/data/cycc_minutes_reviewed_sample.json`
- `dashboard/data/content_schedule.json`
- `dashboard/data/daily_execution_list.json`
- `dashboard/data/public_material_review_queue.json`
- `dashboard/data/approved_materials_sample.json`
- `dashboard/data/command_center_overview.json`
- `dashboard/data/dashboard_health_check.json`
- `dashboard/data/weekly_system_report.json`

要求：

1. UTF-8。
2. 結尾有 newline。
3. `generated_at` 使用 `+08:00`。
4. path 使用 `/`，不要使用 Windows 反斜線。
5. 不含電話、地址、email、身分證、捐款人或志工個資。

---

## 四、導覽與入口檢查

`dashboard/shared-nav.js` 與 `dashboard/data/site_map.json` 必須包含：

- 內容排程
- 每日執行
- 公開審核
- 已核准素材
- 總控台
- 健康檢查
- 每週系統報告

若 `dashboard/index.html` 有入口卡片，也應包含上述頁面或至少能透過 shared nav 到達。

---

## 五、法遵與安全檢查

合併前確認：

1. 無自動發文。
2. 無自動寄信。
3. 無社群平台 API 發布。
4. 無金流或付款行為。
5. 無刪除、公開分享或權限修改。
6. 無 token、API key、credential。
7. 無個資、私人陳情、捐款人、志工或支持者名單。
8. 不把 dashboard 數據稱為民調或支持度調查。
9. 對外素材仍需人工查證與人工審核。

---

## 六、建議合併判斷

可以合併的條件：

```text
Actions 全綠
health check 無缺檔
四個新模組頁面可讀
JSON valid
沒有個資與自動發布功能
人工 review 後確認內容符合 internal dashboard 用途
```

若上述條件成立，PR #123 可以進入 merge 前最後人工確認。
