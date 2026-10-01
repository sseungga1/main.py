import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Minion Badminton",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit 기본 UI 제거
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

[data-testid="stHeader"] {
    display: none !important;
}

[data-testid="stToolbar"] {
    display: none !important;
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
    display: block !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<style>

* {
    box-sizing: border-box;
    user-select: none;
}

html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #222;
    font-family: Arial, sans-serif;
}

#game {
    position: relative;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    perspective: 900px;
    background: #e8e5dc;
    cursor: crosshair;
}


/* =====================================================
   카메라가 바라보는 전체 세계
   ===================================================== */

#world {
    position: absolute;

    width: 1600px;
    height: 900px;

    left: 50%;
    top: 50%;

    transform-style: preserve-3d;

    transform:
        translate(-50%, -50%)
        translate3d(0px, 0px, 0px)
        rotateX(0deg)
        rotateY(0deg);

    transition: transform 0.03s linear;
}


/* =====================================================
   체육관 벽
   ===================================================== */

.wall {
    position: absolute;

    left: 0;
    top: 0;

    width: 1600px;
    height: 580px;

    background:
        linear-gradient(
            to bottom,
            #ebe8df 0%,
            #e5e2d8 78%,
            #d2cec3 78%,
            #d2cec3 100%
        );
}


/* 벽 패널 */
.wall-panel {
    position: absolute;

    left: 0;
    top: 500px;

    width: 1600px;
    height: 80px;

    background: #d0ccc1;

    border-top: 5px solid #b8b3a8;
    border-bottom: 5px solid #aaa69c;
}


/* =====================================================
   창문
   ===================================================== */

.window {
    position: absolute;

    top: 80px;

    width: 300px;
    height: 230px;

    background: #b8d4df;

    border: 9px solid #777b7c;

    box-shadow:
        inset 0 0 30px rgba(255,255,255,0.5);
}

.window.left {
    left: 80px;
}

.window.right {
    right: 80px;
}

.window .v {
    position: absolute;

    left: 50%;
    top: 0;

    width: 8px;
    height: 100%;

    background: #777b7c;
}

.window .h {
    position: absolute;

    left: 0;
    top: 50%;

    width: 100%;
    height: 8px;

    background: #777b7c;
}


/* =====================================================
   천장 조명
   ===================================================== */

.light {
    position: absolute;

    top: 45px;

    width: 250px;
    height: 28px;

    background: #fffbdc;

    border-radius: 20px;

    box-shadow:
        0 15px 35px rgba(255,245,170,0.35);
}

.light.one {
    left: 500px;
}

.light.two {
    right: 500px;
}


/* =====================================================
   체육관 바닥
   ===================================================== */

.floor {
    position: absolute;

    left: 0;
    top: 580px;

    width: 1600px;
    height: 320px;

    background-color: #c78b4c;

    background-image:
        repeating-linear-gradient(
            to bottom,
            rgba(100,60,25,0.15) 0px,
            rgba(100,60,25,0.15) 3px,
            transparent 3px,
            transparent 52px
        ),
        repeating-linear-gradient(
            to right,
            transparent 0px,
            transparent 220px,
            rgba(100,60,25,0.12) 220px,
            rgba(100,60,25,0.12) 223px
        );
}


/* =====================================================
   코트 라인
   ===================================================== */

.court-line {
    position: absolute;

    height: 7px;

    background: white;

    left: 80px;
    width: 1440px;
}

.court-line.one {
    top: 620px;
}

.court-line.two {
    top: 850px;
}


/* =====================================================
   네트
   ===================================================== */

.net {
    position: absolute;

    left: 800px;
    top: 365px;

    width: 6px;
    height: 490px;

    background: #555;

    z-index: 30;
}

.net-top {
    position: absolute;

    left: 790px;
    top: 355px;

    width: 26px;
    height: 10px;

    background: white;

    z-index: 31;
}

.net-base {
    position: absolute;

    left: 760px;
    top: 850px;

    width: 80px;
    height: 16px;

    background: #444;

    border-radius: 10px;

    z-index: 30;
}


/* =====================================================
   Jerry 플레이어
   ===================================================== */

.jerry {
    position: absolute;

    left: 520px;
    top: 500px;

    width: 220px;
    height: 350px;

    z-index: 50;

    transform-origin: bottom center;

    filter: drop-shadow(
        0 10px 8px rgba(0,0,0,0.25)
    );
}


/* Jerry 몸 */
.jerry-body {
    position: absolute;

    left: 35px;
    bottom: 0;

    width: 150px;
    height: 220px;

    background: #f0d72d;

    border-radius:
        75px 75px
        45px 45px;

    border: 5px solid #333;
}


