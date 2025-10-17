"""Serialization utilities for network and save data."""

import json
import pickle
from typing import Any, Dict


class Serializer:
    """Data serialization helpers."""

    @staticmethod
    def to_json(data: Any) -> str:
        """Serialize data to JSON string."""
        return json.dumps(data, indent=2)

    @staticmethod
    def from_json(json_str: str) -> Any:
        """Deserialize JSON string to data."""
        return json.loads(json_str)

    @staticmethod
    def to_json_file(data: Any, filepath: str):
        """Save data to JSON file."""
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def from_json_file(filepath: str) -> Any:
        """Load data from JSON file."""
        with open(filepath, "r") as f:
            return json.load(f)

    @staticmethod
    def to_binary(data: Any) -> bytes:
        """Serialize data to binary using pickle."""
        return pickle.dumps(data)

    @staticmethod
    def from_binary(binary_data: bytes) -> Any:
        """Deserialize binary data using pickle."""
        return pickle.loads(binary_data)

    @staticmethod
    def to_binary_file(data: Any, filepath: str):
        """Save data to binary file."""
        with open(filepath, "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def from_binary_file(filepath: str) -> Any:
        """Load data from binary file."""
        with open(filepath, "rb") as f:
            return pickle.load(f)


class GameStateSerializer:
    """Serialize game state for saving/loading."""

    @staticmethod
    def serialize_car_state(car) -> Dict:
        """Serialize car state."""
        return {
            "position": [
                car.entity.position.x,
                car.entity.position.y,
                car.entity.position.z,
            ],
            "rotation": [
                car.entity.rotation.x,
                car.entity.rotation.y,
                car.entity.rotation.z,
            ],
            "velocity": [
                car.physics.velocity.x,
                car.physics.velocity.y,
                car.physics.velocity.z,
            ],
            "speed": car.speed,
        }

    @staticmethod
    def deserialize_car_state(car, state: Dict):
        """Deserialize car state."""
        from ursina import Vec3

        car.entity.position = Vec3(*state["position"])
        car.entity.rotation = Vec3(*state["rotation"])
        car.physics.velocity = Vec3(*state["velocity"])
        car.speed = state["speed"]

    @staticmethod
    def serialize_race_state(race_manager) -> Dict:
        """Serialize race state."""
        return {
            "state": race_manager.state,
            "current_lap": race_manager.current_lap,
            "total_laps": race_manager.total_laps,
            "countdown_timer": race_manager.countdown_timer,
            "race_start_time": race_manager.race_start_time,
        }

    @staticmethod
    def serialize_game_save(world, race_manager) -> Dict:
        """Serialize complete game state for saving."""
        return {
            "version": "0.1.0",
            "track": world.track.name,
            "player_car": GameStateSerializer.serialize_car_state(world.player_car),
            "race": GameStateSerializer.serialize_race_state(race_manager),
            "timestamp": __import__("time").time(),
        }


class NetworkDataSerializer:
    """Serialize data for network transmission."""

    @staticmethod
    def serialize_position(position) -> list:
        """Serialize position vector."""
        return [float(position.x), float(position.y), float(position.z)]

    @staticmethod
    def serialize_rotation(rotation) -> list:
        """Serialize rotation vector."""
        return [float(rotation.x), float(rotation.y), float(rotation.z)]

    @staticmethod
    def compress_float(value: float, precision: int = 2) -> float:
        """Compress float to reduce bandwidth."""
        return round(value, precision)

    @staticmethod
    def compress_vector(vec, precision: int = 2) -> list:
        """Compress vector components."""
        return [round(v, precision) for v in vec]
