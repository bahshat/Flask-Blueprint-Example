import base64

ENCRYPTION_KEY = b'a_very_secret_key_for_aes_256_cbc'

def encrypt_data(plaintext):
    encoded_text = base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')
    return f"{encoded_text}"


def decrypt_data(ciphertext):
    decoded_text = base64.b64decode(ciphertext[len(""):].encode('utf-8')).decode('utf-8')
    return f"{decoded_text}"