from fastapi import FastAPI

app = FastAPI(title="System Catalyst API")


@app.get("/")
def read_root():
    return {"message": "Welcome to System Catalyst API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
