# 資料來源頁規格 v1

本文件定義 `dashboard/sources.html` 的頁面內容與資料結構。

---

## 頁面定位

```text
資料來源與更新狀態頁
```

用途是讓使用者知道：

1. 本平台使用哪些資料來源。
2. 哪些資料已接入。
3. 哪些資料仍在盤點中。
4. 各資料來源的更新時間。
5. 各資料集的限制與注意事項。

---

## 建議網址

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/sources.html
```

---

## 頁面主要區塊

### 1. Hero

標題：

```text
資料來源與更新狀態
```

副標：

```text
公開資料、官方資訊與地方議題資料的整理狀態。
```

---

### 2. 資料來源總覽

資料來源包含：

- 嘉義市議會會議紀錄
- 嘉義市議員質詢影音 metadata
- 嘉義市政府 1999 / 陳情資料
- 政府資料開放平台
- 嘉義市政府各局處公開資料
- 地方議題意見徵集資料

---

### 3. 資料集狀態表

欄位：

| 欄位 | 說明 |
|---|---|
| source_name | 資料來源名稱 |
| source_type | 官方資料 / 開放資料 / 使用者回報 / prototype |
| status | planned / crawling / processed / verified / published |
| latest_update | 最近更新時間 |
| record_count | 資料筆數 |
| source_url | 來源網址 |
| notes | 資料限制 |

---

## JSON 資料

建議建立：

```text
dashboard/data/data_sources.json
```

範例：

```json
[
  {
    "source_name": "嘉義市議會會議紀錄",
    "source_type": "官方公開資料",
    "status": "crawling",
    "latest_update": "2026-05-21",
    "record_count": 10,
    "source_url": "https://www.cycc.gov.tw/",
    "notes": "目前先抓取 metadata，尚未解析全文。"
  }
]
```

---

## 導覽關係

`sources.html` 應與下列頁面互相連結：

- index.html
- insights.html
- methodology.html
- reports.html

---

## 資料聲明

本頁需顯示短版聲明：

```text
本平台資料來自公開資訊、官方資料與原型資料整理。分析結果為城市治理與地方議題研究用途，不代表完整民意調查，也不作為個人評價結論。
```
