# CI 品質門檻計畫 v1

本文件定義「嘉義城市故障分析資料庫」在 GitHub Actions / pytest 中應納入的品質門檻。

目前先以文件與測試檔建立規格，暫不直接修改 `.github/workflows/*`，避免與 Codex 的 dashboard data pipeline workflow 任務產生衝突。

---

## 目的

讓專案不是只有頁面能顯示，而是每次修改都能自動檢查：

```text
資料格式正確
→ 沒有個資
→ JSON 可讀
→ 地名符合嘉義在地用語
→ dashboard 不容易壞掉
```

---

## 第一階段必跑測試

建議 CI 至少執行：

```bash
pytest
```

若要分段顯示，可拆成：

```bash
pytest tests/test_local_terminology.py
pytest tests/test_local_place_dictionary.py
pytest tests/test_dashboard_json_validation.py
```

---

## 品質門檻項目

| 類型 | 測試檔 | 目的 |
|---|---|---|
| 在地用語 | `tests/test_local_terminology.py` | 避免 public-facing 檔案出現禁用地名 |
| 地名字典 | `tests/test_local_place_dictionary.py` | 確認地名字典欄位完整、ID 不重複、名稱正確 |
| Dashboard JSON | `tests/test_dashboard_json_validation.py` | 確認 JSON 可 parse、欄位完整、不含個資 |
| Python processor | 現有 pytest | 確認資料處理程式不壞掉 |

---

## 在地用語品質門檻

以下情況應讓 CI 失敗：

1. `dashboard/data/*.json` 出現禁用地名。
2. `dashboard/**/*.html` 出現禁用地名。
3. `docs/report_template.md`、週報、社群模板出現禁用地名。
4. `local_place_dictionary.json` 的 `display_name`、`local_name`、`formal_name` 使用禁用地名。

允許出現禁用詞的檔案只有：

```text
docs/local_terminology_style_guide.md
docs/local_terms_validation_rules.md
docs/local_place_dictionary.md
dashboard/data/local_place_dictionary.json
```

原因：這些檔案需要記錄 `avoid_terms` 或說明禁用詞。

---

## 建議 GitHub Actions 結構

未來可在 workflow 中加入：

```yaml
- name: Run tests
  run: pytest
```

若要讓錯誤比較清楚，也可以拆：

```yaml
- name: Validate local terminology
  run: pytest tests/test_local_terminology.py tests/test_local_place_dictionary.py

- name: Validate dashboard JSON
  run: pytest tests/test_dashboard_json_validation.py
```

---

## PR 必備回報

任何 PR 若涉及 dashboard、data、docs、report、sample data，PR 描述應包含：

```text
Tests:
- pytest
- pytest tests/test_local_terminology.py tests/test_local_place_dictionary.py

Local terminology:
- Checked local place dictionary: yes/no
- New place names: yes/no
- Banned terms found: no
```

---

## 不在本文件直接處理的項目

目前先不直接修改：

```text
.github/workflows/*
src/processors/build_dashboard_data.py
```

這些留給 Codex dashboard data pipeline 任務統一處理，避免多人或多代理同時修改 workflow 與 pipeline 造成 conflict。

---

## 原則

```text
能用測試擋下的錯誤，就不要靠人工記憶。
```
