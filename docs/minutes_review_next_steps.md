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
| 會議紀錄人工審核 SOP | 已建立。 |

---

## 二、正在銜接的下一步

下一個工程任務應把 reviewed sample data 與 issue candidates 往週報草稿與 dashboard 摘要銜接。

預期新增：

```text
scripts/build_cycc_minutes_reviewed_sample.py
scripts/build_cycc_minutes_issue_candidates.py
data/processed/cycc_minutes_reviewed_sample.json
dashboard/data/cycc_minutes_issue_candidates.json
dashboard/minutes-issues.html
dashboard/minutes-issues.js
tests/test_build_cycc_minutes_reviewed_sample.py
tests/test_build_cycc_minutes_issue_candidates.py
tests/test_minutes_issues_page.py
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
  -> future weekly summary draft
```

在人工 review 完成前，任何資料都只能作為候選清單。

---

## 四、下一階段驗收重點

1. Reviewed sample item 必須有穩定 `reviewed_id`。
2. Issue candidate item 必須有穩定 `candidate_id`。
3. `public_use_status` 必須維持 `internal_reviewed_sample`。
4. `confidence_level` 必須維持 `sample_only`。
5. Dashboard 必須清楚標示不是正式結論。
6. 不得加入外部連線。
7. 不得加入 credential、token 或 API key。
8. 不得把 fixture / sample 資料當作正式分析結果。

---

## 五、合併後可再做

若 reviewed sample 與 issue candidates 完成，下一步可做：

1. future weekly summary draft builder。
2. dashboard summary 接入 sample_only 議題候選。
3. 人工政策審核欄位與審核結果回填流程。
4. 正式 parser 接入前的欄位品質檢查。
5. reviewed / unreviewed / sample_only 比例顯示。

---

## 六、操作原則

```text
先 queue，再 review。
先 reviewed，再 processed。
先 processed，再摘要。
先人工確認，再對外使用。
```
