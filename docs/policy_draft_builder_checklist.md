# Policy Draft Builder Checklist

本文件用來審查未來 policy draft builder 與 dashboard PR。目標是把 weekly summary draft 或 issue candidates 轉成內部政策提案草稿，而不是自動發布的正式政見。

---

## 一、預期資料流

```text
issue candidates / weekly summary draft
  -> policy draft candidates
  -> human policy review
  -> public policy material draft
  -> final human approval
```

第一版建議只讀本地 JSON，不連外部服務。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_policy_draft_candidates.py` |
| dashboard data | `dashboard/data/policy_draft_candidates.json` |
| dashboard page | `dashboard/policy-drafts.html` |
| dashboard renderer | `dashboard/policy-drafts.js` |
| builder test | `tests/test_build_policy_draft_candidates.py` |
| page test | `tests/test_policy_drafts_page.py` |

---

## 三、policy_draft_candidates.json 必要欄位

```text
draft_id
source_candidate_id
issue_title
problem_statement
possible_root_causes
policy_options
first_action
responsible_department
source_urls
review_status
public_use_status
risk_notes
recommended_next_step
```

驗收重點：

1. `draft_id` 穩定。
2. `problem_statement` 只根據來源摘要，不可誇大。
3. `possible_root_causes` 應標示為待確認。
4. `policy_options` 應是 list。
5. `first_action` 應是一人團隊可執行的下一步。
6. `review_status` 應是 `needs_policy_review`。
7. `public_use_status` 應標示 internal draft。
8. `risk_notes` 應提醒需人工確認來源與上下文。

---

## 四、政策草稿格式

每筆政策草稿建議轉成：

```markdown
## 議題名稱

### 問題描述

### 可能真因

### 可執行解法
1.
2.
3.

### 第一個可行動作

### 需確認資料

### 對外使用提醒
```

---

## 五、Dashboard 驗收

`dashboard/policy-drafts.html` 應顯示：

1. 政策草稿候選清單。
2. 總草稿數。
3. 需要人工審核數。
4. 涉及局處數。
5. 每筆 policy draft card。

每張 card 至少顯示：

1. `issue_title`
2. `problem_statement`
3. `possible_root_causes`
4. `policy_options`
5. `first_action`
6. `responsible_department`
7. `recommended_next_step`
8. `risk_notes`

頁面必須提醒：

1. 這是內部政策草稿。
2. 不是正式政見。
3. 對外使用前需人工審核。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 weekly summary 或 issue candidates builder 後執行：

```bash
python scripts/build_policy_draft_candidates.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
policy-drafts.html
```

---

## 八、測試指令

```bash
python scripts/build_policy_draft_candidates.py
pytest -q tests/test_build_policy_draft_candidates.py
pytest -q tests/test_policy_drafts_page.py
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
8. 不把候選草稿描述為正式政見。

---

## 十、下一步

合併 policy draft builder 後，可再推進：

1. social post draft builder。
2. short video script draft builder。
3. policy review dashboard。
4. n8n 每週人工審核通知。
