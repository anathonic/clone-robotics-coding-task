import sys
import logging
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware

API_VERSION = "1.0.0"
UPDATE_FREQUENCY = 10
LOGGING_LEVEL = logging.INFO

logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

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
)

origins = ["http://127.0.0.1:8081"]

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
