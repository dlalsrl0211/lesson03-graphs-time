import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

st.title("영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치 일별 박스오피스 데이터를 시간의 흐름에 따라 살펴봅니다.")

# -------------------------------------------------------------------
# 데이터 불러오기
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜: 하이픈 없는 8자리 숫자(예: 20250101) → 실제 날짜형
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str).str.replace(r"\.0$", "", regex=True),
        format="%Y%m%d",
        errors="coerce",
    )

    # 숫자형 열 정리
    numeric_columns = ["순위", "영화코드", "일관객", "누적관객", "스크린수", "상영횟수"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.dropna(subset=["날짜", "영화명", "일관객"]).sort_values("날짜")


df = load_data()

# -------------------------------------------------------------------
# 그래프 1. 영화별 일관객 변화
# -------------------------------------------------------------------
st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())
selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
    key="movie_select",
)

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"〈{selected_movie}〉 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객",
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,",
    },
)

fig.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>관객수: %{y:,}명<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객",
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.caption("선택한 영화의 일별 관객수가 시간에 따라 어떻게 변했는지 확인할 수 있습니다.")

# -------------------------------------------------------------------
# 그래프 2. 앞으로 추가할 영역
# -------------------------------------------------------------------
st.divider()
st.header("그래프 2")
st.info("앞으로 추가할 그래프 영역입니다.")

# -------------------------------------------------------------------
# 그래프 3. 앞으로 추가할 영역
# -------------------------------------------------------------------
st.divider()
st.header("그래프 3")
st.info("앞으로 추가할 그래프 영역입니다.")
