# 風險登錄表 v1

本文件整理「嘉義市 12 年城市故障分析資料庫」的主要風險與處理方式。

---

## R1. 資料來源不完整

| 項目 | 說明 |
|---|---|
| 風險 | 1999 / 陳情逐案資料可能未公開或不完整 |
| 影響 | 無法建立完整 12 年投訴資料庫 |
| 等級 | 高 |
| 緩解 | 先使用公開 metadata、統計資料、議會資料、開放資料補強；必要時提出資訊公開或資料詢問 |
| 相關文件 | `source_inventory.md`, `1999_data_onboarding_plan.md` |

---

## R2. 個資外洩

| 項目 | 說明 |
|---|---|
| 風險 | 使用者回報或陳情資料可能含姓名、電話、地址、email |
| 影響 | 法律與信任風險 |
| 等級 | 高 |
| 緩解 | 公開前去識別化、地址降精度、移除個資欄位 |
| 相關文件 | `privacy_deidentification.md`, `data_governance.md` |

---

## R3. 過度解讀資料

| 項目 | 說明 |
|---|---|
| 風險 | 把樣本資料或 metadata 解讀成完整民意或績效結論 |
| 影響 | 公信力下降、引發爭議 |
| 等級 | 高 |
| 緩解 | 明確標示 prototype / mock / metadata；使用「觀察」「追蹤」等語氣 |
| 相關文件 | `public_disclaimer.md`, `project_public_positioning.md` |

---

## R4. Crawler 造成網站負擔

| 項目 | 說明 |
|---|---|
| 風險 | 高頻請求官方網站造成負載 |
| 影響 | 技術與倫理風險 |
| 等級 | 中 |
| 緩解 | 限速、分批抓取、錯誤停止、不下載大量影音 |
| 相關文件 | `crawler_ethics_and_limits.md` |

---

## R5. GitHub Pages 頁面壞掉

| 項目 | 說明 |
|---|---|
| 風險 | JSON 格式錯誤或 JS selector 不一致導致頁面空白 |
| 影響 | 公開頁面不可用 |
| 等級 | 中 |
| 緩解 | JSON validation tests、frontend rendering contract、release checklist |
| 相關文件 | `json_validation_rules.md`, `frontend_rendering_contract.md`, `release_checklist.md` |

---

## R6. Codex / 多人協作衝突

| 項目 | 說明 |
|---|---|
| 風險 | 多個任務同時改同一檔案造成 conflict |
| 影響 | PR 難合併、進度混亂 |
| 等級 | 中 |
| 緩解 | 每個 PR 單一任務；Codex 先做 status check；避免同時改 index / app / workflow |
| 相關文件 | `codex_resume_plan.md`, `pr_review_guide.md`, `development_board.md` |

---

## R7. AI 摘要產生不當內容

| 項目 | 說明 |
|---|---|
| 風險 | AI 做出無來源指控、人身攻擊或過度推論 |
| 影響 | 法律與公信力風險 |
| 等級 | 高 |
| 緩解 | AI prompt 限制、人工覆核、資料聲明、低信心標示 uncertain |
| 相關文件 | `ai_classification_prompt.md`, `ai_issue_summarizer_spec.md` |

---

## R8. WordPress iframe 顯示不穩

| 項目 | 說明 |
|---|---|
| 風險 | 不同裝置或主題造成 iframe 高度、寬度或樣式問題 |
| 影響 | 官網使用體驗不佳 |
| 等級 | 低至中 |
| 緩解 | 優先使用按鈕導流；iframe 放獨立頁面；保留 fallback link |
| 相關文件 | `wordpress_embed_blocks.md`, `wordpress_integration_spec.md` |

---

## R9. 資料授權不清楚

| 項目 | 說明 |
|---|---|
| 風險 | 未確認資料是否可再利用或公開展示 |
| 影響 | 法律與信任風險 |
| 等級 | 中 |
| 緩解 | 保留來源、確認授權、必要時詢問機關或使用統計摘要 |
| 相關文件 | `information_request_templates.md`, `source_inventory.md` |

---

## R10. 專案範圍過大

| 項目 | 說明 |
|---|---|
| 風險 | 同時做 crawler、dashboard、AI、n8n、WordPress，導致任務分散 |
| 影響 | 完成度下降 |
| 等級 | 中 |
| 緩解 | 依版本路線圖推進：v0.1 → v0.2 → v0.3，不一次做完全部 |
| 相關文件 | `versioning_and_milestones.md`, `development_board.md` |
