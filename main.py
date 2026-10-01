import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Minion Badminton",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit 여백 제거
st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] {
        margin: 0;
        padding: 0;
        overflow: hidden;
    }

    [data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    iframe {
        display: block;
        border: none;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 배드민턴 체육관 배경
# "옆에서 바라보는 2D 게임 화면"
# ---------------------------------------------------------

html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>
    * {
        box-sizing: border-box;
    }

    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }

    body {
        background: #d7d3c9;
    }

    .game {
        position: relative;
        width: 100vw;
        height: 100vh;
        overflow: hidden;

        /* 화면 전체를 옆에서 보는 체육관 */
        background:
            linear-gradient(
                to bottom,
                #e8e5dc 0%,
                #e8e5dc 63%,
                #c78b4c 63%,
                #c78b4c 100%
            );
    }


    /* =========================================
       체육관 벽
       ========================================= */

    .wall-line {
        position: absolute;
        left: 0;
        top: 62%;
        width: 100%;
        height: 8px;
        background: #aaa69d;
    }

    .wall-panel {
        position: absolute;
        left: 0;
        top: 55%;
        width: 100%;
        height: 7%;
        background: #d3cfc5;
        border-top: 4px solid #c1bdb3;
        border-bottom: 4px solid #aaa69d;
    }


    /* =========================================
       창문
       ========================================= */

    .window {
        position: absolute;
        top: 9%;
        width: 19%;
        height: 27%;

        background: #b9d7e2;

        border: 8px solid #777b7c;
        border-radius: 4px;

        box-shadow:
            inset 0 0 25px rgba(255,255,255,0.5);
    }

    .window.left {
        left: 6%;
    }

    .window.right {
        right: 6%;
    }

    .window::before {
        content: "";
        position: absolute;
        left: 50%;
        top: 0;
        width: 7px;
        height: 100%;
        background: #777b7c;
        transform: translateX(-50%);
    }

    .window::after {
        content: "";
        position: absolute;
        left: 0;
        top: 50%;
        width: 100%;
        height: 7px;
        background: #777b7c;
        transform: translateY(-50%);
    }


    /* =========================================
       천장 조명
       ========================================= */

    .light {
        position: absolute;
        top: 5%;
        width: 16%;
        height: 22px;

        background: #faf6d8;
        border-radius: 20px;

        box-shadow:
            0 10px 25px rgba(255, 244, 170, 0.25);
    }

    .light.one {
        left: 28%;
    }

    .light.two {
        right: 28%;
    }


    /* =========================================
       체육관 바닥
       ========================================= */

    .floor {
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        height: 37%;

        background:
            repeating-linear-gradient(
                to bottom,
                rgba(120, 75, 35, 0.15) 0px,
                rgba(120, 75, 35, 0.15) 3px,
                transparent 3px,
                transparent 52px
            ),
            #c78b4c;
    }

    /* 나무 바닥의 세로 판자 */
    .floor::after {
        content: "";
        position: absolute;
        inset: 0;

        background:
            repeating-linear-gradient(
                to right,
                transparent 0px,
                transparent 220px,
                rgba(120, 75, 35, 0.12) 220px,
                rgba(120, 75, 35, 0.12) 223px
            );
    }


    /* =========================================
       배드민턴 코트 바닥선
       옆에서 보면 수평선으로 보임
       ========================================= */

    .court-line {
        position: absolute;
        left: 7%;
        width: 86%;
        height: 6px;
        background: white;
        z-index: 3;
    }

    .court-line.top {
        top: 69%;
    }

    .court-line.bottom {
        top: 91%;
    }


    /* =========================================
       중앙 네트
       핵심: 옆에서 보면 네트가 "선"처럼 보임
       ========================================= */

    .net {
        position: absolute;

        left: 50%;
        top: 37%;

        width: 5px;
        height: 54%;

        transform: translateX(-50%);

        background: #555;
        z-index: 20;

        box-shadow:
            2px 0 0 rgba(0,0,0,0.12);
    }


    /* 네트의 위쪽 테이프 */
    .net-top {
        position: absolute;

        left: 50%;
        top: 37%;

        width: 18px;
        height: 8px;

        transform: translateX(-50%);

        background: white;

        z-index: 21;
    }


    /* 네트 기둥 아래 */
    .net-base {
        position: absolute;

        left: 50%;
        top: 90%;

        width: 75px;
        height: 14px;

        transform: translateX(-50%);

        background: #555;
        border-radius: 8px;

        z-index: 19;
    }


    /* =========================================
       네트의 아주 얇은 망 느낌
       옆모습이므로 거의 선처럼 표현
       ========================================= */

    .net-shadow {
        position: absolute;

        left: calc(50% - 1px);
        top: 38%;

        width: 2px;
        height: 52%;

        background: rgba(255,255,255,0.35);

        z-index: 22;
    }


    /* =========================================
       중앙 바닥 그림자
       ========================================= */

    .net-floor-shadow {
        position: absolute;

        left: 50%;
        top: 91%;

        width: 150px;
        height: 18px;

        transform: translateX(-50%);

        background: rgba(80,45,20,0.22);
        border-radius: 50%;

        filter: blur(2px);

        z-index: 5;
    }


    /* =========================================
       장식
       ========================================= */

    .basketball-hoop {
        position: absolute;
        right: 20%;
        top: 39%;

        width: 80px;
        height: 55px;

        border: 7px solid #777;
        border-left: none;

        opacity: 0.45;
    }

    .basketball-hoop::after {
        content: "";

        position: absolute;
        right: -25px;
        top: 5px;

        width: 35px;
        height: 35px;

        border: 5px solid #777;
        border-radius: 50%;
    }


    /* =========================================
       게임 영역 표시용
       ========================================= */

    .left-side,
    .right-side {
        position: absolute;
        top: 65%;
        height: 27%;
        width: 43%;

        z-index: 10;
    }

    .left-side {
        left: 3%;
    }

    .right-side {
        right: 3%;
    }

</style>
</head>


<body>

<div class="game">

    <!-- 체육관 창문 -->
    <div class="window left"></div>
    <div class="window right"></div>

    <!-- 조명 -->
    <div class="light one"></div>
    <div class="light two"></div>

    <!-- 체육관 벽 패널 -->
    <div class="wall-panel"></div>
    <div class="wall-line"></div>

    <!-- 농구 골대 장식 -->
    <div class="basketball-hoop"></div>

    <!-- 체육관 바닥 -->
    <div class="floor"></div>

    <!-- 코트 바닥선 -->
    <div class="court-line top"></div>
    <div class="court-line bottom"></div>

    <!-- 미니언이 들어갈 영역 -->
    <div class="left-side"></div>
    <div class="right-side"></div>

    <!-- 네트 그림자 -->
    <div class="net-floor-shadow"></div>

    <!-- 중앙 네트 -->
    <div class="net"></div>
    <div class="net-shadow"></div>
    <div class="net-top"></div>
    <div class="net-base"></div>

</div>

</body>
</html>
"""


# ---------------------------------------------------------
# HTML을 실제 화면으로 렌더링
# ---------------------------------------------------------

components.html(
    html,
    height=900,
    scrolling=False
)
