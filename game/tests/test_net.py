"""Tests for networking functionality."""

import pytest
import asyncio
from game.net.messages import (
    JoinMessage,
    InputMessage,
    StateSnapshot,
    serialize_message,
    deserialize_message,
)


class TestMessages:
    """Test message serialization and deserialization."""

    def test_join_message(self):
        """Test JoinMessage serialization."""
        msg = JoinMessage(player_name="TestPlayer")
        data = serialize_message("join", msg)

        assert data is not None
        assert isinstance(data, bytes)

        # Deserialize
        decoded = deserialize_message(data)
        assert decoded["type"] == "join"
        assert decoded["data"]["player_name"] == "TestPlayer"

    def test_input_message(self):
        """Test InputMessage serialization."""
        msg = InputMessage(
            player_id="player_1",
            throttle=1.0,
            steer=0.5,
            brake=False,
            handbrake=True,
            boost=False,
            timestamp=123.456,
        )
        data = serialize_message("input", msg)

        decoded = deserialize_message(data)
        assert decoded["type"] == "input"
        assert decoded["data"]["player_id"] == "player_1"
        assert decoded["data"]["throttle"] == 1.0
        assert decoded["data"]["steer"] == 0.5
        assert decoded["data"]["handbrake"] is True

    def test_state_snapshot(self):
        """Test StateSnapshot serialization."""
        players = [
            {
                "id": "player_1",
                "position": [0, 1, 0],
                "rotation": [0, 0, 0],
                "velocity": [5, 0, 0],
            }
        ]

        msg = StateSnapshot(timestamp=123.456, players=players)
        data = serialize_message("state", msg)

        decoded = deserialize_message(data)
        assert decoded["type"] == "state"
        assert len(decoded["data"]["players"]) == 1
        assert decoded["data"]["players"][0]["id"] == "player_1"


class TestStateSynchronization:
    """Test state synchronization."""

    def test_interpolation_buffer(self):
        """Test state buffer management."""
        from game.net.state_sync import StateSynchronizer

        sync = StateSynchronizer()

        # Add states
        state1 = {"timestamp": 1.0, "players": []}
        state2 = {"timestamp": 2.0, "players": []}

        sync.add_state(state1)
        sync.add_state(state2)

        assert len(sync.state_buffer) == 2

    def test_buffer_trimming(self):
        """Test that buffer is trimmed when full."""
        from game.net.state_sync import StateSynchronizer

        sync = StateSynchronizer()
        sync.max_buffer_size = 5

        # Add more states than buffer size
        for i in range(10):
            sync.add_state({"timestamp": i, "players": []})

        assert len(sync.state_buffer) <= sync.max_buffer_size


class TestNetworkClient:
    """Test network client functionality."""

    @pytest.mark.asyncio
    async def test_client_connection_failure(self):
        """Test client handles connection failure gracefully."""
        from game.net.client import NetworkClient

        # Try to connect to invalid server
        client = NetworkClient("invalid_host", 9999, "TestPlayer", None)

        # Wait a bit
        await asyncio.sleep(0.5)

        # Should not be connected
        assert not client.connected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
