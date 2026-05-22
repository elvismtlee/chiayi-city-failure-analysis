# Public Material Review Checklist

本文件用來審查未來 public material review dashboard 與 builder PR。目標是把社群文案、短影音腳本、政策草稿、每日執行清單等內部草稿，集中到人工審核工作台，確保對外使用前完成檢查。

---

## 一、預期資料流

```text
social drafts
video scripts
policy drafts
daily execution items
  -> public material review queue
  -> human approval
  -> final public draft
  -> manual publishing
```

第一版只讀本地 JSON，只產生審核佇列，不自動發布。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_public_material_review_queue.py` |
| dashboard data | `dashboard/data/public_material_review_queue.json` |
| dashboard page | `dashboard/public-review.html` |
| dashboard renderer | `dashboard/public-review.js` |
| builder test | `tests/test_build_public_material_review_queue.py` |
| page test | `tests/test_public_review_page.py` |

---

## 三、public_material_review_queue.json 必要欄位

```text
review_item_id
source_type
source_id
title
draft_text
source_urls
required_checks
review_status
public_use_status
risk_notes
recommended_next_step
```

---

## 四、required_checks 建議項目

每筆 item 的 `required_checks` 應是 list，可包含：

1. source_check
2. tone_check
3. privacy_check
4. legal_check
5. local_context_check
6. final_human_approval

---

## 五、狀態規則

1. review_status 初始應為 `needs_public_review`。
2. public_use_status 初始應為 `internal_review_queue`。
3. recommended_next_step 應為 `manual_public_review`。
4. risk_notes 應提醒人工確認來源、語氣、個資、法遵與上下文。

---

## 六、Dashboard 驗收

`dashboard/public-review.html` 應顯示：

1. 對外素材人工審核清單。
2. 總審核項目數。
3. 各 source_type 數量。
4. 需要人工審核數。
5. 每筆 review card。

每張 card 至少顯示：

1. `source_type`
2. `title`
3. `draft_text`
4. `source_urls`
5. `required_checks`
6. `review_status`
7. `risk_notes`

頁面必須提醒：

1. 這是內部人工審核清單。
2. 不是自動發布流程。
3. 對外使用前需人工核准。

---

## 七、Workflow 驗收

若納入 Dashboard Data workflow，應在所有草稿 builder 後執行：

```bash
python scripts/build_public_material_review_queue.py
```

---

## 八、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
public-review.html
```

---

## 九、測試指令

```bash
python scripts/build_public_material_review_queue.py
pytest -q tests/test_build_public_material_review_queue.py
pytest -q tests/test_public_review_page.py
pytest -q
```

---

## 十、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不自動發布。
5. 不呼叫平台 API。
6. 不輸出私人資料欄位。
7. 文案清楚標示人工審核。
8. 每筆資料都保留來源或 source_id。

---

## 十一、下一步

合併 public material review dashboard 後，可再推進：

1. final approved material draft schema。
2. printable approval checklist。
3. n8n 每週人工審核提醒。
4. campaign command center overview。
