from fastapi import FastAPI

app = FastAPI(title="CapitalColumn API")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "app": "capitalcolumn-api"
    }
