# Troubleshooting 手冊 v1

本文件整理本專案常見錯誤與處理方式。

---

## 1. GitHub Actions 失敗

### 可能原因

- requirements.txt 缺套件
- pytest 測試失敗
- JSON 格式錯誤
- processor 找不到 raw CSV
- crawler 網站連線失敗

### 處理步驟

1. 打開 failed workflow。
2. 找到第一個 failed step。
3. 看錯誤是 Python、資料、JSON 還是網路。
4. 若是資料不存在，確認是否應使用 fallback。
5. 若是 JSON validation fail，修 JSON 或 processor。
6. 修正後重新 push，不要只重跑失敗 workflow。

---

## 2. GitHub Pages 沒更新

### 可能原因

- Pages workflow 還在排隊
- workflow failed
- browser cache
- dashboard 資料夾不是 deploy source
- 檔案路徑大小寫錯誤

### 處理步驟

1. 檢查 Actions 是否 deploy 成功。
2. 等待 1 - 3 分鐘。
3. 用無痕視窗打開。
4. 確認 URL：

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/
```

5. 確認檔案在 `dashboard/` 目錄內。

---

## 3. 頁面空白

### 可能原因

- JavaScript error
- JSON 讀取失敗
- selector 不存在
- 檔案路徑錯誤
- CORS / relative path 問題

### 處理步驟

1. 打開瀏覽器 DevTools Console。
2. 看是否有 404 或 JS error。
3. 確認 JSON URL 是否正確，例如：

```text
./data/dashboard_summary.json
```

4. 確認 HTML 有對應 selector。
5. 若 JSON 不存在，先補 fallback data。

---

## 4. Codex branch 衝突

### 可能原因

- main 已更新
- 多個任務同時改同一檔案
- PR 太大
- 先前工具直接 commit 到 main

### 處理步驟

1. 先不要繼續修改。
2. 檢查 PR changed files。
3. 若 branch 落後 main，先 rebase 或 merge main。
4. 若 conflict 太多，考慮關閉舊 PR，從最新 main 重新開 branch。
5. 每個 PR 控制單一任務。

---

## 5. JSON validation fail

### 常見原因

- 少必要欄位
- number 被寫成 string
- trend 值不合法
- score 超過 0 - 100
- JSON trailing comma
- report_url 空白

### 處理方式

1. 根據錯誤訊息找到檔案。
2. 對照 `docs/json_validation_rules.md`。
3. 修資料或修 processor。
4. 重新跑 pytest。

---

## 6. Crawler 抓不到資料

### 可能原因

- 網頁結構改變
- 網站暫時無回應
- encoding 問題
- pagination 改變
- query 條件錯誤

### 處理步驟

1. 保留錯誤 URL。
2. 不要無限重試。
3. 儲存 error log。
4. 降低請求頻率。
5. 確認是否仍為公開資料。
6. 必要時改為 manual download。

---

## 7. WordPress iframe 顯示不正常

### 可能原因

- iframe 高度不足
- 手機版寬度問題
- WordPress 編輯器過濾 style
- 外掛或主題覆蓋 CSS

### 處理方式

1. 增加 iframe height。
2. 外層加 max-width container。
3. 使用 WordPress 自訂 HTML 區塊。
4. 若仍不穩，改用按鈕連結，不用 iframe。

---

## 8. 資料含個資疑慮

### 處理方式

1. 立即停止公開該資料。
2. 移除或遮蔽相關欄位。
3. 依照 `docs/privacy_deidentification.md` 重新處理。
4. 重新產生 processed data。
5. 再重新發布 dashboard JSON。

---

## 9. 緊急回復方式

若 dashboard 壞掉：

1. 找到上一個正常 commit。
2. 優先 revert 造成問題的 commit。
3. 若只是 JSON 壞掉，先恢復上一版 JSON。
4. 開 hotfix PR。
5. merge 後確認 Pages 正常。

---

## 10. 查問題時要記錄

每次錯誤應記錄：

```text
時間：
錯誤頁面 / workflow：
錯誤訊息：
可能原因：
處理方式：
結果：
```
