# 嘉義城市故障分析資料庫進度紀錄

更新時間：2026-05-23 台北時間

## 一、目前完成狀態

第一批真實公開資料線已完成：嘉義市議會公開 metadata。

第二批官方資料來源盤點已完成第一階段：嘉義市政府與官方公開資料 URL inventory。

已完成流程：

```text
CYCC metadata crawler
→ CYCC Manual Crawl GitHub Action
→ artifact
→ dashboard summary report
→ 141 筆逐筆 metadata JSON
→ cycc-review.html 表格、搜尋、篩選
→ sources.html / cycc-review.html 互相連結
→ CYCC review gate
→ CYCC review queue schema / SOP
→ open data URL inventory
→ open-data-inventory.html 表格、搜尋、篩選
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
- PR #147：新增 project progress log。
- PR #148：新增 CYCC metadata review workflow 與 review gate。
- PR #150：新增 CYCC review queue schema 與 reviewer SOP。
- PR #152：新增官方 open data URL inventory dashboard。

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

### 官方 open data URL inventory

- 候選官方 URL：29 筆。
- 狀態：internal_url_inventory。
- topic_group：traffic_parking、social_welfare、culture_events、public_works_environment、complaints_service。
- manual_review_required：true。
- no_auto_publish：true。
- no_personal_data：true。
- no live crawler。

主要檔案：

```text
config/chiayi_open_data_url_inventory.yml
dashboard/data/open_data_url_inventory.json
dashboard/open-data-inventory.html
scripts/build_open_data_url_inventory.py
```

## 四、CYCC 審核治理狀態

已完成：

```text
docs/cycc_metadata_review_workflow.md
config/cycc_metadata_review_gate.yml
config/cycc_review_queue_schema.yml
docs/cycc_review_queue_sop.md
```

目前規則：

- 只有 `citation_ready` 可以進入對外引用候選。
- `needs_review`、`source_verified`、`content_reviewed` 都不可直接對外引用。
- 每筆資料都必須保留 source_url / detail_url。
- 對外引用前必須人工閱讀或觀看原始內容。
- 不自動發布。
- 不收集個資。
- 不把 metadata 直接改寫成指控或結論。

## 五、已關閉 issue / PR

- Issue #145：Link CYCC table pages，已完成並關閉。
- PR #149：舊版 open data URL inventory dashboard，已由 PR #152 取代並關閉。

## 六、下一階段

Codex 正在進行或即將進行：

```text
feat/open-data-review-queue
```

任務方向：

- 把 29 筆官方 URL inventory 轉為人工 URL 審核佇列。
- 新增 open-data-review.html。
- 建立 source reachability、official source verification、license review、crawler candidate、crawler priority 等欄位。
- 只做審核佇列，不啟動 live crawler。

## 七、安全邊界

目前所有真實資料接入都必須維持：

- 不抓私人陳情全文。
- 不收集姓名、電話、email、地址等個資。
- 不自動發布。
- 不直接產生競選文案。
- 不把 metadata 或 URL inventory 改寫成指控或結論。
- 人工審核後才可進入對外說明素材。
