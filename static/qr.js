// ══════════════════════════════════════════
//  QR CODE GENERATION + DOWNLOAD
// ══════════════════════════════════════════

function generateQR(containerId, text, color) {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  new QRCode(container, {
    text: text,
    width: 160,
    height: 160,
    colorDark: color,
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M
  });
}

function downloadQR(containerId, filename) {
  const container = document.getElementById(containerId);
  const canvas = container.querySelector("canvas");
  if (!canvas) { alert("Generate QR first."); return; }
  const link = document.createElement("a");
  link.download = filename + ".png";
  link.href = canvas.toDataURL("image/png");
  link.click();
}