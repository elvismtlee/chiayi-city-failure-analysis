# 嘉義市政府開放資料 Inventory

本文件是「嘉義市 12 年城市故障分析資料庫」第二批真實資料來源盤點。

第一批已接入嘉義市議會公開資料 summary report。下一步不是直接亂爬所有網站，而是先建立嘉義市政府及局處公開資料的 inventory，確認來源、授權、欄位與是否可用於 dashboard。

## 一、目前定位

本階段只做資料來源盤點，不啟用 live crawler。

目前狀態：

- `manual_review_required: true`
- `no_auto_publish: true`
- `no_personal_data: true`
- `review_status: needs_dataset_url_review`

## 二、優先資料類別

### 1. 交通與停車

用途：市場周邊交通、停車熱點、通勤與路口安全。

候選資料：

- 停車場
- 停車格
- 公車路線
- 公共自行車站點
- 交通安全或事故統計

### 2. 長照、兒少與社福

用途：高齡照護、兒少服務、社區支持資源。

候選資料：

- 長照據點
- 老人服務據點
- 兒少服務據點
- 社福設施

### 3. 文化活動與場館

用途：文化嘉義、小型博物館城市、閱讀與藝文政策背景。

候選資料：

- 公共活動
- 圖書館
- 博物館
- 文化資產
- 展演空間

### 4. 公共工程、環境與城市維護

用途：道路、人行道、排水、公園、環境品質與城市維護議題。

候選資料：

- 道路工程
- 人行道
- 排水
- 公園綠地
- 環境清潔
- 空氣或水質等環境資料

## 三、下一步工程

下一個 PR 可做：

```text
feat/open-data-source-url-inventory
```

任務：

1. 搜尋官方資料集 URL。
2. 紀錄 dataset title、URL、owner、format、license、update cadence。
3. 只標記候選，不直接爬資料。
4. 人工 review 後，才建立 source-specific crawler。

## 四、安全邊界

- 不使用登入後資料。
- 不使用私人陳情全文。
- 不收集個資。
- 不自動公開發布。
- 不把資料包裝成完整民調或正式結論。
