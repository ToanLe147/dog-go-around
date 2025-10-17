"""Network message definitions."""

from dataclasses import dataclass
from typing import List, Dict, Any
import msgpack


@dataclass
class JoinMessage:
    """Player join request."""

    player_name: str
    version: str = "0.1.0"

    def to_dict(self):
        return {"player_name": self.player_name, "version": self.version}


@dataclass
class InputMessage:
    """Player input state."""

    player_id: str
    throttle: float
    steer: float
    brake: bool
    handbrake: bool
    boost: bool
    timestamp: float

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "throttle": self.throttle,
            "steer": self.steer,
            "brake": self.brake,
            "handbrake": self.handbrake,
            "boost": self.boost,
            "timestamp": self.timestamp,
        }


@dataclass
class StateSnapshot:
    """Game state snapshot."""

    timestamp: float
    players: List[Dict[str, Any]]

    def to_dict(self):
        return {"timestamp": self.timestamp, "players": self.players}


@dataclass
class ChatMessage:
    """Chat message."""

    player_name: str
    message: str
    timestamp: float

    def to_dict(self):
        return {
            "player_name": self.player_name,
            "message": self.message,
            "timestamp": self.timestamp,
        }


@dataclass
class ResultsMessage:
    """Race results."""

    standings: List[Dict[str, Any]]

    def to_dict(self):
        return {"standings": self.standings}


@dataclass
class LobbyStateMessage:
    """Lobby state update."""

    players: List[Dict[str, Any]]
    track: str
    ready_count: int

    def to_dict(self):
        return {
            "players": self.players,
            "track": self.track,
            "ready_count": self.ready_count,
        }


def serialize_message(message_type: str, message: Any) -> bytes:
    """Serialize a message to bytes."""
    data = {
        "type": message_type,
        "data": message.to_dict() if hasattr(message, "to_dict") else message,
    }
    return msgpack.packb(data)


def deserialize_message(data: bytes) -> Dict[str, Any]:
    """Deserialize bytes to message."""
    return msgpack.unpackb(data, raw=False)
