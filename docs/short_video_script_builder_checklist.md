# Short Video Script Builder Checklist

本文件用來審查未來 short video script draft builder 與 dashboard PR。目標是把政策草稿或社群草稿轉成內部短影音腳本草稿，而不是自動發布或製造誤導影片。

---

## 一、預期資料流

```text
policy draft candidates / social post drafts
  -> short video script drafts
  -> human communication review
  -> filming plan
  -> manual publishing
```

第一版只讀本地 JSON，只產生草稿，不接影音平台 API。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_short_video_script_drafts.py` |
| dashboard data | `dashboard/data/short_video_script_drafts.json` |
| dashboard page | `dashboard/video-scripts.html` |
| dashboard renderer | `dashboard/video-scripts.js` |
| builder test | `tests/test_build_short_video_script_drafts.py` |
| page test | `tests/test_video_scripts_page.py` |

---

## 三、short_video_script_drafts.json 必要欄位

```text
script_id
source_draft_id
issue_title
hook
opening_line
scene_plan
voiceover
subtitle_lines
call_to_action
source_urls
review_status
public_use_status
risk_notes
recommended_next_step
```

驗收重點：

1. `script_id` 穩定。
2. `hook` 不可誇大或恐嚇。
3. `opening_line` 應簡短、清楚、可口語化。
4. `scene_plan` 應是 list，包含可一人拍攝的畫面。
5. `voiceover` 應保守，不超出來源資料。
6. `subtitle_lines` 應是 list，適合 30 到 60 秒短影音。
7. `call_to_action` 應是中性意見回饋或追蹤資訊。
8. `review_status` 應是 `needs_video_review`。
9. `public_use_status` 應是 `internal_video_draft`。
10. `risk_notes` 應提醒需人工確認來源、語氣與法遵。

---

## 四、腳本格式建議

每支短影音草稿建議包含：

```markdown
## 影片題目

### 片頭 3 秒

### 主要畫面
1.
2.
3.

### 旁白

### 字幕
1.
2.
3.

### 結尾行動呼籲

### 拍攝提醒
```

---

## 五、Dashboard 驗收

`dashboard/video-scripts.html` 應顯示：

1. 短影音腳本草稿清單。
2. 總腳本數。
3. 需要人工審核數。
4. 可一人拍攝數。
5. 每筆 script card。

每張 card 至少顯示：

1. `issue_title`
2. `hook`
3. `opening_line`
4. `scene_plan`
5. `voiceover`
6. `subtitle_lines`
7. `call_to_action`
8. `risk_notes`

頁面必須提醒：

1. 這是內部短影音腳本草稿。
2. 不是自動發布內容。
3. 對外使用前需人工審核。
4. 不得使用深偽、冒充或誤導剪輯。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 policy draft 或 social draft builder 後執行：

```bash
python scripts/build_short_video_script_drafts.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
video-scripts.html
```

---

## 八、測試指令

```bash
python scripts/build_short_video_script_drafts.py
pytest -q tests/test_build_short_video_script_drafts.py
pytest -q tests/test_video_scripts_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不自動發布。
5. 不呼叫影音平台 API。
6. 不生成或要求深偽內容。
7. 不輸出私人資料欄位。
8. 文案清楚標示內部草稿。
9. 不把草稿描述為正式對外影片。

---

## 十、下一步

合併 short video script draft builder 後，可再推進：

1. filming checklist builder。
2. public material review dashboard。
3. n8n 每週人工審核提醒。
4. content calendar draft builder。
