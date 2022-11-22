import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.route import decryption_route, encryption_route

# METADATA TAGS FOR SWAGGER AND DOCS
tags_metadata = [
    {
        "name": "Encryption",
        "description": "Contains all API's related to Encryption",
    },
    {
        "name": "Decryption",
        "description": "Contains all API's related to Decryption",
    }
]

# DESCRIPTION OF APP
app_description = (
    "Consists of **APIs** which performs **Encryption/Decryption** operations."
)

# CREATE FASTAPI APP
app = FastAPI(
    title="C360 ENCRYPTION",
    description=app_description,
    openapi_tags=tags_metadata,
)

# APPLY MIDDLEWARE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CUSTOM VALIDATION ERROR RESPONSE
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {
            "name": err["loc"][-1],
            "location": err["loc"][0],
            "detail": err["msg"],
            "type": err["type"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"validation_error": errors}),
    )


# INCLUDE ROUTERS
app.include_router(decryption_route.decryption_api)
app.include_router(encryption_route.encryption_api)

# APP START
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
