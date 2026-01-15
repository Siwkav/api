from fastapi import FastAPI, Request
from mcstatus import JavaServer
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)  # позволяет FastAPI работать в serverless

@app.get("/mc")
async def mc_status(request: Request):
    ip = request.query_params.get("ip")
    port = int(request.query_params.get("port", 25565))

    if not ip:
        return {"online": False, "error": "IP is required"}

    try:
        server = JavaServer.lookup(f"{ip}:{port}")
        status = server.status()

        return {
            "online": True,
            "ip": ip,
            "port": port,
            "version": status.version.name,
            "protocol": status.version.protocol,
            "players": {
                "online": status.players.online,
                "max": status.players.max
            },
            "motd": status.description.to_plain_text()
        }

    except Exception:
        return {"online": False, "error": "Server offline or unreachable"}
