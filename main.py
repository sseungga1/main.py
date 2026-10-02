import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# Streamlit 설정
# =========================================================

st.set_page_config(
    page_title="Minion Badminton",
    page_icon="🏸",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# Streamlit 기본 여백 제거
# =========================================================

st.markdown("""
<style>

html,
body {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

[data-testid="stAppViewContainer"] {
    margin: 0 !important;
    padding: 0 !important;
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


# =========================================================
# 게임 화면
# =========================================================

html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">


<style>

/* =====================================================
   기본
   ===================================================== */

* {
    box-sizing: border-box;
}

html,
body {

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: #222;

}

#game {

    position: fixed;

    left: 0;
    top: 0;

    width: 100vw;
    height: 100vh;

    overflow: hidden;

    background: #222;

    cursor: default;

}


/* =====================================================
   Canvas
   ===================================================== */

canvas {

    display: block;

    width: 100%;
    height: 100%;

}


/* =====================================================
   중앙 조준점
   ===================================================== */

#crosshair {

    position: fixed;

    left: 50%;
    top: 50%;

    width: 18px;
    height: 18px;

    transform:
        translate(-50%, -50%);

    pointer-events: none;

    z-index: 20;

}


#crosshair::before {

    content: "";

    position: absolute;

    left: 8px;
    top: 0;

    width: 2px;
    height: 18px;

    background:
        rgba(255,255,255,0.8);

}


#crosshair::after {

    content: "";

    position: absolute;

    left: 0;
    top: 8px;

    width: 18px;
    height: 2px;

    background:
        rgba(255,255,255,0.8);

}


/* =====================================================
   사용 안내
   ===================================================== */

#message {

    position: fixed;

    left: 50%;
    top: 6%;

    transform:
        translateX(-50%);

    padding:
        11px 22px;

    background:
        rgba(0,0,0,0.55);

    color: white;

    border-radius: 25px;

    font-family:
        Arial,
        sans-serif;

    font-size: 16px;

    z-index: 30;

    pointer-events: none;

    opacity: 1;

    transition:
        opacity 0.5s;

}

</style>

</head>


<body>


<div id="game">

    <canvas id="canvas"></canvas>

</div>


<div id="crosshair"></div>


<div id="message">
    마우스를 움직여 시점을 바꿔보세요
</div>


<script>


// =====================================================
// Canvas
// =====================================================

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");


const game =
    document.getElementById("game");

const message =
    document.getElementById("message");


let width = 0;
let height = 0;

let centerX = 0;
let centerY = 0;


function resize() {

    const dpr =
        window.devicePixelRatio || 1;

    width =
        window.innerWidth;

    height =
        window.innerHeight;


    canvas.width =
        width * dpr;

    canvas.height =
        height * dpr;


    canvas.style.width =
        width + "px";

    canvas.style.height =
        height + "px";


    ctx.setTransform(
        dpr,
        0,
        0,
        dpr,
        0,
        0
    );


    centerX =
        width / 2;

    centerY =
        height / 2;

}


window.addEventListener(
    "resize",
    resize
);

resize();


// =====================================================
// 카메라
// =====================================================

const camera = {

    x: 0,

    y: 1.7,
    
    z: 1.4,

    yaw: 0,

    pitch: 0

};


// =====================================================
// 목표 카메라
// =====================================================

let targetYaw = 0;

let targetPitch = 0;


// =====================================================
// 마우스 위치
// =====================================================

let mouseX =
    centerX;

let mouseY =
    centerY;


// =====================================================
// 최대 시야각
//
// 좌우 약 ±80도
// 위아래 약 ±55도
// =====================================================

const MAX_YAW =
    80 * Math.PI / 180;

const MAX_PITCH =
    55 * Math.PI / 180;


// =====================================================
// 마우스 움직임
//
// 클릭하지 않아도 바로 작동
// =====================================================

game.addEventListener(
    "mousemove",
    function(event) {

        mouseX =
            event.clientX;

        mouseY =
            event.clientY;


        // -----------------------------------------
        // 화면 중앙 기준 위치
        // -1 ~ +1
        // -----------------------------------------

        let horizontal =
            (mouseX - centerX)
            / centerX;


        let vertical =
            (mouseY - centerY)
            / centerY;


        // -----------------------------------------
        // 범위를 제한
        // -----------------------------------------

        horizontal =
            Math.max(
                -1,
                Math.min(
                    1,
                    horizontal
                )
            );


        vertical =
            Math.max(
                -1,
                Math.min(
                    1,
                    vertical
                )
            );


        // -----------------------------------------
        // 좌우 시선
        // -----------------------------------------

        targetYaw =
            -horizontal * MAX_YAW;


        // -----------------------------------------
        // 위아래 시선
        //
        // 마우스가 위에 있을수록
        // 카메라는 위를 바라봄
        // -----------------------------------------

        targetPitch =
            vertical * MAX_PITCH;


        // -----------------------------------------
        // 안내문 조금 후 사라짐
        // -----------------------------------------

        message.style.opacity = "0";

    }
);


// =====================================================
// 마우스가 게임 화면에 들어왔을 때
// =====================================================

game.addEventListener(
    "mouseenter",
    function() {

        message.style.opacity = "1";

        setTimeout(
            function() {

                message.style.opacity = "0";

            },
            1500
        );

    }
);


// =====================================================
// 3D → 2D 투영
// =====================================================

const FOV =
    75;


function project(point) {


    // -----------------------------------------
    // 카메라 기준 좌표
    // -----------------------------------------

    let x =
        point.x - camera.x;

    let y =
        point.y - camera.y;

    let z =
        point.z - camera.z;


    // -----------------------------------------
    // 좌우 회전
    // -----------------------------------------

    const cosY =
        Math.cos(-camera.yaw);

    const sinY =
        Math.sin(-camera.yaw);


    const rotatedX =
        x * cosY -
        z * sinY;


    const rotatedZ =
        x * sinY +
        z * cosY;


    // -----------------------------------------
    // 위아래 회전
    // -----------------------------------------

    const cosP =
        Math.cos(-camera.pitch);

    const sinP =
        Math.sin(-camera.pitch);


    const rotatedY =
        y * cosP -
        rotatedZ * sinP;


    const finalZ =
        y * sinP +
        rotatedZ * cosP;


    // 카메라 뒤쪽

    if (finalZ <= 0.05) {

        return null;

    }


    // -----------------------------------------
    // 원근
    // -----------------------------------------

    const focal =
        (width / 2) /
        Math.tan(
            (FOV * Math.PI / 180) / 2
        );


    const screenX =
        centerX +
        (rotatedX / finalZ)
        * focal;


    const screenY =
        centerY -
        (rotatedY / finalZ)
        * focal;


    return {

        x: screenX,

        y: screenY,

        depth: finalZ

    };

}


// =====================================================
// 3D 사각형
// =====================================================

function drawQuad(
    points,
    fill,
    stroke = null,
    lineWidth = 1
) {


    const projected =
        points.map(project);


    if (
        projected.some(
            p => p === null
        )
    ) {

        return;

    }


    ctx.beginPath();


    ctx.moveTo(
        projected[0].x,
        projected[0].y
    );


    for (
        let i = 1;
        i < projected.length;
        i++
    ) {

        ctx.lineTo(
            projected[i].x,
            projected[i].y
        );

    }


    ctx.closePath();


    ctx.fillStyle =
        fill;

    ctx.fill();


    if (stroke) {

        ctx.strokeStyle =
            stroke;

        ctx.lineWidth =
            lineWidth;

        ctx.stroke();

    }

}


// =====================================================
// 3D 선
// =====================================================

function drawLine(
    a,
    b,
    color,
    lineWidth = 2
) {
    const p1 =
        project(a);

    const p2 =
        project(b);


    if (!p1 || !p2) {

        return;

    }


    ctx.beginPath();


    ctx.moveTo(
        p1.x,
        p1.y
    );


    ctx.lineTo(
        p2.x,
        p2.y
    );


    ctx.strokeStyle =
        color;

    ctx.lineWidth =
        lineWidth;

    ctx.stroke();

}


// =====================================================
// 체육관
// =====================================================

const COURT_WIDTH = 6.10;
const COURT_LENGTH = 13.40;

// 체육관 자체는 코트보다 넓게 설정
const GYM_WIDTH = 12;
const GYM_LENGTH = 20;

const WALL_HEIGHT = 8;

// 코트 중앙 = 13.40 / 2
const NET_Z = COURT_LENGTH / 2;


function drawGym() {


    // -----------------------------------------
    // 뒤쪽 벽
    // -----------------------------------------

    drawQuad(

        [

            {
                x: -GYM_WIDTH / 2,
                y: 0,
                z: GYM_LENGTH
            },

            {
                x: GYM_WIDTH / 2,
                y: 0,
                z: GYM_LENGTH
            },

            {
                x: GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: GYM_LENGTH
            },

            {
                x: -GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: GYM_LENGTH
            }

        ],

        "#e6e3da"

    );


    // -----------------------------------------
    // 왼쪽 벽
    // -----------------------------------------

    drawQuad(

        [

            {
                x: -GYM_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: -GYM_WIDTH / 2,
                y: 0,
                z: GYM_LENGTH
            },

            {
                x: -GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: GYM_LENGTH
            },

            {
                x: -GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            }

        ],

        "#dcd8ce"

    );


    // -----------------------------------------
    // 오른쪽 벽
    // -----------------------------------------

    drawQuad(

        [

            {
                x: GYM_WIDTH / 2,
                y: 0,
                z: GYM_LENGTH
            },

            {
                x: GYM_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            },

            {
                x: GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: GYM_LENGTH
            }

        ],

        "#d7d3c9"

    );


    // -----------------------------------------
    // 천장
    // -----------------------------------------

    drawQuad(

        [

            {
                x: -GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            },

            {
                x: GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            },

            {
                x: GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: GYM_LENGTH
            },

            {
                x: -GYM_WIDTH / 2,
                y: WALL_HEIGHT,
                z: GYM_LENGTH
            }

        ],

        "#d3d0c8"

    );


    // -----------------------------------------
    // 바닥
    // -----------------------------------------

    drawQuad(

        [

            {
                x: -GYM_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: GYM_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: GYM_WIDTH / 2,
                y: 0,
                z: GYM_LENGTH
            },

            {
                x: -GYM_WIDTH / 2,
                y: 0,
                z: GYM_LENGTH
            }

        ],

        "#c18447"

    );

}


// =====================================================
// 체육관 바닥 나무 무늬
// =====================================================

function drawFloor() {


    // =====================================================
    // 실제 배드민턴 코트 규격
    // =====================================================
    //
    // 전체 복식 코트:
    // 폭 6.10m
    // 길이 13.40m
    //
    // 단식 사이드라인:
    // 복식 사이드라인에서 좌우 각각 0.46m 안쪽
    //
    // 짧은 서비스 라인:
    // 네트에서 각 코트 방향으로 1.98m
    //
    // 복식 롱 서비스 라인:
    // 뒤쪽 경계선에서 0.76m 안쪽
    //
    // 중앙선:
    // 짧은 서비스 라인부터 뒤쪽 경계선까지
    // =====================================================


    const white =
        "rgba(255,255,255,0.95)";


    const doublesHalfWidth =
        COURT_WIDTH / 2;       // 3.05m


    const singlesHalfWidth =
        5.18 / 2;              // 2.59m


    const halfLength =
        COURT_LENGTH / 2;      // 6.70m


    const shortServiceOffset =
        1.98;


    const shortServiceNear =
        halfLength - shortServiceOffset;


    const shortServiceFar =
        halfLength + shortServiceOffset;


    const doublesLongServiceNear =
        0.76;


    const doublesLongServiceFar =
        COURT_LENGTH - 0.76;


    const lineY =
        0.025;


    // =====================================================
    // 바닥 나무 무늬
    // =====================================================

    // 가로 나무판
    for (
        let z = 1;
        z < GYM_LENGTH;
        z += 1
    ) {

        drawLine(

            {
                x: -GYM_WIDTH / 2,
                y: 0.01,
                z: z
            },

            {
                x: GYM_WIDTH / 2,
                y: 0.01,
                z: z
            },
                        "rgba(95,55,20,0.20)",

            1

        );

    }


    // 세로 나무판
    for (
        let x = -GYM_WIDTH / 2;
        x <= GYM_WIDTH / 2;
        x += 1
    ) {

        drawLine(

            {
                x: x,
                y: 0.015,
                z: 0
            },

            {
                x: x,
                y: 0.015,
                z: GYM_LENGTH
            },

            "rgba(95,55,20,0.14)",

            1

        );

    }


    // =====================================================
    // ① 복식 바깥 사이드라인
    // =====================================================

    drawLine(

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: 0
        },

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: COURT_LENGTH
        },

        white,

        3

    );


    drawLine(

        {
            x: doublesHalfWidth,
            y: lineY,
            z: 0
        },

        {
            x: doublesHalfWidth,
            y: lineY,
            z: COURT_LENGTH
        },

        white,

        3

    );


    // =====================================================
    // ② 단식 안쪽 사이드라인
    // =====================================================

    drawLine(

        {
            x: -singlesHalfWidth,
            y: lineY,
            z: 0
        },

        {
            x: -singlesHalfWidth,
            y: lineY,
            z: COURT_LENGTH
        },

        white,

        2.5

    );


    drawLine(

        {
            x: singlesHalfWidth,
            y: lineY,
            z: 0
        },

        {
            x: singlesHalfWidth,
            y: lineY,
            z: COURT_LENGTH
        },

        white,

        2.5

    );


    // =====================================================
    // ③ 앞쪽 / 뒤쪽 베이스라인
    // =====================================================

    drawLine(

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: 0
        },

        {
            x: doublesHalfWidth,
            y: lineY,
            z: 0
        },

        white,

        3

    );


    drawLine(

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: COURT_LENGTH
        },

        {
            x: doublesHalfWidth,
            y: lineY,
            z: COURT_LENGTH
        },

        white,

        3

    );


    // =====================================================
    // ④ 짧은 서비스 라인
    // 네트에서 양쪽으로 1.98m
    // =====================================================

    drawLine(

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: shortServiceNear
        },

        {
            x: doublesHalfWidth,
            y: lineY,
            z: shortServiceNear
        },

        white,

        2.5

    );


    drawLine(

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: shortServiceFar
        },

        {
            x: doublesHalfWidth,
            y: lineY,
            z: shortServiceFar
        },

        white,

        2.5

    );


    // =====================================================
    // ⑤ 복식 롱 서비스 라인
    // 뒤쪽 경계선에서 0.76m 안쪽
    // =====================================================

    drawLine(

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: doublesLongServiceNear
        },

        {
            x: doublesHalfWidth,
            y: lineY,
            z: doublesLongServiceNear
        },

        white,

        2.5

    );


    drawLine(

        {
            x: -doublesHalfWidth,
            y: lineY,
            z: doublesLongServiceFar
        },

        {
            x: doublesHalfWidth,
            y: lineY,
            z: doublesLongServiceFar
        },

        white,

        2.5

    );


    // =====================================================
    // ⑥ 중앙선
    // 짧은 서비스 라인부터 반대쪽 뒤쪽까지
    // =====================================================

    drawLine(

        {
            x: 0,
            y: lineY,
            z: 0
        },

        {
            x: 0,
            y: lineY,
            z: shortServiceNear
        },

        white,

        2

    );


    drawLine(

        {
            x: 0,
            y: lineY,
            z: shortServiceFar
        },

        {
            x: 0,
            y: lineY,
            z: COURT_LENGTH
        },

        white,

        2

    );

}


// =====================================================
// 네트
// =====================================================

function drawNet() {

    // =====================================================
    // 실제 배드민턴 네트
    // =====================================================

    const netLeft =
        -COURT_WIDTH / 2;       // -3.05m

    const netRight =
        COURT_WIDTH / 2;        // +3.05m

    const netCenterHeight =
        1.524;

    const netPostHeight =
        1.55;

    const netDepth =
        0.76;


    // =====================================================
    // 네트 기둥
    // 기둥은 복식 사이드라인 위에 위치
    // =====================================================

    drawLine(

        {
            x: netLeft,
            y: 0,
            z: NET_Z
        },

        {
            x: netLeft,
            y: netPostHeight,
            z: NET_Z
        },

        "#555555",

        7

    );


    drawLine(

        {
            x: netRight,
            y: 0,
            z: NET_Z
        },

        {
            x: netRight,
            y: netPostHeight,
            z: NET_Z
        },

        "#555555",

        7

    );


    // =====================================================
    // 네트 본체
    // 실제 깊이 약 760mm
    // =====================================================

    // 촘촘한 세로 망
    for (
        let x = netLeft;
        x <= netRight;
        x += 0.18
    ) {

        drawLine(

            {
                x: x,
                y: 0,
                z: NET_Z
            },

            {
                x: x,
                y: netCenterHeight,
                z: NET_Z
            },

            "rgba(20,20,20,0.72)",

            1

        );

    }


    // 촘촘한 가로 망
    for (
        let y = 0.10;
        y < netCenterHeight;
        y += 0.10
    ) {

        drawLine(

            {
                x: netLeft,
                y: y,
                z: NET_Z
            },

            {
                x: netRight,
                y: y,
                z: NET_Z
            },

            "rgba(20,20,20,0.72)",

            1

        );

    }


    // =====================================================
    // 네트 상단 흰색 테이프
    // =====================================================

    drawLine(

        {
            x: netLeft,
            y: netPostHeight,
            z: NET_Z
        },

        {
            x: netRight,
            y: netPostHeight,
            z: NET_Z
        },

        "white",

        6

    );


    // 중앙에서는 1.524m가 되도록
    // 위쪽 테이프와 망의 높이를 시각적으로 연결
    drawLine(

        {
            x: netLeft,
            y: netPostHeight,
            z: NET_Z
        },

        {
            x: 0,
            y: netCenterHeight,
            z: NET_Z
        },

        "white",

        4

    );


    drawLine(

        {
            x: 0,
            y: netCenterHeight,
            z: NET_Z
        },

        {
            x: netRight,
            y: netPostHeight,
            z: NET_Z
        },

        "white",

        4

    );

}


// =====================================================
// 천장 조명
// =====================================================

function drawLights() {


    const lightPositions = [

        -6,
        0,
        6

    ];


    for (
        const x of lightPositions
    ) {


        const p =
            project({

                x: x,

                y: WALL_HEIGHT - 0.1,

                z: 10

            });


        if (!p) {

            continue;

        }


        ctx.beginPath();


        ctx.ellipse(

            p.x,
            p.y,

            65,
            13,

            0,

            0,
            Math.PI * 2

        );


        ctx.fillStyle =
            "rgba(255,248,205,0.75)";


        ctx.fill();

    }

}

// =====================================================
// 렌더링
// =====================================================

function render() {


    // -----------------------------------------
    // 부드러운 카메라 이동
    // -----------------------------------------

    camera.yaw +=
        (targetYaw - camera.yaw)
        * 0.12;


    camera.pitch +=
        (targetPitch - camera.pitch)
        * 0.12;


    // -----------------------------------------
    // 배경
    // -----------------------------------------

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            height
        );


    gradient.addColorStop(
        0,
        "#d2d0cb"
    );


    gradient.addColorStop(
        0.55,
        "#e6e2d8"
    );


    gradient.addColorStop(
        1,
        "#b97a42"
    );


    ctx.fillStyle =
        gradient;


    ctx.fillRect(
        0,
        0,
        width,
        height
    );


    // -----------------------------------------
    // 체육관
    // -----------------------------------------

    drawGym();


    // -----------------------------------------
    // 바닥
    // -----------------------------------------

    drawFloor();


    // -----------------------------------------
    // 네트
    // -----------------------------------------

    drawNet();


    // -----------------------------------------
    // 조명
    // -----------------------------------------

    drawLights();


    requestAnimationFrame(
        render
    );

}


render();


</script>

</body>

</html>
"""


# =========================================================
# 실행
# =========================================================

components.html(
    html,
    height=900,
    scrolling=False
)
