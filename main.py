"""Pygbag entry point for web deployment.

This file must be at the project root and named main.py for pygbag to work.
It uses asyncio to yield control to the browser event loop.
"""

import asyncio
import sys
from pathlib import Path

# Add src to path so we can import the package
src_path = Path(__file__).parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from dog_go_around.cli import async_main


# Pygbag will call this automatically
if __name__ == "__main__":
    asyncio.run(async_main(fullscreen=False))
