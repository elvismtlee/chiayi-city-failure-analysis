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
| 會議紀錄人工審核 SOP | 已建立。 |

---

## 二、正在銜接的下一步

下一個工程任務應把 parser prototype 產出轉成 dashboard 可讀取的審核 queue。

預期新增：

```text
scripts/build_cycc_minutes_review_queue.py
dashboard/data/cycc_minutes_review_queue.json
dashboard/minutes-review.html
dashboard/minutes-review.js
tests/test_build_cycc_minutes_review_queue.py
tests/test_minutes_review_page.py
```

---

## 三、資料流

```text
fixture parser output
  -> review queue JSON
  -> dashboard review page
  -> human review
  -> reviewed data candidate
  -> issue classification / weekly summary draft
```

在人工 review 完成前，任何資料都只能作為候選清單。

---

## 四、下一階段驗收重點

1. Queue item 必須有穩定 `queue_id`。
2. `raw_text_excerpt` 不應放完整長文。
3. `review_status` 初始必須是 `unreviewed`。
4. `needs_manual_review` 必須是 `true`。
5. Dashboard 必須清楚標示資料尚未人工審核。
6. 不得加入外部連線。
7. 不得加入 credential、token 或 API key。
8. 不得把 fixture 資料當作正式分析結果。

---

## 五、合併後可再做

若 review queue dashboard 完成，下一步可做：

1. reviewed data schema。
2. manual review output 範例。
3. issue classifier 接 reviewed minutes。
4. weekly summary draft builder。
5. dashboard 顯示 reviewed / unreviewed 比例。

---

## 六、操作原則

```text
先 queue，再 review。
先 reviewed，再 processed。
先 processed，再摘要。
先人工確認，再對外使用。
```
