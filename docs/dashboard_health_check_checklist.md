# Dashboard Health Check Checklist

本文件用來審查未來 dashboard health check builder 與 dashboard PR。目標是檢查資料檔、頁面與導覽是否完整，讓一人團隊快速發現資料流程是否斷線。

---

## 一、資料流

```text
dashboard data files
dashboard html/js pages
site map
shared navigation
  -> dashboard health check summary
```

第一版只讀本地檔案，只產生健康檢查摘要，不修改既有資料。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_dashboard_health_check.py` |
| data | `dashboard/data/dashboard_health_check.json` |
| page | `dashboard/health-check.html` |
| renderer | `dashboard/health-check.js` |
| builder test | `tests/test_build_dashboard_health_check.py` |
| page test | `tests/test_health_check_page.py` |

---

## 三、dashboard_health_check.json 必要欄位

```text
check_id
generated_at
checked_files
missing_files
empty_files
invalid_json_files
page_checks
nav_checks
warnings
status
public_use_status
notes
```

---

## 四、檢查規則

1. 檢查重要 JSON 是否存在。
2. 檢查重要 HTML / JS 頁面是否存在。
3. 檢查 site map 是否包含重要頁面。
4. 檢查 shared navigation 是否包含重要頁面。
5. 若沒有缺檔、空檔與 invalid JSON，status 可為 `ok`。
6. 若有缺檔、空檔或 invalid JSON，status 應為 `needs_attention`。
7. public_use_status 應為 `internal_health_check`。
8. notes 應提醒這是內部健康檢查摘要。

---

## 五、Dashboard 驗收

`dashboard/health-check.html` 應顯示：

1. Dashboard 健康檢查。
2. 整體 status。
3. checked_files 數量。
4. missing_files。
5. empty_files。
6. invalid_json_files。
7. page_checks。
8. nav_checks。
9. warnings。

頁面必須提醒：

1. 這是內部系統健康檢查。
2. 只檢查本地檔案。
3. 不代表資料內容已完成人工審核。

---

## 六、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
health-check.html
```

---

## 七、測試指令

```bash
python scripts/build_dashboard_health_check.py
pytest -q tests/test_build_dashboard_health_check.py
pytest -q tests/test_health_check_page.py
pytest -q
```

---

## 八、合併條件

1. Python Tests 成功。
2. 只讀本地檔案。
3. 不修改既有資料。
4. 不呼叫外部 API。
5. 能偵測缺檔、空檔與 invalid JSON。
6. 頁面清楚標示內部健康檢查。

---

## 九、下一步

合併 dashboard health check 後，可再推進：

1. command center 整合 health status。
2. weekly system report。
3. production readiness checklist。
