from pydantic import BaseModel, Field

class decryption_payload_model(BaseModel):
    payload: str = Field(
        ..., description="payload for decryption", example="encryptedpayload", min_length=1
    )
