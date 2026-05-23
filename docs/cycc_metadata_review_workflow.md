# CYCC 公開 metadata 人工審核流程

本文件規範嘉義市議會公開資料 metadata 進入 dashboard 後，如何從內部審核資料轉為可引用的城市議題素材。

目前資料來源：

- `dashboard/data/cycc_minutes_metadata.json`
- `dashboard/data/cycc_question_video_metadata.json`
- 合計 141 筆公開 metadata。

## 一、資料定位

目前資料僅為 internal metadata table。

可用於：

- 內部資料整理。
- 議題索引。
- 找出需要人工閱讀的會議紀錄或質詢影音。
- 建立下一步人工審核清單。

不可直接用於：

- 對外指控。
- 人物評價。
- 自動產生競選文案。
- 自動發布社群貼文。
- 推論完整民意或完整市政結論。

## 二、人工審核狀態

每筆資料預設：

```text
review_status: needs_review
```

建議後續人工審核狀態：

- `needs_review`：尚未人工檢查。
- `source_verified`：已確認來源連結可開啟，且為公開來源。
- `content_reviewed`：已人工閱讀或觀看內容。
- `citation_ready`：可作為資料來源引用。
- `needs_context`：需要搭配其他資料才能解讀。
- `do_not_use_publicly`：不適合對外引用。

## 三、引用前檢查清單

任何資料對外引用前，必須完成：

1. 開啟 source_url 或 detail_url。
2. 確認來源是嘉義市議會或其他官方公開頁面。
3. 確認標題、日期、屆期、會期或影片資訊沒有誤讀。
4. 若要引用內容，必須人工閱讀原始會議紀錄或觀看影音，不可只看 metadata。
5. 若涉及特定人物或單位，必須保留中性描述，不做未查證推論。
6. 若資料只顯示議程或標題，不得延伸成結論。
7. 若資料將用於社群或政見草稿，必須標示「資料來源」與「仍需人工確認」。

## 四、安全邊界

不得：

- 擷取私人陳情全文。
- 收集姓名、電話、email、地址等個資。
- 將 metadata 直接改寫成攻擊、指控或結論。
- 自動發文。
- 自動寄信。
- 自動建立募款或金流內容。

必須：

- 保持 manual_review_required。
- 保持 no_auto_publish。
- 保持 metadata_only，除非另有人工審核後的衍生資料檔。
- 對外引用前保留原始連結。

## 五、建議下一步資料表欄位

後續如果建立人工審核佇列，可加入以下欄位：

- reviewer
- reviewed_at
- source_verified_at
- content_review_status
- citation_notes
- public_summary_allowed
- suggested_topic_group
- west_district_relevance
- caution_notes

## 六、與 dashboard 的關係

`cycc-review.html` 顯示的是內部審核表格，不是正式資料發布頁。

`sources.html` 顯示資料來源與更新狀態，用於透明揭露資料管線狀態。

正式對外素材應由後續的 public-review 或 approved-materials 流程處理。
