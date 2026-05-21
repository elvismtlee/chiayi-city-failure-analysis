# Codex 工作指令包

## Codex 現在應該做什麼？

請 Codex 先從 GitHub Issues 依序處理：

1. Issue #1：建立嘉義市議會會議紀錄 crawler
2. Issue #2：建立議員質詢影音 metadata crawler
3. Issue #3：建立城市故障熱點地圖系統

## 建議 Codex 第一個任務

先不要急著做大型架構，請先完成：

### 任務 A：讓專案可以在本機穩定執行

請執行：

```bash
pip install -r requirements.txt
python src/classifiers/issue_classifier.py
python src/utils/data_validator.py
streamlit run dashboard/streamlit_app.py
```

如果有任何錯誤，請直接修正。

## 任務 B：補齊 crawler 基礎架構

建立以下檔案：

```text
src/crawlers/base_crawler.py
src/crawlers/cycc_video_crawler.py
src/parsers/html_parser.py
src/parsers/pdf_parser.py
src/utils/file_io.py
```

## 任務 C：擴充測試

建立：

```text
tests/test_issue_classifier.py
tests/test_data_validator.py
```

## 任務 D：更新 GitHub Actions

讓 GitHub Actions 自動執行：

```bash
python src/classifiers/issue_classifier.py
python src/utils/data_validator.py
pytest
```

## 任務 E：不要硬寫死網址

所有官方網址先放在：

```text
config/sources.yml
```

crawler 必須讀取 config，不要把網址寫死在 Python 裡。

## 任務 F：產出 PR

每個 Issue 建議開一個 branch：

```text
feature/issue-1-cycc-minutes-crawler
feature/issue-2-cycc-video-crawler
feature/issue-3-hotspot-map
```

每個 Issue 完成後開 PR，PR 內容要包含：

- 完成項目
- 測試方式
- 尚未完成限制
- 下一步建議
