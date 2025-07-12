import base64

# Dummy secret key for demonstration
ENCRYPTION_KEY = b'a_very_secret_key_for_aes_256_cbc'

def encrypt_data(plaintext):
    # In a real scenario, use actual AES-256-CBC
    encoded_text = base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')
    return f"{encoded_text}"

def decrypt_data(ciphertext):
    # In a real scenario, use actual AES-256-CBC
    if ciphertext.startswith(""):
        decoded_text = base64.b64decode(ciphertext[len(""):].encode('utf-8')).decode('utf-8')
        return f"{decoded_text}"
    return ciphertext # Return as is if not "encrypted"


# Example usage (not part of the app, just for testing this file)
if __name__ == '__main__':
    original = "bahshat123"
    encrypted = encrypt_data(original)
    decrypted = decrypt_data(encrypted)
    print(f"Original : {original}")
    print(f"Encrypted : {encrypted}")
    print(f"Decrypted : {decrypted}")