# PR #19 Review Status｜2026-05-21

PR：Build dashboard data pipeline

URL：

```text
https://github.com/elvismtlee/chiayi-city-failure-analysis/pull/19
```

---

## 目前結論

PR #19 目前暫不建議 merge。

原因不是 dashboard data pipeline 方向錯，而是 merge 前仍有兩個風險需要處理：

1. PR branch 目前顯示 mergeable false，需更新 branch 或處理衝突。
2. processor fallback data 仍需確認已完全符合嘉義在地用語規範。

---

## 已完成的正面進展

PR #19 已完成：

- 強化 `src/processors/build_dashboard_data.py`
- 可讀取 CYCC 會議紀錄與質詢影音 metadata CSV
- 可產生 dashboard JSON
- 新增 dashboard data workflow
- 新增 processor 相關 pytest
- GitHub Actions 曾顯示 Dashboard Data passed
- GitHub Actions 曾顯示 Python Tests passed

---

## merge 前必須再確認

### 1. Branch 狀態

目前 PR 曾顯示：

```text
mergeable: false
```

需請 Codex 或人工更新 branch，讓 PR 重新對齊 main。

---

### 2. fallback source

需確認：

```text
src/processors/build_dashboard_data.py
```

fallback data 不應輸出不符合嘉義在地語感的地名。

注意：不能只修改 `dashboard/data/*.json`，因為 workflow 會重新執行 processor；如果 source 沒修，output 可能再次被產生回來。

---

### 3. fallback 測試

建議 `tests/test_build_dashboard_data.py` 增加測試：

- raw CSV 不存在時仍可產生 fallback JSON
- fallback hotspot 使用嘉義在地稱呼
- fallback output 不含不建議稱呼

---

### 4. 建議驗證命令

```bash
python src/processors/build_dashboard_data.py
pytest -q
```

若 PR 修改地名、processor 或 dashboard output，還應做全文搜尋，確認 source、dashboard output、一般測試資料沒有殘留不建議稱呼。

---

## 給 Codex 的下一步

請 Codex 繼續修改 PR #19 的同一個 branch：

```text
codex/build-dashboard-data-pipeline
```

請不要開新 PR。

下一步應做：

1. 更新 branch 對齊 main。
2. 修正 processor fallback source。
3. 補 fallback test。
4. 重新執行 pytest。
5. 確認 GitHub Actions 全部 passed。
6. 確認 PR 回到 mergeable true。

---

## merge 判斷

可 merge 條件：

```text
PR mergeable true
Dashboard Data passed
Python Tests passed
fallback source 已修正
fallback test 已補
沒有 blocking comment
```

目前尚未達到上述全部條件。
