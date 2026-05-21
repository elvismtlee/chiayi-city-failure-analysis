# Dashboard JSON 驗證規則 v1

本文件定義 `dashboard/data/*.json` 的基本驗證規則，供 processor、pytest、GitHub Actions 與 Codex 任務使用。

---

## 目的

避免 GitHub Pages 上線後發生：

1. JSON 格式錯誤，導致頁面空白。
2. 欄位缺漏，導致 JavaScript rendering 失敗。
3. mock data 與正式資料混淆。
4. 數字、日期、URL 型別不一致。
5. dashboard 顯示無法追溯來源。

---

## 共通規則

所有 dashboard JSON 建議符合：

1. 必須是合法 JSON。
2. 必須使用 UTF-8。
3. 不可包含註解。
4. 不可包含個資。
5. 日期欄位需使用 `YYYY-MM-DD` 或 ISO datetime。
6. 對外資料應包含 `data_status` 或可推導目前狀態。
7. 原型資料需標示 `mock`、`prototype` 或 `sample`。

---

## dashboard_summary.json

必要欄位：

```json
{
  "updated_at": "2026-05-21 09:00:00",
  "total_cases": 0,
  "top_issue": "交通停車",
  "total_hotspots": 0,
  "total_questions": 0
}
```

驗證規則：

- `updated_at` 必須存在。
- `total_cases` 必須是 number。
- `total_hotspots` 必須是 number。
- `total_questions` 必須是 number。
- `top_issue` 必須是 string。

---

## issue_ranking.json

應為 array。

每筆必要欄位：

```json
{
  "issue": "交通停車",
  "count": 100,
  "percent": 35.2
}
```

驗證規則：

- 必須是 array。
- 每筆 `issue` 必須是 string。
- 每筆 `count` 必須是 number。
- 若有 `percent`，必須是 number。
- 若有 `trend`，必須為 `up`、`down`、`stable`、`spike` 之一。

---

## hotspots.json

應為 array。

每筆必要欄位：

```json
{
  "name": "文化路商圈",
  "district": "西區",
  "category": "交通停車",
  "score": 92,
  "action": "盤點停車與人行衝突點"
}
```

驗證規則：

- 必須是 array。
- `name` 必須是 string。
- `district` 必須是 string。
- `category` 必須是 string。
- `score` 必須是 number，範圍 0 - 100。
- 若有 `lat` / `lng`，必須是 number 或 null。
- 不可公開完整個人地址。

---

## ai_issue_summary.json

必要欄位：

```json
{
  "updated_at": "2026-05-21 09:00:00",
  "summary_title": "本週嘉義城市故障觀察",
  "summary": "摘要內容",
  "top_findings": [],
  "recommended_actions": []
}
```

驗證規則：

- `summary_title` 必須是 string。
- `summary` 必須是 string。
- `top_findings` 必須是 array。
- `recommended_actions` 必須是 array。
- 不可包含無來源指控。
- 不可包含人身攻擊。

---

## issue_trends.json

應為 array。

每筆必要欄位：

```json
{
  "issue": "停車",
  "trend": "up",
  "change_percent": 31,
  "summary": "停車議題上升"
}
```

驗證規則：

- `trend` 必須為 `up`、`down`、`stable`、`spike` 之一。
- `change_percent` 必須是 number。
- `summary` 必須是 string。

---

## data_sources.json

應為 array。

每筆必要欄位：

```json
{
  "source_name": "嘉義市議會會議紀錄",
  "source_type": "官方公開資料",
  "status": "crawling",
  "latest_update": "2026-05-21",
  "record_count": 10,
  "source_url": "https://www.cycc.gov.tw/"
}
```

驗證規則：

- `source_name` 必須是 string。
- `status` 必須是 string。
- `record_count` 必須是 number。
- `source_url` 必須是 string 或 null。
- 若 `status` 是 `published`，必須有來源 URL 或明確 notes。

---

## reports_index.json

應為 array。

每筆必要欄位：

```json
{
  "report_id": "2026-W21",
  "title": "嘉義城市故障週報｜2026 第 21 週",
  "week_start": "2026-05-18",
  "week_end": "2026-05-24",
  "summary": "摘要",
  "report_url": "./reports/2026-W21.html"
}
```

驗證規則：

- `report_id` 必須是 string。
- `title` 必須是 string。
- `week_start` / `week_end` 必須存在。
- `report_url` 必須是 string。

---

## 建議 pytest 驗收

未來可建立：

```text
tests/test_dashboard_json_validation.py
```

測試項目：

1. 所有 JSON 都能 parse。
2. 必要欄位存在。
3. 數字欄位型別正確。
4. score 在 0 - 100。
5. trend 值合法。
6. 不含明顯個資欄位。
7. report_url 指向存在路徑。

---

## 失敗處理

若 validation 失敗：

1. GitHub Actions 應 fail。
2. 不應 deploy 到正式 Pages。
3. PR description 應列出錯誤 JSON 與欄位。
4. 若是資料不足，應回到 fallback mock data，而不是讓頁面空白。