/* Jerry 얼굴 */
.jerry-head {
    position: absolute;

    left: 10px;
    top: 0;

    width: 200px;
    height: 180px;

    background: #f1d82e;

    border-radius: 50%;

    border: 5px solid #333;

    z-index: 5;
}


/* 고글 */
.goggle {
    position: absolute;

    left: 35px;
    top: 43px;

    width: 130px;
    height: 65px;

    border-radius: 40px;

    background: #777;

    border: 7px solid #333;

    z-index: 10;
}

.goggle-glass {
    position: absolute;

    left: 8px;
    top: 8px;

    width: 100px;
    height: 43px;

    border-radius: 30px;

    background: #dbeaf0;

    border: 4px solid #222;
}


/* 눈 */
.eye {
    position: absolute;

    left: 48px;
    top: 48px;

    width: 40px;
    height: 40px;

    background: white;

    border-radius: 50%;

    z-index: 20;
}

.pupil {
    position: absolute;

    left: 13px;
    top: 10px;

    width: 17px;
    height: 20px;

    background: #222;

    border-radius: 50%;
}


/* 입 */
.jerry-mouth {
    position: absolute;

    left: 70px;
    top: 120px;

    width: 65px;
    height: 28px;

    border-bottom: 6px solid #333;

    border-radius: 50%;

    z-index: 20;
}


/* 멜빵 */
.jerry-overall {
    position: absolute;

    left: 38px;
    bottom: 0;

    width: 145px;
    height: 110px;

    background: #315da8;

    border-radius:
        20px 20px
        35px 35px;

    border: 5px solid #333;

    z-index: 8;
}


/* 다리 */
.leg {
    position: absolute;

    bottom: -45px;

    width: 48px;
    height: 65px;

    background: #f0d72d;

    border: 5px solid #333;

    border-radius: 20px;
}

.leg.left {
    left: 45px;
}

.leg.right {
    right: 45px;
}


/* 신발 */
.shoe {
    position: absolute;

    bottom: -52px;

    width: 75px;
    height: 38px;

    background: #333;

    border-radius: 40px;
}

.shoe.left {
    left: 18px;
}

.shoe.right {
    right: 18px;
}


/* =====================================================
   Gru
   ===================================================== */

.gru {
    position: absolute;

    left: 1050px;
    top: 430px;

    width: 190px;
    height: 420px;

    z-index: 40;

    filter: drop-shadow(
        0 10px 8px rgba(0,0,0,0.25)
    );
}


/* Gru 머리 */
.gru-head {
    position: absolute;

    left: 35px;
    top: 0;

    width: 125px;
    height: 150px;

    background: #e5d0b5;

    border-radius:
        55% 55%
        45% 45%;

    border: 5px solid #333;
}


/* Gru 코 */
.gru-nose {
    position: absolute;

    left: -18px;
    top: 70px;

    width: 55px;
    height: 38px;

    background: #e5d0b5;

    border: 5px solid #333;

    border-radius: 60% 30% 30% 60%;
}


/* Gru 눈 */
.gru-eye {
    position: absolute;

    top: 55px;

    width: 18px;
    height: 18px;

    background: #222;

    border-radius: 50%;
}

.gru-eye.left {
    left: 42px;
}

.gru-eye.right {
    left: 78px;
}


/* Gru 몸 */
.gru-body {
    position: absolute;

    left: 15px;
    top: 130px;

    width: 160px;
    height: 270px;

    background: #333;

    border-radius:
        35px 35px
        15px 15px;

    border: 5px solid #222;
}


/* Gru 스카프 */
.scarf {
    position: absolute;

    left: 22px;
    top: 145px;

    width: 145px;
    height: 25px;

    background: #444;

    border: 3px solid #222;

    z-index: 10;
}


/* Gru 다리 */
.gru-leg {
    position: absolute;

    bottom: 0;

    width: 55px;
    height: 80px;

    background: #222;

    border-radius: 20px;
}

.gru-leg.left {
    left: 25px;
}

.gru-leg.right {
    right: 25px;
}


/* =====================================================
   화면 안내
   ===================================================== */

#message {
    position: fixed;

    left: 50%;
    top: 8%;

    transform: translateX(-50%);

    padding: 12px 24px;

    background: rgba(0,0,0,0.65);

    color: white;

    border-radius: 30px;

    font-size: 17px;

    z-index: 1000;

    pointer-events: none;

    transition: opacity 0.5s;
}


