# 每日資料審核與營運 Runbook

本文件提供一人團隊每日可執行的資料審核節奏，協助把 dashboard、queue、SOP 與後續政策素材整理串成固定流程。

---

## 一、用途

這份 runbook 用來回答三個問題：

1. 今天要看哪些資料？
2. 哪些資料可以進入後續分析？
3. 哪些資料只能留在審核清單，不能對外使用？

本文件是操作節奏，不取代各資料源的 parser、builder 或測試。

---

## 二、每日 20 分鐘基本流程

| 時間 | 動作 | 輸出 |
|---:|---|---|
| 3 分鐘 | 查看 dashboard 首頁與 shared navigation | 確認主要頁面可開啟。 |
| 5 分鐘 | 查看座標審核清單 | 選出 1 到 2 筆需要人工確認的地點。 |
| 5 分鐘 | 查看影音轉錄審核清單 | 選出 1 到 2 筆需要補 metadata 的影音。 |
| 5 分鐘 | 查看最新 issue 或 PR 狀態 | 確認是否有測試失敗、重複 PR 或待合併 PR。 |
| 2 分鐘 | 記錄今日結果 | 寫下今日可追蹤議題與待補資料。 |

---

## 三、每日 60 分鐘完整流程

| 階段 | 建議時間 | 工作內容 |
|---|---:|---|
| 資料健康檢查 | 10 分鐘 | 確認 JSON、GeoJSON、dashboard 頁面與 Actions 狀態。 |
| 座標人工審核 | 15 分鐘 | 檢查地名、座標精度、review_status 與公開地圖可驗證性。 |
| 影音 metadata 審核 | 15 分鐘 | 補議員姓名、日期、會期、影音來源與 topic_guess。 |
| 議題素材整理 | 15 分鐘 | 將已審核資料整理成地方問題紀錄。 |
| 明日待辦 | 5 分鐘 | 決定明天優先審核的 queue 類型與數量。 |

---

## 四、每日檢查清單

### 1. GitHub 狀態

- [ ] 是否有 open PR？
- [ ] 是否有重複 PR？
- [ ] 是否有 Actions failure？
- [ ] 是否有 main 已完成但舊分支仍開著？
- [ ] 是否有需要人工 review 的 Codex PR？

### 2. Dashboard 狀態

- [ ] `dashboard/index.html` 是否仍可作為入口？
- [ ] `dashboard/map.html` 是否可查看熱點？
- [ ] `dashboard/geocoding-review.html` 是否可查看座標審核？
- [ ] `dashboard/video-review.html` 是否可查看影音審核？
- [ ] `dashboard/insights.html` 是否可查看趨勢？

### 3. 資料檔狀態

- [ ] `dashboard/data/hotspots.json` 是否存在？
- [ ] `dashboard/data/hotspots.geojson` 是否存在？
- [ ] `dashboard/data/geocoding_review_queue.json` 是否存在？
- [ ] `dashboard/data/transcript_review_queue.json` 是否存在？
- [ ] `dashboard/data/site_map.json` 是否包含最新頁面？

---

## 五、資料是否可用的判斷

| 狀態 | 可否進入正式分析 | 說明 |
|---|---|---|
| `unreviewed` | 否 | 尚未人工確認。 |
| `needs_metadata_review` | 否 | 基本欄位不完整。 |
| `reviewed` | 可以，但仍需保守引用 | 已人工確認，可進入下一階段。 |
| `verified` | 可以 | 已由可信來源交叉驗證。 |
| `rejected` | 否 | 不納入後續使用。 |

---

## 六、每天建議輸出格式

```markdown
# 每日資料審核紀錄

日期：YYYY-MM-DD

## 今日檢查
- GitHub PR：
- Actions：
- Dashboard：
- 資料檔：

## 今日審核
| 類型 | queue_id / candidate_id | 結果 | 後續動作 |
|---|---|---|---|
| 座標 |  |  |  |
| 影音 |  |  |  |

## 今日可累積議題
1. 
2. 
3. 

## 明日待辦
1. 
2. 
3. 
```

---

## 七、可轉成社群或政策素材的條件

資料要轉成社群文案、政策素材或簡報前，至少要滿足：

1. 有公開來源。
2. 有日期或時間脈絡。
3. 有人工 review 紀錄。
4. 沒有私人個資。
5. 沒有超出資料可支持範圍的結論。
6. 可以用中性語氣說明，不需要人身攻擊。

---

## 八、暫時不可對外使用的情況

以下情況先留在內部審核：

1. 來源不明。
2. 日期缺漏。
3. 地點仍是 prototype 座標。
4. 影音 metadata 尚未補齊。
5. 逐字稿尚未人工確認。
6. 只有 AI 初稿，沒有人工 review。
7. 涉及個資、私人地址、電話、email 或身分證字號。
8. 結論容易被誤解為正式調查結果。

---

## 九、每週一次整理

每週建議整理一次：

| 項目 | 目的 |
|---|---|
| 本週新增資料 | 確認 crawler / builder 是否持續產生資料。 |
| 本週已審核資料 | 確認人工 review 是否累積。 |
| 本週高頻議題 | 找出可以發展成政策提案的方向。 |
| 本週測試狀態 | 確認 Actions 與 pytest 是否穩定。 |
| 下週優先工作 | 決定要優先做 parser、dashboard、SOP 或資料清理。 |

---

## 十、故障處理

| 狀況 | 處理方式 |
|---|---|
| Actions failure | 先看失敗測試名稱，再抓 job log。 |
| JSON validation failure | 檢查必要欄位、狀態值、資料型別。 |
| Dashboard 頁面空白 | 檢查資料檔路徑與 renderer selector。 |
| PR 重複 | 確認 main 是否已有同等內容，有就關閉重複 PR。 |
| Codex 與手動 PR 可能衝突 | 先不碰同一批檔案，改做文件或 dashboard 文案。 |
| 地名不一致 | 以 local terminology 測試與在地常用名稱為準。 |

---

## 十一、核心原則

```text
先留痕，再分析。
先審核，再發布。
先確認來源，再形成結論。
先做小而穩的流程，再擴大自動化。
```

一人團隊不需要一天完成全部資料；只要每天穩定審核 3 到 5 筆，長期就能累積成可查證、可說明、可轉化為政策的城市故障分析資料庫。
