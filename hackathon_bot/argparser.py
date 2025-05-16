"""This module provides the command line argument parser.

The command line argument parser is used to parse the command line arguments
when starting the hackathon bot.

Functions
---------
get_args
    Parses the command line arguments.

Classes
-------
Arguments
    Represents the parsed arguments from the command line.
"""

import argparse
import sys
from dataclasses import dataclass

from .enums import TankType


@dataclass(slots=True, frozen=True)
class Arguments:
    """Represents a parsed arguments from the command line.

    Attributes
    ----------
    host: :class:`str`
        The host address.
    port: :class:`int`
        The port to connect to.
    code: :class:`str`
        The optional game code for joining specific lobby.
    team_name: :class:`str`
        The name of the team.
    tank_type: :class:`.TankType`
        The type of tank to use.
    """

    host: str
    port: int
    code: str | None
    team_name: str
    tank_type: TankType


def _tank_type_from_string(value: str) -> TankType:
    """Converts a string to a TankType enum value."""
    try:
        return TankType[value.upper()]
    except KeyError as e:
        raise argparse.ArgumentTypeError(
            f"Invalid tank type: {value}. Valid options are: {', '.join(t.name for t in TankType)}"
        ) from e


def get_args() -> Arguments:
    """Parses the command line arguments.

    Returns
    -------
    Arguments
        The parsed arguments from the command line.
    """

    parser = argparse.ArgumentParser(
        description="Game Client Argument Parser", add_help=False
    )

    parser.add_argument(
        "-h",
        "--host",
        type=str,
        default="localhost",
        help="Host address (default: localhost)",
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=5000,
        help="Port to connect to (default: 5000)",
    )

    parser.add_argument(
        "-c",
        "--code",
        type=str,
        default=None,
        help="Optional game code for joining specific lobby",
    )

    parser.add_argument(
        "-n",
        "--team-name",
        type=str,
        required=True,
        help="Team name (required)",
    )

    parser.add_argument(
        "-t",
        "--tank-type",
        type=_tank_type_from_string,
        required=True,
        help="Tank type (required) [LIGHT or HEAVY]",
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        sys.exit(1)

    return Arguments(
        host=args.host,
        port=args.port,
        code=args.code,
        team_name=args.team_name,
        tank_type=args.tank_type,
    )
