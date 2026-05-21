import pandas as pd
import streamlit as st

st.set_page_config(page_title="嘉義市城市故障分析", layout="wide")

st.title("嘉義市 12 年城市故障分析儀表板")
st.caption("科技分析城市問題，文化理解地方生活，幸福改善市民日常。")

cases = pd.read_csv("data/samples/sample_1999_cases.csv")
questions = pd.read_csv("data/samples/sample_council_questions.csv")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("1999 樣本案件", len(cases))

with col2:
    st.metric("質詢樣本", len(questions))

with col3:
    st.metric("主要議題", "交通")

st.subheader("1999 樣本資料")
st.dataframe(cases)

st.subheader("議員質詢樣本")
st.dataframe(questions)

st.subheader("議題統計")
issue_counts = cases["issue_category_lv1"].value_counts()
st.bar_chart(issue_counts)
