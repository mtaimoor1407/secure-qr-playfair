from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from playfair import (
    encrypt, decrypt,
    get_grid_data,
    get_encryption_steps,
    get_keyword_strength
)

# ── Create FastAPI app ──
app = FastAPI(
    title="Secure QR Generator",
    description="Playfair Cipher encryption API — Information Security Lab Project",
    version="1.0.0"
)

# ── Mount static files and templates ──
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ══════════════════════════════════════════
#  REQUEST MODELS — Pydantic validates these
#  automatically. If wrong data is sent,
#  FastAPI returns a clear error instantly.
# ══════════════════════════════════════════

class EncryptRequest(BaseModel):
    message: str
    keyword: str

class DecryptRequest(BaseModel):
    cipher:  str
    keyword: str

class GridRequest(BaseModel):
    keyword: str


# ══════════════════════════════════════════
#  ROUTES
# ══════════════════════════════════════════

# ── Serve main page ──
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# ── API: Encrypt ──
@app.post("/api/encrypt")
async def api_encrypt(body: EncryptRequest):
    message = body.message.strip()
    keyword = body.keyword.strip()

    # Validate
    if not message:
        return {"error": "Message is required"}
    clean_kw = ''.join(c for c in keyword if c.isalpha())
    if len(clean_kw) < 2:
        return {"error": "Keyword must have at least 2 letters"}

    cipher = encrypt(message, keyword)
    steps  = get_encryption_steps(message, keyword)
    grid   = get_grid_data(keyword)

    return {
        "cipher": cipher,
        "steps":  steps,
        "grid":   grid
    }


# ── API: Decrypt ──
@app.post("/api/decrypt")
async def api_decrypt(body: DecryptRequest):
    cipher  = body.cipher.strip()
    keyword = body.keyword.strip()

    if not cipher:
        return {"error": "Ciphertext is required"}
    if not keyword:
        return {"error": "Keyword is required"}

    plain = decrypt(cipher, keyword)

    return {"plain": plain}


# ── API: Grid + Strength (called live as user types) ──
@app.post("/api/grid")
async def api_grid(body: GridRequest):
    keyword = body.keyword.strip()

    if not keyword:
        return {"grid": [], "strength": 0}

    grid     = get_grid_data(keyword)
    strength = get_keyword_strength(keyword)

    return {
        "grid":     grid,
        "strength": strength
    }