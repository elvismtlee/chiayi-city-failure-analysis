# Official Source Intake SOP

本文件用來規劃未來從 sample / fixture 走向正式公開資料來源時的人工覆核流程。目標是讓資料來源、擷取方法、解析結果與對外使用邊界都能被追蹤。

---

## 一、適用範圍

```text
official meeting records
public complaint records
public dashboard data
open data files
manual review notes
```

第一版仍以人工確認與本地檔案為主，不在未審核前自動抓取或自動發布。

---

## 二、來源登記欄位

每個正式來源應建立來源登記紀錄，至少包含：

```text
source_id
source_name
source_url
source_owner
access_method
license_or_terms
retrieved_at
retrieved_by
review_status
notes
```

---

## 三、人工覆核步驟

1. 確認來源是否為公開資料。
2. 確認網址與來源單位。
3. 確認使用條款或授權限制。
4. 確認資料是否含個資或敏感欄位。
5. 確認解析後欄位是否正確。
6. 確認資料仍為內部分析草稿。
7. 對外使用前再次人工審核。

---

## 四、狀態建議

```text
needs_source_review
source_reviewed
needs_parser_review
parser_reviewed
needs_policy_review
internal_only
ready_for_manual_use
```

---

## 五、不可做事項

1. 不在未確認授權前大量下載。
2. 不繞過網站限制。
3. 不收集非必要個資。
4. 不把未審核資料當正式結論。
5. 不自動發布來源資料解讀。

---

## 六、建議新增檔案

未來可新增：

| 類型 | 路徑 |
|---|---|
| source registry | `data/source_registry.json` |
| intake builder | `scripts/build_source_intake_queue.py` |
| dashboard data | `dashboard/data/source_intake_queue.json` |
| dashboard page | `dashboard/source-intake.html` |
| tests | `tests/test_source_intake_queue.py` |

---

## 七、Dashboard 驗收

`dashboard/source-intake.html` 應顯示：

1. 來源名稱。
2. 來源網址。
3. 來源單位。
4. 取得方式。
5. 授權或使用條款備註。
6. review_status。
7. notes。

頁面必須提醒：

1. 這是內部來源審核清單。
2. 不代表資料已正式採用。
3. 對外使用前需人工確認。

---

## 八、測試建議

```bash
python scripts/build_source_intake_queue.py
pytest -q tests/test_source_intake_queue.py
pytest -q
```

---

## 九、合併條件

1. 不自動連外。
2. 不下載大量資料。
3. 不輸出私人資料欄位。
4. 來源狀態清楚。
5. 人工覆核節點清楚。
6. 對外使用邊界清楚。

---

## 十、下一步

合併本 SOP 後，可再推進：

1. source registry sample。
2. source intake queue builder。
3. source intake dashboard。
4. official data parser acceptance checklist。
