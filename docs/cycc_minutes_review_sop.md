# 嘉義市議會會議紀錄審核 SOP

本文件定義會議紀錄解析資料進入人工 review 的操作流程。適用於 `cycc_minutes_review_queue` 類型資料，目標是把 fixture parser、未來正式 parser 與人工審核工作台串成可追蹤流程。

此 SOP 不取代 parser spec，也不代表資料已完成正式驗證。所有未審核資料都應維持 `review_status: unreviewed`。

---

## 一、目前定位

會議紀錄解析流程目前分為三層：

| 階段 | 目的 | 狀態 |
|---|---|---|
| Parser prototype | 驗證 PDF / HTML 欄位解析契約 | fixture-only |
| Review queue | 將 parser output 轉成人工審核清單 | 待建立 / 擴充 |
| Reviewed data | 人工確認後才進入正式 processed data | 尚未建立 |

目前所有 fixture parser output 都不可直接作為正式分析結果。

---

## 二、審核角色

一人團隊可用代號記錄審核者，不需放真實個資。

建議代號：

```text
reviewer: campaign_ops
```

若未來多人協作，可改用：

```text
reviewer: reviewer_001
reviewer: reviewer_002
```

---

## 三、每日操作流程

### Step 1：查看 queue

打開會議紀錄審核 dashboard，先看：

1. 總筆數。
2. `unreviewed` 筆數。
3. 缺日期筆數。
4. 缺議員姓名筆數。
5. 涉及局處數。
6. 來源 URL 是否可回查。

### Step 2：選擇今日審核項目

每天建議審核 3 到 5 筆即可。

優先順序：

| 優先 | 條件 | 原因 |
|---:|---|---|
| 1 | 日期完整、來源明確、局處明確 | 最容易快速確認。 |
| 2 | 議題與交通、長照、兒少、商圈相關 | 可累積政策素材。 |
| 3 | 來源明確但 metadata 缺漏 | 適合補欄位。 |
| 4 | raw text 太短或上下文不足 | 需保留待補，不急著使用。 |

### Step 3：比對來源

逐筆確認：

1. `source_url` 是否為公開來源。
2. `meeting_name` 是否與來源頁面一致。
3. `meeting_date` 是否與來源頁面一致。
4. `councilor_name` 是否真的出現在原文或 metadata。
5. `department` 是否真的出現在原文或 metadata。
6. `agenda_item` 是否符合原文段落。
7. `issue_keywords` 是否只是初步標籤，不可過度推論。

### Step 4：判斷狀態

| 狀態 | 使用條件 |
|---|---|
| `unreviewed` | 尚未人工確認。 |
| `needs_metadata_review` | 缺日期、會議名稱、議員、局處或來源。 |
| `reviewed` | 已確認來源與欄位，可進入下一階段整理。 |
| `verified` | 已交叉比對可信來源。 |
| `rejected` | 來源錯誤、欄位錯誤、資料不適合使用。 |

第一階段建議只使用：

```text
unreviewed
needs_metadata_review
reviewed
rejected
```

`verified` 留到正式資料源與人工交叉驗證完成後再使用。

---

## 四、審核紀錄格式

每筆資料人工審核後，建議補上：

```text
reviewed_at
reviewer
review_notes
source_context
```

範例：

```json
{
  "reviewed_at": "2026-05-22",
  "reviewer": "campaign_ops",
  "review_notes": "已確認會議名稱、日期、局處與議題段落。議題關鍵字仍為初步標籤。",
  "source_context": "來源頁面標題與段落文字一致，未發現私人個資。"
}
```

---

## 五、可進入正式整理的條件

一筆會議紀錄資料至少需滿足以下條件，才可進入後續 processed data：

1. `source_url` 可回查。
2. `meeting_name` 不為空。
3. `meeting_date` 不為空且格式一致。
4. `councilor_name` 來自原始資料，不是猜測。
5. `department` 來自原始資料，不是猜測。
6. `raw_text_excerpt` 可回溯到原文段落。
7. `review_status` 已由 `unreviewed` 改為 `reviewed`。
8. 不含私人電話、email、地址、身分證字號等敏感欄位。

---

## 六、不可進入正式整理的情況

以下情況不得進入正式分析：

1. 來源 URL 失效。
2. 日期無法確認。
3. 議員姓名或局處名稱由 AI 推測而來。
4. 只有摘要，沒有原文段落可回查。
5. `review_status` 仍為 `unreviewed`。
6. `parser_status` 顯示解析失敗。
7. 內容含私人個資。
8. 文字容易被誤解為正式調查、民調或支持度結果。

---

## 七、議題素材轉換規則

經人工確認後，可以轉成以下素材：

| 素材 | 可以使用的內容 | 注意事項 |
|---|---|---|
| 地方問題紀錄 | 會議名稱、日期、局處、議題 | 不做人身攻擊。 |
| 政策素材 | 問題描述、局處回應、後續解法 | 保留來源與日期。 |
| 社群文案草稿 | 中性議題說明與改善方向 | 不把初步分類當結論。 |
| 短影音腳本 | 市民聽得懂的問題說明 | 不斷章取義。 |
| dashboard 統計 | 已 review 的議題分類 | 標示資料來源與樣本限制。 |

---

## 八、法遵與風險提醒

1. 會議紀錄資料可用於市政研究，但引用時要保留來源與上下文。
2. 不得將片段文字包裝成未經查證的指控。
3. 不得把 AI 摘要當成正式逐字稿。
4. 不得把 dashboard 統計稱為民調或支持度調查。
5. 不得使用資料進行不透明選民操作或個資分析。
6. 不得公開非公開來源資料。

---

## 九、建議欄位生命週期

```text
parsed_from_fixture / unreviewed
  -> needs_metadata_review
  -> reviewed
  -> processed_candidate
  -> published_summary_draft
  -> human_approved_public_material
```

公開前最後一步一定要人工確認。

---

## 十、每週整理輸出

每週可整理一次：

```markdown
# 本週會議紀錄審核摘要

## 本週審核數量
- 新增 queue：
- 已 review：
- 需補 metadata：
- rejected：

## 本週高頻議題
1.
2.
3.

## 本週涉及局處
1.
2.
3.

## 可發展政策素材
1.
2.
3.

## 下週待補資料
1.
2.
3.
```

---

## 十一、核心原則

```text
資料能回查，才可引用。
人工有審核，才可分析。
結論要保守，不能超出原文。
城市有問題，就找真因；資料要能查證，說法要能負責。
```

---

## 十二、reviewed sample 與政策審核

`data/processed/cycc_minutes_reviewed_sample.json` 只是人工審核流程的範例資料，用來示範 queue 如何進入 reviewed sample，再轉成議題候選。這些資料仍屬 sample data，不是正式結論；若要進入政策素材、對外圖文或週報草稿，必須再經人工政策審核，確認來源、上下文、用語與 public use 邊界都合格後才可使用。
