# 樣本資料建置計畫 v1

本文件定義在正式 1999 / 陳情資料、完整 crawler 與 n8n 自動化尚未全部完成前，如何先建立 sample data，讓 dashboard、週報、AI 摘要與現場行動流程可以先跑通。

---

## 目的

先用小量、去識別化、可控制的樣本資料，驗證整個系統流程：

```text
sample data
→ processor
→ dashboard JSON
→ dashboard rendering
→ AI summary
→ weekly report
→ field action
→ social content draft
```

---

## 樣本資料原則

1. 不使用個資。
2. 不使用完整住家地址。
3. 不使用真實姓名、電話、email、車牌。
4. 可以使用公開地標、路段、學校、市場、公園等公共場所。
5. 可混合真實觀察與假資料，但必須標示 `data_status: sample` 或 `prototype`。
6. 不把樣本資料對外說成正式統計。

---

## 第一批 sample data 建議數量

| 類型 | 筆數 | 用途 |
|---|---:|---|
| 城市故障案例 | 30 | 測試議題分類、排行、週報 |
| 熱點地點 | 10 | 測試地圖與現場行動 |
| 現場觀察 | 10 | 測試 field observation schema |
| 改善追蹤 | 10 | 測試 action tracking schema |
| 社群內容草稿 | 14 | 測試一週內容行事曆 |

---

## 建議第一批議題分布

| 議題 | 建議筆數 |
|---|---:|
| 交通停車 | 6 |
| 道路路平 | 4 |
| 人行安全 | 5 |
| 環境衛生 | 4 |
| 市場商圈 | 3 |
| 通學安全 | 3 |
| 公園休憩 | 2 |
| 行政服務 | 1 |
| 其他 | 2 |

---

## 建議第一批地點

可先用公共地點或區域，不使用私人地址：

| 地點 | 類型 | 可能議題 |
|---|---|---|
| 文化路夜市周邊 | 市場 / 商圈 | 停車、人行、市場動線 |
| 嘉義火車站前站周邊 | 交通節點 | 接送、停車、人行 |
| 北興市場周邊 | 市場 | 停車、環境、動線 |
| 中央廣場周邊 | 公共空間 | 活動、人行、環境 |
| 民生南路部分路段 | 路段 | 車流、人行、路平 |
| 新民路部分路段 | 路段 | 交通、停車 |
| 世賢路部分路段 | 路段 | 車流、道路 |
| 學校周邊通學路線 | 通學 | 人行、交通安全 |
| 公園周邊 | 公園 | 照明、環境、設施 |
| 市府周邊 | 行政 / 交通 | 停車、行政服務 |

---

## sample case 欄位

建議建立：

```text
data/sample/city_failure_cases_sample.csv
```

欄位：

| 欄位 | 說明 |
|---|---|
| case_id | sample-0001 |
| date | YYYY-MM-DD |
| district | 東區 / 西區 / 全市 |
| location_display | 對外顯示地點 |
| primary_issue | issue_taxonomy code |
| secondary_tags | 逗號分隔 |
| summary_public | 去識別化摘要 |
| source_type | sample / field_observation / public_record |
| data_status | sample |
| privacy_checked | TRUE |

---

## sample case 範例

```csv
case_id,date,district,location_display,primary_issue,secondary_tags,summary_public,source_type,data_status,privacy_checked
sample-0001,2026-05-21,西區,文化路夜市周邊,traffic,"illegal_parking,pedestrian,market_traffic",尖峰時段臨停與人行動線重疊，建議盤點臨停熱點與行人穿越動線。,sample,sample,TRUE
sample-0002,2026-05-21,西區,學校周邊通學路線,pedestrian,"school_route,crossing_safety",通學時段行人與車流交會，建議整理通學動線與路口安全需求。,sample,sample,TRUE
```

---

## sample data 驗收

- [ ] 不含個資
- [ ] 不含完整地址
- [ ] 每筆有 case_id
- [ ] 每筆有 primary_issue
- [ ] primary_issue 符合 issue_taxonomy
- [ ] data_status 標示 sample
- [ ] privacy_checked 為 TRUE
- [ ] 可以被 processor 轉成 dashboard JSON

---

## 對外標示

若 dashboard 使用 sample data，頁面必須標示：

```text
目前資料為原型樣本資料，僅供系統展示與流程測試，不代表正式統計結果。
```

---

## 後續轉正式資料

當正式資料進來後：

1. sample data 不直接刪除，可保留在 `data/sample/`。
2. processor 應優先使用正式 processed data。
3. 若正式資料不足，才使用 sample fallback。
4. dashboard 必須明確標示目前資料狀態。
