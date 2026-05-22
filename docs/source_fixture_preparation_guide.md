# Source Fixture Preparation Guide

本文件用來規劃如何把人工下載或公開樣本資料整理成 parser fixture。目標是讓 parser 可以在不連網、不接觸私人資料、不依賴外部網站狀態的情況下被穩定測試。

---

## 一、目的

```text
manual download
  -> source review
  -> sanitized fixture
  -> parser test
  -> parser output review queue
```

fixture 是測試用樣本，不是正式資料庫，也不是對外結論。

---

## 二、建議資料夾

```text
tests/fixtures/official_sources/
  README.md
  source_id_sample.html
  source_id_sample.txt
  source_id_sample.json
```

若 fixture 來自人工下載，原始下載紀錄應回查到：

```text
data/raw/manual_downloads/source_registry.json
```

---

## 三、fixture 必要 metadata

每個 fixture 至少應有對應 metadata，包含：

```text
fixture_id
source_id
source_name
source_url
fixture_file
created_at
created_by
sanitization_status
review_status
public_use_status
notes
```

---

## 四、清理與去識別規則

建立 fixture 前應檢查：

1. 是否含電話。
2. 是否含 email。
3. 是否含身分證字號。
4. 是否含完整地址。
5. 是否含非公開個人姓名與可識別描述。
6. 是否含登入 token、cookie、API key。
7. 是否含非公開內部備註。

若 parser 測試必須保留欄位格式，應使用假資料替代，不可提交真實敏感資料。

---

## 五、fixture 寫法建議

1. 保留足夠的 HTML / text 結構，讓 parser 可以被測試。
2. 刪除與測試無關的大量內容。
3. 用短樣本覆蓋主要欄位。
4. 加入至少一個正常案例。
5. 加入至少一個缺欄位或格式異常案例。
6. 不放入大型檔案。
7. 不依賴外部網址即時可用。

---

## 六、review_status 建議

```text
needs_fixture_review
fixture_reviewed
needs_sanitization
sanitized_sample
not_safe_for_repo
```

---

## 七、public_use_status 建議

```text
internal_fixture_only
sanitized_test_sample
not_for_public_use
```

---

## 八、測試建議

未來新增 parser fixture 時，至少測試：

1. fixture 檔案存在。
2. fixture 不為空。
3. parser 可讀取 fixture。
4. parser output 欄位完整。
5. raw_hash 穩定。
6. review_status 正確。
7. public_use_status 正確。
8. fixture 不含 credential。
9. fixture 不含私人資料欄位。
10. parser 不因格式異常而 crash。

---

## 九、不可做事項

1. 不提交含個資的原始檔。
2. 不提交登入後頁面內容。
3. 不提交 cookies、token、API key。
4. 不把 fixture 當正式資料來源。
5. 不把 parser 測試結果當正式市政結論。
6. 不自動發布 fixture 內容。

---

## 十、合併條件

1. Python Tests 成功。
2. fixture 可回查來源登記。
3. fixture 已去識別。
4. fixture 不含 credential。
5. parser output 仍需人工覆核。
6. 對外使用邊界清楚。

---

## 十一、下一步

合併本 guide 後，可再推進：

1. fixture metadata schema。
2. parser fixture review dashboard。
3. official source sample fixtures。
4. source update cadence checklist。
