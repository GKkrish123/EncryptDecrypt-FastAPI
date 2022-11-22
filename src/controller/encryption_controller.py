import base64
import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from src.config import SECRET_KEY, logger
from src.response import get_response

def gcm_encrypt(key, plaintext, iv):
    try:
        # CONSTRUCT AN AES-GCM CIPHER OBJECT WITH THE KEY, IV AND TAG
        encryptor = Cipher(
            algorithms.AES256(key),
            modes.GCM(iv),
        ).encryptor()
        # GCM DOES NOT REQUIRE PADDING
        cipher_text = encryptor.update(plaintext) + encryptor.finalize()
        auth_tag = encryptor.tag
        return cipher_text, auth_tag
    except Exception as e:
        logger.error(f'gcm_encrypt:{e}')
        raise e

def aes_encrypt_controller(data, bypass=False):
    try:
        # GENERATING RANDOM BYTES FOR INITIALIZATION VECTOR
        iv = base64.b64encode(os.urandom(16))
        # # ENCRYPTION OF DATA USING AES 256 GCM
        cipher_text, auth_tag = gcm_encrypt(SECRET_KEY[:32].encode(), json.dumps(data, separators=(',', ':')).encode(), iv=base64.b64decode(iv))
        # CONSTRUCTING ENCODED ENCRYPTION DATA
        encrypted_data = f"{iv.decode()}:{base64.b64encode(cipher_text + auth_tag).decode()}"
        logger.info("AES Data Encryption Successful")
        if bypass:
            return encrypted_data
        return get_response("AES_ENCRYPT_SUCC001", encrypted_data, 200)
    except Exception as e:
        logger.error(f'aes_encrypt_controller:{e}')
        raise e


def base64_encrypt_controller(data):
    try:
        aes_encrypted_data = aes_encrypt_controller(data, bypass=True)
        # ENCODING THE ENCRYPTED DATA WITH URL_SAFE BASE64
        encrypted_data =  base64.urlsafe_b64encode(aes_encrypted_data.encode())
        logger.info("BASE64 Data Encryption Successful")
        return get_response("BASE64_ENCRYPT_SUCC001", encrypted_data, 200)
    except Exception as e:
        logger.error(f'base64_encrypt_controller:{e}')
        raise e
