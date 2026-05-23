# 嘉義城市故障分析資料庫進度紀錄

更新時間：2026-05-23 台北時間

## 一、目前完成狀態

第一批真實公開資料線已完成：嘉義市議會公開 metadata。

已完成流程：

```text
CYCC metadata crawler
→ CYCC Manual Crawl GitHub Action
→ artifact
→ dashboard summary report
→ 141 筆逐筆 metadata JSON
→ cycc-review.html 表格、搜尋、篩選
→ sources.html / cycc-review.html 互相連結
```

## 二、已合併重點 PR

- PR #131：新增 CYCC crawler runbook。
- PR #132：新增 CYCC Manual Crawl workflow。
- PR #134：修正 crawler script import path。
- PR #136：接入 CYCC crawl summary report。
- PR #140：新增 CYCC metadata review page。
- PR #141：把 CYCC review page 加入 dashboard 導覽。
- PR #142：接入 141 筆逐筆 CYCC metadata table。
- PR #143：新增嘉義市政府開放資料 inventory 起始設定與文件。
- PR #146：讓 sources.html 與 cycc-review.html 互相連結。

## 三、目前資料狀態

### CYCC 公開 metadata

- 會議紀錄 metadata：10 筆。
- 質詢影音 metadata：131 筆。
- 合計：141 筆。
- 狀態：internal metadata table。
- review_status：needs_review。
- manual_review_required：true。
- no_auto_publish：true。
- metadata_only：true。

主要檔案：

```text
dashboard/data/cycc_public_records_crawl_report.json
dashboard/data/cycc_minutes_metadata.json
dashboard/data/cycc_question_video_metadata.json
dashboard/cycc-review.html
dashboard/sources.html
```

## 四、已關閉 issue

- Issue #145：Link CYCC table pages，已完成並關閉。

## 五、下一階段

Codex 正在進行：

```text
feat/open-data-url-inventory-dashboard
```

任務方向：

- 建立第二批真實資料來源 URL inventory。
- 盤點嘉義市政府與官方公開資料來源。
- 涵蓋 traffic_parking、social_welfare、culture_events、public_works_environment、complaints_service。
- 新增 dashboard/open-data-inventory.html。
- 只盤點 URL 與來源狀態，不啟動 live crawler。

## 六、安全邊界

目前所有真實資料接入都必須維持：

- 不抓私人陳情全文。
- 不收集姓名、電話、email、地址等個資。
- 不自動發布。
- 不直接產生競選文案。
- 不把 metadata 改寫成指控或結論。
- 人工審核後才可進入對外說明素材。
