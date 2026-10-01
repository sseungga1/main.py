import streamlit as st

st.set_page_config(
    page_title="Minion Badminton",
    page_icon="🏸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit 기본 여백 제거
st.markdown("""
<style>
    .stApp {
        background: #222222;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 배드민턴 체육관 배경
# ---------------------------------------------------------

court_svg = """
<svg
    width="100%"
    height="100%"
    viewBox="0 0 1600 900"
    preserveAspectRatio="xMidYMid slice"
    xmlns="http://www.w3.org/2000/svg"
>

    <!-- ========================= -->
    <!-- 체육관 전체 벽 -->
    <!-- ========================= -->

    <rect x="0" y="0" width="1600" height="900" fill="#e8e5dc"/>

    <!-- 위쪽 벽 -->
    <rect x="0" y="0" width="1600" height="570" fill="#e9e6dd"/>

    <!-- 벽의 가로 패널 -->
    <rect x="0" y="500" width="1600" height="12" fill="#d2cec3"/>
    <rect x="0" y="512" width="1600" height="8" fill="#f5f2eb"/>

    <!-- ========================= -->
    <!-- 체육관 창문 -->
    <!-- ========================= -->

    <!-- 왼쪽 창문 -->
    <rect x="70" y="80" width="280" height="250"
          rx="4" fill="#a9c9d9" stroke="#777b7b" stroke-width="10"/>

    <line x1="210" y1="80" x2="210" y2="330"
          stroke="#777b7b" stroke-width="8"/>

    <line x1="70" y1="205" x2="350" y2="205"
          stroke="#777b7b" stroke-width="8"/>

    <!-- 창문 빛 -->
    <rect x="82" y="92" width="116" height="101" fill="#dceef2" opacity="0.65"/>
    <rect x="222" y="92" width="116" height="101" fill="#dceef2" opacity="0.65"/>
    <rect x="82" y="217" width="116" height="101" fill="#cce6ed" opacity="0.55"/>
    <rect x="222" y="217" width="116" height="101" fill="#cce6ed" opacity="0.55"/>


    <!-- 오른쪽 창문 -->
    <rect x="1250" y="80" width="280" height="250"
          rx="4" fill="#a9c9d9" stroke="#777b7b" stroke-width="10"/>

    <line x1="1390" y1="80" x2="1390" y2="330"
          stroke="#777b7b" stroke-width="8"/>

    <line x1="1250" y1="205" x2="1530" y2="205"
          stroke="#777b7b" stroke-width="8"/>

    <rect x="1262" y="92" width="116" height="101" fill="#dceef2" opacity="0.65"/>
    <rect x="1402" y="92" width="116" height="101" fill="#dceef2" opacity="0.65"/>
    <rect x="1262" y="217" width="116" height="101" fill="#cce6ed" opacity="0.55"/>
    <rect x="1402" y="217" width="116" height="101" fill="#cce6ed" opacity="0.55"/>


    <!-- ========================= -->
    <!-- 체육관 조명 -->
    <!-- ========================= -->

    <rect x="530" y="45" width="540" height="18"
          rx="9" fill="#777777"/>

    <rect x="610" y="62" width="150" height="28"
          rx="14" fill="#f7f4dd"/>

    <rect x="840" y="62" width="150" height="28"
          rx="14" fill="#f7f4dd"/>

    <ellipse cx="685" cy="105" rx="100" ry="20"
             fill="#fff9d5" opacity="0.22"/>

    <ellipse cx="915" cy="105" rx="100" ry="20"
             fill="#fff9d5" opacity="0.22"/>


    <!-- ========================= -->
    <!-- 체육관 아래쪽 벽 -->
    <!-- ========================= -->

    <rect x="0" y="520" width="1600" height="65"
          fill="#d9d5cb"/>

    <!-- 벽 보호 패널 -->
    <rect x="0" y="535" width="1600" height="35"
          fill="#c6c1b6"/>


    <!-- ========================= -->
    <!-- 체육관 바닥 -->
    <!-- ========================= -->

    <rect x="0" y="585" width="1600" height="315"
          fill="#c68a4b"/>

    <!-- 나무 바닥 줄무늬 -->
    <line x1="0" y1="635" x2="1600" y2="635"
          stroke="#a86f38" stroke-width="4" opacity="0.55"/>

    <line x1="0" y1="690" x2="1600" y2="690"
          stroke="#a86f38" stroke-width="4" opacity="0.55"/>

    <line x1="0" y1="745" x2="1600" y2="745"
          stroke="#a86f38" stroke-width="4" opacity="0.55"/>

    <line x1="0" y1="800" x2="1600" y2="800"
          stroke="#a86f38" stroke-width="4" opacity="0.55"/>

    <line x1="0" y1="855" x2="1600" y2="855"
          stroke="#a86f38" stroke-width="4" opacity="0.55"/>


    <!-- 세로 나무판 느낌 -->
    <line x1="150" y1="585" x2="150" y2="900"
          stroke="#b8793f" stroke-width="3" opacity="0.35"/>

    <line x1="420" y1="585" x2="420" y2="900"
          stroke="#b8793f" stroke-width="3" opacity="0.35"/>

    <line x1="700" y1="585" x2="700" y2="900"
          stroke="#b8793f" stroke-width="3" opacity="0.35"/>

    <line x1="980" y1="585" x2="980" y2="900"
          stroke="#b8793f" stroke-width="3" opacity="0.35"/>

    <line x1="1250" y1="585" x2="1250" y2="900"
          stroke="#b8793f" stroke-width="3" opacity="0.35"/>

    <line x1="1480" y1="585" x2="1480" y2="900"
          stroke="#b8793f" stroke-width="3" opacity="0.35"/>


    <!-- ========================= -->
    <!-- 배드민턴 코트 라인 -->
    <!-- ========================= -->

    <!-- 뒤쪽 코트 라인 -->
    <line x1="170" y1="590" x2="1430" y2="590"
          stroke="#ffffff" stroke-width="7" opacity="0.9"/>

    <!-- 앞쪽 코트 라인 -->
    <line x1="170" y1="855" x2="1430" y2="855"
          stroke="#ffffff" stroke-width="7" opacity="0.9"/>

    <!-- 가운데 코트 라인 -->
    <line x1="800" y1="590" x2="800" y2="855"
          stroke="#ffffff" stroke-width="6" opacity="0.8"/>


    <!-- ========================= -->
    <!-- 배드민턴 네트 그림자 -->
    <!-- ========================= -->

    <ellipse cx="800" cy="865"
             rx="180" ry="18"
             fill="#70451f"
             opacity="0.28"/>


    <!-- ========================= -->
    <!-- 네트 기둥 -->
    <!-- ========================= -->

    <rect x="620" y="350" width="14" height="505"
          rx="7" fill="#555555"/>

    <rect x="966" y="350" width="14" height="505"
          rx="7" fill="#555555"/>


    <!-- 기둥 아래 -->
    <rect x="600" y="850" width="55" height="16"
          rx="8" fill="#444444"/>

    <rect x="945" y="850" width="55" height="16"
          rx="8" fill="#444444"/>


    <!-- ========================= -->
    <!-- 네트 -->
    <!-- ========================= -->

    <rect x="627" y="360"
          width="340"
          height="260"
          fill="#303030"
          opacity="0.25"/>

    <!-- 네트 테두리 -->
    <rect x="625" y="350"
          width="342"
          height="270"
          fill="none"
          stroke="#eeeeee"
          stroke-width="7"/>


    <!-- 네트 가로줄 -->
    <line x1="630" y1="390" x2="962" y2="390"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="630" y1="430" x2="962" y2="430"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="630" y1="470" x2="962" y2="470"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="630" y1="510" x2="962" y2="510"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="630" y1="550" x2="962" y2="550"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="630" y1="590" x2="962" y2="590"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>


    <!-- 네트 세로줄 -->
    <line x1="670" y1="355" x2="670" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="710" y1="355" x2="710" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="750" y1="355" x2="750" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="790" y1="355" x2="790" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="830" y1="355" x2="830" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="870" y1="355" x2="870" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="910" y1="355" x2="910" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>

    <line x1="950" y1="355" x2="950" y2="615"
          stroke="#eeeeee" stroke-width="2" opacity="0.8"/>


    <!-- ========================= -->
    <!-- 네트 위쪽 테이프 -->
    <!-- ========================= -->

    <rect x="620" y="345"
          width="360"
          height="16"
          rx="5"
          fill="#ffffff"/>


    <!-- ========================= -->
    <!-- 작은 체육관 장식 -->
    <!-- ========================= -->

    <!-- 벽에 붙은 배드민턴 라켓 보관함 -->
    <rect x="400" y="350"
          width="100"
          height="90"
          rx="8"
          fill="#b8b3a8"/>

    <rect x="1100" y="350"
          width="100"
          height="90"
          rx="8"
          fill="#b8b3a8"/>

    <!-- 체육관 안전 표시 -->
    <rect x="20" y="540"
          width="80" height="20"
          rx="4"
          fill="#f0d66b"/>

    <rect x="1500" y="540"
          width="80" height="20"
          rx="4"
          fill="#f0d66b"/>

</svg>
"""


# ---------------------------------------------------------
# 화면 출력
# ---------------------------------------------------------

st.markdown(
    f"""
    <div style="
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        margin: 0;
        padding: 0;
        position: relative;
        left: 50%;
        transform: translateX(-50%);
    ">
        {court_svg}
    </div>
    """,
    unsafe_allow_html=True
)
