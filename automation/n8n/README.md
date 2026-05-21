# n8n 第一階段 Workflow Templates

本資料夾放置「嘉義市 12 年城市故障分析資料庫」第一階段 n8n 自動化流程範本。

目前檔案：

```text
phase1_workflow_templates.json
```

這份 JSON 是建置參考範本，不含 credentials、token、password 或真實 webhook URL。

---

## 第一階段 Workflow

### CYFA-WF-001-Weekly-Data-Update

用途：每週觸發 GitHub workflow，更新 dashboard JSON，並建立內部更新通知。

主要節點：

```text
Cron
→ GitHub workflow_dispatch
→ Wait / Poll workflow run
→ Fetch dashboard JSON
→ Validate required files
→ Gmail internal notification
```

### CYFA-WF-003-Weekly-Report-Draft

用途：讀取 dashboard JSON，產生週報草稿。

主要節點：

```text
Cron
→ GitHub Read Files
→ Function Build Report Payload
→ AI Draft Summary
→ Google Docs Draft
→ Gmail Draft
```

### CYFA-WF-005-Update-Failure-Alert

用途：GitHub Actions 或 n8n workflow 發生錯誤時，建立內部異常通知。

主要節點：

```text
Webhook / Error Trigger
→ Parse Error
→ Remove Sensitive Data
→ Gmail Internal Alert
```

---

## 安裝方式

1. 在 n8n 建立三個 workflow。
2. 依照 `phase1_workflow_templates.json` 建立節點。
3. 在 n8n credential store 設定 GitHub / Gmail / Google Docs / AI model credentials。
4. 不要把任何 credential、token、password 或 webhook secret 寫入 repo。
5. 先手動執行測試，再開啟 Cron。

---

## 必要 GitHub 目標

第一階段優先觸發：

```text
.github/workflows/dashboard-data.yml
```

必要檢查檔案：

```text
dashboard/data/dashboard_summary.json
dashboard/data/issue_ranking.json
dashboard/data/hotspots.json
dashboard/data/data_sources.json
```

---

## 安全底線

第一階段只做內部草稿與通知。

不可做：

1. 不自動發文。
2. 不公開 Google Drive / Google Docs 分享權限。
3. 不自動寄出對外 email。
4. 不公開個人表單資料。
5. 不把 GitHub token 寫入 repo。
6. 不把錯誤 log 中的 secret 原文寄出。

需要人工確認後才可做：

1. 正式公開週報。
2. 對外寄送 email。
3. 修改 Google Drive 分享權限。
4. 發布社群文章。
5. 把表單資料公開展示。

---

## 驗收清單

### WF-001

- [ ] 可手動觸發。
- [ ] 可觸發 GitHub workflow_dispatch。
- [ ] 可讀取 workflow run 結果。
- [ ] 可確認 dashboard JSON 存在。
- [ ] 可建立內部通知。

### WF-003

- [ ] 可讀取 dashboard JSON。
- [ ] 可產生 Markdown 週報草稿。
- [ ] 可建立 Google Doc 草稿。
- [ ] 可建立 Gmail 草稿。
- [ ] 報告內含資料限制與聲明。

### WF-005

- [ ] 可接收錯誤事件。
- [ ] 可整理錯誤摘要。
- [ ] 可移除敏感資訊。
- [ ] 可寄送內部異常通知。

---

## 專案內測試

```bash
pytest -q tests/test_n8n_phase1_contract.py
pytest -q tests/test_n8n_phase1_workflow_templates.py
pytest -q
```

---

## 對外說明原則

週報與自動摘要只能稱為：

```text
城市治理資料整理
城市故障分析草稿
公開資料輔助分析
```

不可稱為：

```text
民調
支持度調查
完整民意結論
對個人的評價結論
```
