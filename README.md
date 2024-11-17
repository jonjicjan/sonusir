from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

def pad(data):
    block_size = AES.block_size
    padding = block_size - len(data) % block_size
    return data + bytes([padding]) * padding

def unpad(data):
    padding = data[-1]
    return data[:-padding]

def generate_key(password):
    # Use a fixed key derivation method, no salt
    return PBKDF2(password, b'', dkLen=32)  # Empty salt for simplicity

def encrypt(plaintext, password):
    iv = get_random_bytes(AES.block_size)
    key = generate_key(password)
    plaintext = pad(plaintext.encode('utf-8'))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)
    encrypted_data = iv + ciphertext
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt(encrypted_data, password):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]
    key = generate_key(password)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    decrypted_data = unpad(decrypted_data)
    return decrypted_data.decode('utf-8')

if __name__ == '__main__':
    password = input("Enter password for encryption/decryption: ")
    plaintext = input("Enter plaintext to encrypt: ")
    encrypted_text = encrypt(plaintext, password)
    print("Encrypted Text:", encrypted_text)

    decrypted_text = decrypt(encrypted_text, password)
    print("Decrypted Text:", decrypted_text)
