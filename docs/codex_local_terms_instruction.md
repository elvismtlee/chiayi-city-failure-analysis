# Codex 在地用語執行指令 v1

本文件提供給 Codex 或其他開發代理使用，確保修改 dashboard、sample data、週報、AI 摘要與資料處理流程時，不會產生不符合嘉義在地語感的地名。

---

## 核心要求

任何涉及地名、熱點、週報、社群文案、sample data、dashboard JSON 的修改，都必須先參考：

```text
docs/local_terminology_style_guide.md
docs/local_place_dictionary.md
dashboard/data/local_place_dictionary.json
docs/local_terms_validation_rules.md
```

---

## Codex 修改前檢查

修改前請先確認：

1. 是否新增或修改了地名？
2. 是否使用了外地觀光式稱呼？
3. 是否把商圈、路段、生活區域誤稱為夜市？
4. 是否應該使用 `display_name`、`local_name` 或 `aliases`？
5. 是否需要更新 `dashboard/data/local_place_dictionary.json`？

---

## 文化路規則

嚴格規定：

```text
不要使用：文化路夜市
建議使用：文化路、文化路商圈、文化路周邊、文化路商圈周邊
```

使用情境：

| 情境 | 建議 |
|---|---|
| dashboard 熱點名稱 | 文化路商圈 |
| 口語社群文案 | 文化路 |
| 週報分析 | 文化路商圈周邊 |
| 地點標準化 | 文化路商圈 |
| 路段資料 | 文化路部分路段 |

---

## 修改後必跑測試

若修改任何地名相關內容，請執行：

```bash
pytest tests/test_local_terminology.py tests/test_local_place_dictionary.py
```

若有完整 CI，請執行：

```bash
pytest
```

---

## 禁用詞處理

若看到：

```text
文化路夜市
嘉義市中心夜市區
嘉義著名夜市觀光區
```

不要只修改當前檔案，請全面搜尋：

```bash
grep -R "文化路夜市\|嘉義市中心夜市區\|嘉義著名夜市觀光區" dashboard docs data reports tests
```

允許出現的檔案只有：

```text
docs/local_terminology_style_guide.md
docs/local_terms_validation_rules.md
docs/local_place_dictionary.md
dashboard/data/local_place_dictionary.json
```

因為這些檔案需要記錄 avoid_terms。

---

## PR 回覆格式

若 PR 涉及地名，回覆中應包含：

```text
Local terminology check:
- Updated place names: yes/no
- Checked local_place_dictionary.json: yes/no
- Ran tests/test_local_terminology.py: yes/no
- Ran tests/test_local_place_dictionary.py: yes/no
```

---

## 原則

```text
地名不是小問題。地名錯，市民會立刻知道你不是在地整理。
```
