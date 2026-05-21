# Google Sheet 模板規格 v1

本文件定義本專案可先用 Google Sheet 管理的資料表結構。正式自動化前，可用這些表作為人工輸入與 n8n 串接基礎。

---

## 目的

讓非工程人員也可以協助整理資料，並讓資料未來能匯出 CSV、接進 processor 或 n8n。

---

## 建議工作簿名稱

```text
嘉義城市故障分析資料庫｜人工資料工作簿
```

---

## Sheet 1：城市故障案例

工作表名稱：

```text
city_failure_cases
```

欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| case_id | Y | case-2026-0001 |
| received_at | Y | 收到日期 |
| source_type | Y | sample / form / field / public_record |
| district | Y | 東區 / 西區 / 全市 / unknown |
| location_text_raw | N | 原始地點，內部使用 |
| location_display | Y | 對外顯示地點 |
| primary_issue | Y | issue_taxonomy code |
| secondary_tags | N | 逗號分隔 |
| summary_public | Y | 去識別化摘要 |
| privacy_checked | Y | TRUE / FALSE |
| data_status | Y | sample / internal / deidentified / published |
| notes_internal | N | 內部備註 |

---

## Sheet 2：熱點清單

工作表名稱：

```text
hotspots
```

欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| hotspot_id | Y | hotspot-0001 |
| name | Y | 熱點名稱 |
| district | Y | 行政區 |
| location_display | Y | 對外地點 |
| primary_issue | Y | 主要議題 |
| score | Y | 0 - 100 |
| geo_precision | Y | landmark / road_segment / district |
| lat | N | 可公開才填 |
| lng | N | 可公開才填 |
| recommended_action | Y | 建議行動 |
| data_status | Y | sample / processed / published |

---

## Sheet 3：現場觀察

工作表名稱：

```text
field_observations
```

欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| observation_id | Y | field-2026-0001 |
| related_hotspot_id | N | 對應熱點 |
| observed_at | Y | 觀察時間 |
| location_name | Y | 地點名稱 |
| district | Y | 行政區 |
| primary_issue | Y | 主要議題 |
| observation_summary | Y | 去識別化摘要 |
| evidence_type | N | photo, video, note |
| photo_count | N | 照片數 |
| video_count | N | 影片數 |
| privacy_checked | Y | TRUE / FALSE |
| publish_status | Y | internal / deidentified / published |
| recommended_action | Y | 建議行動 |

---

## Sheet 4：改善追蹤

工作表名稱：

```text
action_tracking
```

欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| tracking_id | Y | track-2026-0001 |
| issue_title | Y | 議題標題 |
| related_hotspot_id | N | 對應熱點 |
| related_observation_id | N | 對應現場觀察 |
| district | Y | 行政區 |
| location_display | Y | 對外地點 |
| primary_issue | Y | 主要議題 |
| status | Y | observed / documented / submitted / responded / improved / monitoring / closed |
| current_summary | Y | 目前狀態 |
| recommended_action | Y | 建議行動 |
| responsible_unit | N | 不確定可空白 |
| last_checked_at | Y | 最近追蹤日期 |
| next_check_at | N | 下次追蹤日期 |
| data_status | Y | internal / deidentified / published |

---

## Sheet 5：內容行事曆

工作表名稱：

```text
content_calendar
```

欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| content_id | Y | content-2026-0001 |
| publish_date | Y | 預計發布日期 |
| channel | Y | fb / threads / line / short_video / website |
| content_type | Y | post / image_card / video_script / report_link |
| issue | Y | 議題 |
| location_display | N | 地點 |
| source_type | Y | dashboard / weekly_report / field_observation / manual |
| source_id | N | 對應資料 ID |
| title | Y | 標題 |
| body | Y | 內文 |
| call_to_action | N | 行動呼籲 |
| status | Y | draft / reviewed / scheduled / published / archived |
| risk_checked | Y | TRUE / FALSE |
| privacy_checked | Y | TRUE / FALSE |

---

## Sheet 6：資料來源

工作表名稱：

```text
data_sources
```

欄位：

| 欄位 | 必填 | 說明 |
|---|---|---|
| source_id | Y | source-0001 |
| source_name | Y | 資料來源名稱 |
| source_type | Y | 官方資料 / 開放資料 / 表單 / 人工整理 |
| source_url | N | 原始來源 |
| access_method | Y | crawler / api / manual_download / form |
| update_frequency | N | daily / weekly / monthly / unknown |
| contains_personal_data | Y | TRUE / FALSE |
| risk_level | Y | low / medium / high |
| status | Y | planned / collecting / processed / published |
| notes | N | 備註 |

---

## 匯出規則

1. 每個 sheet 可匯出成 CSV。
2. 欄位名稱使用 snake_case。
3. TRUE / FALSE 統一大寫。
4. 日期使用 YYYY-MM-DD。
5. 不確定資料留空，不要亂填。
6. 對外欄位不可放個資。

---

## n8n 串接原則

n8n 可以：

- 讀取 Google Sheet
- 檢查必填欄位
- 匯出 CSV
- 觸發 GitHub workflow
- 產生草稿內容

n8n 不應：

- 自動公開未審核資料
- 自動發布公共議題內容
- 把 Google credential 寫進 repo

---

## 最小可行版本

一開始只需要建立三張表：

```text
city_failure_cases
hotspots
action_tracking
```

這三張表就足以測試：

```text
案例 → 熱點 → 改善追蹤 → dashboard
```
