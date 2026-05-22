# Filming Checklist Builder Checklist

本文件用來審查未來 filming checklist builder 與 dashboard PR。目標是把短影音腳本草稿轉成一人團隊可執行的拍攝清單，而不是自動發布影片。

---

## 一、預期資料流

```text
short video script drafts
  -> filming checklist candidates
  -> human filming review
  -> filming day plan
  -> manual recording and publishing
```

第一版只讀本地 JSON，只產生拍攝工作清單，不呼叫影音平台 API。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_filming_checklists.py` |
| dashboard data | `dashboard/data/filming_checklists.json` |
| dashboard page | `dashboard/filming-checklists.html` |
| dashboard renderer | `dashboard/filming-checklists.js` |
| builder test | `tests/test_build_filming_checklists.py` |
| page test | `tests/test_filming_checklists_page.py` |

---

## 三、filming_checklists.json 必要欄位

```text
checklist_id
source_script_id
issue_title
shooting_goal
location_type
scene_tasks
a_roll_notes
b_roll_notes
props_needed
audio_notes
estimated_minutes
review_status
public_use_status
risk_notes
recommended_next_step
```

驗收重點：

1. `checklist_id` 穩定。
2. `shooting_goal` 應是清楚可執行的拍攝目標。
3. `location_type` 可為 office、street、market、school_area、park、other。
4. `scene_tasks` 應是 list，且每項可一人完成。
5. `a_roll_notes` 應說明人物口播畫面。
6. `b_roll_notes` 應說明補充畫面，不得要求偷拍或侵犯隱私。
7. `props_needed` 應是 list。
8. `audio_notes` 應提醒收音與環境噪音。
9. `estimated_minutes` 應是合理拍攝時間。
10. `review_status` 應是 `needs_filming_review`。
11. `public_use_status` 應是 `internal_filming_plan`。
12. `risk_notes` 應提醒需人工確認地點、影像權與安全。

---

## 四、拍攝清單格式建議

每筆拍攝清單建議轉成：

```markdown
## 拍攝主題

### 拍攝目標

### 需要畫面
1.
2.
3.

### 口播重點

### B-roll 補充畫面

### 道具

### 收音提醒

### 風險提醒
```

---

## 五、Dashboard 驗收

`dashboard/filming-checklists.html` 應顯示：

1. 拍攝清單候選。
2. 總清單數。
3. 需要人工審核數。
4. 估計拍攝時間總量。
5. 每筆 checklist card。

每張 card 至少顯示：

1. `issue_title`
2. `shooting_goal`
3. `location_type`
4. `scene_tasks`
5. `a_roll_notes`
6. `b_roll_notes`
7. `props_needed`
8. `estimated_minutes`
9. `risk_notes`

頁面必須提醒：

1. 這是內部拍攝清單。
2. 不是自動發布內容。
3. 拍攝前需人工確認地點與影像權。
4. 不得偷拍、冒充或使用誤導剪輯。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 short video script builder 後執行：

```bash
python scripts/build_filming_checklists.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
filming-checklists.html
```

---

## 八、測試指令

```bash
python scripts/build_filming_checklists.py
pytest -q tests/test_build_filming_checklists.py
pytest -q tests/test_filming_checklists_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不自動發布。
5. 不呼叫影音平台 API。
6. 不要求偷拍、冒充或誤導剪輯。
7. 不輸出私人資料欄位。
8. 文案清楚標示內部拍攝計畫。

---

## 十、下一步

合併 filming checklist builder 後，可再推進：

1. content calendar draft builder。
2. public material review dashboard。
3. n8n 每週人工審核提醒。
4. filming day printable checklist。
