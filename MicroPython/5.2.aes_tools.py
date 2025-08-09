# aes_tools.py
import ucryptolib
# AES encryption function using ucryptolib
def aes_encrypt(data,aes_key):
    cipher = ucryptolib.aes(aes_key, 1)  # 1 = ECB mode
    encrypted = cipher.encrypt(data)     # data size  must be multiple 16 bytes
    return encrypted
# AES decryption function
def aes_decrypt(encrypted_data,aes_key):
    cipher = ucryptolib.aes(aes_key, 1)  # 1 = ECB mode
    data = cipher.decrypt(encrypted_data)   # data size  must be multiple 16 bytes
    return data

