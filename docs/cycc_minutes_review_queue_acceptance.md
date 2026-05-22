# 會議紀錄審核 Queue 驗收清單

本文件用於審查 issue #1「嘉義市議會會議紀錄 crawler」下一階段 PR：從 fixture-only parser prototype 進入會議紀錄人工審核 queue 與 dashboard。

此文件只定義驗收標準，不取代 parser、builder、dashboard 或測試。

---

## 一、驗收目標

新 PR 應完成以下目標：

1. 從既有 fixture parser output 產生人工審核 queue。
2. 產出 dashboard 可讀取的 JSON。
3. 新增會議紀錄審核頁面。
4. 加入 shared navigation 與 site map。
5. 使用 pytest 驗證資料 schema、頁面結構與安全邊界。
6. 保持 fixture-only，不接正式外部資料源。

---

## 二、必要新增檔案

| 類型 | 路徑 | 驗收重點 |
|---|---|---|
| Builder | `scripts/build_cycc_minutes_review_queue.py` | 從 fixture parser output 產生 queue JSON。 |
| Queue JSON | `dashboard/data/cycc_minutes_review_queue.json` | 結構穩定，可由 dashboard 讀取。 |
| Dashboard HTML | `dashboard/minutes-review.html` | 清楚顯示會議紀錄解析審核清單。 |
| Dashboard JS | `dashboard/minutes-review.js` | 讀取 queue JSON 並 render cards / stats。 |
| Builder test | `tests/test_build_cycc_minutes_review_queue.py` | 驗證 queue schema 與安全欄位。 |
| Page test | `tests/test_minutes_review_page.py` | 驗證頁面、導覽與安全文案。 |

---

## 三、Queue 欄位驗收

每筆 queue item 至少應包含：

```text
queue_id
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
review_priority
needs_manual_review
recommended_action
notes
```

欄位規則：

1. `queue_id` 應由 `raw_hash` 穩定產生。
2. `raw_text_excerpt` 不應超過 120 字。
3. `parser_status` 應維持 `parsed_from_fixture`。
4. `review_status` 應維持 `unreviewed`。
5. `needs_manual_review` 應為 `true`。
6. `recommended_action` 應為 `manual_minutes_review`。
7. `issue_keywords` 必須是 list。
8. `notes` 應提醒資料尚未人工審核，不可當正式結論。

---

## 四、Dashboard 頁面驗收

頁面應顯示：

1. 總筆數。
2. 待人工審核筆數。
3. 涉及局處數。
4. parser 狀態摘要。
5. 每筆 queue card。

每張 card 至少顯示：

1. 會議名稱。
2. 日期。
3. 議員。
4. 局處。
5. 議題或關鍵字。
6. 來源連結。
7. 原文摘要。
8. 狀態。
9. 建議動作。

---

## 五、安全邊界驗收

PR 不得包含：

1. 任何 credential。
2. 任何 token。
3. 任何 API key。
4. 外部連線行為。
5. Google Sheet 寫入流程。
6. 非公開資料。
7. 私人電話、email、地址、身分證字號等敏感欄位。
8. 將 fixture output 標為正式結論的文字。

Dashboard 文案應清楚標示：

1. fixture-only 或 fixture prototype。
2. 不連網。
3. 不寫入 Google Sheet。
4. 不使用 credential。
5. `review_status` 預設為 `unreviewed`。
6. 不能當正式結論。

---

## 六、Navigation 驗收

若新增 `dashboard/minutes-review.html`，應同步檢查：

| 檔案 | 驗收 |
|---|---|
| `dashboard/data/site_map.json` | 包含 `minutes-review.html`。 |
| `dashboard/shared-nav.js` | 包含 `minutes-review.html`。 |

不應大幅重排既有 navigation；只做必要新增。

---

## 七、測試驗收

至少應通過：

```bash
python scripts/build_cycc_minutes_review_queue.py
pytest -q tests/test_build_cycc_minutes_review_queue.py
pytest -q tests/test_minutes_review_page.py
pytest -q
```

若任一測試失敗，應先修測試原因，不應跳過測試或降低安全驗收標準。

---

## 八、人工 Review 問題清單

審查 PR 時逐項確認：

1. 這個 PR 是否只從 fixture parser output 產生 queue？
2. 是否有任何外部連線？
3. 是否有任何 credential、token、API key？
4. 是否把 `unreviewed` 資料當成正式結論？
5. 是否新增 dashboard 頁面與 JS？
6. 是否新增 site map 與 shared nav？
7. 是否新增 builder 測試與 page 測試？
8. 是否保留敏感欄位排除測試？
9. 是否沒有重做已完成的 metadata crawler？
10. 是否沒有碰 geocoding、video review、n8n 既有流程？

---

## 九、合併條件

PR 可合併條件：

1. GitHub Actions 成功。
2. 改動檔案符合任務範圍。
3. Queue JSON 可由 builder 重跑產生。
4. Dashboard 頁面可讀取 queue JSON。
5. 安全文案清楚。
6. 未新增敏感資料或外部憑證。
7. 沒有把 prototype 或 fixture 資料宣稱為正式分析結果。

---

## 十、合併後下一步

合併後可再規劃：

1. 會議紀錄審核 queue 的人工 review SOP。
2. 將 reviewed queue 匯入 processed data 的資料結構。
3. 將會議紀錄議題與既有 issue classifier 串接。
4. 將 reviewed minutes 與影音 metadata 做交叉比對。
5. 產出每週市政議題摘要，但仍需人工確認後才能對外使用。
