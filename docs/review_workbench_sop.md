# 人工審核工作台 SOP

本文件整理目前 dashboard 內「人工審核工作台」的共同作業原則，讓座標審核、影音轉錄審核與後續會議紀錄解析審核有一致流程。

---

## 一、工作台目標

人工審核工作台不是對外發布系統，而是把 crawler、builder、dashboard 產出的原型資料，先經過人工確認，再進入正式分析。

目前已建立的審核工作台：

| 工作台 | 頁面 | 資料檔 | 主要目的 |
|---|---|---|---|
| 座標審核 | `dashboard/geocoding-review.html` | `dashboard/data/geocoding_review_queue.json` | 檢查 prototype 座標與地名是否合理。 |
| 影音轉錄審核 | `dashboard/video-review.html` | `dashboard/data/transcript_review_queue.json` | 檢查質詢影音 metadata，安排後續轉錄與人工校對。 |

後續可加入：

| 工作台 | 預定用途 |
|---|---|
| 會議紀錄解析審核 | 檢查 PDF / HTML parser 產出的會議名稱、日期、議員、局處、議題與原文段落。 |
| 1999 資料審核 | 檢查資料來源授權、欄位去識別化、分類與公開範圍。 |
| 週報審核 | 檢查 n8n 週報草稿是否可公開、是否有未查證結論或個資。 |

---

## 二、共通原則

1. 先審核，再分析。
2. 原型資料不可標示為正式結論。
3. 未人工 review 的資料不得用於對外指控。
4. 不將 API key、token、credential 寫入 repo。
5. 不輸出私人地址、電話、email、身分證字號等敏感欄位。
6. 對外引用時應保留來源、日期、連結與上下文。
7. 不自動公開發布；自動化流程只能產生草稿、清單或內部通知。
8. 儀表板用於城市治理研究，不是民調，也不是支持度調查。

---

## 三、標準審核流程

### Step 1：確認來源

每筆資料應先確認：

| 檢查項目 | 說明 |
|---|---|
| 來源是否公開 | 只使用公開可查證來源。 |
| 來源是否穩定 | 是否有固定網址、檔案、頁面或 raw hash。 |
| 來源是否需授權 | 若不是公開資料，不得直接匯入。 |
| 是否含個資 | 若含個資，先去識別化或排除。 |

### Step 2：確認欄位完整性

基本欄位應包含：

```text
source_id
raw_hash
review_status
notes
```

依資料類型補充：

| 類型 | 必要欄位 |
|---|---|
| 座標審核 | `place_name`、`lat`、`lng`、`geo_precision`、`suggested_review_method` |
| 影音審核 | `video_title`、`video_url`、`video_platform`、`transcript_status` |
| 會議紀錄 | `meeting_name`、`meeting_date`、`councilor_name`、`department`、`agenda_item` |

### Step 3：人工修正或標記

人工審核後，應選擇明確狀態：

| 狀態 | 使用時機 |
|---|---|
| `unreviewed` | 尚未檢查。 |
| `needs_metadata_review` | 缺日期、名稱、會期、來源等基本資料。 |
| `reviewed` | 已人工確認，可進入下一階段。 |
| `verified` | 已由可信來源交叉驗證。 |
| `rejected` | 來源錯誤、資料失效、不適合使用。 |

### Step 4：記錄人工判斷理由

每次把資料從 `unreviewed` 改成 `reviewed` 或 `verified`，應留下：

```text
reviewed_at
reviewer
review_notes
source_context
```

`reviewer` 建議用代號，不放個資。

---

## 四、各工作台操作重點

### 1. 座標審核

頁面：

```text
dashboard/geocoding-review.html
```

資料：

```text
dashboard/data/geocoding_review_queue.json
```

審核重點：

1. `place_name` 是否為嘉義市在地常用名稱。
2. 是否避免使用不建議稱呼，例如使用「文化路商圈」作為統一稱呼。
3. `geo_precision` 是否仍為 `prototype`、`unknown` 或 `uncertain`。
4. `review_status` 是否尚未人工確認。
5. 地點是否能用公開地圖交叉檢查。

