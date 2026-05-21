# AI Issue Summarizer 規格 v1

本文件定義「城市故障 AI 摘要器」的輸入、輸出與用途。

## 目的

把 crawler / parser 取得的 metadata、會議紀錄、質詢影音標題、1999 或陳情案件，轉成可讀的城市議題摘要。

## 輸入資料

來源包括：

- data/raw/cycc_minutes_metadata.csv
- data/raw/cycc_question_video_metadata.csv
- data/raw/1999_cases.csv
- data/processed/issue_classified.csv

## 輸出資料

```text
dashboard/data/ai_issue_summary.json
```

## JSON 格式

```json
{
  "updated_at": "2026-05-21 09:00:00",
  "summary_title": "本週嘉義城市故障觀察",
  "summary": "本週資料顯示，交通、停車與道路仍是高關注議題。",
  "top_findings": [
    "文化路夜市周邊停車與人行問題值得優先追蹤",
    "市場周邊垃圾與動線問題可列入生活議題改善",
    "學校周邊通學安全適合轉為短影音與政見說明"
  ],
  "recommended_actions": [
    "建立市場周邊停車與卸貨時段規劃",
    "盤點西區通學步道與斑馬線安全",
    "建立路燈與夜間照明巡檢清單"
  ]
}
```

## 摘要原則

1. 不做無根據指控
2. 不做人身攻擊
3. 以官方資料與公開資料為基礎
4. 用市民聽得懂的語言
5. 可以轉成政策、貼文、短影音腳本

## 後續應用

- dashboard AI 摘要區塊
- 每週城市故障週報
- FB / Threads 草稿
- LINE 志工群摘要
- 拜訪里鄰前議題簡報
