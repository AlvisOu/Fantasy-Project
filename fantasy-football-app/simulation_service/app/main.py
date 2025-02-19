from fastapi import FastAPI

app = FastAPI(title="Simulation Service")

@app.get("/")
async def root():
    return {"message": "Welcome to the Simulation Service!"}