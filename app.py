
import streamlit as st
import random
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Bảo vệ bóng bay 🎈",
    page_icon="🎈",
    layout="centered"
)

st.title("🎈 BẢO VỆ BÓNG BAY")
st.write("Di chuyển tấm chắn để bảo vệ quả bóng khỏi các vật thể!")

html = """
<div style="text-align:center">
<canvas id="game" width="360" height="500"
style="width:100%;max-width:360px;background:#eaf6ff;
border:3px solid #7db9e8;border-radius:12px;
touch-action:none"></canvas>
<p>⬅️ ➡️ Dùng phím mũi tên hoặc kéo tấm chắn</p>
</div>

<script>
const c = document.getElementById("game");
const ctx = c.getContext("2d");

let bx=180, by=390, px=180;
let enemies=[], score=0, over=false;
let left=false, right=false, frame=0;

function key(e, v) {
  if(e.key==="ArrowLeft") left=v;
  if(e.key==="ArrowRight") right=v;
}
window.addEventListener("keydown",e=>key(e,true));
window.addEventListener("keyup",e=>key(e,false));

c.addEventListener("pointermove",e=>{
  if(e.buttons) {
    let r=c.getBoundingClientRect();
    px=(e.clientX-r.left)*c.width/r.width;
  }
});

function restart() {
  bx=180; by=390; px=180;
  enemies=[]; score=0; over=false; frame=0;
}

c.addEventListener("click",()=>{
  if(over) restart();
});

function draw() {
  ctx.clearRect(0,0,360,500);
  ctx.fillStyle="#eaf6ff";
  ctx.fillRect(0,0,360,500);

  if(!over) {
    if(left) px-=5;
    if(right) px+=5;
    px=Math.max(45,Math.min(315,px));

    frame++;
    if(frame%28===0)
      enemies.push({
        x:Math.random()*340+10,
        y:-10,
        v:2+Math.random()*2
      });

    enemies.forEach((e,i)=>{
      e.y+=e.v;
      ctx.fillStyle="#ff5252";
      ctx.beginPath();
      ctx.arc(e.x,e.y,9,0,Math.PI*2);
      ctx.fill();

      if(Math.abs(e.x-px)<58 && e.y>438 && e.y<465) {
        enemies.splice(i,1);
        score++;
        return;
      }

      if(Math.hypot(e.x-bx,e.y-by)<29) over=true;
    });
    enemies=enemies.filter(e=>e.y<510);
  }

  // Bong bay
  ctx.fillStyle="#ff65a3";
  ctx.beginPath();
  ctx.ellipse(bx,by,23,29,0,0,Math.PI*2);
  ctx.fill();
  ctx.strokeStyle="#555";
  ctx.beginPath();
  ctx.moveTo(bx,by+29);
  ctx.lineTo(bx,by+52);
  ctx.stroke();

  // Tam chan
  ctx.fillStyle="#24b47e";
  ctx.fillRect(px-55,445,110,12);

  ctx.fillStyle="#17324d";
  ctx.font="bold 20px Arial";
  ctx.fillText("Điểm: "+score,12,28);

  if(over) {
    ctx.fillStyle="rgba(0,0,0,0.65)";
    ctx.fillRect(0,0,360,500);
    ctx.fillStyle="white";
    ctx.textAlign="center";
    ctx.font="bold 22px Arial";
    ctx.fillText("BÓNG BAY BỊ VỠ!",180,225);
    ctx.font="16px Arial";
    ctx.fillText("Nhấn vào màn hình để chơi lại",180,260);
    ctx.textAlign="left";
  }

  requestAnimationFrame(draw);
}
draw();
</script>
"""

components.html(html, height=550)

st.info("🔴 Chặn vật thể đỏ bằng tấm chắn màu xanh để bảo vệ bóng bay!")
