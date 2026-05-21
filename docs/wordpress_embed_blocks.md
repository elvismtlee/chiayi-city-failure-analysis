# WordPress 嵌入模組 v1

本文件提供可直接貼到 WordPress 自訂 HTML 區塊的模組。

---

## 模組 1：城市故障分析中心導流卡片

適合放在 chiayi2026.com 首頁或「城市故障回報」頁面。

```html
<section style="max-width:1100px;margin:40px auto;padding:28px;border-radius:28px;background:linear-gradient(135deg,#064e3b,#0f766e);color:white;font-family:'Noto Sans TC',system-ui,sans-serif;box-shadow:0 18px 50px rgba(15,23,42,.18);">
  <div style="display:inline-block;padding:7px 12px;border:1px solid rgba(255,255,255,.35);border-radius:999px;background:rgba(255,255,255,.12);font-size:14px;letter-spacing:.08em;">
    CHIAYI URBAN FAILURE ANALYSIS
  </div>
  <h2 style="font-size:clamp(30px,5vw,52px);line-height:1.1;margin:18px 0 12px;">
    嘉義城市故障分析中心
  </h2>
  <p style="font-size:18px;line-height:1.8;max-width:760px;color:rgba(255,255,255,.9);">
    用資料工程整理城市問題，用科技治理改善市民生活。查看嘉義市生活議題熱點、城市故障指數與 AI 城市觀察摘要。
  </p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:22px;">
    <a href="https://elvismtlee.github.io/chiayi-city-failure-analysis/" target="_blank" rel="noopener" style="display:inline-block;padding:12px 18px;border-radius:999px;background:white;color:#064e3b;text-decoration:none;font-weight:800;">
      查看城市儀表板
    </a>
    <a href="https://elvismtlee.github.io/chiayi-city-failure-analysis/insights.html" target="_blank" rel="noopener" style="display:inline-block;padding:12px 18px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.35);color:white;text-decoration:none;font-weight:800;">
      查看城市洞察分析
    </a>
  </div>
</section>
```

---

## 模組 2：iframe 嵌入 dashboard

適合放在獨立頁面，例如：

```text
https://www.chiayi2026.com/city-dashboard/
```

```html
<div style="max-width:1280px;margin:30px auto;padding:0 16px;">
  <iframe
    src="https://elvismtlee.github.io/chiayi-city-failure-analysis/"
    style="width:100%;height:1400px;border:0;border-radius:24px;box-shadow:0 18px 50px rgba(15,23,42,.12);overflow:hidden;"
    loading="lazy"
    title="嘉義城市故障分析中心">
  </iframe>
</div>
```

---

## 模組 3：資料聲明小字

```html
<p style="max-width:1100px;margin:16px auto;color:#64748b;font-size:14px;line-height:1.8;font-family:'Noto Sans TC',system-ui,sans-serif;">
  本平台資料來自公開資訊、官方資料與原型資料整理。分析結果為城市治理與地方議題研究用途，不代表完整民意調查，也不作為個人評價結論。正式引用前，仍應回到原始來源查證。
</p>
```

---

## 模組 4：資料站頁面按鈕列

```html
<div style="max-width:1100px;margin:24px auto;display:flex;gap:12px;flex-wrap:wrap;font-family:'Noto Sans TC',system-ui,sans-serif;">
  <a href="https://elvismtlee.github.io/chiayi-city-failure-analysis/" target="_blank" rel="noopener" style="padding:10px 16px;border-radius:999px;background:#0f766e;color:white;text-decoration:none;font-weight:800;">城市儀表板</a>
  <a href="https://elvismtlee.github.io/chiayi-city-failure-analysis/insights.html" target="_blank" rel="noopener" style="padding:10px 16px;border-radius:999px;background:#0f766e;color:white;text-decoration:none;font-weight:800;">城市洞察</a>
  <a href="https://elvismtlee.github.io/chiayi-city-failure-analysis/sources.html" target="_blank" rel="noopener" style="padding:10px 16px;border-radius:999px;background:#0f766e;color:white;text-decoration:none;font-weight:800;">資料來源</a>
  <a href="https://elvismtlee.github.io/chiayi-city-failure-analysis/methodology.html" target="_blank" rel="noopener" style="padding:10px 16px;border-radius:999px;background:#0f766e;color:white;text-decoration:none;font-weight:800;">方法論</a>
  <a href="https://elvismtlee.github.io/chiayi-city-failure-analysis/reports.html" target="_blank" rel="noopener" style="padding:10px 16px;border-radius:999px;background:#0f766e;color:white;text-decoration:none;font-weight:800;">城市週報</a>
</div>
```

---

## 建議使用順序

1. 先用「模組 1」放在首頁或城市故障回報頁。
2. 再建立 `/city-dashboard/` 頁面放「模組 2」。
3. 頁面底部放「模組 3」。
4. 若需要多頁導流，加入「模組 4」。
