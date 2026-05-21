# n8n 自動化流程藍圖 v1

本文件定義「嘉義城市故障分析資料庫」可用的 n8n 自動化流程。

---

## 目標

讓資料平台未來能自動完成：

1. 定期觸發 crawler
2. 更新 dashboard JSON
3. 產生城市週報
4. 產生社群文案草稿
5. 寄送 Gmail 摘要
6. 寫入 Google Sheet / Google Docs

---

## Workflow 1：每週資料更新

### 名稱

```text
WF-001｜每週嘉義城市故障資料更新
```

### 觸發

```text
Cron｜每週一 09:00
```

### 流程

```text
Cron
→ GitHub Actions workflow_dispatch
→ crawler
→ raw CSV
→ processor
→ dashboard JSON
→ GitHub Pages deploy
→ Gmail 通知
```

### 輸出

- data/raw/*.csv
- dashboard/data/*.json
- GitHub Actions log
- Gmail 更新通知

---

## Workflow 2：Google Sheet 人工校正後更新 dashboard

### 名稱

```text
WF-002｜Google Sheet 校正資料同步 dashboard
```

### 觸發

```text
Google Sheets Trigger
```

### 流程

```text
Google Sheets Trigger
→ Read Rows
→ Transform JSON
→ GitHub API Update File
→ GitHub Pages deploy
→ Gmail 通知
```

### 適合資料

- 熱點資料
- 議題分類字典
- 資料來源狀態
- 城市週報摘要

---

## Workflow 3：每週城市故障週報

### 名稱

```text
WF-003｜嘉義城市故障週報生成
```

### 觸發

```text
Cron｜每週一 10:00
```

### 流程

```text
Cron
→ Read dashboard JSON
→ AI summary
→ Generate Markdown
→ Generate HTML
→ Create Google Doc
→ Create Gmail draft
→ GitHub commit reports
```

### 輸出

- reports/markdown/YYYY-WW.md
- dashboard/reports/YYYY-WW.html
- reports/json/YYYY-WW.json
- Google Doc
- Gmail draft

---

## Workflow 4：社群文案草稿

### 名稱

```text
WF-004｜城市故障週報社群文案草稿
```

### 輸入

- 最新週報
- issue_trends.json
- ai_issue_summary.json

### 輸出

1. FB 長文
2. Threads 短文
3. LINE 群組版
4. 短影音 30 秒口播稿
5. 海報標語

### 注意

不可使用：

- 民調
- 支持度調查
- 人身攻擊
- 無來源指控

---

## Workflow 5：資料異常通知

### 名稱

```text
WF-005｜資料更新異常通知
```

### 觸發

```text
GitHub Actions failed
```

### 流程

```text
GitHub webhook
→ n8n
→ Parse error
→ Gmail / LINE 通知
```

### 通知內容

- failed workflow name
- failed commit
- error summary
- next action suggestion

---

## Workflow 6：城市故障回報資料同步

### 名稱

```text
WF-006｜城市故障回報資料同步
```

### 資料來源

- WordPress form
- SureForms
- Google Forms
- Google Sheet

### 流程

```text
Form submit
→ Google Sheet
→ 去識別化
→ issue classification
→ hotspot update
→ dashboard JSON
```

### 隱私原則

1. 不公開姓名
2. 不公開電話
3. 不公開 email
4. 只公開分類、地點與摘要統計

---

## 建議導入順序

### 第一階段

1. WF-001 每週資料更新
2. WF-003 每週週報
3. WF-005 異常通知

### 第二階段

4. WF-002 Google Sheet 校正同步
5. WF-004 社群文案草稿

### 第三階段

6. WF-006 城市故障回報資料同步

---

## API / 權限需求

- GitHub token
- Google Sheet OAuth
- Google Docs OAuth
- Gmail OAuth
- OpenAI / AI model API key
- WordPress form webhook

---

## 安全注意事項

1. GitHub token 不可寫在 repo。
2. n8n credentials 使用 n8n 內建 credential store。
3. 表單資料需先去識別化再公開。
4. AI 摘要需標示為輔助分析，不代表最終事實。
5. 所有自動發文流程第一階段只產生草稿，不自動發布。
