# GitHub Actions 自動化策略 v1

本文件定義「嘉義城市故障分析資料庫」的 GitHub Actions 自動化方向。

---

## 目標

讓每次 PR / merge 都能自動檢查：

1. Python 測試是否通過
2. crawler 是否可執行
3. processor 是否可產生 dashboard JSON
4. dashboard JSON 是否格式正確
5. GitHub Pages 是否可部署
6. 不會把錯誤資料發布到公開頁面

---

## 建議 workflow

### 1. Python Tests

檔案建議：

```text
.github/workflows/python-tests.yml
```

觸發：

```yaml
on:
  pull_request:
  push:
    branches: [main]
```

執行項目：

```bash
python -m pip install -r requirements.txt
pytest
```

---

### 2. Dashboard Data Build

檔案建議：

```text
.github/workflows/build-dashboard-data.yml
```

用途：

```text
CSV → dashboard JSON
```

執行項目：

```bash
python src/processors/build_dashboard_data.py
python -m pytest tests/test_dashboard_json_validation.py
```

---

### 3. GitHub Pages Deploy

檔案建議：

```text
.github/workflows/pages.yml
```

部署來源：

```text
dashboard/
```

公開網址：

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/
```

---

## 建議分階段導入

### 第一階段

- Python Tests
- JSON validation tests

### 第二階段

- Dashboard Data Build
- Pages Deploy

### 第三階段

- Scheduled crawler
- Scheduled weekly reports
- Failed workflow notification

---

## workflow_dispatch

建議所有重要 workflow 支援手動觸發：

```yaml
on:
  workflow_dispatch:
```

用途：

1. 手動重建 dashboard JSON
2. 手動重跑 crawler
3. 手動產生週報
4. n8n 可透過 GitHub API 觸發

---

## Scheduled workflow

建議 weekly crawler：

```yaml
on:
  schedule:
    - cron: '0 1 * * 1'
```

說明：

UTC 週一 01:00，約台灣時間週一 09:00。

---

## PR 檢查要求

PR merge 前至少應通過：

- Python Tests
- JSON validation

若 PR 影響 dashboard，還應確認：

- Pages preview 或本地靜態頁正常
- dashboard/data/*.json 可正常讀取

---

## 避免 secrets 外洩

不得將下列內容寫入 repo：

- GitHub token
- OpenAI API key
- Google OAuth secret
- Gmail token
- WordPress password
- n8n credential

應使用：

```text
GitHub Actions Secrets
n8n Credentials
local .env file
```

`.env` 必須加入 `.gitignore`。

---

## 失敗處理原則

若 workflow failed：

1. 先看 failed job log。
2. 不要直接 re-run 全部。
3. 判斷是 code 問題、資料問題、網路問題或環境問題。
4. 若是資料來源暫時失敗，processor 應 fallback，不應讓整個 dashboard 空白。
5. 若是 JSON validation fail，應阻止部署。

---

## 成功標準

一個完整自動化循環應達到：

```text
crawler success
→ raw CSV updated
→ processor success
→ dashboard JSON valid
→ tests passed
→ GitHub Pages deployed
→ user can open dashboard
```
