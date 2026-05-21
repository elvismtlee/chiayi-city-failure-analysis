# PR Merge 前品質檢查清單 v1

本文件用於 Codex 或其他開發代理完成 PR 後，merge 前的人工檢查。

重點：不要只看 GitHub Actions 綠燈。若 processor source、fallback data 或 public-facing output 還有品質問題，仍不應 merge。

---

## 一、基本狀態

- [ ] PR 狀態為 open
- [ ] PR 不是 draft
- [ ] PR 顯示 mergeable
- [ ] 沒有尚未處理的 blocking comment
- [ ] PR 說明有列出修改內容與驗證方式

---

## 二、GitHub Actions

- [ ] Python Tests 通過
- [ ] Dashboard Data workflow 通過
- [ ] 若修改 GitHub Pages 相關檔案，Pages deploy 沒有失敗
- [ ] 若 workflow 有新檔案，確認不與既有 workflow 重複或互相覆蓋

---

## 三、processor 與 fallback data

- [ ] processor source 沒有硬寫錯誤地名或不合在地語感的 mock data
- [ ] fallback mode 有測試覆蓋
- [ ] raw CSV 不存在時，dashboard 仍可產生合法 JSON
- [ ] fallback output 與 raw CSV output 都通過在地用語測試
- [ ] 產生器修正後有重新產生 dashboard JSON

---

## 四、dashboard JSON

- [ ] `dashboard/data/*.json` 都是合法 JSON
- [ ] 前端讀取的 JSON path 沒有被改壞
- [ ] output 欄位仍符合 `docs/frontend_rendering_contract.md`
- [ ] 熱點、議題排行、AI 摘要的欄位名稱一致
- [ ] public-facing JSON 不含未確認地名或不建議稱呼

---

## 五、在地用語與地名字典

- [ ] 新增或修改地名時，有對照 `dashboard/data/local_place_dictionary.json`
- [ ] 對外顯示優先使用 `display_name`
- [ ] 口語文案可使用 `local_name`
- [ ] 不建議稱呼只應出現在規則文件或地名字典的說明欄位
- [ ] 一般 dashboard、週報、processor output 不應輸出不建議稱呼

---

## 六、資料治理

- [ ] 不包含個人姓名、電話、完整地址等個資
- [ ] 地址或地點已依精度規則降階處理
- [ ] raw data 與 processed data 分層清楚
- [ ] 對外資料不寫成定罪、指控或績效定論
- [ ] AI 摘要有保留不確定性，不過度推論

---

## 七、建議本機檢查命令

```bash
python src/processors/build_dashboard_data.py
pytest -q
```

若 PR 修改地名或 processor，請額外做全文搜尋，確認不建議稱呼沒有出現在 source、dashboard output 或一般測試資料中。

---

## 八、merge 判斷

可以 merge：

```text
Actions 全綠
source 沒有明顯品質問題
fallback mode 被測到
dashboard output 正常
沒有 blocking comment
```

暫不 merge：

```text
Actions 雖然全綠，但 processor source 仍會在 fallback mode 產生錯誤 output
Actions 全綠，但 public-facing output 有錯誤地名
Actions 全綠，但 PR 說明與實際修改不一致
Actions 全綠，但缺少必要測試
```

---

## 原則

```text
workflow 綠燈是必要條件，不是充分條件。
```
