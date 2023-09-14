from fastapi import FastAPI
import requests
import asyncio

app = FastAPI()

pong_time_ms = None
pong_task = None

@app.post("/ping")
async def ping():
    if pong_time_ms:
        await asyncio.sleep(pong_time_ms / 1000)
        response = requests.post("http://127.0.0.1:8001/pong")
        return response.text
    else:
        return {"message": "Game not started"}

@app.post("/pong")
async def pong():
    if pong_time_ms:
        await asyncio.sleep(pong_time_ms / 1000)
        response = requests.post("http://127.0.0.1:8001/ping")
        return response.text
    else:
        return {"message": "Game not started"}

@app.on_event("startup")
async def startup_event():
    global pong_task
    pong_task = asyncio.create_task(ping_pong())

async def ping_pong():
    global pong_time_ms
    while True:
        await asyncio.sleep(pong_time_ms / 1000)
        response = requests.post("http://127.0.0.1:8001/ping")
        print(response.text)

@app.on_event("shutdown")
async def shutdown_event():
    global pong_task
    pong_task.cancel()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
