# MVP 上線計畫 v1

本文件定義「嘉義城市故障分析資料庫」第一個可公開展示版本的最小可行範圍。

---

## MVP 目標

先完成一個能對外展示、可持續更新、資料狀態清楚的原型版本。

MVP 不追求一次完成完整 12 年資料庫，而是先完成：

```text
資料來源透明
→ dashboard 可看
→ sample / prototype 狀態清楚
→ JSON 可驗證
→ 週報可產生
→ 官網可導流
```

---

## MVP 必備頁面

| 頁面 | 狀態目標 |
|---|---|
| `index.html` | 城市儀表板首頁可正常顯示 |
| `insights.html` | 城市洞察分析可正常顯示 |
| `sources.html` | 資料來源與更新狀態清楚 |
| `methodology.html` | 方法論與資料限制清楚 |
| `reports.html` | 週報列表可正常顯示 |
| `reports/2026-W21.html` | 第一篇 prototype 週報可讀 |
| `404.html` | 錯誤頁可返回首頁 |

---

## MVP 必備資料

| 資料 | 檔案 | 狀態 |
|---|---|---|
| 總覽 KPI | `dashboard/data/dashboard_summary.json` | 必備 |
| 議題排行 | `dashboard/data/issue_ranking.json` | 必備 |
| 熱點資料 | `dashboard/data/hotspots.json` | 必備 |
| AI 摘要 | `dashboard/data/ai_issue_summary.json` | 必備 |
| 趨勢資料 | `dashboard/data/issue_trends.json` | 必備 |
| 資料來源 | `dashboard/data/data_sources.json` | 必備 |
| 週報索引 | `dashboard/data/reports_index.json` | 必備 |

---

## MVP 資料狀態

MVP 可以使用：

- mock data
- sample data
- prototype data
- 已公開 metadata

但必須清楚標示：

```text
目前資料為原型樣本資料，僅供系統展示與流程測試，不代表正式統計結果。
```

---

## MVP 不做的事

第一版先不做：

1. 完整 12 年資料庫。
2. 自動下載影音。
3. 自動發布外部內容。
4. 公開使用者原始回報內容。
5. 未審核的 AI 自動結論。

---

## MVP 驗收標準

### 前端

- [ ] 首頁可開啟
- [ ] insights 可開啟
- [ ] sources 可開啟
- [ ] methodology 可開啟
- [ ] reports 可開啟
- [ ] 手機版可閱讀
- [ ] JSON 讀取失敗時不整頁空白

### 資料

- [ ] 所有 dashboard JSON 可 parse
- [ ] 必要欄位存在
- [ ] prototype / sample 狀態清楚
- [ ] 不含個資
- [ ] sources.html 有資料來源說明

### GitHub

- [ ] pytest 通過
- [ ] GitHub Actions 通過
- [ ] Pages 部署成功
- [ ] docs 有入口

---

## MVP 推進順序

```text
1. Codex 狀態檢查
2. 確認 crawler metadata PR 狀態
3. build dashboard data pipeline
4. JSON validation tests
5. GitHub Actions build workflow
6. 全站共用導覽與 footer
7. Leaflet 熱點地圖
8. 官網導流
```

---

## MVP 對外說法

```text
嘉義城市故障分析中心目前為 prototype 原型站，正在逐步整合公開資料、議會資料與地方議題觀察。現階段資料主要用於展示資料流程與城市治理分析方法，正式引用前仍應回到原始來源查證。
```

---

## MVP 成功定義

第一版成功不等於資料完整，而是代表：

```text
網站可開
資料可更新
來源可追溯
風險有聲明
下一步可接正式資料
```
