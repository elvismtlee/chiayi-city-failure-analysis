# 本機開發指南

## 1. Clone Repo

```bash
git clone https://github.com/elvismtlee/chiayi-city-failure-analysis.git
cd chiayi-city-failure-analysis
```

## 2. 建立虛擬環境

```bash
python -m venv venv
```

Windows:

```bash
venv\\Scripts\\activate
```

Mac / Linux:

```bash
source venv/bin/activate
```

## 3. 安裝套件

```bash
pip install -r requirements.txt
```

## 4. 執行分類器測試

```bash
python src/classifiers/issue_classifier.py
```

## 5. 執行資料驗證器

```bash
python src/utils/data_validator.py
```

## 6. 啟動 Streamlit Dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

## 7. 未來方向

- crawler
- parser
- geocoding
- AI 摘要
- heatmap
- Looker Studio
- n8n workflow
