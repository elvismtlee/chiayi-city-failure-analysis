# GitHub Pages SEO 與社群分享設定 v1

本文件定義資料站各頁面的 title、description 與社群分享文字。

---

## 目的

讓 GitHub Pages 資料站在分享時具備清楚標題與說明，避免使用者不知道這是什麼專案。

---

## 全站預設

### site_name

```text
嘉義城市故障分析中心
```

### default_description

```text
以公開資料與資料工程整理嘉義市長期生活議題，建立可視覺化、可追蹤、可改善的城市治理資料平台。
```

### default_keywords

```text
嘉義市, 城市治理, 公開資料, 城市故障分析, 1999, 議會質詢, 地方議題, CivicTech, GovTech
```

---

## 首頁 index.html

### title

```text
嘉義城市故障分析中心｜城市儀表板
```

### description

```text
查看嘉義市城市故障儀表板，包含生活議題 KPI、熱點地圖、議題排行與城市治理資料觀察。
```

---

## insights.html

### title

```text
嘉義城市洞察分析｜AI 城市治理摘要
```

### description

```text
以 AI 摘要、議題趨勢、城市故障分數、局處負荷與議員質詢資料，分析嘉義市長期生活議題。
```

---

## sources.html

### title

```text
資料來源與更新狀態｜嘉義城市故障分析中心
```

### description

```text
公開說明嘉義城市故障分析中心使用的資料來源、更新狀態、資料筆數與資料限制。
```

---

## methodology.html

### title

```text
分析方法與城市故障分數｜嘉義城市故障分析中心
```

### description

```text
說明嘉義城市故障分析中心的議題分類、趨勢分析、AI 摘要與城市故障分數計算方法。
```

---

## reports.html

### title

```text
嘉義城市故障週報｜城市治理資料觀察
```

### description

```text
整理嘉義市每週城市故障觀察，包含熱門議題、熱點、趨勢與建議行動。
```

---

## Open Graph 建議

每頁可加入：

```html
<meta property="og:site_name" content="嘉義城市故障分析中心">
<meta property="og:type" content="website">
<meta property="og:title" content="頁面標題">
<meta property="og:description" content="頁面描述">
<meta property="og:url" content="頁面網址">
```

---

## Twitter / X Card 建議

```html
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="頁面標題">
<meta name="twitter:description" content="頁面描述">
```

---

## SEO 注意事項

1. 不使用誇大或攻擊性標題。
2. 不使用民調、支持度調查等容易誤導字眼。
3. 每頁 title 不要完全相同。
4. description 要說明頁面用途。
5. 若未來加分享圖，需確保繁體中文正確。
