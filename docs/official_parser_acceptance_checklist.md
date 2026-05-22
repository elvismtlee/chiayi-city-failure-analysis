# Official Parser Acceptance Checklist

本文件用來審查未來正式公開資料 parser PR。目標是在從 sample / fixture 走向正式來源前，先建立解析器的安全邊界、資料欄位、人工覆核與測試標準。

---

## 一、適用範圍

```text
source registry
source intake queue
official public source files
parser output
manual review queue
internal analysis draft
```

第一版應以本地測試資料與人工覆核為主，不直接大量抓取外部資料。

---

## 二、Parser 基本要求

每個 parser 應符合：

1. 可從 repo root 執行。
2. 輸入來源清楚。
3. 輸出路徑固定。
4. 必要欄位有驗證。
5. 不輸出私人資料欄位。
6. 不把解析結果當正式結論。
7. 解析結果必須進入人工審核 queue。
8. 有對應 pytest。

---

## 三、建議輸出欄位

每筆 parser output 至少包含：

```text
record_id
source_id
source_name
source_url
retrieved_at
record_date
record_type
raw_text_excerpt
raw_hash
parser_status
review_status
public_use_status
risk_notes
recommended_next_step
```

---

## 四、狀態規則

1. `parser_status` 可為 `parsed_from_sample`、`parsed_from_public_source`、`parser_warning`。
2. `review_status` 初始應為 `needs_manual_review`。
3. `public_use_status` 初始應為 `internal_parser_output`。
4. `recommended_next_step` 應為 `manual_parser_review`。
5. `risk_notes` 應提醒來源、欄位、語意與人工覆核需求。

---

## 五、不可做事項

1. 不繞過網站限制。
2. 不下載非必要的大量資料。
3. 不收集非必要個資。
4. 不輸出私人地址、電話、email、身分證字號等欄位。
5. 不把未審核解析結果作為正式指控或正式結論。
6. 不自動發布任何解析結果。

---

## 六、測試建議

測試至少涵蓋：

1. parser 可執行。
2. output JSON 可讀。
3. 必要欄位存在。
4. raw_hash 穩定。
5. review_status 正確。
6. public_use_status 正確。
7. 不含私人資料欄位。
8. 不含「民調」。
9. 不含「支持度調查」。
10. dashboard 或 queue page 能清楚標示人工審核。

---

## 七、建議測試指令

```bash
python scripts/build_source_intake_queue.py
python scripts/parse_official_source_sample.py
pytest -q tests/test_parse_official_source_sample.py
pytest -q
```

---

## 八、合併條件

1. Python Tests 成功。
2. 不自動連外大量抓取。
3. 不加入 credential。
4. 不輸出私人資料欄位。
5. parser output 清楚標示內部解析結果。
6. 所有結果需要人工覆核。
7. 對外使用邊界清楚。

---

## 九、下一步

合併 parser acceptance checklist 後，可再推進：

1. official source sample fixture。
2. parser output review queue。
3. parser review dashboard。
4. crawler permission review checklist。
