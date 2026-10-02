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

// =====================================================
// 마우스 드래그 카메라
// =====================================================
//
// 왼쪽 버튼을 누른 상태에서만 카메라 회전
// 좌우 : 자유 회전
// 위아래 : ±55도 제한
// =====================================================

let isDragging =
    false;

let lastMouseX =
    0;

let lastMouseY =
    0;


// =====================================================
// 카메라 회전 감도
// =====================================================

const MOUSE_SENSITIVITY =
    0.008;


// =====================================================
// 위아래 시야 제한
// =====================================================

const MAX_PITCH =
    55 * Math.PI / 180;


// =====================================================
// 마우스 왼쪽 버튼 누르기
// =====================================================

game.addEventListener(
    "mousedown",
    function(event) {

        // 왼쪽 버튼만 사용
        if (event.button !== 0) {
            return;
        }

        isDragging =
            true;

        lastMouseX =
            event.clientX;

        lastMouseY =
            event.clientY;

        // 브라우저의 기본 드래그 동작 방지
        event.preventDefault();

    }
);


// =====================================================
// 마우스를 움직일 때
// =====================================================

game.addEventListener(
    "mousemove",
    function(event) {

        // 왼쪽 버튼을 누르고 있을 때만 회전
        if (!isDragging) {
            return;
        }


        // -----------------------------------------
        // 이전 위치와 현재 위치의 차이
        // -----------------------------------------

        const deltaX =
            event.clientX -
            lastMouseX;

        const deltaY =
            event.clientY -
            lastMouseY;


        // -----------------------------------------
        // 현재 위치 저장
        // -----------------------------------------

        lastMouseX =
            event.clientX;

        lastMouseY =
            event.clientY;


        // -----------------------------------------
        // 좌우 회전
        //
        // 제한 없음
        // → 360도 이상 계속 회전 가능
        // -----------------------------------------

        targetYaw -=
            deltaX *
            MOUSE_SENSITIVITY;


        // -----------------------------------------
        // 위아래 회전
        // -----------------------------------------

        targetPitch +=
            deltaY *
            MOUSE_SENSITIVITY;


        // -----------------------------------------
        // 위아래만 ±55도 제한
        // -----------------------------------------

        targetPitch =
            Math.max(
                -MAX_PITCH,
                Math.min(
                    MAX_PITCH,
                    targetPitch
                )
            );


        // -----------------------------------------
        // 안내문 숨기기
        // -----------------------------------------

        message.style.opacity =
            "0";


        event.preventDefault();

    }
);


// =====================================================
// 마우스 버튼을 놓으면 회전 중지
// =====================================================

window.addEventListener(
    "mouseup",
    function(event) {

        if (event.button === 0) {

            isDragging =
                false;

        }

    }
);


// =====================================================
// 게임 화면 밖으로 나가더라도
// 마우스 버튼을 놓으면 회전 중지
// =====================================================

window.addEventListener(
    "blur",
    function() {

        isDragging =
            false;

    }
);


// =====================================================
// 마우스가 게임 화면에 들어왔을 때
// =====================================================

