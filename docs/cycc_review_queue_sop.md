# CYCC metadata 人工審核佇列 SOP

本 SOP 用於處理 `cycc-review.html` 內的 141 筆公開 metadata。目標是把資料從「可搜尋的內部索引」推進到「可引用的審核素材」，但不自動發布、不自動產生競選文案。

## 一、審核原則

每一筆 metadata 預設都不是對外素材。

預設狀態：

```text
review_status: needs_review
```

只有通過人工審核、確認來源與內容後，才可以進入：

```text
review_status: citation_ready
```

## 二、逐筆審核流程

1. 在 `cycc-review.html` 搜尋或篩選資料。
2. 開啟 `source_url` 或 `detail_url`。
3. 確認連結可開啟，且來源為嘉義市議會或官方公開來源。
4. 確認標題、日期、資料類型沒有誤讀。
5. 若要引用內容，必須閱讀原始會議紀錄或觀看原始影片。
6. 撰寫中性摘要，不做人身評價，不做未查證推論。
7. 填寫 `caution_notes`，記錄限制、脈絡與不確定處。
8. 確認沒有個資、私人陳情全文或未公開資訊。
9. 才能把 `citation_ready` 設為 true。

## 三、狀態使用方式

- `needs_review`：尚未看過原始來源。
- `source_verified`：只確認來源可開啟，還不能對外引用。
- `content_reviewed`：已閱讀或觀看內容，但仍需補脈絡。
- `citation_ready`：可引用，但仍需保留來源連結與中性文字。
- `needs_context`：資料可能有用，但需要其他資料補充。
- `do_not_use_publicly`：不適合對外使用。

## 四、對外引用標準

可對外引用前必須同時成立：

- `review_status` 是 `citation_ready`。
- `source_verified` 是 true。
- `original_content_reviewed` 是 true。
- `citation_ready` 是 true。
- 有保留原始來源連結。
- 有中性摘要。
- `caution_notes` 已填寫。

## 五、不可做的事

- 不可只看 metadata 就下結論。
- 不可把 metadata 直接改寫成指控。
- 不可自動發布。
- 不可收集或公開個資。
- 不可使用私人陳情全文。
- 不可把單筆資料推論成完整民意。

## 六、一人團隊建議工作節奏

每天可處理 5 到 10 筆：

1. 先篩選一個主題，例如交通、社福、文化或工程。
2. 只做來源確認與內容閱讀。
3. 當天不急著發文。
4. 每週再把 `citation_ready` 的資料彙整成政策背景素材。
5. 發布前再進 public-review 流程。

## 七、輸出成果

人工審核後的衍生資料應另存，不直接覆蓋原始 metadata JSON。

建議未來新增：

```text
dashboard/data/cycc_review_queue.json
dashboard/data/cycc_citation_ready_items.json
```

這兩份資料仍必須維持人工審核與不自動發布原則。
