from fastapi import FastAPI

app = FastAPI(
    title="SNRT Smart Archive API",
    description="API de gestion intelligente des archives multimédias de la SNRT",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to SNRT Smart Archive API"
    }