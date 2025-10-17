"""State synchronization utilities."""

import time
from typing import List, Dict, Any


class StateSynchronizer:
    """Handles state synchronization between client and server."""

    def __init__(self, interpolation_delay=0.1):
        self.interpolation_delay = interpolation_delay
        self.state_buffer: List[Dict[str, Any]] = []
        self.max_buffer_size = 30

    def add_state(self, state: Dict[str, Any]):
        """Add a new state to the buffer."""
        self.state_buffer.append(state)

        # Trim buffer
        if len(self.state_buffer) > self.max_buffer_size:
            self.state_buffer.pop(0)

    def get_interpolated_state(self) -> Dict[str, Any]:
        """Get interpolated state for current time."""
        if len(self.state_buffer) < 2:
            return self.state_buffer[-1] if self.state_buffer else {}

        render_time = time.time() - self.interpolation_delay

        # Find bracketing states
        for i in range(len(self.state_buffer) - 1):
            t0 = self.state_buffer[i]["timestamp"]
            t1 = self.state_buffer[i + 1]["timestamp"]

            if t0 <= render_time <= t1:
                # Interpolate
                alpha = (render_time - t0) / (t1 - t0) if t1 != t0 else 0
                return self.interpolate_states(
                    self.state_buffer[i], self.state_buffer[i + 1], alpha
                )

        # Return most recent if no match
        return self.state_buffer[-1]

    def interpolate_states(self, state0: Dict, state1: Dict, alpha: float) -> Dict:
        """Interpolate between two states."""
        result = {
            "timestamp": state0["timestamp"] * (1 - alpha) + state1["timestamp"] * alpha
        }

        # Interpolate player data
        if "players" in state0 and "players" in state1:
            result["players"] = []

            for p0 in state0["players"]:
                # Find matching player in state1
                p1 = next((p for p in state1["players"] if p["id"] == p0["id"]), None)

                if p1:
                    interpolated = {
                        "id": p0["id"],
                        "name": p0["name"],
                        "position": self.lerp_list(
                            p0["position"], p1["position"], alpha
                        ),
                        "rotation": self.lerp_list(
                            p0["rotation"], p1["rotation"], alpha
                        ),
                        "velocity": self.lerp_list(
                            p0["velocity"], p1["velocity"], alpha
                        ),
                        "lap": p1["lap"],
                        "checkpoint": p1["checkpoint"],
                    }
                    result["players"].append(interpolated)

        return result

    def lerp_list(self, a: List[float], b: List[float], t: float) -> List[float]:
        """Linear interpolation between two lists."""
        return [a[i] + (b[i] - a[i]) * t for i in range(len(a))]

    def clear(self):
        """Clear the state buffer."""
        self.state_buffer.clear()


class ClientPrediction:
    """Client-side prediction for local player."""

    def __init__(self):
        self.predicted_position = [0, 0, 0]
        self.predicted_velocity = [0, 0, 0]
        self.input_history = []
        self.max_history = 60

    def predict(self, input_data: Dict[str, Any], dt: float):
        """Predict next state based on input."""
        # Simple prediction - would need proper physics
        self.input_history.append({"input": input_data, "timestamp": time.time()})

        if len(self.input_history) > self.max_history:
            self.input_history.pop(0)

    def reconcile(self, server_state: Dict[str, Any]):
        """Reconcile prediction with server state."""
        # Check difference between prediction and server
        # Re-simulate if needed
        pass

    def clear(self):
        """Clear prediction history."""
        self.input_history.clear()
