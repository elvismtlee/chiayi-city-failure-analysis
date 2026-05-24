# 上線 QA 檢查清單

這份清單是 `chiayi-city-failure-analysis` 在 GitHub Pages 上線前的最後人工驗收。

## 1. 上線網址

預期網址：

- https://elvismtlee.github.io/chiayi-city-failure-analysis/

## 2. 主要入口檢查

請人工打開以下頁面：

- `index.html`
- `project-landing.html`
- `source-verification-workspace.html`
- `command-center.html`
- `open-data-day1-operation-board.html`

## 3. 每頁要人工打開檢查什麼

每一頁都要確認：

- 是否能正常載入
- shared nav 是否有出現
- 手機版是否能閱讀
- 主要 CTA 是否能點
- 是否沒有 `404` 連結
- 是否沒有誤導成已啟動 crawler

## 4. 安全字樣檢查

請確認主要頁面能看到以下安全邊界字樣：

- `no live crawler`
- `no source_url requests`
- `no personal data`
- `no private complaint full text`
- `no auto publish`
- `crawler_execution_allowed = false`
- `engineering_review_allowed = false`
- `approved_for_crawling` 不可自動設定

## 5. 上線後下一步

上線後的實際操作順序：

1. 手動打開資料源人工檢查工作台
2. 選 3 筆官方資料源
3. 人工打開 URL
4. 填 8 個欄位
5. 不寫 crawler
6. 不抓資料
7. 不標 `approved_for_crawling`

## 6. 補充提醒

- 這次上線不是啟動自動抓取
- 這次上線不是宣告資料已審核完成
- 這次上線只是把首頁、主入口、資料源檢查工作台與 GitHub Pages 部署路徑整理到可穩定展示的狀態
