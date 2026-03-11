import streamlit as st
import pandas as pd
import random
from datetime import datetime

st.set_page_config(page_title="주식 추천 대시보드", layout="wide")

st.title("주식 추천 대시보드")
st.caption("장초반 추천 종목 테스트 버전")

st.write("아래 버튼을 누르면 추천 종목 예시를 새로 계산합니다.")

WATCHLIST = [
    {"종목코드": "005930", "종목명": "삼성전자"},
    {"종목코드": "000660", "종목명": "SK하이닉스"},
    {"종목코드": "035420", "종목명": "NAVER"},
    {"종목코드": "051910", "종목명": "LG화학"},
    {"종목코드": "068270", "종목명": "셀트리온"},
    {"종목코드": "207940", "종목명": "삼성바이오로직스"},
]

def make_sample_scores():
    rows = []
    for item in WATCHLIST:
        change_rate = round(random.uniform(-1.5, 4.5), 2)
        strength = random.randint(80, 180)
        inst = random.randint(-30000, 30000)
        foreigner = random.randint(-30000, 30000)
        program = random.randint(-30000, 30000)

        score = 50

        if strength >= 150:
            score += 20
        elif strength >= 120:
            score += 10
        elif strength < 90:
            score -= 10

        if inst > 0:
            score += 8
        if foreigner > 0:
            score += 6
        if program > 0:
            score += 10

        if 0.3 <= change_rate <= 3.5:
            score += 10
        elif change_rate > 5:
            score -= 8

        reason = []
        if strength >= 120:
            reason.append("체결강도 양호")
        if inst > 0:
            reason.append("기관 순매수")
        if foreigner > 0:
            reason.append("외국인 순매수")
        if program > 0:
            reason.append("프로그램 순매수")
        if not reason:
            reason.append("추가 관찰 필요")

        rows.append({
            "종목코드": item["종목코드"],
            "종목명": item["종목명"],
            "점수": score,
            "등락률(%)": change_rate,
            "체결강도": strength,
            "기관순매수": inst,
            "외국인순매수": foreigner,
            "프로그램순매수": program,
            "추천사유": ", ".join(reason)
        })

    df = pd.DataFrame(rows).sort_values("점수", ascending=False).reset_index(drop=True)
    return df

if "result_df" not in st.session_state:
    st.session_state.result_df = make_sample_scores()

col1, col2 = st.columns([1, 3])

with col1:
    if st.button("추천 불러오기", use_container_width=True):
        st.session_state.result_df = make_sample_scores()

with col2:
    st.info(f"마지막 계산 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

df = st.session_state.result_df

top = df.iloc[0]
st.subheader("오늘의 1위 추천")
st.metric(label=f"{top['종목명']} ({top['종목코드']})", value=f"{top['점수']}점", delta=f"{top['등락률(%)']}%")

st.subheader("추천 종목 순위")
st.dataframe(df, use_container_width=True)
