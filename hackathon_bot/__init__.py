"""
StereoTanks API Wrapper
-----------------------

A wrapper for the HackArena 2.5 - StereoTanks game.
"""

__title__ = "HackArena2.5-StereoTanks-Python"
__author__ = "KN init"
__copyright__ = "2025 KN init"
__license__ = "GPL-3.0"
__version__ = "1.0.0-beta.1"

from .actions import *
from .enums import *
from .hackathon_bot import StereoTanksBot  # type: ignore[no-redef]
from .protocols import *
