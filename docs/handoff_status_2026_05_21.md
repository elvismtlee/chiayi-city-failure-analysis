# 專案交接狀態｜2026-05-21

本文件記錄目前「嘉義城市故障分析資料庫」的交接狀態，方便晚上重新接 Codex、換新對話、或交給其他協作者時快速理解。

---

## 一、專案定位

專案名稱：

```text
嘉義市 12 年城市故障分析資料庫
```

核心目標：

```text
以公開資料、議會資料、地方議題資料與城市故障回報，建立嘉義市長期生活問題的資料庫、儀表板、AI 摘要、週報與改善追蹤流程。
```

目前階段：

```text
Prototype / MVP 前期
```

---

## 二、主要網站

GitHub repo：

```text
https://github.com/elvismtlee/chiayi-city-failure-analysis
```

GitHub Pages：

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/
```

---

## 三、目前已完成的主要方向

### 1. Dashboard 原型

已建立：

- `dashboard/index.html`
- `dashboard/insights.html`
- `dashboard/sources.html`
- `dashboard/methodology.html`
- `dashboard/reports.html`
- `dashboard/reports/2026-W21.html`
- `dashboard/404.html`

### 2. Dashboard JSON 原型資料

已建立或規劃：

- `dashboard/data/dashboard_summary.json`
- `dashboard/data/issue_ranking.json`
- `dashboard/data/hotspots.json`
- `dashboard/data/ai_issue_summary.json`
- `dashboard/data/issue_trends.json`
- `dashboard/data/data_sources.json`
- `dashboard/data/reports_index.json`
- `dashboard/data/site_map.json`

### 3. 資料與治理文件

已建立大量文件，總入口：

```text
docs/docs_index.md
```

重要文件包括：

- `docs/data_governance.md`
- `docs/public_disclaimer.md`
- `docs/privacy_deidentification.md`
- `docs/data_publication_policy.md`
- `docs/risk_register.md`
- `docs/source_inventory.md`
- `docs/1999_data_onboarding_plan.md`
- `docs/issue_taxonomy.md`
- `docs/data_dictionary.md`
- `docs/json_validation_rules.md`
- `docs/frontend_rendering_contract.md`
- `docs/mvp_launch_plan.md`

### 4. Codex / CI / 自動化文件

已建立：

- `docs/codex_resume_plan.md`
- `docs/codex_prompt_library.md`
- `docs/github_actions_strategy.md`
- `docs/troubleshooting.md`
- `docs/pr_review_guide.md`
- `docs/development_board.md`

---

## 四、目前不建議手動碰的檔案

若 Codex 正在做 dashboard pipeline，暫時避免同時手動修改：

```text
src/processors/build_dashboard_data.py
.github/workflows/*
dashboard/index.html
dashboard/app.js
dashboard/insights.html
dashboard/insights.js
```

原因：

```text
這些檔案最容易與 Codex 的 pipeline、前端 rendering 或 GitHub Actions 任務產生 conflict。
```

---

## 五、下一個技術優先順序

建議順序：

```text
1. Codex 狀態檢查
2. 確認目前 PR / branch / Actions 狀態
3. 建立或完成 dashboard data pipeline
4. 建立 dashboard JSON validation tests
5. 建立 GitHub Actions build-dashboard-data workflow
6. 統一全站導覽與 footer
7. 建立 Leaflet 熱點地圖
8. 接 Google Sheet / sample data
9. 再接正式 1999 / 陳情資料
```

---

## 六、目前可安全繼續做的事

不會干擾 Codex 的工作：

- 補文件
- 補 issue
- 補資料字典
- 補人工輸入模板
- 補 Google Sheet 規格
- 補對外文案
- 補風險與 QA 文件
- 整理 sample data 計畫

---

## 七、需要人工協助的資料

詳見：

```text
docs/user_input_needed.md
```

最重要三項：

1. 嘉義市 1999 / 市政信箱 / 陳情資料來源網址。
2. 西區重要地點清單。
3. 10 - 20 筆城市故障 sample cases。

---

## 八、晚上重新接 Codex 時的第一句指令

建議先貼：

```text
請先依照 docs/codex_resume_plan.md 進行狀態檢查。請不要修改任何檔案，先回報目前 main、open PR、branch、GitHub Actions、Pages 與 dashboard data pipeline 的狀態，並告訴我下一步建議。
```

---

## 九、目前專案成功標準

第一階段不要求完整 12 年資料，而是先達到：

```text
網站可開
資料可更新
來源可追溯
JSON 可驗證
風險有聲明
sample data 可跑通
下一步可接正式資料
```
