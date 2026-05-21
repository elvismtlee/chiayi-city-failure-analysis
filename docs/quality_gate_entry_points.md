# 品質門檻入口文件 v1

本文件是嘉義市城市故障分析資料庫的品質檢查入口。  
目的不是重寫所有規則，而是讓開發者、Codex 或人工審查者能快速找到要看的文件、要跑的測試與 merge 前必查項目。

---

## 一、品質門檻總覽

目前專案的品質門檻分成五層：

| 類型 | 目的 | 主要入口 |
|---|---|---|
| 在地用語檢查 | 避免 public-facing 文件、dashboard output 或 processor fallback 出現不符合嘉義在地語感的詞 | `tests/test_local_terminology.py` |
| 地名字典檢查 | 確保地名字典欄位完整、display name 正確、place_id 不重複 | `tests/test_local_place_dictionary.py` |
| Dashboard JSON 驗證 | 確保 dashboard JSON 可 parse、欄位存在、score 範圍合理、trend 合法 | `tests/test_dashboard_json_validation.py` |
| Dashboard data build | 確保 processor 能產生 dashboard JSON，且 fallback mode 可用 | `tests/test_build_dashboard_data.py` |
| PR merge 前人工檢查 | 避免只看 GitHub Actions 綠燈，卻漏掉 source、fallback 或 public-facing output 問題 | `docs/pr_merge_quality_checklist.md` |

---

## 二、重要規格文件

### 在地用語與地名字典

- `docs/local_terminology_style_guide.md`
- `docs/local_terms_validation_rules.md`
- `docs/local_place_dictionary.md`
- `dashboard/data/local_place_dictionary.json`

### Dashboard JSON 與前端資料

- `docs/json_validation_rules.md`
- `docs/frontend_rendering_contract.md`
- `docs/data_dictionary.md`

### CI 與 PR 審查

- `docs/pr_merge_quality_checklist.md`
- `.github/workflows/python-tests.yml`
- `.github/workflows/dashboard-data.yml`

---

## 三、重要測試入口

| 測試檔 | 檢查內容 |
|---|---|
| `tests/test_local_terminology.py` | 掃描 public-facing 檔案與 source，避免輸出不建議稱呼 |
| `tests/test_local_place_dictionary.py` | 驗證地名字典必要欄位、資料型別與 place_id 唯一性 |
| `tests/test_build_dashboard_data.py` | 驗證 dashboard data processor 能產生必要 JSON |
| `tests/test_dashboard_json_validation.py` | 驗證 dashboard JSON schema、score、trend 與敏感欄位 |

---

## 四、建議本機驗證指令

修改 processor、dashboard data、地名字典、文件或 workflow 前後，建議至少執行：

```bash
python src/processors/build_dashboard_data.py
pytest -q
```

若只想針對品質門檻逐項檢查，可執行：

```bash
pytest -q tests/test_local_terminology.py
pytest -q tests/test_local_place_dictionary.py
pytest -q tests/test_build_dashboard_data.py
pytest -q tests/test_dashboard_json_validation.py
```

---

## 五、GitHub Actions 品質門檻

目前 GitHub Actions 主要有兩個入口：

### Python Tests

檔案：

```text
.github/workflows/python-tests.yml
```

用途：

- push 時執行
- pull request 時執行
- 跑完整 `pytest`

### Dashboard Data

檔案：

```text
.github/workflows/dashboard-data.yml
```

用途：

- build dashboard JSON
- 驗證必要 dashboard JSON 可 parse
- 執行 dashboard data 測試
- 執行 dashboard JSON validation
- 執行在地用語與地名字典測試

---

## 六、merge 前必看提醒

merge 前請先看：

```text
docs/pr_merge_quality_checklist.md
```

尤其注意：

1. 不只看 GitHub Actions 綠燈。
2. 必須檢查 processor fallback output。
3. 必須檢查 public-facing docs / dashboard output。
4. 地名請優先對照 `dashboard/data/local_place_dictionary.json`。
5. 不建議稱呼只能留在規則文件或字典 `avoid_terms`，不應出現在 dashboard output。
6. 若 PR 修改 `.github/workflows/*`，需確認沒有與既有 workflow 衝突。
7. 若 PR 修改 dashboard JSON path，需確認前端讀取路徑沒有被改壞。

---

## 七、建議開發順序

後續任務建議照以下順序：

1. 先確認測試與品質門檻穩定。
2. 再擴充地名字典匯入流程。
3. 再擴充資料來源頁、Leaflet 地圖與趨勢分析。
4. 最後再導入更複雜的 AI 摘要與週報自動化。

目前下一個適合推進的任務：

```text
Issue #18：建立地名審核 CSV 匯入 local_place_dictionary.json 流程
```

---

## 八、核心原則

```text
資料要像嘉義人整理的，不像外地人用觀光印象寫的。
```

```text
workflow 綠燈是必要條件，不是充分條件。
```
