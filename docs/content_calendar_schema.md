# 城市故障內容行事曆 Schema v1

本文件定義如何把城市故障資料、週報與現場觀察轉成可排程的社群內容。

---

## 目的

讓資料分析成果可以穩定轉成：

- FB 長文
- Threads 短文
- LINE 群組訊息
- 短影音腳本
- 海報圖卡主題
- 官網最新動態

---

## 建議檔案位置

### CSV

```text
data/processed/content_calendar.csv
```

### JSON

```text
dashboard/data/content_calendar.json
```

---

## 欄位定義

| 欄位 | 類型 | 說明 |
|---|---|---|
| content_id | string | 內容 ID |
| publish_date | date/string | 預計發布日期 |
| channel | string | fb / threads / line / short_video / website |
| content_type | string | post / image_card / video_script / report_link |
| issue | string | 議題名稱 |
| location_display | string/null | 地點顯示 |
| source_type | string | dashboard / weekly_report / field_observation / manual |
| source_id | string/null | 對應資料 ID |
| title | string | 標題 |
| body | string | 內文 |
| call_to_action | string | 行動呼籲 |
| status | string | draft / reviewed / scheduled / published / archived |
| risk_checked | boolean | 是否完成風險檢查 |
| privacy_checked | boolean | 是否完成個資檢查 |
| created_at | datetime/string | 建立時間 |
| updated_at | datetime/string | 更新時間 |

---

## JSON 範例

```json
{
  "content_id": "content-2026-0001",
  "publish_date": "2026-05-22",
  "channel": "fb",
  "content_type": "post",
  "issue": "市場周邊停車與人行安全",
  "location_display": "西區市場周邊",
  "source_type": "field_observation",
  "source_id": "field-2026-0001",
  "title": "城市問題不是只有抱怨，也可以被整理成資料",
  "body": "最近整理市場周邊停車與人行安全問題，發現尖峰時段臨停與行人動線容易重疊。這不是民調，也不是評分，而是希望把地方問題整理成可追蹤的改善清單。",
  "call_to_action": "如果你也熟悉這個地點，歡迎提供觀察。",
  "status": "draft",
  "risk_checked": true,
  "privacy_checked": true,
  "created_at": "2026-05-21 20:00:00",
  "updated_at": "2026-05-21 20:00:00"
}
```

---

## channel 定義

| channel | 說明 |
|---|---|
| fb | Facebook 長文或圖卡 |
| threads | Threads 短文 |
| line | LINE 群組或官方帳號文字 |
| short_video | Reels / Shorts / TikTok 腳本 |
| website | 官網最新動態 |

---

## status 定義

| status | 說明 |
|---|---|
| draft | 草稿 |
| reviewed | 已審稿 |
| scheduled | 已排程 |
| published | 已發布 |
| archived | 已封存 |

---

## 發布前檢查

- [ ] 不含個資
- [ ] 不含完整地址
- [ ] 不含車牌
- [ ] 不做人身攻擊
- [ ] 不做無來源指控
- [ ] 不使用民調 / 支持度調查語言
- [ ] 有清楚改善方向
- [ ] 繁體中文正確

---

## 每週內容節奏建議

```text
週一：本週城市故障觀察
週二：一個熱點一張圖
週三：現場觀察短影音
週四：資料來源 / 方法論說明
週五：本週改善追蹤
週六：地方生活議題故事
週日：下週追蹤預告
```

---

## 與 n8n 的關係

未來 n8n 可自動：

1. 讀取 weekly report。
2. 產生 draft content。
3. 寫入 Google Sheet。
4. 通知人工審稿。
5. 審稿後再手動發布。

原則：

```text
n8n 可以產生草稿，但不應自動發布政治或公共議題內容。
```
