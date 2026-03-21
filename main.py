from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
import base64
import codecs

app = FastAPI()

# SECURITY: Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, change "*" to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- GAME DATA ---
PHASE1_WORDS = {
    "bfbwoykk": "cheaters",
    "egoarued": "firewall",
    "zlxhttxk": "analyzes"
}

VALID_PHASE1_KEYS = {
    "cheaters-1101": True,
    "firewall-1001": True,
    "analyzes-0101": True
}

ZIP_MASTER_KEY = "TRC-8891"
TARGET_HASH = "ec9decdf25466e7a79498a2257a44ca7cb828168a7073b4e808c16c3a3790d866"

# --- DATA MODELS ---
class Part1Guess(BaseModel):
    cipher_used: str
    guess: str

class FinalHash(BaseModel):
    sha_hash: str

# --- API ENDPOINTS ---
@app.get("/get-cipher")
def get_cipher():
    scrambled = random.choice(list(PHASE1_WORDS.keys()))
    return {"cipher": scrambled}

@app.post("/verify-part1")
def verify_part1(data: Part1Guess):
    correct_word = PHASE1_WORDS.get(data.cipher_used)
    if not correct_word or data.guess.lower() != correct_word:
        raise HTTPException(status_code=400, detail="Invalid sequence")
    return {"success": True}

@app.post("/verify-final")
def verify_final(data: Part1Guess):
    if data.guess.lower() not in VALID_PHASE1_KEYS:
        raise HTTPException(status_code=400, detail="Signature mismatch")
    return {
        "success": True, 
        "hint": "Check the standard web crawler exclusion protocol."
    }

@app.post("/verify-hash")
def verify_hash(data: FinalHash):
    # 1. THE VERIFICATION (Unchanged - strictly matches the strings)
    if data.sha_hash.strip().lower() != TARGET_HASH:
        raise HTTPException(status_code=400, detail="Hash mismatch")
    
    # 2. THE DYNAMIC ENCODING (Randomizes the Instagram handle format)
    target_handle = "@genz_sherlock"
    techniques = ["base64", "hex", "binary", "rot13"]
    choice = random.choice(techniques)
    
    if choice == "base64":
        encoded_handle = base64.b64encode(target_handle.encode('utf-8')).decode('utf-8')
        cipher_hint = "B64"
    elif choice == "hex":
        encoded_handle = target_handle.encode('utf-8').hex()
        cipher_hint = "HEX"
    elif choice == "binary":
        encoded_handle = ' '.join(format(ord(c), '08b') for c in target_handle)
        cipher_hint = "BIN"
    elif choice == "rot13":
        encoded_handle = codecs.encode(target_handle, 'rot_13')
        cipher_hint = "ROT"
        
    message = f"SYSTEM CRACKED. DM YOUR VICTORY TO [{cipher_hint}]: {encoded_handle}"
    
    return {"success": True, "message": message}