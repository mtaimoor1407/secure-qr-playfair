// ══════════════════════════════════════════
//  QR CODE CAMERA SCANNER
// ══════════════════════════════════════════

let scannerStream  = null;
let scannerRunning = false;
let scannerTimer   = null;

function startScanner() {
  const videoWrap = document.getElementById("scanner-video-wrap");
  const video     = document.getElementById("scanner-video");
  const resultBox = document.getElementById("scanner-result-box");
  const startBtn  = document.getElementById("startScanBtn");
  const stopBtn   = document.getElementById("stopScanBtn");

  resultBox.style.display = "none";
  resultBox.textContent   = "";

  navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
    .then(stream => {
      scannerStream   = stream;
      scannerRunning  = true;
      video.srcObject = stream;
      videoWrap.style.display = "block";
      startBtn.style.display  = "none";
      stopBtn.style.display   = "inline-block";
      video.play();
      scannerTimer = setInterval(() => scanFrame(video), 300);
    })
    .catch(() => {
      alert("Camera access denied or not available.");
    });
}

function stopScanner() {
  clearInterval(scannerTimer);
  scannerRunning = false;
  if (scannerStream) {
    scannerStream.getTracks().forEach(t => t.stop());
    scannerStream = null;
  }
  document.getElementById("scanner-video-wrap").style.display = "none";
  document.getElementById("startScanBtn").style.display  = "inline-block";
  document.getElementById("stopScanBtn").style.display   = "none";
}

function scanFrame(video) {
  if (!scannerRunning || video.readyState !== video.HAVE_ENOUGH_DATA) return;
  const canvas  = document.getElementById("scanner-canvas");
  const ctx     = canvas.getContext("2d");
  canvas.width  = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const code      = jsQR(imageData.data, imageData.width, imageData.height);
  if (code) {
    const scanned   = code.data;
    const resultBox = document.getElementById("scanner-result-box");
    resultBox.style.display = "block";
    resultBox.textContent   = "✅  Scanned: " + scanned;
    document.getElementById("cipherIn").value = scanned;
    stopScanner();
    document.getElementById("cipherIn").scrollIntoView({ behavior: "smooth" });
  }
}