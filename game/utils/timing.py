"""Timing utilities for race and game timing."""

import time


class Timer:
    """Simple timer for tracking elapsed time."""

    def __init__(self):
        """Initialize timer."""
        self.start_time = 0
        self.pause_time = 0
        self.elapsed = 0
        self.running = False
        self.paused = False

    def start(self):
        """Start the timer."""
        self.start_time = time.time()
        self.running = True
        self.paused = False

    def stop(self):
        """Stop the timer."""
        if self.running:
            self.elapsed = self.get_elapsed()
            self.running = False

    def pause(self):
        """Pause the timer."""
        if self.running and not self.paused:
            self.pause_time = time.time()
            self.paused = True

    def resume(self):
        """Resume the timer."""
        if self.running and self.paused:
            pause_duration = time.time() - self.pause_time
            self.start_time += pause_duration
            self.paused = False

    def reset(self):
        """Reset the timer."""
        self.start_time = 0
        self.pause_time = 0
        self.elapsed = 0
        self.running = False
        self.paused = False

    def get_elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if not self.running:
            return self.elapsed

        if self.paused:
            return self.pause_time - self.start_time

        return time.time() - self.start_time

    def get_formatted(self) -> str:
        """Get formatted time string (MM:SS.mmm)."""
        elapsed = self.get_elapsed()
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 1000)
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


class LapTimer:
    """Timer for tracking lap times."""

    def __init__(self):
        """Initialize lap timer."""
        self.lap_times = []
        self.current_lap_timer = Timer()

    def start_lap(self):
        """Start timing a new lap."""
        self.current_lap_timer.reset()
        self.current_lap_timer.start()

    def finish_lap(self) -> float:
        """Finish current lap and record time."""
        lap_time = self.current_lap_timer.get_elapsed()
        self.lap_times.append(lap_time)
        self.current_lap_timer.reset()
        self.current_lap_timer.start()
        return lap_time

    def get_current_lap_time(self) -> float:
        """Get current lap elapsed time."""
        return self.current_lap_timer.get_elapsed()

    def get_lap_time(self, lap_number: int) -> float:
        """Get time for specific lap."""
        if 0 <= lap_number < len(self.lap_times):
            return self.lap_times[lap_number]
        return 0.0

    def get_best_lap(self) -> float:
        """Get best lap time."""
        return min(self.lap_times) if self.lap_times else 0.0

    def get_total_time(self) -> float:
        """Get total time for all laps."""
        return sum(self.lap_times) + self.current_lap_timer.get_elapsed()

    def reset(self):
        """Reset all lap times."""
        self.lap_times.clear()
        self.current_lap_timer.reset()


class Stopwatch:
    """Simple stopwatch utility."""

    def __init__(self, name="Stopwatch"):
        """Initialize stopwatch."""
        self.name = name
        self.start_time = None

    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        """Stop timing and print result."""
        elapsed = time.time() - self.start_time
        print(f"{self.name}: {elapsed:.4f}s")

    @staticmethod
    def measure(func):
        """Decorator to measure function execution time."""

        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
            return result

        return wrapper
