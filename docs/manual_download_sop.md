# Manual Download SOP

本文件用來規劃正式公開資料進入系統前的人工下載流程。目標是在 crawler / fetcher 尚未通過權限審查前，仍能用低風險、可追蹤、可人工覆核的方式建立本地資料樣本。

---

## 一、適用範圍

```text
official public pages
open data files
council records
public complaint summaries
city project reports
budget or procurement documents
```

本 SOP 適合用於第一階段資料建立、來源確認、parser fixture 製作與人工覆核。

---

## 二、基本原則

1. 優先使用公開來源。
2. 優先使用官方下載功能或公開開放資料檔。
3. 不繞過登入、驗證碼、付費牆或技術限制。
4. 不下載非必要大量資料。
5. 不收集非必要個資。
6. 每次下載都要記錄來源、時間、檔名與用途。
7. 下載後先進人工審核，不直接對外發布。

---

## 三、建議資料夾結構

```text
data/raw/manual_downloads/
  source_registry.json
  README.md
  YYYYMMDD_source-name_file-name.ext

tests/fixtures/official_sources/
  sample_source_name.html
  sample_source_name.txt
  sample_source_name.json
```

---

## 四、每次下載需記錄欄位

每筆人工下載紀錄至少包含：

```text
download_id
source_id
source_name
source_url
downloaded_at
downloaded_by
file_path
file_sha256
file_type
review_status
public_use_status
notes
```

---

## 五、狀態規則

1. `review_status` 初始應為 `needs_manual_review`。
2. `public_use_status` 初始應為 `internal_source_sample`。
3. `file_sha256` 應可用來確認檔案未被任意修改。
4. `notes` 應提醒資料來源、下載目的與是否可公開使用仍需確認。

---

## 六、人工覆核步驟

1. 確認來源網址。
2. 確認來源單位。
3. 確認是否為公開資料。
4. 確認授權或使用限制。
5. 確認是否含個資或敏感欄位。
6. 確認檔案是否完整。
7. 確認是否適合轉成 parser fixture。
8. 對外使用前再次人工確認。

---

## 七、不可做事項

1. 不把手動下載資料直接當正式分析結論。
2. 不把未審核資料放上公開 dashboard。
3. 不在 repo 內放入含有非公開個資的原始檔。
4. 不提交 credential、token、API key 或登入 cookies。
5. 不下載或散布不符合授權的資料。
6. 不把人工下載流程包裝成即時自動資料系統。

---

## 八、建議測試與驗收

未來若新增 manual download registry builder，測試至少涵蓋：

1. registry JSON 可讀。
2. 必要欄位存在。
3. file_sha256 格式正確。
4. review_status 正確。
5. public_use_status 正確。
6. 不含 credential 欄位。
7. 不含電話、email、身分證字號等私人資料欄位。
8. dashboard 或 review queue 清楚標示人工審核。

---

## 九、合併條件

1. Python Tests 成功。
2. 不連外自動抓資料。
3. 不加入 credential。
4. 不輸出私人資料欄位。
5. 資料來源與下載紀錄可追蹤。
6. 所有資料進入人工覆核。
7. 對外使用邊界清楚。

---

## 十、下一步

合併 manual download SOP 後，可再推進：

1. manual download registry sample。
2. source fixture preparation guide。
3. official data update cadence checklist。
4. parser fixture review dashboard。
