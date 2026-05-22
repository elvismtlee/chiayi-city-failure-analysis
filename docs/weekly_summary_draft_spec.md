# 每週市政議題摘要草稿規格

本文件定義 reviewed data 與 issue candidates 後續如何產生每週市政議題摘要草稿。此規格只建立資料流與欄位，不代表自動發布，也不代表正式結論。

---

## 一、用途

每週摘要草稿用於把已審核或已標記為 sample 的議題候選整理成內部工作材料，協助一人團隊快速判斷：

1. 本週有哪些議題值得追蹤。
2. 哪些局處與議題類型出現頻率較高。
3. 哪些內容可轉成政策提案草稿。
4. 哪些內容仍需人工補資料。

---

## 二、輸入資料

第一階段建議輸入：

| 資料 | 用途 |
|---|---|
| `dashboard/data/cycc_minutes_issue_candidates.json` | 會議紀錄議題候選。 |
| `dashboard/data/transcript_review_queue.json` | 影音 metadata 與轉錄審核候選。 |
| `dashboard/data/geocoding_review_queue.json` | 地點與座標審核候選。 |
| `dashboard/data/issue_trends.json` | 既有議題趨勢資料。 |

第一版可以只使用 `cycc_minutes_issue_candidates.json`，等資料穩定後再加入其他資料源。

---

## 三、輸出資料

建議未來新增：

```text
dashboard/data/weekly_summary_draft.json
docs/weekly_summary_draft_example.md
```

`weekly_summary_draft.json` 建議欄位：

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

---

## 四、top_issues 欄位

每筆 top issue 建議包含：

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

## 五、資料使用邊界

1. 第一版 weekly summary 只能當內部草稿。
2. 若資料來源仍是 sample，摘要必須標示 sample-only。
3. 任何對外素材都必須人工審核後才能使用。
4. 不可把草稿稱為正式統計。
5. 不可把 dashboard 統計稱為民調或支持度調查。
6. 不可輸出私人聯絡、身分或住址欄位。

---

## 六、草稿文案格式

未來可產生以下 Markdown 草稿：

```markdown
# 本週市政議題摘要草稿

期間：YYYY-MM-DD ~ YYYY-MM-DD
資料狀態：internal draft / sample-only / reviewed candidates

## 一、本週重點議題
1.
2.
3.

## 二、涉及局處
| 局處 | 候選議題數 | 主要關鍵字 |
|---|---:|---|

## 三、可發展政策題目
1.
2.
3.

## 四、仍需人工補充
1.
2.
3.

## 五、使用提醒
本摘要為內部草稿，需人工確認來源與上下文後，才可轉為對外文案或政策素材。
```

---

## 七、未來 builder 建議

未來可新增：

```text
scripts/build_weekly_summary_draft.py
tests/test_build_weekly_summary_draft.py
dashboard/weekly-summary.html
dashboard/weekly-summary.js
```

第一版 builder 應：

1. 只讀本地 JSON。
2. 不連外部服務。
3. 不自動發布。
4. 不寄出 email。
5. 不寫入 Google Sheet。
6. 只輸出 JSON / Markdown 草稿。

---

## 八、建議流程

```text
issue candidates
  -> weekly summary draft
  -> human policy review
  -> social post draft
  -> final human approval
```

---

## 九、合格條件

每週摘要草稿若要轉為政策素材，至少應符合：

1. 來源可回查。
2. 時間範圍清楚。
3. 已排除私人資料。
4. 不誇大結論。
5. 有人工審核紀錄。
6. 可用一般市民聽得懂的語言說明。

---

## 十、一句話原則

```text
週報可以自動產生草稿，但不能自動變成正式結論；資料要先被確認，說法才可以公開。
```