/* 조준점 */
#crosshair {
    position: fixed;

    left: 50%;
    top: 50%;

    transform: translate(-50%, -50%);

    width: 14px;
    height: 14px;

    z-index: 1000;

    pointer-events: none;
}

#crosshair::before,
#crosshair::after {
    content: "";

    position: absolute;

    background: rgba(255,255,255,0.8);
}

#crosshair::before {
    left: 6px;
    top: 0;

    width: 2px;
    height: 14px;
}

#crosshair::after {
    left: 0;
    top: 6px;

    width: 14px;
    height: 2px;
}


/* 클릭 안내 */
#click-screen {
    position: fixed;

    inset: 0;

    z-index: 900;

    cursor: crosshair;
}

</style>
</head>


<body>

<div id="game">

    <div id="world">

        <!-- 체육관 -->
        <div class="wall"></div>

        <div class="wall-panel"></div>

        <!-- 창문 -->
        <div class="window left">
            <div class="v"></div>
            <div class="h"></div>
        </div>

        <div class="window right">
            <div class="v"></div>
            <div class="h"></div>
        </div>

        <!-- 조명 -->
        <div class="light one"></div>
        <div class="light two"></div>

        <!-- 바닥 -->
        <div class="floor"></div>

        <!-- 코트 라인 -->
        <div class="court-line one"></div>
        <div class="court-line two"></div>


        <!-- ===============================
             네트
             =============================== -->

        <div class="net"></div>
        <div class="net-top"></div>
        <div class="net-base"></div>


        <!-- ===============================
             Jerry
             =============================== -->

        <div class="jerry">

            <div class="jerry-head">

                <div class="goggle">
                    <div class="goggle-glass"></div>
                </div>

                <div class="eye">
                    <div class="pupil"></div>
                </div>

                <div class="jerry-mouth"></div>

            </div>

            <div class="jerry-body"></div>

            <div class="jerry-overall"></div>

            <div class="leg left"></div>
            <div class="leg right"></div>

            <div class="shoe left"></div>
            <div class="shoe right"></div>

        </div>


        <!-- ===============================
             Gru
             =============================== -->

        <div class="gru">

            <div class="gru-head">

                <div class="gru-nose"></div>

                <div class="gru-eye left"></div>
                <div class="gru-eye right"></div>

            </div>

            <div class="gru-body"></div>

            <div class="scarf"></div>

            <div class="gru-leg left"></div>
            <div class="gru-leg right"></div>

        </div>

    </div>

</div>


<!-- 안내 -->
<div id="message">
    화면을 클릭한 뒤 마우스를 움직여 보세요
</div>

<!-- 조준점 -->
<div id="crosshair"></div>

<div id="click-screen"></div>


<script>

const game = document.getElementById("game");
const world = document.getElementById("world");
const clickScreen = document.getElementById("click-screen");
const message = document.getElementById("message");


// =====================================================
// 카메라 변수
// =====================================================

let cameraX = 0;
let cameraY = 0;

let targetX = 0;
let targetY = 0;


// 마우스 감도
const sensitivity = 0.08;


// 움직일 수 있는 범위
const maxX = 120;
const maxY = 75;


// =====================================================
// 클릭하면 마우스 포인터 고정
// =====================================================

clickScreen.addEventListener("click", function() {

    clickScreen.requestPointerLock();

});


// =====================================================
// 마우스 움직임
// =====================================================

document.addEventListener("mousemove", function(event) {

    if (document.pointerLockElement !== clickScreen) {
        return;
    }


    targetX += event.movementX * sensitivity;
    targetY += event.movementY * sensitivity;


    // 좌우 제한
    targetX = Math.max(
        -maxX,
        Math.min(maxX, targetX)
    );


    // 위아래 제한
    targetY += event.movementY * sensitivity;

    targetY = Math.max(
        -maxY,
        Math.min(maxY, targetY)
    );

});


// =====================================================
// 부드러운 카메라
// =====================================================

function updateCamera() {

    cameraX += (targetX - cameraX) * 0.12;
    cameraY += (targetY - cameraY) * 0.12;


    world.style.transform =
        `
        translate(-50%, -50%)
        translate3d(
            ${-cameraX}px,
            ${-cameraY}px,
            0px
        )
        `;


    requestAnimationFrame(updateCamera);
}

updateCamera();


// =====================================================
// 마우스 고정 상태 변화
// =====================================================

document.addEventListener(
    "pointerlockchange",
    function() {

        if (
            document.pointerLockElement === clickScreen
        ) {

            message.style.opacity = "0";

        } else {

            message.style.opacity = "1";

        }

    }
);

</script>

</body>
</html>
"""


components.html(
    html,
    height=900,
    scrolling=False
)
