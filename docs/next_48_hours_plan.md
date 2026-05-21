# 下一個 48 小時執行計畫 v1

本文件把目前專案工作收斂成接下來 48 小時可以執行的順序。

---

## 目標

48 小時內不要擴散太多新功能，優先讓 MVP 技術流程可以穩定往前推進。

核心目標：

```text
確認狀態
→ 接 data pipeline
→ 補 validation
→ 補 workflow
→ 建 sample data 入口
```

---

## Day 1：Codex 恢復後

### Step 1. 狀態檢查

執行：

```text
請先依照 docs/codex_resume_plan.md 進行狀態檢查，不要修改檔案。
```

檢查：

- main 是否最新
- 是否有 open PR
- PR #8 是否已合併
- Actions 是否通過
- Pages 是否正常
- dashboard data pipeline 是否有未完成 branch

---

### Step 2. Dashboard data pipeline

任務：

```text
Build dashboard data pipeline
```

參考文件：

- `docs/data_dictionary.md`
- `docs/json_validation_rules.md`
- `docs/frontend_rendering_contract.md`
- `docs/sample_data_plan.md`

目標：

- raw / sample CSV 可轉 dashboard JSON
- JSON 欄位符合前端需要
- 缺資料時有 fallback

---

### Step 3. JSON validation tests

對應 Issue：

```text
#13 建立 dashboard JSON validation tests
```

目標：

- 所有 dashboard/data/*.json 可 parse
- 必要欄位存在
- score 0 - 100
- trend 值合法
- 不含常見個資欄位

---

## Day 2：自動化與前端收斂

### Step 4. GitHub Actions build workflow

對應 Issue：

```text
#14 建立 GitHub Actions dashboard data build workflow
```

目標：

- pull_request 會跑
- push main 會跑
- workflow_dispatch 可手動跑
- pipeline + validation fail 時 workflow fail

---

### Step 5. 全站共用導覽與 footer

對應 Issue：

```text
#11 重構全站共用導覽列與 footer
```

目標：

- index / insights / sources / methodology / reports / 404 導覽一致
- footer 有資料聲明
- active 狀態正確

---

### Step 6. Leaflet 熱點地圖

對應 Issue：

```text
#6 建立第一版 Leaflet 熱點地圖
```

目標：

- 讀 hotspots.json
- 顯示點位或 fallback list
- popup 顯示熱點名稱、議題、分數、建議行動

---

## 人工資料準備

同時可由人工整理：

- 10 - 20 筆城市故障 sample cases
- 10 個西區重要地點
- 嘉義市 1999 / 陳情資料來源 URL

參考：

- `docs/user_input_needed.md`
- `docs/google_sheet_templates.md`
- `docs/sample_data_plan.md`

---

## 這 48 小時先不要做

避免分散：

1. 不做完整 12 年資料。
2. 不做自動社群發布。
3. 不直接接大量敏感資料。
4. 不重寫整個前端設計。
5. 不新增太多新頁面。

---

## 完成判斷

48 小時後應達到：

```text
data pipeline 有方向
JSON validation 可跑
Actions 有初步 workflow
Pages 可正常顯示
sample data 可被規劃接入
下一步明確
```
