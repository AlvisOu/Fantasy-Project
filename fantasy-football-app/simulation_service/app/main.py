from fastapi import FastAPI
from app.routes import player, lineup

app = FastAPI(title="Simulation Service")

app.include_router(player.router, prefix="/player", tags=["player"])
app.include_router(lineup.router, prefix="/lineup", tags=["lineup"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Simulation Service!"}