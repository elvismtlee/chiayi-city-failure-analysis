# Approved Material Schema Checklist

本文件用來審查未來 approved material schema 與 builder PR。目標是把已通過人工審核的內容，整理成可追蹤、可回查、可手動發布的最終草稿資料格式。

---

## 一、預期資料流

```text
public material review queue
  -> approved material records
  -> final public draft archive
  -> manual publishing
```

第一版只讀本地 JSON，只產生已核准素材紀錄，不自動發布。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_approved_materials_sample.py` |
| dashboard data | `dashboard/data/approved_materials_sample.json` |
| dashboard page | `dashboard/approved-materials.html` |
| dashboard renderer | `dashboard/approved-materials.js` |
| builder test | `tests/test_build_approved_materials_sample.py` |
| page test | `tests/test_approved_materials_page.py` |

---

## 三、approved_materials_sample.json 必要欄位

```text
approved_id
source_review_item_id
material_type
title
final_draft
source_urls
approved_at
approver
approval_notes
publication_status
public_use_status
risk_notes
```

---

## 四、欄位規則

1. `approved_id` 必須穩定。
2. `source_review_item_id` 必須可回查原始 review item。
3. `material_type` 可包含 social_post、video_script、policy_note、field_note。
4. `final_draft` 仍是待手動發布草稿。
5. `approved_at` 第一版可使用固定 sample 日期。
6. `approver` 可使用 `campaign_ops`。
7. `publication_status` 初始應為 `ready_for_manual_publish`。
8. `public_use_status` 應為 `human_approved_sample`。
9. `risk_notes` 應保留來源、語氣、法遵與上下文提醒。

---

## 五、Dashboard 驗收

`dashboard/approved-materials.html` 應顯示：

1. 已核准素材樣本清單。
2. 總筆數。
3. 各 material_type 數量。
4. publication_status 統計。
5. 每筆 approved material card。

每張 card 至少顯示：

1. `material_type`
2. `title`
3. `final_draft`
4. `source_urls`
5. `approved_at`
6. `approver`
7. `publication_status`
8. `risk_notes`

頁面必須提醒：

1. 這是人工核准後的樣本資料。
2. 仍須手動發布。
3. 不是自動發布流程。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 public material review builder 後執行：

```bash
python scripts/build_approved_materials_sample.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
approved-materials.html
```

---

## 八、測試指令

```bash
python scripts/build_approved_materials_sample.py
pytest -q tests/test_build_approved_materials_sample.py
pytest -q tests/test_approved_materials_page.py
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
7. publication_status 清楚標示手動發布。
8. 每筆資料可回查 source_review_item_id。

---

## 十、下一步

合併 approved material schema 後，可再推進：

1. publish-ready archive dashboard。
2. printable approval record。
3. n8n 每週人工審核提醒。
4. command center overview。
