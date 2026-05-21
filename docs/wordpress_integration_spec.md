# WordPress 官網整合規格 v1

本文件定義如何將「嘉義城市故障分析中心」整合到 chiayi2026.com。

## 目標

讓競選主官網與城市資料平台分工清楚：

- chiayi2026.com：形象、政見、活動、加入我們、城市回報
- GitHub Pages dashboard：資料儀表板、熱點地圖、AI 摘要、週報

---

## 建議網址架構

### 方案 A：主站按鈕連結

```text
https://www.chiayi2026.com/city-dashboard/
```

頁面中放置按鈕：

```text
進入嘉義城市故障分析中心
```

連到：

```text
https://elvismtlee.github.io/chiayi-city-failure-analysis/
```

---

### 方案 B：iframe 嵌入

在 WordPress 自訂 HTML 區塊加入：

```html
<iframe
  src="https://elvismtlee.github.io/chiayi-city-failure-analysis/"
  style="width:100%;height:1200px;border:0;border-radius:18px;overflow:hidden;"
  loading="lazy"
  title="嘉義城市故障分析中心">
</iframe>
```

---

### 方案 C：子網域

未來可設定：

```text
dashboard.chiayi2026.com
```

或：

```text
data.chiayi2026.com
```

指向 GitHub Pages。

---

## 官網導流區塊建議文案

標題：

```text
嘉義城市故障分析中心
```

副標：

```text
用資料工程看見城市問題，用科技治理改善市民生活。
```

按鈕：

```text
查看城市故障儀表板
```

---

## 注意事項

1. 若用 iframe，手機高度要測試。
2. 若資料仍是 prototype，頁面需標示「原型資料」。
3. 不要稱為民調或支持度調查。
4. 所有數據應標示來源與更新時間。
5. 正式資料上線前，避免做過度結論。
