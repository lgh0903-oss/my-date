import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 필요한 데이터만 사용
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


# 데이터 로딩
try:
    df = load_data()

except Exception as e:
    st.error("데이터를 불러오는 중 문제가 발생했습니다.")
    st.error(f"오류 내용: {e}")
    st.stop()


# 연도 추출
df["연도"] = df["날짜"].dt.year


# 연평균 기온 계산
yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

# 100년 범위 선택
min_year = yearly_temp["연도"].min()
max_year = yearly_temp["연도"].max()

# 제목
st.title("🌡️ 서울의 100년 기온 변화")
st.subheader("연평균 기온은 지난 100년 동안 어떻게 변했을까?")

st.write(
    "서울의 일별 기온 데이터를 이용하여 연평균 기온을 계산하고, "
    "시간에 따른 변화를 그래프로 나타낸 것입니다."
)


# 데이터 기간 정보
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("데이터 시작 연도", f"{min_year}년")

with col2:
    st.metric("데이터 마지막 연도", f"{max_year}년")

with col3:
    st.metric("분석한 연도 수", f"{len(yearly_temp)}년")


# 그래프
st.subheader("📈 서울 연평균 기온 변화")

chart_data = yearly_temp.set_index("연도")

st.line_chart(
    chart_data,
    y="평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)"
)


# 간단한 분석
st.subheader("🔎 데이터 살펴보기")

first_temp = yearly_temp.iloc[0]["평균기온"]
last_temp = yearly_temp.iloc[-1]["평균기온"]
change = last_temp - first_temp

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "첫해 연평균 기온",
        f"{first_temp:.1f} ℃"
    )

with col2:
    st.metric(
        "마지막 해 연평균 기온",
        f"{last_temp:.1f} ℃"
    )

with col3:
    st.metric(
        "첫해 → 마지막 해 변화",
        f"{change:+.1f} ℃"
    )


st.info(
    "※ 연평균 기온은 해당 연도의 일별 평균기온을 평균하여 계산했습니다. "
    "관측 자료의 시작·종료 연도에 따라 실제 분석 기간은 달라질 수 있습니다."
)


# 원본 데이터 확인
with st.expander("📋 연평균 기온 데이터 보기"):
    display_data = yearly_temp.copy()
    display_data["평균기온"] = display_data["평균기온"].round(2)

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


st.caption(
    "자료: 기상청 서울 기온 관측 자료(seoul.csv) | "
    "데이터 제공: GitHub modudata"
)
