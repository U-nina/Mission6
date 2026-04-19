import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. 한글 폰트 설정 (배포 환경에 따라 달라질 수 있으나 기본 설정 시도)
plt.rcParams['font.family'] = 'NanumGothic'  # 리눅스 서버용 폰트 권장
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="산점도 분석 앱", layout="wide")

st.title("📊 산점도 데이터 분석 시각화")
st.markdown("X축, Y축과 색상 기준을 선택하여 상관관계를 분석하세요.")


# 데이터 불러오기
@st.cache_data
def load_data():
    file_path = '6주차_실습4.csv'
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return None


import os

df = load_data()

if df is not None:
    # 사이드바 설정 영역
    st.sidebar.header("설정 옵션")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    all_cols = df.columns.tolist()

    x_col = st.sidebar.selectbox("X축 선택 (숫자)", numeric_cols, index=0)
    y_col = st.sidebar.selectbox("Y축 선택 (숫자)", numeric_cols, index=1)
    hue_col = st.sidebar.selectbox("색상 구분 기준", ["없음"] + all_cols, index=1)

    show_reg = st.sidebar.checkbox("추세선(회귀선) 표시", value=False)

    # 그래프 그리기
    fig, ax = plt.subplots(figsize=(10, 6))

    current_hue = None if hue_col == "없음" else hue_col

    try:
        if show_reg:
            sns.regplot(data=df, x=x_col, y=y_col, ax=ax, scatter=False, color='red')

        sns.scatterplot(data=df, x=x_col, y=y_col, hue=current_hue, ax=ax)

        ax.set_title(f"{x_col} vs {y_col} 상관관계 분석")
        st.pyplot(fig)

        # 데이터 요약 정보 보여주기
        st.subheader("📋 선택된 데이터 요약")
        st.write(df[[x_col, y_col] + ([current_hue] if current_hue else [])].head())

    except Exception as e:
        st.error(f"그래프를 생성하는 중 오류가 발생했습니다: {e}")
else:
    st.error("CSV 파일을 찾을 수 없습니다. '6주차_실습4.csv' 파일이 같은 경로에 있는지 확인하세요.")