game.addEventListener(
    "mouseenter",
    function() {

        message.style.opacity =
            "1";

        setTimeout(
            function() {

                message.style.opacity =
                    "0";

            },
            1500
        );

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

// =====================================================
// 3D 선
// 카메라 뒤쪽을 지나가는 선도 화면에 보이는 부분은
// 잘라서 계속 표시
// =====================================================

function drawLine(
    a,
    b,
    color,
    lineWidth = 2
) {

    // -----------------------------------------
    // 두 점을 카메라 기준 좌표로 변환
    // -----------------------------------------

    function cameraSpace(point) {

        let x =
            point.x - camera.x;

        let y =
            point.y - camera.y;

        let z =
            point.z - camera.z;

        // 좌우 회전
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

        // 상하 회전
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

        return {
            x: rotatedX,
            y: rotatedY,
            z: finalZ
        };
    }


    // -----------------------------------------
    // 카메라 기준 좌표
    // -----------------------------------------

    let ca =
        cameraSpace(a);

    let cb =
        cameraSpace(b);


    // -----------------------------------------
    // 카메라 바로 앞의 최소 거리
    // -----------------------------------------

    const NEAR =
        0.05;


    // -----------------------------------------
    // 두 점 모두 카메라 뒤쪽이면
    // 선 전체가 보이지 않으므로 그리지 않음
    // -----------------------------------------

    if (
        ca.z <= NEAR &&
        cb.z <= NEAR
    ) {

        return;

    }


    // -----------------------------------------
    // 한쪽 점이 카메라 뒤에 있다면
    // 카메라 앞쪽 경계까지 선을 잘라냄
    // -----------------------------------------

    if (ca.z <= NEAR) {

        const t =
            (NEAR - ca.z) /
            (cb.z - ca.z);

        ca = {
            x: ca.x + (cb.x - ca.x) * t,
            y: ca.y + (cb.y - ca.y) * t,
            z: NEAR
        };

    }


    if (cb.z <= NEAR) {

        const t =
            (NEAR - cb.z) /
            (ca.z - cb.z);

        cb = {
            x: cb.x + (ca.x - cb.x) * t,
            y: cb.y + (ca.y - cb.y) * t,
            z: NEAR
        };

    }


    // -----------------------------------------
    // 3D → 2D 투영
    // -----------------------------------------

    const focal =
        (width / 2) /
        Math.tan(
            (FOV * Math.PI / 180) / 2
        );


    const p1 = {

        x:
            centerX +
            (ca.x / ca.z) * focal,

        y:
            centerY -
            (ca.y / ca.z) * focal

    };


    const p2 = {

        x:
            centerX +
            (cb.x / cb.z) * focal,

        y:
            centerY -
            (cb.y / cb.z) * focal

    };


    // -----------------------------------------
    // 선 그리기
    // -----------------------------------------

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
 // 실제 배드민턴 네트 (BWF 규격 반영)
 // =====================================================

function drawNet() {

    const netLeft = -COURT_WIDTH / 2;
    const netRight = COURT_WIDTH / 2;

    // BWF 네트 규격
    const NET_TOP_SIDE = 1.55;
    const NET_TOP_CENTER = 1.524;
    const NET_VERTICAL_DEPTH = 0.76;
    const NET_TAPE_HEIGHT = 0.075;

    // 네트의 위치별 상단 높이
    function getNetTopHeight(x) {

        const ratio =
            Math.abs(x) / (COURT_WIDTH / 2);

        return (
            NET_TOP_CENTER +
            (NET_TOP_SIDE - NET_TOP_CENTER) * ratio
        );
    }

    // 네트의 위치별 아래쪽 높이
    // 반드시 바닥보다 위에 위치하도록 계산
    function getNetBottomHeight(x) {

        return (
            getNetTopHeight(x) -
            NET_VERTICAL_DEPTH
        );
    }

    // =====================================================
    // 네트 기둥
    // 복식 사이드라인 위치
    // =====================================================

    drawLine(
        {
            x: netLeft,
            y: 0,
            z: NET_Z
        },
        {
            x: netLeft,
            y: NET_TOP_SIDE,
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
            y: NET_TOP_SIDE,
            z: NET_Z
        },
        "#555555",
        7
    );

    // =====================================================
    // 네트 본체
    // 아래쪽이 바닥에 닿지 않도록 구현
    // =====================================================

    // 세로 망
    for (
        let x = netLeft;
        x <= netRight;
        x += 0.18
    ) {

        const topY =
            getNetTopHeight(x) - NET_TAPE_HEIGHT;

        const bottomY =
            getNetBottomHeight(x);

        drawLine(
            {
                x: x,
                y: bottomY,
                z: NET_Z
            },
            {
                x: x,
                y: topY,
                z: NET_Z
            },
            "rgba(20,20,20,0.78)",
            1
        );
    }

    // 가로 망
    // 위쪽 테이프 아래부터 네트 하단까지
    for (
        let t = 0.12;
        t < 1;
        t += 0.12
    ) {

        for (
            let x = netLeft;
            x < netRight;
            x += 0.18
        ) {

            const nextX =
                Math.min(x + 0.18, netRight);

            const bottomY1 =
                getNetBottomHeight(x);

            const bottomY2 =
                getNetBottomHeight(nextX);

            const topY1 =
                getNetTopHeight(x) - NET_TAPE_HEIGHT;

            const topY2 =
                getNetTopHeight(nextX) - NET_TAPE_HEIGHT;

            const y1 =
                bottomY1 + (topY1 - bottomY1) * t;

            const y2 =
                bottomY2 + (topY2 - bottomY2) * t;

            drawLine(
                {
                    x: x,
                    y: y1,
                    z: NET_Z
                },
                {
                    x: nextX,
                    y: y2,
                    z: NET_Z
                },
                "rgba(20,20,20,0.78)",
                1
            );
        }
    }

    // 네트 아래쪽 테두리
    for (
        let x = netLeft;
        x < netRight;
        x += 0.18
    ) {

        const nextX =
            Math.min(x + 0.18, netRight);

        drawLine(
            {
                x: x,
                y: getNetBottomHeight(x),
                z: NET_Z
            },
            {
                x: nextX,
                y: getNetBottomHeight(nextX),
                z: NET_Z
            },
            "#333333",
            1.5
        );
    }

    // =====================================================
    // 상단 흰색 테이프
    // 높이 75mm
    // 중앙 높이 1.524m / 양쪽 높이 1.55m
    // =====================================================

    for (
        let x = netLeft;
        x < netRight;
        x += 0.15
    ) {

        const nextX =
            Math.min(x + 0.15, netRight);

        const top1 =
            getNetTopHeight(x);

        const top2 =
            getNetTopHeight(nextX);

        const bottom1 =
            top1 - NET_TAPE_HEIGHT;

        const bottom2 =
            top2 - NET_TAPE_HEIGHT;

        drawQuad(
            [
                {
                    x: x,
                    y: top1,
                    z: NET_Z
                },
                {
                    x: nextX,
                    y: top2,
                    z: NET_Z
                },
                {
                    x: nextX,
                    y: bottom2,
                    z: NET_Z
                },
                {
                    x: x,
                    y: bottom1,
                    z: NET_Z
                }
            ],
            "white"
        );
    }

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
