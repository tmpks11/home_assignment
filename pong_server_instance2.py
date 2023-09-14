from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.post("/ping")
async def ping():
    await asyncio.sleep(pong_time_ms / 1000)
    return "Pong"

@app.post("/pong")
async def pong():
    await asyncio.sleep(pong_time_ms / 1000)
    return "Pong"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
