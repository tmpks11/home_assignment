import sys
import asyncio
from httpx import AsyncClient

pong_time_ms = None
pong_task = None
game_running = False

async def start_game():
    global pong_time_ms, pong_task, game_running
    pong_time_ms = int(sys.argv[2])
    pong_task = asyncio.create_task(ping_pong())
    game_running = True
    print("start pong game with {} second between pongs.".format(pong_time_ms/1000))

async def ping_pong():
    global pong_time_ms
    while game_running:
        await asyncio.sleep(pong_time_ms / 1000)
        async with AsyncClient() as client:
            await client.post("http://127.0.0.1:8000/ping")  # Use '127.0.0.1' for IPv4 loopback

def pause_game():
    global game_running
    if game_running:
        game_running = False
    else:
        print("Game is not running or has not started yet.")

async def resume_game():
    global pong_task, game_running
    if not game_running:
        game_running = True
        pong_task = asyncio.create_task(ping_pong())
    else:
        print("Game is already running.")

def stop_game():
    sys.exit()

if __name__ == "__main__":
    command = sys.argv[1]

    if command == "start":
        asyncio.run(start_game())
    elif command == "pause":
        pause_game()
    elif command == "resume":
        asyncio.run(resume_game())
    elif command == "stop":
        stop_game()
    else:
        print("Invalid command. Usage: python pong-cli.py <command: string> <param: number>")
