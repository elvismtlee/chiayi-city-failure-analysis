# 使用者路徑設計 v1

本文件定義不同使用者進入「嘉義城市故障分析中心」後，應該如何理解與使用平台。

---

## 1. 一般市民

### 進站原因

市民可能想知道：

- 嘉義市最近哪些生活問題比較多人關心？
- 自己遇到的交通、道路、環境問題是不是反覆發生？
- 城市故障回報後，是否能被整理與追蹤？

### 建議路徑

```text
首頁 index.html
→ 看 KPI 與熱門議題
→ 看熱點與城市故障追蹤表
→ 進入 sources.html 了解資料來源
→ 若想深入，再看 insights.html
```

### 頁面應回答

1. 這是什麼平台？
2. 目前資料是否正式？
3. 我可以看到哪些問題？
4. 我如何回報或提供資料？
5. 我的個資是否會被公開？

---

## 2. 志工 / 團隊成員

### 進站原因

志工可能需要：

- 找出適合拜訪的里鄰議題
- 找出適合拍短影音的地點
- 整理一週地方問題摘要
- 回覆市民留言時有資料根據

### 建議路徑

```text
首頁 index.html
→ insights.html
→ reports.html
→ reports/YYYY-WW.html
```

### 可用功能

- 城市故障分數排行
- 議題趨勢
- 局處負荷觀察
- 城市週報
- 建議行動

### 注意事項

志工對外說明時，不應說：

```text
這是民調結果
這證明大家都不滿
這代表某局處一定有問題
```

應改說：

```text
這是公開資料與地方議題整理，目前可作為後續追蹤參考。
```

---

## 3. 媒體 / 地方觀察者

### 進站原因

媒體或地方觀察者可能想知道：

- 這個資料站是否可信？
- 資料來源是什麼？
- 分析方法是否透明？
- 是否有過度政治化或指控風險？

### 建議路徑

```text
project_public_positioning.md
→ sources.html
→ methodology.html
→ public_disclaimer.md
→ risk_register.md
```

### 頁面應強調

1. 這是城市治理資料工具。
2. 不是民調。
3. 不公開個資。
4. 不做個人評分。
5. 分析結果需回到原始來源查證。

---

## 4. 工程 / Codex / 開發者

### 進站原因

開發者需要知道：

- 要改哪些檔案？
- JSON 格式是什麼？
- 前端 selector 是什麼？
- 測試怎麼跑？
- PR 怎麼開？

### 建議路徑

```text
docs/docs_index.md
→ docs/development_board.md
→ docs/data_dictionary.md
→ docs/frontend_rendering_contract.md
→ docs/json_validation_rules.md
→ docs/codex_prompt_library.md
```

### 必看文件

- `docs/codex_resume_plan.md`
- `docs/pr_review_guide.md`
- `docs/github_actions_strategy.md`
- `docs/troubleshooting.md`

---

## 5. WordPress 官網訪客

### 進站原因

從 chiayi2026.com 進來的訪客可能只想快速了解：

- 這個資料站跟主官網有什麼關係？
- 為什麼要看 dashboard？
- 看完後可以做什麼？

### 建議路徑

```text
chiayi2026.com 城市故障回報頁
→ 資料站導流卡片
→ GitHub Pages dashboard
→ sources.html / public FAQ
```

### WordPress 導流文案

```text
如果你想知道城市問題如何被整理、追蹤與分析，可以進入嘉義城市故障分析中心，查看目前的議題儀表板與城市洞察分析。
```

---

## 6. 每個頁面的使用者任務

| 頁面 | 使用者任務 |
|---|---|
| index.html | 快速理解目前城市故障總覽 |
| insights.html | 看 AI 摘要、趨勢與建議行動 |
| sources.html | 查資料來源與更新狀態 |
| methodology.html | 了解分類、分數與限制 |
| reports.html | 找每週城市故障週報 |
| reports/YYYY-WW.html | 閱讀完整週報 |
| 404.html | 找回首頁 |

---

## 設計原則

1. 一般市民要能在 30 秒內知道這是什麼。
2. 志工要能在 3 分鐘內找到可行動議題。
3. 媒體要能快速找到資料來源與限制。
4. 開發者要能快速找到欄位規格與測試規則。
5. 所有人都要看到資料聲明與非民調定位。
