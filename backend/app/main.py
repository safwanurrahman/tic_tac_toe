from fastapi import FastAPI


app = FastAPI(title="Tic Tac Toe API")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
