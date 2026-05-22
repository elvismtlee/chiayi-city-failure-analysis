# 會議紀錄審核流程下一步

本文件整理會議紀錄解析與人工審核流程的下一階段工作，方便在 parser prototype、review queue、dashboard 與人工審核 SOP 之間銜接。

---

## 一、目前已具備

| 項目 | 狀態 |
|---|---|
| PDF / HTML 解析規格 | 已建立。 |
| fixture-only parser prototype | 已建立。 |
| parser 測試 | 已建立。 |
| review queue 驗收清單 | 已建立。 |
| reviewed sample data | 已建立範例。 |
| issue candidates | 已建立範例。 |
| weekly summary draft | 已建立內部草稿範例。 |
| policy draft candidates | 已建立內部草稿候選。 |
| 會議紀錄人工審核 SOP | 已建立。 |

---

## 二、正在銜接的下一步

下一個工程任務應把 policy draft candidates 往人工審核回填與週報草稿審核流程銜接。

預期新增：

```text
scripts/build_weekly_summary_draft.py
scripts/build_policy_draft_candidates.py
dashboard/data/weekly_summary_draft.json
dashboard/data/policy_draft_candidates.json
dashboard/weekly-summary.html
dashboard/policy-drafts.html
tests/test_build_weekly_summary_draft.py
tests/test_build_policy_draft_candidates.py
tests/test_weekly_summary_page.py
tests/test_policy_drafts_page.py
```

---

## 三、資料流

```text
fixture parser output
  -> review queue JSON
  -> dashboard review page
  -> human review
  -> reviewed sample data
  -> issue candidates
  -> weekly summary draft
  -> policy draft candidates
  -> human policy review
  -> future weekly summary draft / public material candidate
```

issue candidates 後可產生 weekly summary draft；weekly summary draft 後可產生 policy draft candidates。policy draft candidates 仍需人工政策審核，才可進入任何對外素材流程。

---

## 四、下一階段驗收重點

1. Weekly summary 必須有穩定 `summary_id`。
2. Policy draft candidate 必須有穩定 `draft_id`。
3. `public_use_status` 必須維持 `internal_weekly_draft` 或 `internal_policy_draft`。
4. `review_status` 必須維持 `needs_policy_review`。
5. Dashboard 必須清楚標示不是正式結論、不是正式政見。
6. 不得加入外部連線。
7. 不得加入 credential、token 或 API key。
8. 不得把 fixture / sample 資料當作正式分析結果。

---

## 五、合併後可再做

若 weekly summary draft 與 policy draft candidates 完成，下一步可做：

1. 人工政策審核欄位與審核結果回填流程。
2. 週報草稿人工審核表。
3. dashboard summary 接入已審核的 policy draft 狀態。
4. future weekly public summary draft builder。
5. 正式 parser 接入前的欄位品質檢查。

---

## 六、操作原則

```text
先 queue，再 review。
先 reviewed，再 processed。
先 processed，再摘要。
先人工確認，再對外使用。
```
