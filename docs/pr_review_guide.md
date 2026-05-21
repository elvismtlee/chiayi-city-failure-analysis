# PR 審查指南 v1

本文件定義本專案 Pull Request 的審查標準。

---

## PR 基本要求

每個 PR 必須清楚回答：

1. 這個 PR 解決哪一個 Issue？
2. 改了哪些檔案？
3. 有沒有新增資料檔？
4. 有沒有影響 GitHub Pages？
5. 有沒有測試？
6. 有沒有可能造成資料或文案誤導？
7. 有沒有新增或修改嘉義在地地名？

---

## PR 描述範本

```markdown
## Summary

- 
- 

## Changed files

- 
- 

## Tests

- [ ] pytest
- [ ] pytest tests/test_local_terminology.py tests/test_local_place_dictionary.py
- [ ] python src/processors/build_dashboard_data.py
- [ ] GitHub Pages checked

## Data impact

- [ ] No data change
- [ ] Mock data only
- [ ] Raw CSV changed
- [ ] Dashboard JSON changed

## Local terminology impact

- [ ] No place-name change
- [ ] Place names checked against docs/local_terminology_style_guide.md
- [ ] local_place_dictionary.json updated if needed
- [ ] No banned local terms in public-facing files

## Risk

- [ ] Low
- [ ] Medium
- [ ] High

## Notes


```

---

## 程式 PR 審查

檢查：

- [ ] 不硬寫死不必要 URL
- [ ] 可讀取 config
- [ ] 有 fallback
- [ ] 有錯誤處理
- [ ] 有 tests
- [ ] 不把 secrets 寫入 repo
- [ ] 不產生大量不必要檔案

---

## Dashboard PR 審查

檢查：

- [ ] 首頁不壞掉
- [ ] insights 不壞掉
- [ ] sources / methodology / reports 可開啟
- [ ] JS 讀 JSON 正常
- [ ] 手機版可讀
- [ ] 導覽一致
- [ ] footer 有資料聲明
- [ ] 地名符合嘉義在地用語規範

---

## 資料 PR 審查

檢查：

- [ ] CSV 欄位符合 schema
- [ ] JSON 格式正確
- [ ] 有 updated_at 或 latest_update
- [ ] source_url 保留
- [ ] mock data 標示清楚
- [ ] 沒有個資
- [ ] 地點名稱優先使用 `dashboard/data/local_place_dictionary.json` 的 `display_name`
- [ ] 禁用詞只出現在 allowlist 檔案中的 `avoid_terms` 或規則說明

---

## 文案 PR 審查

不可出現：

- 民調
- 支持度調查
- 無來源指控
- 人身攻擊
- 絕對化結論
- 把樣本資料說成正式資料
- 外地觀光式地名稱呼

建議使用：

- 城市議題觀察
- 公開資料分析
- 城市故障追蹤
- 議題關注度
- 局處案件負荷觀察
- 嘉義人在地日常稱呼

---

## 在地用語 PR 審查

若 PR 涉及地點、熱點、週報、sample data、AI 摘要或社群文案，必須檢查：

- [ ] 是否參考 `docs/local_terminology_style_guide.md`
- [ ] 是否參考 `dashboard/data/local_place_dictionary.json`
- [ ] 是否避免使用 `avoid_terms`
- [ ] 是否執行 `pytest tests/test_local_terminology.py tests/test_local_place_dictionary.py`

文化路規則：

```text
不要使用：文化路夜市
建議使用：文化路、文化路商圈、文化路周邊、文化路商圈周邊
```

---

## Merge 原則

1. GitHub Actions 通過後再 merge。
2. 有 conflict 先修 conflict，不要硬 merge。
3. 大型 PR 優先 squash merge。
4. Merge 後確認 GitHub Pages 正常部署。
5. Merge 後若發現頁面壞掉，優先 revert 或 hotfix。
6. Merge 後若發現地名錯誤，應全面搜尋與修正，不只改單一頁面。
