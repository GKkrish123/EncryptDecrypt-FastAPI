from fastapi import Body
from fastapi.exceptions import RequestValidationError
from src.response import get_response
from src.controller import aes_encrypt_controller, base64_encrypt_controller
from src.config import logger
from src.route import encryption_api

@encryption_api.post("/aes")
def acs_encrypt(encryption_payload: dict=Body(...)):
    try:
        return aes_encrypt_controller(encryption_payload)
    except Exception:
        logger.exception("acs_encrypt exception:")
        return get_response("AES_ENCRYPT_ERR001", None, 409)

@encryption_api.post("/base64")
def base64_encrypt(encryption_payload:  dict=Body(...)):
    try:
        return base64_encrypt_controller(encryption_payload)
    except Exception:
        logger.exception("base64_encrypt exception:")
        return get_response("BASE64_ENCRYPT_ERR001", None, 409)
