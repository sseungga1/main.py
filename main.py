import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Minion Badminton",
    page_icon="🏸",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------------------------------------------------
# Streamlit 기본 여백 제거
# ---------------------------------------------------------

st.markdown("""
<style>
html, body {
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


# ---------------------------------------------------------
# 3D 배드민턴 체육관
# ---------------------------------------------------------

html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

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

    background: #202020;
}

#game {
    position: fixed;

    left: 0;
    top: 0;

    width: 100vw;
    height: 100vh;

    overflow: hidden;

    background: #202020;

    cursor: crosshair;
}

canvas {
    display: block;

    width: 100%;
    height: 100%;
}

#message {
    position: fixed;

    left: 50%;
    top: 7%;

    transform: translateX(-50%);

    padding: 13px 25px;

    background: rgba(0, 0, 0, 0.65);

    color: white;

    border-radius: 30px;

    font-family: Arial, sans-serif;

    font-size: 16px;

    z-index: 20;

    pointer-events: none;

    transition: opacity 0.5s;
}

#crosshair {
    position: fixed;

    left: 50%;
    top: 50%;

    width: 18px;
    height: 18px;

    transform:
        translate(-50%, -50%);

    pointer-events: none;

    z-index: 10;
}

#crosshair::before {
    content: "";

    position: absolute;

    left: 8px;
    top: 0;

    width: 2px;
    height: 18px;

    background: rgba(255,255,255,0.8);
}

#crosshair::after {
    content: "";

    position: absolute;

    left: 0;
    top: 8px;

    width: 18px;
    height: 2px;

    background: rgba(255,255,255,0.8);
}

</style>

</head>


<body>


<div id="game">

    <canvas id="canvas"></canvas>

</div>


<div id="message">
    화면을 클릭한 뒤 마우스를 움직여 보세요
</div>


<div id="crosshair"></div>


<script>


// =====================================================
// Canvas
// =====================================================

const canvas =
    document.getElementById("canvas");

const ctx =
    canvas.getContext("2d");

const message =
    document.getElementById("message");


// =====================================================
// 화면 크기
// =====================================================

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
// 플레이어 카메라
//
// x = 좌우
// y = 위아래
// z = 앞뒤
// =====================================================

const camera = {

    x: 0,

    y: 1.7,

    z: 1.2,

    yaw: 0,

    pitch: 0

};


// =====================================================
// 카메라 목표값
// =====================================================

let targetYaw = 0;

let targetPitch = 0;


// =====================================================
// 마우스 감도
// =====================================================

const mouseSensitivity = 0.0025;


// =====================================================
// 시야각
// =====================================================

const FOV = 75;


// =====================================================
// 체육관 크기
// =====================================================

const COURT_WIDTH = 18;

const COURT_LENGTH = 32;

const WALL_HEIGHT = 8;


// =====================================================
// 네트 위치
// =====================================================

const NET_Z = 17;


// =====================================================
// Pointer Lock
// =====================================================

document
    .getElementById("game")
    .addEventListener(
        "click",
        function() {

            this.requestPointerLock();

        }
    );


// =====================================================
// 마우스 움직임
// =====================================================

document.addEventListener(
    "mousemove",
    function(event) {

        if (
            document.pointerLockElement
            !== document.getElementById("game")
        ) {

            return;

        }


        // 좌우 시선

        targetYaw +=
            event.movementX
            * mouseSensitivity;


        // 위아래 시선

        targetPitch -=
            event.movementY
            * mouseSensitivity;


        // 위아래 제한
        //
        // 너무 뒤집히지 않도록 제한

        const limit =
            Math.PI * 0.48;

        targetPitch =
            Math.max(
                -limit,
                Math.min(
                    limit,
                    targetPitch
                )
            );

    }
);


// =====================================================
// Pointer Lock 상태
// =====================================================

document.addEventListener(
    "pointerlockchange",
    function() {

        if (
            document.pointerLockElement
            === document.getElementById("game")
        ) {

            message.style.opacity = "0";

        } else {

            message.style.opacity = "1";

        }

    }
);


// =====================================================
// 3D → 2D 투영
// =====================================================

function project(point) {

    let x =
        point.x - camera.x;

    let y =
        point.y - camera.y;

    let z =
        point.z - camera.z;


    // -------------------------------
    // Yaw
    // 좌우 회전
    // -------------------------------

    const cosY =
        Math.cos(-camera.yaw);

    const sinY =
        Math.sin(-camera.yaw);


    const x1 =
        x * cosY -
        z * sinY;

    const z1 =
        x * sinY +
        z * cosY;


    // -------------------------------
    // Pitch
    // 위아래 회전
    // -------------------------------

    const cosP =
        Math.cos(-camera.pitch);

    const sinP =
        Math.sin(-camera.pitch);


    const y2 =
        y * cosP -
        z1 * sinP;

    const z2 =
        y * sinP +
        z1 * cosP;


    // 카메라 뒤에 있으면 표시하지 않음

    if (z2 <= 0.05) {

        return null;

    }


    const focal =
        (width / 2) /
        Math.tan(
            (FOV * Math.PI / 180) / 2
        );


    const screenX =
        centerX +
        (x1 / z2) * focal;


    const screenY =
        centerY -
        (y2 / z2) * focal;


    return {

        x: screenX,

        y: screenY,

        depth: z2

    };

}


// =====================================================
// 3D 사각형 그리기
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


    if (fill) {

        ctx.fillStyle =
            fill;

        ctx.fill();

    }


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
    widthLine = 2
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
        widthLine;

    ctx.stroke();

}


// =====================================================
// 체육관 배경
// =====================================================

function drawGym() {

    // ------------------------------------------
    // 먼 벽
    // ------------------------------------------

    drawQuad(

        [
            {
                x: -COURT_WIDTH / 2,
                y: 0,
                z: COURT_LENGTH
            },

            {
                x: COURT_WIDTH / 2,
                y: 0,
                z: COURT_LENGTH
            },

            {
                x: COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: COURT_LENGTH
            },

            {
                x: -COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: COURT_LENGTH
            }
        ],

        "#e7e4da"

    );


    // ------------------------------------------
    // 왼쪽 벽
    // ------------------------------------------

    drawQuad(

        [
            {
                x: -COURT_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: -COURT_WIDTH / 2,
                y: 0,
                z: COURT_LENGTH
            },

            {
                x: -COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: COURT_LENGTH
            },

            {
                x: -COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            }
        ],

        "#ddd9cf"

    );


    // ------------------------------------------
    // 오른쪽 벽
    // ------------------------------------------

    drawQuad(

        [
            {
                x: COURT_WIDTH / 2,
                y: 0,
                z: COURT_LENGTH
            },

            {
                x: COURT_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            },

            {
                x: COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: COURT_LENGTH
            }
        ],

        "#d8d4c9"

    );


    // ------------------------------------------
    // 천장
    // ------------------------------------------

    drawQuad(

        [
            {
                x: -COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            },

            {
                x: COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: 0
            },

            {
                x: COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: COURT_LENGTH
            },

            {
                x: -COURT_WIDTH / 2,
                y: WALL_HEIGHT,
                z: COURT_LENGTH
            }
        ],

        "#d8d5cc"

    );


    // ------------------------------------------
    // 바닥
    // ------------------------------------------

    drawQuad(

        [
            {
                x: -COURT_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: COURT_WIDTH / 2,
                y: 0,
                z: 0
            },

            {
                x: COURT_WIDTH / 2,
                y: 0,
                z: COURT_LENGTH
            },

            {
                x: -COURT_WIDTH / 2,
                y: 0,
                z: COURT_LENGTH
            }
        ],

        "#bd8045"

    );

}


// =====================================================
// 바닥 나무판 줄
// =====================================================

function drawFloorBoards() {

    for (
        let z = 2;
        z < COURT_LENGTH;
        z += 2
    ) {

        drawLine(

            {
                x: -COURT_WIDTH / 2,
                y: 0.015,
                z: z
            },

            {
                x: COURT_WIDTH / 2,
                y: 0.015,
                z: z
            },

            "rgba(90,50,20,0.28)",

            1

        );

    }


    for (
        let x = -COURT_WIDTH / 2;
        x <= COURT_WIDTH / 2;
        x += 2
    ) {

        drawLine(

            {
                x: x,
                y: 0.018,
                z: 0
            },

            {
                x: x,
                y: 0.018,
                z: COURT_LENGTH
            },

            "rgba(90,50,20,0.18)",

            1

        );

    }

}


// =====================================================
// 배드민턴 코트 라인
// =====================================================

function drawCourtLines() {

    const white =
        "rgba(255,255,255,0.95)";


    // 양쪽 사이드라인

    drawLine(

        {
            x: -6,
            y: 0.025,
            z: 0
        },

        {
            x: -6,
            y: 0.025,
            z: COURT_LENGTH
        },

        white,

        3

    );


    drawLine(

        {
            x: 6,
            y: 0.025,
            z: 0
        },

        {
            x: 6,
            y: 0.025,
            z: COURT_LENGTH
        },

        white,

        3

    );


    // 가운데 선

    drawLine(

        {
            x: 0,
            y: 0.026,
            z: 0
        },

        {
            x: 0,
            y: 0.026,
            z: COURT_LENGTH
        },

        white,

        2

    );


    // 뒤쪽 선

    drawLine(

        {
            x: -6,
            y: 0.027,
            z: 4
        },

        {
            x: 6,
            y: 0.027,
            z: 4
        },

        white,

        3

    );


    drawLine(

        {
            x: -6,
            y: 0.027,
            z: 28
        },

        {
            x: 6,
            y: 0.027,
            z: 28
        },

        white,

        3

    );

}


// =====================================================
// 네트
// =====================================================

function drawNet() {

    const netHeight = 1.55;


    // 네트 기둥

    drawLine(

        {
            x: -6.5,
            y: 0,
            z: NET_Z
        },

        {
            x: -6.5,
            y: netHeight,
            z: NET_Z
        },

        "#555",

        6

    );


    drawLine(

        {
            x: 6.5,
            y: 0,
            z: NET_Z
        },

        {
            x: 6.5,
            y: netHeight,
            z: NET_Z
        },

        "#555",

        6

    );


    // 네트 윗부분

    drawLine(

        {
            x: -6.5,
            y: netHeight,
            z: NET_Z
        },

        {
            x: 6.5,
            y: netHeight,
            z: NET_Z
        },

        "white",

        7

    );


    // 네트 망

    for (
        let x = -6.5;
        x <= 6.5;
        x += 0.65
    ) {

        drawLine(

            {
                x: x,
                y: 0,
                z: NET_Z
            },

            {
                x: x,
                y: netHeight,
                z: NET_Z
            },

            "rgba(255,255,255,0.55)",

            1

        );

    }


    for (
        let y = 0.25;
        y < netHeight;
        y += 0.25
    ) {

        drawLine(

            {
                x: -6.5,
                y: y,
                z: NET_Z
            },

            {
                x: 6.5,
                y: y,
                z: NET_Z
            },

            "rgba(255,255,255,0.55)",

            1

        );

    }

}


// =====================================================
// 체육관 조명
// =====================================================

function drawLights() {

    const lights = [

        -6,

        0,

        6

    ];


    for (
        const x of lights
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

    // 배경

    ctx.fillStyle =
        "#202020";

    ctx.fillRect(
        0,
        0,
        width,
        height
    );


    // 하늘빛 / 천장빛

    const gradient =
        ctx.createLinearGradient(
            0,
            0,
            0,
            height
        );

    gradient.addColorStop(
        0,
        "#d9d9d4"
    );

    gradient.addColorStop(
        0.5,
        "#e5e2d8"
    );

    gradient.addColorStop(
        1,
        "#bd8045"
    );


    ctx.fillStyle =
        gradient;

    ctx.fillRect(
        0,
        0,
        width,
        height
    );


    // 부드러운 카메라

    camera.yaw +=
        (targetYaw - camera.yaw)
        * 0.12;


    camera.pitch +=
        (targetPitch - camera.pitch)
        * 0.12;


    // 체육관

    drawGym();


    // 바닥 판자

    drawFloorBoards();


    // 코트 라인

    drawCourtLines();


    // 네트

    drawNet();


    // 조명

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


components.html(
    html,
    height=900,
    scrolling=False
)
