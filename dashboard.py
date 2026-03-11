import streamlit as st
import pandas as pd

st.set_page_config(page_title="주식 추천 대시보드", layout="wide")

st.title("주식 추천 대시보드")
st.write("배포 테스트용 첫 화면입니다.")

data = pd.DataFrame([
    {"종목코드": "005930", "종목명": "삼성전자", "점수": 82},
    {"종목코드": "000660", "종목명": "SK하이닉스", "점수": 76},
    {"종목코드": "035420", "종목명": "NAVER", "점수": 68},
])

st.dataframe(data, use_container_width=True)
