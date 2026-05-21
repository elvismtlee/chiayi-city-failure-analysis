# 嘉義在地用語 Validation 規則 v1

本文件定義如何在文件、dashboard JSON、週報與 AI 輸出中檢查不符合嘉義在地語感的用語。

---

## 目的

避免同一類錯誤反覆發生：

```text
先產生錯誤外地式名稱
→ 使用者指出
→ 才人工修正
```

未來應改成：

```text
產生資料或文案
→ 自動檢查在地用語
→ 發現禁用詞就 fail 或提醒
→ 修正後才發布
```

---

## 參考文件

主要參考：

```text
docs/local_terminology_style_guide.md
```

相關文件：

```text
docs/qa_checklist.md
docs/json_validation_rules.md
docs/report_template.md
docs/data_governance.md
```

---

## 第一批禁用詞

| banned_term | 建議替代 | 原因 |
|---|---|---|
| 文化路夜市 | 文化路 / 文化路商圈 / 文化路周邊 | 嘉義人日常較少這樣稱呼 |
| 嘉義市中心夜市區 | 文化路周邊 / 舊市區 / 文化路商圈 | 外地觀光式稱呼 |
| 嘉義著名夜市觀光區 | 文化路商圈 / 文化路周邊 | 過度觀光化 |
| 老街區 | 舊市區 / 老城區 / 文化路周邊 | 不夠精準 |

---

## 應檢查的檔案類型

需要檢查：

```text
dashboard/**/*.html
dashboard/data/*.json
docs/*.md
data/sample/*.csv
data/processed/*.csv
reports/**/*.md
reports/**/*.json
```

可暫時略過：

```text
node_modules/
.venv/
.git/
```

---

## Validation 行為

### public-facing 檔案

若在以下檔案出現 banned term，應視為錯誤：

```text
dashboard/**/*.html
dashboard/data/*.json
docs/report_template.md
docs/communication_templates.md
docs/social_content_workflow.md
reports/**/*.md
reports/**/*.html
```

### historical / audit 檔案

若是刻意記錄錯誤或說明避免用語，可允許出現，但應只出現在：

```text
docs/local_terminology_style_guide.md
docs/local_terms_validation_rules.md
```

---

## 建議 pytest 規則

未來可建立：

```text
tests/test_local_terminology.py
```

測試邏輯：

```python
BANNED_TERMS = {
    "文化路夜市": "文化路商圈",
    "嘉義市中心夜市區": "文化路周邊",
    "嘉義著名夜市觀光區": "文化路商圈",
}

ALLOWLIST_FILES = {
    "docs/local_terminology_style_guide.md",
    "docs/local_terms_validation_rules.md",
}
```

檢查：

1. 掃描 dashboard、docs、data/sample、reports。
2. 若 public-facing 檔案含 banned term，測試 fail。
3. fail message 顯示檔案、詞彙、建議替代詞。

---

## 錯誤訊息範例

```text
Local terminology validation failed:
- dashboard/data/hotspots.json contains banned term: 文化路夜市
  Suggested replacement: 文化路商圈
```

---

## PR 檢查原則

任何新增：

- dashboard 資料
- sample data
- 週報
- 社群文案
- AI 摘要
- 地點資料

都應檢查是否符合在地用語規範。

---

## 人工 QA 問題

發布前人工檢查：

1. 嘉義人平常會這樣說嗎？
2. 這是不是外地觀光式稱呼？
3. 是否把商圈或路段誤稱為夜市？
4. 是否太像旅遊介紹，而不像城市治理資料？
5. 是否需要 local_name / formal_name / aliases 分開？

---

## 原則

```text
在地名稱不是裝飾，而是資料可信度的一部分。
```
