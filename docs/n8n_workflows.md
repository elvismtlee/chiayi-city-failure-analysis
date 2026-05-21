# n8n 工作流程規劃

## WF-001 每週資料抓取

Cron（每週一）
→ HTTP Request
→ Parser
→ Google Sheets
→ 通知

## WF-002 議題分類

Google Sheets Trigger
→ OpenAI / 關鍵字分類
→ Update Row

## WF-003 城市故障週報

Cron（每週五）
→ 統計分析
→ Google Docs
→ Gmail

## WF-004 社群素材生成

週報完成
→ OpenAI
→ 產生 FB / Threads / LINE 草稿
