
var socket = io.connect(null, {port: location.port, rememberTransport: false});

var socketTimeout;

function postLocation() {
  clearInterval(socketTimeout);
  setTimeout(function(){
    socket.emit('location', {theta: theta, dist: dist})
  }, 100);
  socketTimeout = setTimeout(postLocation, 500);
}

socket.on('nextLocation', postLocation);

socket.on('face', function(data) {
  console.log('got face', data)
  faceIndex = data.face;
  face = new Image();
  face.src = "res/img/face/" + faces[faceIndex];
})

var head_base = new Image();
head_base.src = "res/img/head_base.png";

// faces used in pygame
var faces = [
  "face_shakunetsu_koyori.png",
  "face_shakunetsu_munemune.png",
  "face_shakunetsu_hanabi.png",
  "face_shakunetsu_itsumo.png",
  "face_shakunetsu_kiruka.png",
  "face_shakunetsu_agari.png",
  "face_sao_asuna.png",
  "face_sao_suguha.png",
  "face_angelbeats_yuri.png",
  "face_angelbeats_tachibana.png",
  "face_angelbeats_yui.png",
  "face_clannad_nagisa.png",
  "face_clannad_kyou.png",
  "face_clannad_fuka.png",
  "face_clannad_kotomi.png",
  "face_clannad_tomoyo.png",
  "face_sgdc_isaac.png",
  "face_sgdc_jake.png",
  "face_sgdc_james.png",
  "face_sgdc_adam.png",
  "face_sgdc_katie.png",
  "face_nichijou_mio.png",
  "face_nichijou_yuuko.png",
  "face_nichijou_mai.png",
  "face_teacher_chem.png",
  "face_oreimo_kirino.png",
  "face_snk_sasha.png",
  "face_snk_mikasa.png",
  "face_eva_rei.png",
  "face_eva_asuka.png",
];

var canvas, ctx;
var alpha, beta, gamma, theta, dist;

var faceIndex = -1;
var face;

theta = 0;
dist = 0;

window.addEventListener("deviceorientation", function() {
  var absolute = event.absolute;
  alpha    = event.alpha / 25;
  gamma    = event.gamma / 25;
  beta     = event.beta / 25;
}, true);

window.onload = function() {
  canvas = document.getElementById('canvas');
  ctx = canvas.getContext('2d');
  setInterval(renderLoop, 20);
  canvas.addEventListener('click', function(){
    socket.emit('attack');
  }, true);
};

function renderLoop() {
  var width = ctx.canvas.width = canvas.clientWidth;
  var height = ctx.canvas.height = canvas.clientHeight;
  ctx.save();

  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, width, height);

  ctx.fillStyle = "#000";
  ctx.fillText(beta + ", " + gamma, 20, 20);

  ctx.fillStyle = "#000";
  ctx.translate(width/2, height/2);
  var min = Math.min(width, height);
  
  ctx.fillStyle = "#eee";
  ctx.strokeStyle = "#888";
  ctx.lineWidth = 5;

  // Drawing the Ring
  ctx.beginPath();
  ctx.arc(0, 0, min/2, 0, 6.29);
  ctx.stroke();
  
  // Joystick position
  theta = Math.atan2(beta, gamma);
  dist = Math.min(Math.hypot(gamma, beta) / 1.414, 1);
  var radius = min / 2 - min / 5;
  var x = Math.cos(theta) * dist * radius;
  var y = Math.sin(theta) * dist * radius;

  if(faceIndex >= 0) {
    // Drawing the head
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(
      head_base,
      0, 0,
      head_base.width, head_base.height,
      x - min/4, y - min/4,
      min/2, min/2
    );

    // Drawing the face
    ctx.drawImage(
      face,
      0, 0,
      face.width, face.height,
      x - min/4, y - min/4,
      min/2, min/2
    );
    
  }

  ctx.restore();
}