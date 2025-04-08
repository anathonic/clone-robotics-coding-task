import sys
import json
import uvicorn
import logging
import asyncio
import argparse

from starlette import status
from typing import AsyncGenerator
from starlette.middleware.cors import CORSMiddleware
from services.connection_manager import ConnectionManager
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

from models import FanMode, FanSettings
from resources.robot_mock import RobotMock

API_VERSION = "1.0.0"
LOGGING_LEVEL = logging.INFO

logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

logger = logging.getLogger("Robot API")
manager = ConnectionManager()
robot = None
description = """
**Hello to the entire Clone Robotics team!**

This is the API implementation for robot monitoring and control.

Key Features:
- Monitor robot's state (temperature, power consumption, status, fan speed, uptime, logs).
- Control robot's state (ON/OFF, reset).
- Control fan speed mode (proportional/static).
- Real-time state updates.
- Configurable parameters via CLI.

Configuration:
- Server can be configured using command-line arguments (host, port, log level, refresh rate).
- Logs are available to monitor application behavior.
"""


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global robot
    logger.info("Starting up the app...")
    args = app.state.args
    robot = RobotMock(update_frequency=args.frequency)
    logger.info(f"Robot Monitor starting with update frequency: {args.frequency}Hz")
    asyncio.create_task(broadcast_robot_state())

    yield

    logger.info("Shutting down robot monitor server.")


app = FastAPI(
    title="Robot Control and Monitoring API",
    description=description,
    version=API_VERSION,
    contact={
        "author": "anathonic",
        "email": "anathonic@protonmail.com"
    },
    license_info={
        "name": "The Unlicense",
        "url": "https://unlicense.org",
    },
    lifespan=lifespan
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/", description="Returns the current version of the API.", status_code=status.HTTP_200_OK)
def api_version():
    return {"message": f"API {API_VERSION}"}


async def broadcast_robot_state():
    global robot
    while True:
        if robot and manager.active_connections:
            try:
                state = robot.get_state()
                await manager.broadcast(state)
            except Exception as e:
                logger.error(f"Error broadcasting robot state: {e}")

        await asyncio.sleep(1.0 / app.state.args.frequency)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        if robot:
            await websocket.send_json(robot.get_state())

        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                logger.debug(f"Received WebSocket message: {message}")

            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.get("/robot/state", status_code=status.HTTP_200_OK)
def get_robot_state():
    global robot
    if not robot:
        raise HTTPException(status_code=503, detail="Robot service not available")

    try:
        return robot.get_state()
    except Exception as e:
        logger.error(f"Error getting robot state: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/robot/power", status_code=status.HTTP_201_CREATED)
def toggle_power():
    global robot
    if not robot:
        raise HTTPException(status_code=503, detail="Robot service not available")

    try:
        robot.power_toggle()
        logger.info(f"Robot power toggled. New status: {robot.status}")
        return {"status": robot.status}
    except Exception as e:
        logger.error(f"Error toggling robot power: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/robot/reset", status_code=status.HTTP_201_CREATED)
def reset_robot():
    global robot
    if not robot:
        raise HTTPException(status_code=503, detail="Robot service not available")

    try:
        robot.reset()
        logger.info("Robot reset completed")
        return {"status": robot.status}
    except Exception as e:
        logger.error(f"Error resetting robot: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/robot/fan", status_code=status.HTTP_201_CREATED)
def set_fan_mode(settings: FanSettings):
    global robot
    if not robot:
        raise HTTPException(status_code=503, detail="Robot service not available")

    try:
        robot.set_fan_mode(settings.mode, settings.static_value)
        logger.info(f"Fan mode set to {settings.mode}" +
                    (f" with value {settings.static_value}%" if settings.mode == FanMode.STATIC else ""))
        return {"fan_mode": robot.fan_mode, "static_fan_speed": robot.static_fan_speed}
    except Exception as e:
        logger.error(f"Error setting fan mode: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/debug/error", status_code=status.HTTP_201_CREATED)
def simulate_error():
    global robot
    if not robot:
        raise HTTPException(status_code=503, detail="Robot service not available")

    robot.simulate_error()
    logger.warning("Error condition simulated")
    return {"status": robot.status}


@app.post("/debug/offline", status_code=status.HTTP_201_CREATED)
def toggle_offline():
    global robot
    if not robot:
        raise HTTPException(status_code=503, detail="Robot service not available")

    robot.toggle_offline()
    logger.warning(f"Robot toggled offline status. Current status: {robot.status}")
    return {"status": robot.status}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Robot Monitor Server")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind the server to")
    parser.add_argument("--port", type=int, default=5487, help="Port to bind the server to")
    parser.add_argument("--log-level", type=str, default="info",
                        choices=["debug", "info", "warning", "error", "critical"],
                        help="Logging level")
    parser.add_argument("--frequency", type=float, default=10.0,
                        help="Frequency of state updates in Hz")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    log_level = getattr(logging, args.log_level.upper())
    logging.getLogger().setLevel(log_level)
    logger.setLevel(log_level)

    app.state.args = args

    logger.info(f"Starting server on {args.host}:{args.port}")
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()