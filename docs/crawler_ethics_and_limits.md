# Crawler 使用原則與限制 v1

本文件定義本專案 crawler 的使用原則，避免對資料來源網站造成負擔，也避免不適當使用資料。

---

## 基本原則

1. 只抓取公開可瀏覽資料。
2. 不繞過登入、驗證碼或權限限制。
3. 不抓取個資或敏感資料後公開。
4. 不高頻請求造成網站負擔。
5. 保留 source_url 與 crawled_at。
6. crawler 錯誤時應停止或降速，不應無限重試。

---

## 請求頻率

建議第一階段：

```text
每次請求間隔至少 1 - 3 秒
```

大量資料補抓時：

```text
分批抓取，不一次抓完整 12 年資料
```

---

## 允許抓取

- 公開會議紀錄 metadata
- 公開議員質詢影音 metadata
- 公開附件連結
- 公開新聞與公告標題 metadata
- 開放資料平台 API / CSV / JSON

---

## 暫不抓取

- 需要登入的資料
- 驗證碼後資料
- 個人聯絡資訊
- 非公開附件
- 大量影音檔案本體
- 可能造成網站負載的高頻資料

---

## 影音資料原則

第一階段只抓：

- title
- date
- councilor_name
- video_url
- page_url
- crawled_at

不直接下載影片。

若未來要做語音轉文字，需另行評估：

1. 檔案大小
2. 授權與使用限制
3. 儲存成本
4. 轉錄準確性
5. 對外引用方式

---

## 錯誤處理

crawler 應處理：

- timeout
- 404
- 500
- encoding error
- empty page
- duplicated record
- unexpected table format

錯誤輸出建議：

```json
{
  "source_url": "",
  "error_type": "timeout",
  "error_message": "",
  "crawled_at": "2026-05-21T09:00:00+08:00"
}
```

---

## 資料保存原則

### raw

保留原始抓取欄位，不直接覆蓋。

```text
data/raw/*.csv
```

### processed

經分類、標準化、去識別化後資料。

```text
data/processed/*.csv
```

### dashboard

公開展示用 JSON。

```text
dashboard/data/*.json
```

---

## 對外說明

若資料由 crawler 取得，應於資料來源頁標示：

```text
本資料由公開網頁 metadata 整理而成，仍應以原始官方網站內容為準。
```

---

## 禁止事項

1. 不得使用 crawler 取得非公開資料。
2. 不得公開個資。
3. 不得以 crawler 結果做未經查證的指控。
4. 不得用高頻請求造成官方網站負擔。
5. 不得移除資料來源資訊。
