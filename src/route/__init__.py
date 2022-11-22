from fastapi import APIRouter

# CREATE API ROUTERS
encryption_api = APIRouter(prefix="/encrypt", tags=["Encryption"])
decryption_api = APIRouter(prefix="/decrypt", tags=["Decryption"])
