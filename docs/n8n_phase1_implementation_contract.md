# n8n 第一階段實作契約 v1

本文件把 `docs/n8n_workflow_blueprints.md` 中的第一階段流程，整理成可交給 n8n 建置的實作契約。

第一階段只做資料更新、週報草稿與異常通知，不自動公開發布內容。

---

## 一、第一階段範圍

### 本階段要做

1. WF-001｜每週嘉義城市故障資料更新
2. WF-003｜嘉義城市故障週報生成
3. WF-005｜資料更新異常通知

### 本階段不做

1. 不自動發文到社群平台。
2. 不公開個人表單資料。
3. 不把 GitHub token 寫入 repo。
4. 不直接修改 Google Drive 檔案分享權限。
5. 不自動寄出對外 email，只建立草稿或寄送內部通知。

---

## 二、共用 Credentials

n8n credentials 應存放在 n8n credential store，不得寫入 GitHub repo。

| Credential | 用途 |
|---|---|
| GitHub credential | 觸發 GitHub Actions、讀取 repo 檔案、必要時建立 commit |
| Gmail credential | 寄送內部異常通知或建立週報草稿 |
| Google Docs credential | 建立週報草稿文件 |
| OpenAI / AI model credential | 產生週報摘要草稿 |

---

## 三、WF-001｜每週嘉義城市故障資料更新

### 觸發

```text
Cron：每週一 09:00 Asia/Taipei
```

### 輸入

無人工輸入。

### 節點順序

```text
Cron
→ GitHub workflow_dispatch
→ Wait / Poll workflow run
→ Fetch generated dashboard JSON
→ Validate required files
→ Create internal summary
→ Gmail internal notification
```

### GitHub workflow_dispatch 建議目標

優先觸發：

```text
.github/workflows/dashboard-data.yml
```

若未來 crawler workflow 拆出，可改觸發：

```text
.github/workflows/crawler.yml
```

### 必查輸出檔案

```text
dashboard/data/dashboard_summary.json
dashboard/data/issue_ranking.json
dashboard/data/hotspots.json
dashboard/data/data_sources.json
```

### 成功通知內容

```text
主旨：嘉義城市故障資料更新完成
內容：
- workflow name
- run url
- commit sha
- dashboard JSON 檢查結果
- 下一步建議
```

### 失敗處理

若 GitHub Actions 失敗，轉交 WF-005。

---

## 四、WF-003｜嘉義城市故障週報生成

### 觸發

```text
Cron：每週一 10:00 Asia/Taipei
```

建議排在 WF-001 之後，避免週報讀到舊資料。

### 輸入資料

```text
dashboard/data/dashboard_summary.json
dashboard/data/issue_ranking.json
dashboard/data/hotspots.json
dashboard/data/ai_issue_summary.json
dashboard/data/issue_trends.json
```

若 `ai_issue_summary.json` 或 `issue_trends.json` 尚未存在，週報需以 prototype / data pending 標示，不可假裝已有正式分析。

### 週報輸出格式

1. Markdown 草稿
2. HTML 草稿
3. JSON 摘要
4. Google Doc 草稿
5. Gmail 草稿

### 週報 Markdown 結構

```markdown
# 嘉義城市故障週報 YYYY-WW

## 一、本週摘要

## 二、熱門議題排行

## 三、城市熱點觀察

## 四、局處與行政流程觀察

## 五、下週追蹤事項

## 六、資料限制與聲明
```

### AI 摘要限制

AI 只能做：

1. 摘要
2. 分類
3. 提醒待追蹤事項
4. 產生草稿文字

AI 不可做：

1. 無來源指控
2. 人身攻擊
3. 支持度推論
4. 把 prototype 資料說成正式結論
5. 把資料摘要說成民調

---

## 五、WF-005｜資料更新異常通知

### 觸發

```text
GitHub Actions failed webhook
或 WF-001 / WF-003 中任一節點失敗
```

### 節點順序

```text
Webhook / Error Trigger
→ Parse workflow metadata
→ Fetch failed job summary
→ Create error summary
→ Gmail internal notification
```

### 通知內容

```text
主旨：嘉義城市故障資料流程異常
內容：
- workflow name
- run url
- failed job
- commit sha
- error summary
- 建議處理動作
```

### 異常通知原則

1. 只寄內部通知。
2. 不公開錯誤訊息。
3. 不把 token、credential、secret 放進通知內容。
4. 若錯誤內容含敏感資訊，需摘要後再寄出。

---

## 六、建議 n8n Workflow 命名

```text
CYFA-WF-001-Weekly-Data-Update
CYFA-WF-003-Weekly-Report-Draft
CYFA-WF-005-Update-Failure-Alert
```

CYFA = Chiayi Failure Analysis。

---

## 七、驗收清單

### WF-001

- [ ] 可手動執行一次。
- [ ] 可觸發 GitHub workflow_dispatch。
- [ ] 可讀取 workflow run 結果。
- [ ] 可檢查 dashboard JSON 是否存在。
- [ ] 成功時建立內部通知。

### WF-003

- [ ] 可讀取 dashboard JSON。
- [ ] 可產生 Markdown 週報草稿。
- [ ] 可產生 Google Doc 草稿。
- [ ] 可建立 Gmail 草稿。
- [ ] 報告內含資料限制與聲明。

### WF-005

- [ ] 可接收 workflow failed 事件。
- [ ] 可整理錯誤摘要。
- [ ] 可寄送內部異常通知。
- [ ] 不洩漏 secret / token / credential。

---

## 八、安全底線

```text
第一階段只建立自動化草稿與內部通知，不做公開發布。
```

任何公開發布、分享權限修改、正式寄送對外 email，都需要人工確認。
