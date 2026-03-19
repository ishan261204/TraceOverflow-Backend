from PIL import Image
from PIL.PngImagePlugin import PngInfo
from stegano import lsb

# The final winning hash from your main.py server
FULL_HASH = "ec9decdf25466e7a79498a2257a44ca7cb828168a7073b4e808c16c3a3790d866"

# Split the hash straight down the middle
STEGO_PART = FULL_HASH[:32]
EXIF_PART = FULL_HASH[32:]

print("[*] Initiating Dual-Layer Payload Injection...")

# --- LAYER 1: PIXEL STEGANOGRAPHY ---
print(f"[-] Hiding Part 1 in pixels: {STEGO_PART}")
secret_image = lsb.hide("clean_clue.png", STEGO_PART)
secret_image.save("temp_payload.png")

# --- LAYER 2: METADATA INJECTION ---
print(f"[-] Hiding Part 2 in metadata: {EXIF_PART}")
target_image = Image.open("temp_payload.png")

# Create a custom metadata chunk
metadata = PngInfo()
# We hide it in the 'Description' field, which tools like ExifTool will spot
metadata.add_text("Description", EXIF_PART) 

# Save the final, dual-layered image
target_image.save("clue_image.png", pnginfo=metadata)

print("[+] SUCCESS: clue_image.png generated securely.")