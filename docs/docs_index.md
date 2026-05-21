# 文件總索引｜嘉義城市故障分析資料庫

本文件整理目前 repo 內的重要文件，作為專案知識入口。

---

## 1. 專案定位與公開說明

| 文件 | 用途 |
|---|---|
| `docs/project_public_positioning.md` | 專案對外定位、可用文案、語氣邊界 |
| `docs/public_disclaimer.md` | 對外資料聲明、AI 摘要聲明、使用者回報資料聲明 |
| `docs/data_governance.md` | 資料治理原則、不可使用字眼、AI 摘要限制 |
| `docs/privacy_deidentification.md` | 個資去識別化與地址降精度規則 |

---

## 2. 網站與前端架構

| 文件 | 用途 |
|---|---|
| `docs/site_architecture.md` | GitHub Pages 資料站頁面層級 |
| `docs/frontend_rendering_contract.md` | HTML / JS / JSON 之間的 rendering contract |
| `docs/seo_metadata_plan.md` | 各頁 SEO title / description / Open Graph 規劃 |
| `docs/release_checklist.md` | GitHub Pages 發布前後檢查表 |
| `docs/qa_checklist.md` | 內容、資料、前端與發布 QA 檢查 |

---

## 3. 資料來源與 crawler

| 文件 | 用途 |
|---|---|
| `docs/source_inventory.md` | 嘉義市議會、市府、開放資料、地方回報等資料來源盤點 |
| `docs/crawler_ethics_and_limits.md` | crawler 使用原則、請求頻率、禁止事項 |
| `docs/1999_data_onboarding_plan.md` | 1999 / 陳情資料接入流程 |
| `docs/information_request_templates.md` | 向機關詢問資料與授權的文字範本 |

---

## 4. 資料模型與分類

| 文件 | 用途 |
|---|---|
| `docs/data_dictionary.md` | CSV / JSON 欄位字典 |
| `docs/issue_taxonomy.md` | 城市故障議題分類字典 |
| `docs/location_normalization.md` | 地點標準化、熱點定位與 Geo precision |
| `docs/json_validation_rules.md` | dashboard JSON 驗證規則 |
| `docs/geojson_schema.md` | GeoJSON 格式與地圖資料 schema |

---

## 5. AI 分析與週報

| 文件 | 用途 |
|---|---|
| `docs/ai_issue_summarizer_spec.md` | AI issue summary 規格 |
| `docs/ai_classification_prompt.md` | AI 議題分類 prompt 與輸出格式 |
| `docs/issue_trend_analysis_spec.md` | 議題趨勢分析規格 |
| `docs/report_template.md` | 每週城市故障週報模板 |
| `docs/city_weekly_report_spec.md` | 城市週報輸出規格 |

---

## 6. 議員、局處與城市故障分數

| 文件 | 用途 |
|---|---|
| `docs/councilor_issue_analysis_schema.md` | 議員議題分析 schema |
| `docs/department_performance_schema.md` | 局處處理與回應分析 schema |
| `docs/urban_failure_score_model.md` | 城市故障分數模型 |

---

## 7. 自動化、CI 與協作

| 文件 | 用途 |
|---|---|
| `docs/github_actions_strategy.md` | GitHub Actions 自動化策略 |
| `docs/troubleshooting.md` | 常見錯誤排除手冊 |
| `docs/n8n_workflow_blueprints.md` | n8n 自動化流程藍圖 |
| `docs/google_sheet_n8n_integration.md` | Google Sheet / n8n / GitHub 整合規格 |
| `docs/codex_resume_plan.md` | Codex 晚上接續計畫 |
| `docs/codex_prompt_library.md` | 可直接貼給 Codex 的任務指令 |
| `docs/development_board.md` | 開發工作看板 |
| `docs/pr_review_guide.md` | PR 審查指南 |
| `docs/versioning_and_milestones.md` | 版本路線圖與里程碑 |

---

## 8. WordPress / 官網整合

| 文件 | 用途 |
|---|---|
| `docs/wordpress_integration_spec.md` | chiayi2026.com 與 GitHub Pages dashboard 的整合方式 |
| `docs/wordpress_embed_blocks.md` | 可直接貼到 WordPress 的 HTML 模組 |

---

## 建議閱讀順序

### 第一次理解專案

```text
project_public_positioning.md
→ site_architecture.md
→ development_board.md
→ versioning_and_milestones.md
```

### Codex 要接任務

```text
codex_resume_plan.md
→ codex_prompt_library.md
→ pr_review_guide.md
→ troubleshooting.md
```

### 要做資料 pipeline

```text
data_dictionary.md
→ json_validation_rules.md
→ frontend_rendering_contract.md
→ github_actions_strategy.md
```

### 要接 1999 / 陳情資料

```text
source_inventory.md
→ 1999_data_onboarding_plan.md
→ privacy_deidentification.md
→ location_normalization.md
→ issue_taxonomy.md
```

### 要做 AI 與週報

```text
ai_classification_prompt.md
→ ai_issue_summarizer_spec.md
→ issue_trend_analysis_spec.md
→ report_template.md
```
