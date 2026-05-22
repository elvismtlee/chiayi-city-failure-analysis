# Reviewed Minutes Issue Pipeline Checklist

本文件用來審查 reviewed minutes sample data 到 issue candidates dashboard 的下一階段 PR。

---

## 一、目標

本階段目標是建立以下資料流：

```text
minutes review queue
  -> reviewed sample data
  -> issue candidates data
  -> dashboard summary
```

所有輸出仍屬 sample / internal review 階段，不是正式結論。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| reviewed sample data | `data/processed/cycc_minutes_reviewed_sample.json` |
| reviewed sample builder | `scripts/build_cycc_minutes_reviewed_sample.py` |
| issue candidates data | `dashboard/data/cycc_minutes_issue_candidates.json` |
| issue candidates builder | `scripts/build_cycc_minutes_issue_candidates.py` |
| dashboard page | `dashboard/minutes-issues.html` |
| dashboard renderer | `dashboard/minutes-issues.js` |
| builder tests | `tests/test_build_cycc_minutes_reviewed_sample.py` |
| candidate tests | `tests/test_build_cycc_minutes_issue_candidates.py` |
| page tests | `tests/test_minutes_issues_page.py` |

---

## 三、Reviewed Sample Data 必要欄位

```text
reviewed_id
source_queue_id
source_id
meeting_name
meeting_date
councilor_name
department
agenda_item
issue_keywords
source_url
raw_text_excerpt
raw_hash
parser_status
review_status
reviewed_at
reviewer
review_notes
source_context
public_use_status
public_use_notes
```

驗收重點：

1. `reviewed_id` 穩定。
2. `review_status` 是 `reviewed`。
3. `public_use_status` 是 `internal_reviewed_sample`。
4. `public_use_notes` 要標示 sample / not official。
5. 不輸出私人聯絡或身分欄位。

---

## 四、Issue Candidates 必要欄位

```text
candidate_id
reviewed_id
meeting_date
department
issue_title
issue_keywords
issue_summary
source_url
source_context
review_status
public_use_status
confidence_level
recommended_follow_up
notes
```

驗收重點：

1. `candidate_id` 穩定。
2. `issue_title` 可由 `agenda_item` 產生，但不可誇大。
3. `issue_summary` 必須保守。
4. `confidence_level` 是 `sample_only`。
5. `recommended_follow_up` 是 `manual_policy_review`。
6. `notes` 要標示 sample / not official。

---

## 五、Dashboard 驗收

`dashboard/minutes-issues.html` 應顯示：

1. 會議紀錄議題候選清單。
2. 總候選數。
3. 涉及局處數。
4. 涉及關鍵字數。
5. `sample_only` 筆數。
6. 每筆 candidate card。

頁面必須提醒：

1. 這是 sample data 轉出的議題候選。
2. 不是正式結論。
3. 對外使用前需人工政策審核。

---

## 六、Workflow 驗收

Dashboard Data workflow 應加入：

```bash
python scripts/build_cycc_minutes_reviewed_sample.py
python scripts/build_cycc_minutes_issue_candidates.py
```

順序應為：

```text
review queue -> reviewed sample -> issue candidates
```

---

## 七、Navigation 驗收

應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
minutes-issues.html
```

---

## 八、測試指令

```bash
python scripts/build_cycc_minutes_review_queue.py
python scripts/build_cycc_minutes_reviewed_sample.py
python scripts/build_cycc_minutes_issue_candidates.py
pytest -q tests/test_build_cycc_minutes_reviewed_sample.py
pytest -q tests/test_build_cycc_minutes_issue_candidates.py
pytest -q tests/test_minutes_issues_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 改動檔案符合任務範圍。
4. sample / not official 文案清楚。
5. 沒有私人資料欄位。
6. 沒有把 sample 資料描述為正式統計或正式結論。

---

## 十、合併後下一步

1. reviewed minutes schema 正式化。
2. issue classifier 接 reviewed minutes candidates。
3. weekly summary draft builder。
4. dashboard 顯示 review funnel。
5. n8n 每週草稿流程。
