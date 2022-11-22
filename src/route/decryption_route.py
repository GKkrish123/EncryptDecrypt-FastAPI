from src.response import get_response
from src.request import decryption_payload_model
from src.controller import aes_decrypt_controller, base64_decrypt_controller
from src.config import logger
from src.route import decryption_api

@decryption_api.post("/aes")
def acs_decrypt(decryption_payload: decryption_payload_model):
    try:
        return aes_decrypt_controller(decryption_payload.dict()["payload"])
    except Exception:
        logger.exception("acs_decrypt exception:")
        return get_response("AES_DECRYPT_ERR001", None, 409)

@decryption_api.post("/base64")
def base64_decrypt(decryption_payload: decryption_payload_model):
    try:
        return base64_decrypt_controller(decryption_payload.dict()["payload"])
    except Exception:
        logger.exception("base64_decrypt:")
        return get_response("BASE64_DECRYPT_ERR001", None, 409)
