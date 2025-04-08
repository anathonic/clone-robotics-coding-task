import time
import random

from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from models import RobotStatus, FanMode
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass
class LogEntry:
    message: str
    level: str
    timestamp: datetime = field(default_factory=datetime.now, metadata=config(encoder=str))


class RobotMock:
    def __init__(self, update_frequency: float = 10.0):
        self.status = RobotStatus.IDLE
        self.temperature = 25.0
        self.power_consumption = 8.0
        self.fan_speed = 20
        self.fan_mode = FanMode.PROPORTIONAL
        self.static_fan_speed = 50
        self.start_time = datetime.now()
        self.logs = []
        self.update_frequency = update_frequency
        self.last_update_time = time.time()

    def update(self) -> None:
        current_time = time.time()

        if current_time - self.last_update_time < 1.0 / self.update_frequency:
            return

        self.last_update_time = current_time

        if self.status == RobotStatus.OFFLINE:
            self.power_consumption = None
            self.temperature = None
            self.fan_speed = 0
            return

        if self.status == RobotStatus.RUNNING:
            self.power_consumption = round(random.uniform(15.0, 20.0), 2)
        else:
            self.power_consumption = round(random.uniform(7.0, 10.0), 2)

        if self.fan_mode == FanMode.PROPORTIONAL:
            if self.power_consumption is not None:
                power_ratio = (self.power_consumption - 7.0) / 13.0
                self.fan_speed = max(10, min(100, int(power_ratio * 90 + 10)))
        else:
            self.fan_speed = self.static_fan_speed

        cooling_effect = self.fan_speed / 100.0
        if self.status == RobotStatus.RUNNING:
            target_temp = 60.0 - (30.0 * cooling_effect)
            temp_variance = random.uniform(-0.5, 0.5)
        else:
            target_temp = 35.0 - (10.0 * cooling_effect)
            temp_variance = random.uniform(-0.2, 0.2)

        if self.temperature is not None:
            temp_diff = target_temp - self.temperature
            self.temperature = round(self.temperature + (temp_diff * 0.1) + temp_variance, 2)

        if random.random() < 0.02:
            if self.status == RobotStatus.ERROR:
                self.add_log("Error condition detected: Temperature regulation issue", "error")
            elif self.status == RobotStatus.RUNNING and self.temperature > 55:
                self.add_log("Warning: High temperature detected", "warning")
            elif self.status == RobotStatus.RUNNING:
                self.add_log("System check passed", "info")

    def power_toggle(self) -> None:
        if self.status == RobotStatus.IDLE:
            self.status = RobotStatus.RUNNING
            self.add_log("Robot started", "info")
        elif self.status == RobotStatus.RUNNING:
            self.status = RobotStatus.IDLE
            self.add_log("Robot stopped", "info")
        elif self.status == RobotStatus.ERROR:
            self.add_log("Cannot start: Robot is in ERROR state", "warning")
        elif self.status == RobotStatus.OFFLINE:
            self.status = RobotStatus.IDLE
            self.start_time = datetime.now()
            self.add_log("Robot back online", "info")

    def reset(self) -> None:
        prev_status = self.status
        self.status = RobotStatus.IDLE
        self.start_time = datetime.now()
        self.logs = []

        if prev_status == RobotStatus.ERROR:
            self.add_log("Error cleared, system reset", "info")
        else:
            self.add_log("System reset performed", "info")

    def set_fan_mode(self, mode: FanMode, static_value: Optional[int] = None) -> None:
        self.fan_mode = mode
        if mode == FanMode.STATIC and static_value is not None:
            self.static_fan_speed = max(0, min(100, static_value))
            self.add_log(f"Fan mode set to static: {self.static_fan_speed}%", "info")
        elif mode == FanMode.PROPORTIONAL:
            self.add_log("Fan mode set to proportional", "info")

    def add_log(self, message: str, level: str) -> None:
        self.logs.append(LogEntry(message, level))

        if len(self.logs) > 100:
            self.logs = self.logs[-100:]

    def get_uptime(self) -> str:
        if self.status == RobotStatus.OFFLINE:
            return "N/A"

        uptime_seconds = int((datetime.now() - self.start_time).total_seconds())
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_state(self) -> dict:
        self.update()
        return {
            "status": self.status,
            "temperature": self.temperature,
            "power_consumption": self.power_consumption,
            "fan_speed": self.fan_speed,
            "fan_mode": self.fan_mode,
            "static_fan_speed": self.static_fan_speed,
            "uptime": self.get_uptime(),
            "logs": [log.to_dict() for log in self.logs[-10:]]
        }

    def simulate_error(self) -> None:
        if self.status != RobotStatus.OFFLINE:
            self.status = RobotStatus.ERROR
            self.add_log("Critical system error detected", "error")

    def toggle_offline(self) -> None:
        if self.status == RobotStatus.OFFLINE:
            self.status = RobotStatus.IDLE
            self.add_log("Robot reconnected", "info")
        else:
            self.status = RobotStatus.OFFLINE
            self.add_log("Robot disconnected", "warning")