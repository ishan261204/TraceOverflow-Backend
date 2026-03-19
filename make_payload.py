import hashlib
from stegano import lsb

# 1. Choose the secret phrase that proves they won
secret_phrase = "trace_core_override_complete"

# 2. Generate the SHA-256 Hash of that phrase
hash_object = hashlib.sha256(secret_phrase.encode())
target_hash = hash_object.hexdigest()

print(f"--- SAVE THIS HASH FOR YOUR BACKEND ---")
print(f"Target Hash: {target_hash}")
print(f"---------------------------------------")

# 3. Hide the hash inside the image
# This takes 'base_logo.png', hides the hash, and saves it as 'clue_image.png'
secret_image = lsb.hide("base_logo.jpeg", target_hash)
secret_image.save("clue_image.png")

print("Success! 'clue_image.jpeg' now contains the hidden hash.")