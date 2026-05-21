# 1999 / 陳情資料接入計畫 v1

本文件定義嘉義市 1999 / 陳情資料接入本平台的初步流程。

---

## 目標

將 1999 或陳情資料轉成可分析、可視覺化、可週報化的城市故障資料。

---

## 第一階段：資料來源盤點

需確認：

1. 嘉義市是否有公開 1999 案件資料。
2. 是否有開放資料 API。
3. 是否只有網頁查詢。
4. 是否需要人工匯出。
5. 欄位是否包含個資。
6. 是否允許再利用。

---

## 第二階段：欄位盤點

理想欄位：

| 欄位 | 說明 |
|---|---|
| case_id | 案件編號 |
| date | 受理日期 |
| category | 原始分類 |
| subject | 主旨 |
| description | 內容摘要 |
| location_text | 地點文字 |
| department | 承辦局處 |
| status | 處理狀態 |
| closed_date | 結案日期 |
| response_summary | 回覆摘要 |
| source_url | 來源網址 |

---

## 第三階段：安全處理

公開前需先做：

1. 去識別化
2. 地址降精度
3. 議題分類
4. 地點標準化
5. source_url 保留
6. data_status 標示

---

## 第四階段：轉換格式

### raw

```text
data/raw/1999_cases.csv
```

### processed

```text
data/processed/1999_cases_processed.csv
```

### dashboard

```text
dashboard/data/issue_ranking.json
dashboard/data/hotspots.json
dashboard/data/issue_trends.json
dashboard/data/department_performance.json
```

---

## 第五階段：分析用途

1999 / 陳情資料可用於：

- 熱門議題排行
- 城市故障分數
- 熱點地圖
- 局處案件負荷
- 處理時間分析
- 重複案件分析
- 每週城市故障週報

---

## 風險與限制

1. 1999 資料可能不完整公開。
2. 個資風險較高。
3. 案件數高不等於局處效率差。
4. 單一案件不能代表完整民意。
5. 地址資料需降精度再公開。

---

## 第一版 prototype 建議

若正式 1999 資料尚未取得，可先建立：

```text
data/raw/1999_cases_sample.csv
```

欄位使用假資料或去識別化樣本，用於測試 pipeline、dashboard 與週報格式。

---

## 驗收標準

- [ ] 原始資料來源清楚
- [ ] 欄位字典完成
- [ ] 去識別化流程完成
- [ ] 地點標準化完成
- [ ] 議題分類完成
- [ ] dashboard JSON 可產生
- [ ] 對外頁面有資料限制聲明
