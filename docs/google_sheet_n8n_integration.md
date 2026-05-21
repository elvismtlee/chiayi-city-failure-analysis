# Google Sheet / n8n 整合規格 v1

本文件定義資料如何在 Google Sheet、n8n、GitHub Pages 之間流動。

## 目標

建立低成本、可維護、可人工檢查的資料更新流程。

---

## 資料流

```text
crawler
→ data/raw/*.csv
→ data/processed/*.csv
→ dashboard/data/*.json
→ GitHub Pages
```

第二階段加入：

```text
Google Sheet
→ n8n
→ GitHub API
→ dashboard/data/*.json
→ GitHub Pages
```

---

## Google Sheet 分頁

建議分頁：

1. 資料源盤點
2. 1999陳情案件
3. 議員質詢
4. 議題分類字典
5. 地理熱點
6. 投訴質詢對照
7. 儀表板指標
8. n8n流程設計
9. Codex開發任務

---

## n8n Workflow

### WF-001 每週抓取資料

Cron
→ GitHub Actions workflow dispatch
→ crawler
→ CSV
→ JSON
→ Pages deploy

### WF-002 Google Sheet 更新 dashboard

Google Sheets Trigger
→ Convert Rows to JSON
→ GitHub API Update File
→ Pages deploy

### WF-003 城市週報

Cron
→ Read JSON
→ AI summary
→ Google Docs
→ Gmail draft

---

## GitHub API 更新檔案

n8n 可更新：

```text
dashboard/data/dashboard_summary.json
dashboard/data/issue_ranking.json
dashboard/data/hotspots.json
```

---

## 注意事項

1. Google Sheet 適合人工校正資料。
2. GitHub 適合版本控管與部署。
3. n8n 適合排程與通知。
4. 大量資料未來應轉 BigQuery 或資料庫。
5. 第一階段不要過度複雜化。
