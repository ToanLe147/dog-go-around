"""Input mapping and rebinding system."""

from typing import Dict, Any


class InputMap:
    """Key binding map and rebinding helpers."""

    def __init__(self):
        """Initialize input map with defaults."""
        self.bindings = {
            "throttle_forward": ["w", "up arrow"],
            "throttle_backward": ["s", "down arrow"],
            "steer_left": ["a", "left arrow"],
            "steer_right": ["d", "right arrow"],
            "handbrake": ["space"],
            "boost": ["left shift"],
            "reset": ["r"],
            "camera_toggle": ["c"],
            "chat": ["t"],
            "pause": ["escape"],
            "debug": ["f1"],
        }

        # Custom bindings (overrides defaults)
        self.custom_bindings: Dict[str, list] = {}

    def get_binding(self, action: str) -> list:
        """Get keys bound to an action."""
        if action in self.custom_bindings:
            return self.custom_bindings[action]
        return self.bindings.get(action, [])

    def set_binding(self, action: str, keys: list):
        """Set custom binding for an action."""
        self.custom_bindings[action] = keys

    def reset_binding(self, action: str):
        """Reset binding to default."""
        if action in self.custom_bindings:
            del self.custom_bindings[action]

    def reset_all(self):
        """Reset all bindings to defaults."""
        self.custom_bindings.clear()

    def is_action_pressed(self, action: str, held_keys: Dict) -> bool:
        """Check if any key for this action is pressed."""
        keys = self.get_binding(action)
        return any(held_keys.get(key, False) for key in keys)

    def save_to_file(self, filepath: str):
        """Save custom bindings to file."""
        import json

        with open(filepath, "w") as f:
            json.dump(self.custom_bindings, f, indent=2)

    def load_from_file(self, filepath: str):
        """Load custom bindings from file."""
        import json

        try:
            with open(filepath, "r") as f:
                self.custom_bindings = json.load(f)
        except FileNotFoundError:
            pass

    def get_all_bindings(self) -> Dict[str, list]:
        """Get all current bindings (default + custom)."""
        result = self.bindings.copy()
        result.update(self.custom_bindings)
        return result
