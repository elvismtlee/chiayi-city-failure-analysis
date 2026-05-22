# Source Registry Sample Checklist

本文件用來審查未來 source registry sample 與 intake queue PR。目標是把正式公開資料來源先登記成可追蹤格式，再進入解析與人工覆核流程。

---

## 一、資料流

```text
official source intake SOP
  -> source registry sample
  -> source intake queue
  -> parser review
  -> internal analysis draft
```

第一版只建立本地 sample，不連外抓資料。

---

## 二、建議新增檔案

| 類型 | 路徑 |
|---|---|
| source registry | `data/source_registry.json` |
| builder | `scripts/build_source_intake_queue.py` |
| dashboard data | `dashboard/data/source_intake_queue.json` |
| dashboard page | `dashboard/source-intake.html` |
| renderer | `dashboard/source-intake.js` |
| builder test | `tests/test_build_source_intake_queue.py` |
| page test | `tests/test_source_intake_page.py` |

---

## 三、source_registry.json 必要欄位

每筆來源至少包含：

```text
source_id
source_name
source_type
source_url
source_owner
access_method
license_or_terms
expected_update_frequency
contains_personal_data_hint
retrieval_status
review_status
notes
```

---

## 四、來源類型建議

`source_type` 可包含：

1. council_minutes
2. complaint_record
3. open_data
4. city_budget
5. public_project
6. traffic_data
7. other

---

## 五、狀態規則

1. `retrieval_status` 初始可為 `not_retrieved`。
2. `review_status` 初始可為 `needs_source_review`。
3. `contains_personal_data_hint` 必須是 boolean。
4. `notes` 應提醒這是來源登記樣本。
5. 不應包含 token、密碼、私人憑證或非公開資料。

---

## 六、source intake queue 必要欄位

由 `source_registry.json` 產生的 queue 每筆至少包含：

```text
queue_id
source_id
source_name
source_type
source_url
source_owner
access_method
license_or_terms
review_status
recommended_action
risk_notes
```

---

## 七、Dashboard 驗收

`dashboard/source-intake.html` 應顯示：

1. 來源登記清單。
2. 來源類型統計。
3. 需要人工來源審核數。
4. 每筆 source card。

每張 card 至少顯示：

1. source_name
2. source_type
3. source_owner
4. access_method
5. license_or_terms
6. review_status
7. risk_notes

頁面必須提醒：

1. 這是內部來源審核清單。
2. 不代表資料已正式採用。
3. 不會自動抓取資料。
4. 對外使用前需人工確認。

---

## 八、測試指令

```bash
python scripts/build_source_intake_queue.py
pytest -q tests/test_build_source_intake_queue.py
pytest -q tests/test_source_intake_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. 只讀本地 sample。
3. 不連外抓資料。
4. 不加入 credential。
5. 不輸出私人資料欄位。
6. 來源狀態與人工覆核節點清楚。

---

## 十、下一步

合併 source registry sample 後，可再推進：

1. source intake queue builder。
2. source intake dashboard。
3. official data parser acceptance checklist。
4. crawler permission review checklist。
