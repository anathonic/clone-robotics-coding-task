from enum import Enum

from typing import List, Optional
from pydantic import BaseModel, Field


class RobotStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    OFFLINE = "offline"
    ERROR = "error"


class RobotState(BaseModel):
    temperature: float
    power: float
    status: RobotStatus
    fan_speed: int
    uptime: str
    logs: List[str]


class FanMode(str, Enum):
    PROPORTIONAL = "proportional"
    STATIC = "static"


class FanSettings(BaseModel):
    mode: FanMode
    static_value: Optional[int] = Field(None, ge=0, le=100)
