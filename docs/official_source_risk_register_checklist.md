# Official Source Risk Register Checklist

本文件用來規劃正式公開資料來源的風險登記表。目標是把來源授權、資料過期、格式變更、個資風險、解析風險與對外使用風險集中管理，避免未審核資料被誤用。

---

## 一、適用範圍

```text
source registry
source intake queue
manual download records
crawler permission review
parser fixtures
parser outputs
review queues
dashboards
public material review queue
```

本 checklist 不建立自動發布流程，只建立內部風險管理規格。

---

## 二、風險類型

每個來源至少檢查下列風險：

```text
license_risk
access_risk
staleness_risk
format_change_risk
personal_data_risk
parser_accuracy_risk
context_risk
public_use_risk
```

---

## 三、風險登記欄位

未來若建立 risk register，每筆至少包含：

```text
risk_id
source_id
source_name
risk_type
risk_level
risk_description
impact
mitigation
owner
review_status
last_reviewed_at
next_review_due
public_use_status
notes
```

---

## 四、risk_level 建議

```text
low
medium
high
critical
unknown
```

`unknown` 不可視為安全，應進入人工覆核。

---

## 五、review_status 建議

```text
needs_risk_review
risk_reviewed
needs_legal_review
needs_source_review
needs_parser_review
internal_only
```

---

## 六、風險判斷範例

1. 來源授權不明：`license_risk` = high。
2. 來源需要登入：`access_risk` = high。
3. 超過預期更新頻率未確認：`staleness_risk` = medium 或 high。
4. fixture 與正式頁面格式不同：`format_change_risk` = medium。
5. 來源含電話、email、地址或身分識別資訊：`personal_data_risk` = high。
6. parser confidence 低：`parser_accuracy_risk` = medium。
7. 單一資料片段容易被過度解讀：`context_risk` = medium。
8. 內容可能被誤認為正式指控：`public_use_risk` = high。

---

## 七、Dashboard 顯示要求

若未來建立 source risk dashboard，至少顯示：

1. high / critical 風險數。
2. unknown 風險數。
3. 需要人工覆核的來源數。
4. 逾期未覆核的來源數。
5. 每筆風險的 mitigation 與 owner。
6. public_use_status。

頁面必須提醒：

1. 這是內部風險登記表。
2. 不代表資料已完成法律或政策審核。
3. 對外使用前需人工確認。
4. 不自動發布。

---

## 八、不可做事項

1. 不把 unknown risk 當作 low risk。
2. 不把高風險資料直接對外發布。
3. 不忽略個資風險。
4. 不把 parser output 當正式結論。
5. 不把單一來源當完整事實。
6. 不自動清除風險狀態。

---

## 九、測試建議

未來若新增 risk register builder，測試至少涵蓋：

1. 可產生 risk register JSON。
2. required fields 存在。
3. risk_level 僅使用允許值。
4. unknown risk 進入 review queue。
5. high / critical risk 有 mitigation。
6. public_use_status 是 internal_source_risk_register。
7. 缺檔不 crash，應輸出 warnings。
8. dashboard 顯示內部用途與人工覆核提醒。

---

## 十、建議測試指令

```bash
python scripts/build_source_risk_register.py
pytest -q tests/test_build_source_risk_register.py
pytest -q tests/test_source_risk_register_page.py
pytest -q
```

---

## 十一、合併條件

1. Python Tests 成功。
2. 不自動連外。
3. 不自動下載。
4. 不自動發布。
5. 高風險與未知風險不可被視為已通過。
6. 對外使用前需人工確認。

---

## 十二、下一步

合併本 checklist 後，可再推進：

1. source risk register builder。
2. source risk dashboard。
3. legal review queue sample。
4. public use risk review workflow。