禁止事項：

1. 不接外部 geocoding API。
2. 不加入 API key。
3. 不把 prototype 座標當成正式精準座標。
4. 不用於工程定位、執法或個人評價。

### 2. 影音轉錄審核

頁面：

```text
dashboard/video-review.html
```

資料：

```text
dashboard/data/transcript_review_queue.json
```

審核重點：

1. `councilor_name` 是否缺漏。
2. `meeting_date` 是否缺漏。
3. `video_url` 是否為公開來源。
4. `transcript_status` 是否仍為 `not_started`。
5. 是否需要先補 metadata，再進入轉錄候選。

禁止事項：

1. 不下載影音。
2. 不呼叫 Whisper。
3. 不呼叫外部 ASR API。
4. 不加入 API key。
5. 不把 AI 轉錄初稿標示為正式逐字稿。

### 3. 會議紀錄解析審核

此項等待 parser spec 與 fixture prototype 完成後加入正式頁面。

預計審核重點：

1. PDF / HTML parser 是否正確擷取會議名稱。
2. 日期格式是否一致。
3. 議員姓名是否正確。
4. 局處名稱是否正確。
5. 議題關鍵字是否只是初步標籤。
6. 原文段落是否保留上下文。

禁止事項：

1. 不寫入 Google Sheet credential。
2. 不把 token 寫入 repo。
3. 不抓取非公開資料。
4. 不輸出個資。

---

## 五、資料進入正式分析前的門檻

資料要進入 `processed` 或正式 dashboard 分析，至少要滿足：

| 門檻 | 說明 |
|---|---|
| 來源可追溯 | 有公開來源、檔名、連結或 raw hash。 |
| 欄位完整 | 必要欄位不為空。 |
| 狀態明確 | `review_status` 不可停在 `unreviewed`。 |
| 個資排除 | 不含私人電話、email、地址、身分證字號。 |
| 結論保守 | 不把分類、摘要或 AI 判斷當成事實結論。 |
| 可重跑 | builder 或 parser 應能由 fixture 或 raw data 重跑。 |

---

## 六、對外使用規範

可以對外使用：

1. 經人工確認的公開資料摘要。
2. 有來源連結與日期的市政議題整理。
3. 不針對個人人身攻擊的政策分析。
4. 清楚標示為「資料整理」「趨勢觀察」「城市故障分析」的內容。

不應對外使用：

1. 未人工審核的原型資料。
2. 未查證的 AI 摘要。
3. 片段式截圖或斷章取義。
4. 推論成違法、瀆職、貪污等未查證指控。
5. 作為民調、支持度調查或選民個資分析。

---

## 七、一人團隊每日操作建議

每天 20 分鐘即可執行：

1. 打開 dashboard 首頁，確認資料是否更新。
2. 檢查座標審核 queue 是否有高優先項目。
3. 檢查影音轉錄 queue 是否有 `needs_metadata_review`。
4. 每天人工確認 3 到 5 筆資料。
5. 把可用議題整理成「地方問題紀錄」，不要直接做攻擊文案。
6. 每週整理一次「可提出政策解法」的清單。

---

## 八、PR 驗收清單

未來只要新增人工審核工作台，PR 至少應確認：

1. 有對應 dashboard 頁面或 JSON queue。
2. 有資料 schema 測試。
3. 有安全聲明。
4. 有 fixture 或 sample data。
5. `pytest -q` 通過。
6. 不新增 credential、token、API key。
7. 不自動公開發布。
8. 不輸出敏感個資欄位。
9. 不把 prototype 或 AI 初稿標示為正式結論。

---

## 九、核心判斷句

遇到不確定資料時，使用以下判斷：

```text
這筆資料能不能被公開查證？
這筆資料有沒有經過人工 review？
這筆資料會不會被市民誤認為正式結論？
這筆資料是否包含不該公開的個資？
這個結論是否超出原始資料能支持的範圍？
```

只要有任何一題答案不確定，就先留在 review queue，不進正式分析。
