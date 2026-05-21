# 人工資料輸入模板 v1

本文件定義在正式 crawler、1999 資料或 n8n 自動化尚未完全接好前，如何用人工方式建立可用資料。

---

## 目的

讓專案可以先用人工整理資料推進，而不是等所有自動化完成後才開始運作。

適用於：

1. 現場觀察紀錄
2. 城市故障回報整理
3. 1999 / 陳情資料樣本
4. 議員質詢重點摘要
5. 每週城市故障週報
6. 社群內容排程

---

## 一、城市故障回報人工整理表

建議 Google Sheet 欄位：

| 欄位 | 說明 |
|---|---|
| case_id | 內部案件 ID |
| received_at | 收到時間 |
| source | 表單 / 現場 / LINE / 人工整理 |
| district | 東區 / 西區 / 全市 / unknown |
| location_text_raw | 原始地點文字 |
| location_text_public | 對外顯示地點，需降精度 |
| primary_issue | 主要議題 code |
| secondary_tags | 次要標籤 |
| summary_public | 去識別化摘要 |
| privacy_checked | TRUE / FALSE |
| data_status | raw / deidentified / verified / published |
| notes_internal | 內部備註，不公開 |

---

## 二、現場觀察人工整理表

| 欄位 | 說明 |
|---|---|
| observation_id | 現場觀察 ID |
| observed_at | 觀察時間 |
| location_name | 地點名稱 |
| district | 行政區 |
| primary_issue | 主要議題 code |
| observation_summary | 去識別化摘要 |
| evidence_type | photo / video / note |
| photo_count | 照片數 |
| video_count | 影片數 |
| privacy_checked | TRUE / FALSE |
| recommended_action | 建議行動 |
| publish_status | internal / deidentified / published |

---

## 三、改善追蹤人工整理表

| 欄位 | 說明 |
|---|---|
| tracking_id | 追蹤 ID |
| issue_title | 議題標題 |
| location_display | 對外顯示地點 |
| primary_issue | 主要議題 code |
| status | observed / documented / submitted / responded / improved / monitoring / closed |
| current_summary | 目前狀態摘要 |
| recommended_action | 建議行動 |
| responsible_unit | 可能相關單位，不確定填空 |
| last_checked_at | 最近追蹤日期 |
| next_check_at | 下次追蹤日期 |
| public_note | 對外說明 |
| data_status | internal / deidentified / published |

---

## 四、議員質詢摘要人工整理表

| 欄位 | 說明 |
|---|---|
| question_id | 質詢 ID |
| date | 日期 |
| councilor_name | 議員姓名 |
| meeting_name | 會議名稱 |
| title | 質詢標題 |
| source_url | 原始來源 |
| primary_issue | 主要議題 code |
| secondary_tags | 次要標籤 |
| summary | 摘要 |
| mentioned_department | 提及局處 |
| data_status | metadata / reviewed / published |

注意：

```text
公開呈現時只能描述公開資料中出現的議題，不可推論議員是否關心或不關心。
```

---

## 五、週報人工整理表

| 欄位 | 說明 |
|---|---|
| report_id | 例如 2026-W21 |
| week_start | 週起始日 |
| week_end | 週結束日 |
| top_issue | 本週主題 |
| summary | 本週摘要 |
| top_findings | 三大觀察 |
| recommended_actions | 建議行動 |
| data_status | prototype / reviewed / published |
| report_url | 週報連結 |

---

## 六、人工資料進 dashboard 流程

```text
Google Sheet / CSV
→ 人工檢查
→ 去識別化
→ 匯出 CSV
→ processor 轉 JSON
→ JSON validation
→ dashboard 顯示
```

---

## 七、輸入注意事項

1. 不要把姓名、電話、email 放進公開欄位。
2. 完整地址放內部欄位即可，公開欄位要降精度。
3. 若不確定分類，primary_issue 可先填 `other`。
4. 若不確定資料是否可公開，data_status 保持 `internal`。
5. 任何要公開的資料都要先通過 privacy_checked。

---

## 八、你可以先幫忙準備的資料

未來若要加速，可以人工先整理：

1. 嘉義市常見問題地點清單。
2. 西區市場、學校、公園、重要路口清單。
3. 近一年你自己觀察到的城市故障案例。
4. 已知議員質詢中常出現的議題關鍵字。
5. 1999 或市政信箱是否有公開查詢頁或匯出功能。
