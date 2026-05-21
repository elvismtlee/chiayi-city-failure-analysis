# n8n 手動驗收清單 v1

本文件用於 n8n 第一階段 workflow 正式啟用前的人工檢查。

對應 Issue：

```text
#10｜建立 n8n 每週資料更新與週報流程
```

對應文件：

```text
docs/n8n_workflow_blueprints.md
docs/n8n_phase1_implementation_contract.md
automation/n8n/phase1_workflow_templates.json
automation/n8n/README.md
```

---

## 一、啟用前總原則

第一階段只允許：

```text
內部通知
草稿建立
資料更新檢查
錯誤提醒
```

第一階段不允許：

```text
自動公開發文
自動寄出對外 email
公開分享 Google Drive / Docs
公開個人表單資料
把 token / secret / credential 寫入 repo
```

---

## 二、Credentials 檢查

| 項目 | 狀態 |
|---|---|
| GitHub credential 已存放於 n8n credential store | □ |
| Gmail credential 已存放於 n8n credential store | □ |
| Google Docs credential 已存放於 n8n credential store | □ |
| AI model credential 已存放於 n8n credential store | □ |
| repo 內沒有 token / secret / password / webhook secret | □ |
| workflow 匯出檔不含 credential 原文 | □ |

---

## 三、WF-001 每週資料更新驗收

Workflow 名稱：

```text
CYFA-WF-001-Weekly-Data-Update
```

驗收項目：

| 項目 | 狀態 |
|---|---|
| 可手動執行 workflow | □ |
| 可觸發 GitHub workflow_dispatch | □ |
| 目標 workflow 為 dashboard-data.yml | □ |
| 可讀取 GitHub Actions run status | □ |
| 成功時可整理 run url / commit sha / JSON 檢查摘要 | □ |
| 失敗時會轉入 WF-005 或錯誤通知流程 | □ |
| 通知只寄內部收件人 | □ |

必查 dashboard JSON：

```text
dashboard/data/dashboard_summary.json
dashboard/data/issue_ranking.json
dashboard/data/hotspots.json
dashboard/data/data_sources.json
```

---

## 四、WF-003 週報草稿驗收

Workflow 名稱：

```text
CYFA-WF-003-Weekly-Report-Draft
```

驗收項目：

| 項目 | 狀態 |
|---|---|
| 可手動執行 workflow | □ |
| 可讀取 dashboard JSON | □ |
| 可產生 Markdown 草稿 | □ |
| 可產生 HTML 草稿 | □ |
| 可建立 Google Doc 草稿 | □ |
| 可建立 Gmail draft | □ |
| 不會自動寄出 email | □ |
| 不會公開分享 Google Doc | □ |
| 報告內有資料限制與聲明 | □ |
| prototype / sample 資料有明確標示 | □ |

週報必含段落：

```text
一、本週摘要
二、熱門議題排行
三、城市熱點觀察
四、局處與行政流程觀察
五、下週追蹤事項
六、資料限制與聲明
```

---

## 五、WF-005 異常通知驗收

Workflow 名稱：

```text
CYFA-WF-005-Update-Failure-Alert
```

驗收項目：

| 項目 | 狀態 |
|---|---|
| 可接收 workflow failed event | □ |
| 可接收 n8n error trigger | □ |
| 可整理 workflow name | □ |
| 可整理 run url | □ |
| 可整理 failed job | □ |
| 可整理 error summary | □ |
| 可移除敏感資訊 | □ |
| 只寄內部通知 | □ |
| 不公開錯誤 log | □ |

通知內容應包含：

```text
workflow name
run url
failed job
commit sha
error summary
recommended next action
```

不得包含：

```text
token
secret
credential
private key
password
個人姓名與聯絡資訊
```

---

## 六、資料與用語檢查

| 項目 | 狀態 |
|---|---|
| 不把資料摘要稱為民調 | □ |
| 不把資料摘要稱為支持度調查 | □ |
| 不做支持度推論 | □ |
| 不做人身攻擊 | □ |
| 不做無來源指控 | □ |
| 對外資料使用「文化路商圈」等正確在地稱呼 | □ |
| prototype 資料不得寫成正式結論 | □ |
| 所有對外摘要都含資料限制 | □ |

---

## 七、GitHub repo 檢查

啟用前建議執行：

```bash
pytest -q
python src/processors/build_dashboard_data.py
python scripts/build_issue_classified_sample.py
python scripts/build_issue_trends.py
```

若任何一項失敗，不應啟用 n8n Cron。

---

## 八、啟用順序

建議順序：

```text
1. 手動測試 WF-001
2. 手動測試 WF-005
3. 手動測試 WF-003
4. 啟用 WF-001 Cron
5. 啟用 WF-003 Cron
6. 保留 WF-005 為錯誤處理 workflow
```

---

## 九、回滾方式

若流程異常：

1. 先停用 n8n Cron。
2. 不刪除 repo 檔案。
3. 檢查 GitHub Actions run log。
4. 檢查 n8n execution log。
5. 確認沒有自動公開發布。
6. 修正後再手動測試。

---

## 十、正式啟用前確認

```text
我確認 n8n 第一階段只產生內部通知與草稿，不自動公開發布、不自動對外寄信、不公開個人資料、不寫入 credential 到 repo。
```

確認人：＿＿＿＿＿＿＿＿

日期：＿＿＿＿＿＿＿＿
