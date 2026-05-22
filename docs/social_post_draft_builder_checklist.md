# Social Post Draft Builder Checklist

本文件用來審查未來 social post draft builder 與 dashboard PR。目標是把已人工審核的政策草稿候選，轉成內部社群文案草稿，而不是自動發布。

---

## 一、預期資料流

```text
policy draft candidates
  -> social post draft candidates
  -> human communication review
  -> final public post draft
  -> manual publishing
```

第一版應只讀本地 JSON，只產生草稿，不接任何社群 API。

---

## 二、預期新增檔案

| 類型 | 路徑 |
|---|---|
| builder | `scripts/build_social_post_drafts.py` |
| dashboard data | `dashboard/data/social_post_drafts.json` |
| dashboard page | `dashboard/social-drafts.html` |
| dashboard renderer | `dashboard/social-drafts.js` |
| builder test | `tests/test_build_social_post_drafts.py` |
| page test | `tests/test_social_drafts_page.py` |

---

## 三、social_post_drafts.json 必要欄位

```text
post_id
source_draft_id
issue_title
channel
headline
body
short_version
call_to_action
source_urls
review_status
public_use_status
risk_notes
recommended_next_step
```

驗收重點：

1. `post_id` 穩定。
2. `channel` 第一版可包含 `facebook`, `threads`, `line`。
3. `headline` 不可誇大。
4. `body` 應保留來源脈絡。
5. `short_version` 應適合短文平台。
6. `call_to_action` 應是中性參與或意見回饋，不做操控。
7. `review_status` 應是 `needs_communication_review`。
8. `public_use_status` 應標示 internal draft。
9. `risk_notes` 應提醒需人工確認語氣、來源與法遵。

---

## 四、文案語氣規則

社群草稿應符合：

1. 溫暖。
2. 堅定。
3. 有工程師邏輯。
4. 有嘉義在地感。
5. 不抹黑。
6. 不人身攻擊。
7. 不使用未查證指控。
8. 不把資料描述為民調或支持度調查。

---

## 五、Dashboard 驗收

`dashboard/social-drafts.html` 應顯示：

1. 社群文案草稿清單。
2. 總草稿數。
3. 需要人工審核數。
4. 各 channel 筆數。
5. 每筆 social draft card。

每張 card 至少顯示：

1. `channel`
2. `headline`
3. `body`
4. `short_version`
5. `call_to_action`
6. `source_urls`
7. `review_status`
8. `risk_notes`

頁面必須提醒：

1. 這是內部文案草稿。
2. 不是自動發布內容。
3. 對外使用前需人工審核。

---

## 六、Workflow 驗收

若納入 Dashboard Data workflow，應在 policy draft builder 後執行：

```bash
python scripts/build_social_post_drafts.py
```

---

## 七、Navigation 驗收

若新增 dashboard page，應更新：

1. `dashboard/data/site_map.json`
2. `dashboard/shared-nav.js`

並加入：

```text
social-drafts.html
```

---

## 八、測試指令

```bash
python scripts/build_social_post_drafts.py
pytest -q tests/test_build_social_post_drafts.py
pytest -q tests/test_social_drafts_page.py
pytest -q
```

---

## 九、合併條件

1. Python Tests 成功。
2. Dashboard Data 成功。
3. 只讀本地 JSON。
4. 不自動發布。
5. 不呼叫社群平台 API。
6. 不寄出訊息。
7. 不輸出私人資料欄位。
8. 文案清楚標示內部草稿。
9. 不把草稿描述為正式對外聲明。

---

## 十、下一步

合併 social post draft builder 後，可再推進：

1. short video script draft builder。
2. LINE broadcast draft builder。
3. public material review dashboard。
4. n8n 每週人工審核提醒。
