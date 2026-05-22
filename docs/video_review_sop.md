# 影音轉錄審核 SOP

本文件定義 `dashboard/data/transcript_review_queue.json` 與 `dashboard/video-review.html` 的人工審核流程。目標是先把嘉義市議會質詢影音 metadata 整理成可追蹤的待處理清單，再逐步進入轉錄、人工校對、議題分類與城市故障分析。

---

## 一、目前階段定位

目前階段只做「待轉錄審核佇列」，不是正式逐字稿資料庫。

已完成項目：

1. `scripts/build_transcript_review_queue.py`：從 `data/raw/cycc_question_video_metadata.csv` 產生待審核清單。
2. `dashboard/data/transcript_review_queue.json`：儀表板使用的待轉錄候選資料。
3. `dashboard/video-review.html`：人工查看待轉錄候選的 dashboard 頁面。
4. 測試：確認欄位、狀態、安全聲明與資料格式。

本階段不做：

1. 不下載影音。
2. 不呼叫 Whisper。
3. 不呼叫外部 ASR API。
4. 不寫入 API key、token、credential。
5. 不把未經人工 review 的轉錄文字放入正式分析。

---

## 二、資料來源

主要來源：

```text
data/raw/cycc_question_video_metadata.csv
```

輸出：

```text
dashboard/data/transcript_review_queue.json
```

檢視頁：

```text
dashboard/video-review.html
```

---

## 三、queue 欄位說明

| 欄位 | 說明 | 人工處理方式 |
|---|---|---|
| `queue_id` | 佇列唯一 ID | 不手動修改，除非 raw hash 規則改變。 |
| `source_id` | 來源 ID，應為 `CYCC_QUESTION_VIDEO` | 若來源不同，需新增來源規格。 |
| `councilor_name` | 議員姓名 | 空白時需人工補 metadata。 |
| `council_term` | 屆次 | 檢查是否與議會原始頁一致。 |
| `session_name` | 會期 | 檢查是否與議會原始頁一致。 |
| `video_title` | 影音標題 | 檢查是否能辨識質詢場次。 |
| `video_url` | 影音連結 | 確認為公開來源，不下載檔案。 |
| `video_platform` | 影音平台 | 目前常見為 `youtube`。 |
| `video_id` | 平台影音 ID | 用於去重與後續追蹤。 |
| `meeting_date` | 會議日期 | 空白時需人工補 metadata。 |
| `topic_guess` | 初步議題推測 | 只作初判，不是正式分類。 |
| `raw_hash` | 原始資料 hash | 用於去重。 |
| `transcript_status` | 轉錄狀態 | 初始為 `not_started`。 |
| `review_status` | 人工審核狀態 | 初始為 `unreviewed`。 |
| `priority` | 處理優先度 | `needs_metadata_review`、`medium`、`normal`。 |
| `needs_metadata_review` | 是否需補 metadata | `true` 表示要先補議員姓名或日期。 |
| `recommended_action` | 建議動作 | 目前固定為 `manual_transcript_or_asr_review`。 |
| `notes` | 安全與流程提醒 | 不應移除。 |

---

## 四、人工審核流程

### Step 1：先看 dashboard

打開：

```text
dashboard/video-review.html
```

先確認三個數字：

1. 待轉錄候選。
2. 需補 metadata。
3. 尚未開始。

### Step 2：先補 metadata

若 `needs_metadata_review` 為 `true`，先補：

1. `councilor_name`
2. `meeting_date`
3. 必要時補 `topic_guess`

補資料時只使用公開來源，例如：

1. 嘉義市議會公開頁面。
2. 會議紀錄或議程公開資料。
3. 影音頁面本身公開標題與描述。

不得使用私人通訊紀錄、未授權名冊或個資資料庫。

### Step 3：建立轉錄候選

只有在 metadata 補齊後，才進入轉錄候選。

可接受狀態轉換：

```text
not_started -> queued -> transcribed -> reviewed
```

若資料錯誤或來源失效：

```text
not_started -> rejected
```

### Step 4：轉錄後必須人工 review

即使未來使用 AI 轉錄，仍需人工 review 才能進入正式資料庫。

人工 review 至少檢查：

1. 逐字稿是否對應正確影音。
2. 發言人是否標示清楚。
3. 是否有錯字、漏字、時間軸錯置。
4. 是否把非公開個資、私人資訊或無關言論放入分析。
5. 摘要是否忠實，不加入未出現的指控。

---

## 五、狀態規則

### transcript_status

| 狀態 | 意義 |
|---|---|
| `not_started` | 尚未開始。 |
| `queued` | 已排入後續轉錄流程。 |
| `transcribed` | 已產生初稿，但尚未人工審核。 |
| `reviewed` | 已人工審核，可進入後續分析。 |
| `rejected` | 資料錯誤、來源失效或不適合使用。 |

### review_status

| 狀態 | 意義 |
|---|---|
| `unreviewed` | 尚未人工檢查。 |
| `needs_metadata_review` | 需補議員姓名、日期或會期等 metadata。 |
| `reviewed` | metadata 或轉錄內容已人工審核。 |
| `rejected` | 不納入後續使用。 |

---

## 六、資料安全與法遵原則

1. 只使用公開來源。
2. 不寫入 API key、token、credential。
3. 不把私人地址、電話、email、身分證字號等欄位放進 queue。
4. 不把 AI 轉錄初稿直接當成正式逐字稿。
5. 不用轉錄內容做人身攻擊、未查證指控或斷章取義文案。
6. 對外引用時應標示來源、日期與上下文。
7. 若涉及選舉、公職人員或政治攻防，應保留原始連結與完整脈絡。
8. 任何自動化流程不得自動公開發布，應先產生草稿或人工審核清單。

---

## 七、建議的後續資料結構

未來可以新增：

```text
data/processed/cycc_transcripts_reviewed.json
```

建議欄位：

| 欄位 | 說明 |
|---|---|
| `queue_id` | 對應 transcript review queue。 |
| `video_url` | 原始公開影音連結。 |
| `speaker` | 發言人。 |
| `spoken_at` | 時間軸。 |
| `transcript_text` | 人工審核後逐字稿。 |
| `reviewer` | 審核者代號，不放個資。 |
| `reviewed_at` | 審核時間。 |
| `issue_tags` | 人工或 AI 輔助分類後的議題標籤。 |
| `source_context` | 原始會議、日期、會期與連結。 |
| `review_notes` | 審核備註。 |

---

## 八、PR 驗收清單

未來任何修改轉錄流程的 PR，應檢查：

1. `pytest -q` 通過。
2. `tests/test_build_transcript_review_queue.py` 通過。
3. `tests/test_dashboard_json_validation.py` 通過。
4. 若修改 dashboard 頁面，`tests/test_video_review_page.py` 通過。
5. PR 內不得出現 API key、token 或 credential。
6. PR 不得自動下載影音。
7. PR 不得把 AI 初稿標示為 reviewed。
8. PR 說明需標示資料來源與安全限制。

---

## 九、與競選素材的使用邊界

這份資料可以幫助整理市政議題，但不應直接用來產生攻擊式內容。

可使用方式：

1. 統計長期被討論的市政議題。
2. 比對局處回應與問題類型。
3. 找出可提出政策解法的城市故障點。
4. 製作中性、可查證的市政研究摘要。

不建議使用方式：

1. 擷取片段做人格攻擊。
2. 把 AI 摘要當成原文引用。
3. 未查證就指控特定人瀆職或違法。
4. 用作不透明操控、假訊息或假帳號操作。

原則：城市有問題，就找出真因；資料要能被查證，結論要能被說明。
