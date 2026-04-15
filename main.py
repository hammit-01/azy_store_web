import streamlit as st
import pandas as pd

# =========================
# 기본 설정
# =========================
st.set_page_config(layout="wide")

# 제목
st.markdown(
    "<h1 style='font-size:3rem; padding-top: 3rem; padding-bottom: 1rem;'>📊 매장 재고장 대시보드 web</h1>",
    unsafe_allow_html=True
)

# =========================
# CSS (필터 UI)
# =========================
st.markdown("""
<style>

/* 필터 영역 */
div[data-testid="stHorizontalBlock"] {
    background-color: #f5f5f5;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 10px;
}

/* selectbox 내부 */
div[data-testid="stHorizontalBlock"] div[data-baseweb="select"] > div {
    background-color: white;
    font-size: 1rem;
}

/* 라벨 */
label[data-testid="stWidgetLabel"] {
    font-size: 2rem !important;
    font-weight: 700;
}

/* 전체 컨텐츠 영역 */
.block-container {
    max-width: 1500px;   /* 가로 길이 제한 */
    margin: 0 auto;      /* 가운데 정렬 */
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# =========================
# 데이터 로드
# =========================
df = pd.read_excel("data/상품별재고금액명세(VATPDA)1.xlsx")

# =========================
# 날짜 기준
# =========================
today = pd.Timestamp.now(tz="Asia/Seoul").normalize()

# =========================
# 데이터 전처리
# =========================

# 숫자 처리
df["Box"] = df["Box"] / 10

df["Kg"] = pd.to_numeric(
    df["Kg"].astype(str).str.replace(r"[^\d.]", "", regex=True),
    errors="coerce"
)

df["Box"] = pd.to_numeric(
    df["Box"].astype(str).str.replace(r"[^\d]", "", regex=True),
    errors="coerce"
).fillna(0).astype(int)



# 컬럼 정리
cols = [
    "상품코드", "구분", "품목명", "브랜드", "원산지", "등급",
    "재고단가", "Box", "Kg",
    "재고금액", "비  고"
]
df = df[cols]

# =========================
# 필터 UI
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    a = st.selectbox(
        "브랜드",
        ["전체"] + sorted(df["브랜드"].dropna().unique())
    )

with col2:
    b = st.selectbox(
        "품목명",
        ["전체"] + sorted(df["품목명"].dropna().unique())
    )

with col3:
    c = st.selectbox(
        "구분",
        ["전체"] + sorted(df["구분"].dropna().unique())
    )

# =========================
# 필터 적용
# =========================
filtered_df = df.copy()

if a != "전체":
    filtered_df = filtered_df[filtered_df["브랜드"] == a]

if b != "전체":
    filtered_df = filtered_df[filtered_df["품목명"] == b]

if c != "전체":
    filtered_df = filtered_df[filtered_df["구분"] == c]

# =========================
# KPI
# =========================
colA, colB, colC = st.columns(3)

colA.metric("총 재고수량", int(filtered_df["Box"].sum()))
colB.metric("총 중량", round(filtered_df["Kg"].sum(), 2))
colC.metric("업데이트 일자", today.strftime("%Y-%m-%d"))

colA, colB, colC = st.columns([1,2,1])

# =========================
# 출력
# =========================
st.markdown("<div style='max-width:1500px; margin:0 auto;'>", unsafe_allow_html=True)

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.markdown("</div>", unsafe_allow_html=True)
