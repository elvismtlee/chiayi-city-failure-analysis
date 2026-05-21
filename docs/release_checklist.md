# GitHub Pages 發布檢查表 v1

本文件定義「嘉義城市故障分析中心」每次發布前的檢查項目。

---

## A. 頁面檢查

### 必要頁面

- [ ] `/` 首頁可開啟
- [ ] `/insights.html` 城市洞察分析可開啟
- [ ] `/sources.html` 資料來源頁可開啟
- [ ] `/methodology.html` 方法論頁可開啟
- [ ] `/reports.html` 城市週報列表可開啟
- [ ] `/reports/2026-W21.html` 週報詳細頁可開啟
- [ ] `/404.html` 錯誤頁可開啟

---

## B. 導覽檢查

- [ ] 每頁都有返回首頁連結
- [ ] 每頁都有清楚的目前頁面定位
- [ ] 首頁可導向城市洞察分析
- [ ] 週報列表可導向週報詳細頁
- [ ] 資料來源、方法論、週報頁之間可互相找到

---

## C. JSON 資料檢查

- [ ] `dashboard/data/dashboard_summary.json`
- [ ] `dashboard/data/issue_ranking.json`
- [ ] `dashboard/data/hotspots.json`
- [ ] `dashboard/data/ai_issue_summary.json`
- [ ] `dashboard/data/issue_trends.json`
- [ ] `dashboard/data/urban_failure_scores.json`
- [ ] `dashboard/data/department_performance.json`
- [ ] `dashboard/data/councilor_issue_analysis.json`
- [ ] `dashboard/data/data_sources.json`
- [ ] `dashboard/data/reports_index.json`
- [ ] `dashboard/data/site_map.json`

---

## D. JavaScript 檢查

- [ ] `app.js` 可正常載入首頁資料
- [ ] `insights.js` 可正常載入洞察資料
- [ ] `site-pages.js` 可正常載入資料來源與週報資料
- [ ] JSON 讀取失敗時不會造成整頁空白

---

## E. 文案與法遵檢查

- [ ] 不使用「民調」
- [ ] 不使用「支持度調查」
- [ ] 不做人身攻擊
- [ ] 不做無來源指控
- [ ] prototype / mock data 已標示
- [ ] AI 摘要聲明已標示
- [ ] 資料限制已標示

---

## F. GitHub Actions 檢查

- [ ] Python tests 通過
- [ ] Pages deploy 通過
- [ ] 若有 processor，確認 JSON 產出成功
- [ ] 若 workflow 失敗，先查 logs 再重跑

---

## G. 合併 PR 前檢查

- [ ] PR 沒有 merge conflict
- [ ] PR 只做一個清楚任務
- [ ] 修改檔案符合任務範圍
- [ ] 沒有把 token / credential 寫進 repo
- [ ] 測試結果寫在 PR description

---

## H. 發布後檢查

部署完成後，打開：

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/
```

確認：

1. 首頁可正常顯示。
2. 五個主要頁面可互相連結。
3. JSON 內容有被讀取。
4. 手機版不破版。
5. 頁尾資料聲明清楚。
