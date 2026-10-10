
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Bảo vệ bóng bay 🎈", page_icon="🎈")

st.title("🎈 BẢO VỆ BÓNG BAY")
st.write("Di chuyển thanh đỡ để bảo vệ bóng bay khỏi vật thể đỏ!")

components.html("""
<div style="text-align:center">
<canvas id="game" width="360" height="500"
style="width:100%;max-width:360px;background:#eaf6ff;
border:3px solid #7db9e8;border-radius:12px;
touch-action:none"></canvas>
<p>Dùng phím ← → hoặc kéo thanh đỡ bằng chuột</p>
</div>

<script>
const c=document.getElementById("game");
const ctx=c.getContext("2d");

let bx=180, by=420, px=180;
let enemies=[], score=0, over=false, frame=0;
let left=false, right=false;

window.addEventListener("keydown",e=>{
 if(e.key==="ArrowLeft") left=true;
 if(e.key==="ArrowRight") right=true;
});
window.addEventListener("keyup",e=>{
 if(e.key==="ArrowLeft") left=false;
 if(e.key==="ArrowRight") right=false;
});

c.addEventListener("pointermove",e=>{
 if(e.buttons || e.pointerType==="touch"){
  const r=c.getBoundingClientRect();
  px=(e.clientX-r.left)*360/r.width;
 }
});

c.addEventListener("click",()=>{
 if(over){
  enemies=[]; score=0; over=false; frame=0;
  bx=180; by=420; px=180;
 }
});

function draw(){
 ctx.clearRect(0,0,360,500);
 ctx.fillStyle="#eaf6ff";
 ctx.fillRect(0,0,360,500);

 if(!over){
  if(left) px-=5;
  if(right) px+=5;
  px=Math.max(55,Math.min(305,px));

  frame++;
  if(frame%30===0){
   enemies.push({
    x:Math.random()*330+15,
    y:-10,
    v:2+Math.random()*2
   });
  }

  for(let i=enemies.length-1;i>=0;i--){
   let e=enemies[i];
   e.y+=e.v;

   ctx.fillStyle="#ff4545";
   ctx.beginPath();
   ctx.arc(e.x,e.y,9,0,Math.PI*2);
   ctx.fill();

   // Thanh đỡ nằm phía trên bóng bay
   if(e.y>=365 && e.y<=385 &&
      Math.abs(e.x-px)<58){
    enemies.splice(i,1);
    score++;
    continue;
   }

   // Vật thể chạm bóng bay
   if(Math.hypot(e.x-bx,e.y-by)<29){
    over=true;
   }
  }
  enemies=enemies.filter(e=>e.y<510);
 }

 // Thanh đỡ
 ctx.fillStyle="#20b77a";
 ctx.fillRect(px-55,370,110,12);

 // Bóng bay nằm dưới thanh đỡ
 ctx.fillStyle="#ff65a3";
 ctx.beginPath();
 ctx.ellipse(bx,by,23,29,0,0,Math.PI*2);
 ctx.fill();

 ctx.strokeStyle="#555";
 ctx.beginPath();
 ctx.moveTo(bx,by+29);
 ctx.lineTo(bx,by+52);
 ctx.stroke();

 ctx.fillStyle="#17324d";
 ctx.font="bold 20px Arial";
 ctx.fillText("Điểm: "+score,12,28);

 if(over){
  ctx.fillStyle="rgba(0,0,0,.7)";
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
""", height=550)

st.info("🟢 Thanh đỡ ở phía trên, bóng bay ở ngay bên dưới.")
