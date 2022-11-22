import base64
import json
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from src.config import SECRET_KEY, logger
from src.response import get_response


def gcm_decrypt(key, iv, ciphertext, tag):
    try:
        # CONSTRUCT AN AES-GCM CIPHER OBJECT WITH THE KEY, IV AND TAG
        decryptor = Cipher(
            algorithms.AES256(key),
            # GCM TAG USED FOR AUTHENTICATING THE MESSAGE
            modes.GCM(iv, tag),
        ).decryptor()
        # IF THE TAG DOES NOT MATCH AN INVALIDTAG EXCEPTION WILL BE RAISED.
        return decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as e:
        logger.error(f'gcm_decrypt:{e}')
        raise e

def aes_decrypt_controller(data, bypass=False):
    try:
        # SPLITTING THE PAYLOAD DATA
        data_parts = data.split(":")
        # GATHER CIPHER ESSENTIALS FROM THE DATA
        iv = base64.b64decode(data_parts[0])
        cipher_data = base64.b64decode(data_parts[1])
        encrypted_data = cipher_data[:-16]
        tag = cipher_data[-16:]
        # DECRYPTION OF DATA USING AES 256 GCM
        decrypted_data = gcm_decrypt(SECRET_KEY[:32].encode(), iv, encrypted_data, tag)
        # CONVERT DECRYPTED DATA TO JSON
        decrypted_json_data = json.loads(decrypted_data.decode())
        logger.info("Data Decryption with AES Successful")
        if bypass:
            return decrypted_json_data
        return get_response("AES_DECRYPT_SUCC001", decrypted_json_data, 200)
    except Exception as e:
        logger.error(f'aes_decrypt_controller:{e}')
        raise e


def base64_decrypt_controller(data):
    try:
        # DECODING THE PAYLOAD DATA WITH URL_SAFE BASE64
        decoded_data = base64.urlsafe_b64decode(data + "=" * (4 - len(data) % 4))
        # DECRYPTION WITH THE DECODED PAYLOAD DATA
        decrypted_json_data = aes_decrypt_controller(decoded_data.decode(), bypass=True)
        logger.info("Data Decryption with BASE64 Successful")
        return get_response("BASE64_DECRYPT_SUCC001", decrypted_json_data, 200)
    except Exception as e:
        logger.error(f'base64_decrypt_controller:{e}')
        raise e
