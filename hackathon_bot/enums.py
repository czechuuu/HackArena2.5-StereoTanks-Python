"""This module contains the enums used in the library.

Enums
-----
TankType
    Represents a tank type.
Direction
    Represents a direction.
MovementDirection
    Represents a movement direction.
RotationDirection
    Represents a rotation direction.
Orientation
    Represents an orientation.
SecondaryItemType
    Represents a secondary item type.
ItemType
    Represents an item type on the tile.
Ability
    Represents an ability.
PacketType
    Represents a type of a packet.
WarningType
    Represents a type of a warning.
"""

from enum import IntEnum

__all__ = (
    "TankType",
    "Direction",
    "MovementDirection",
    "RotationDirection",
    "Orientation",
    "Ability",
    "PacketType",
    "WarningType",
)


class TankType(IntEnum):
    """Represents a tank type.

    Attributes
    ----------
    LIGHT: :class:`int`
        Represents a light tank type.
    HEAVY: :class:`int`
        Represents a heavy tank type.
    """

    LIGHT = 0
    HEAVY = 1


class Direction(IntEnum):
    """Represents a direction.

    Attributes
    ----------
    UP: :class:`int`
        Represents an upward direction.
    RIGHT: :class:`int`
        Represents a right direction.
    DOWN: :class:`int`
        Represents a down direction.
    LEFT: :class:`int`
        Represents a left direction.
    """

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class MovementDirection(IntEnum):
    """Represents a movement direction.

    Attributes
    ----------
    FORWARD: :class:`int`
        Represents a forward direction.
    BACKWARD: :class:`int`
        Represents a backward direction.
    """

    FORWARD = 0
    BACKWARD = 1


class RotationDirection(IntEnum):
    """Represents a rotation direction.

    Attributes
    ----------
    LEFT: :class:`int`
        Represents a left rotation
        direction (counter-clockwise).
    RIGHT: :class:`int`
        Represents a right rotation
        direction (clockwise)."""

    LEFT = 0
    RIGHT = 1


class Orientation(IntEnum):
    """Represents an orientation.

    Attributes
    ----------
    HORIZONTAL: :class:`int`
        Represents a horizontal orientation.
    VERTICAL: :class:`int`
        Represents a vertical orientation.
    """

    HORIZONTAL = 0
    VERTICAL = 1


class WallType(IntEnum):
    """Represents a wall type.

    Attributes
    ----------
    SOLID: :class:`int`
        Represents a solid wall type.
    PENETRABLE: :class:`int`
        Represents a penetrable wall type.
    """

    SOLID = 0
    PENETRABLE = 1


class BulletType(IntEnum):
    """Represents a bullet type.

    Attributes
    ----------
    BASIC: :class:`int`
        Represents a basic bullet type.
    DOUBLE: :class:`int`
        Represents a double bullet type.
    HEALING: :class:`int`
        Represents a healing bullet type.
    STUN: :class:`int`
        Represents a stun bullet type.
    """

    BASIC = 0
    DOUBLE = 1
    HEALING = 2
    STUN = 3


class Ability(IntEnum):
    """Represents an ability.

    Attributes
    ----------
    FIRE_BULLET: :class:`int`
        Represents a fire bullet ability.
    USE_LASER: :class:`int`
        Represents a laser usage ability.
    FIRE_DOUBLE_BULLET: :class:`int`
        Represents a double bullet firing ability.
    USE_RADAR: :class:`int`
        Represents a radar usage ability.
    DROP_MINE: :class:`int`
        Represents a mine dropping ability.
    FIRE_HEALING_BULLET: :class:`int`
        Represents a healing bullet firing ability.
    FIRE_STUN_BULLET: :class:`int`
        Represents a stun bullet firing ability.
    """

    FIRE_BULLET = 0
    USE_LASER = 1
    FIRE_DOUBLE_BULLET = 2
    USE_RADAR = 3
    DROP_MINE = 4
    FIRE_HEALING_BULLET = 5
    FIRE_STUN_BULLET = 6


class PacketType(IntEnum):
    """Represents a type of a packet.

    Each packet type is represented by a 8-bit integer.

    Attributes
    ----------
    UNKNOWN: :class:`int`
        Represents an unknown packet type.
    HAS_PAYLOAD: :class:`int`
        Represents a flag that indicates that the packet has a payload.
    COMMUNICATION_GROUP: :class:`int`
        Represents a group for communication packets.
    PING: :class:`int`
        Represents a ping packet.
    PONG: :class:`int`
        Represents a pong packet.
    CONNECTION_ACCEPTED: :class:`int`
        Represents a connection accepted packet.
    CONNECTION_REJECTED: :class:`int`
        Represents a connection rejected packet.
    LOBBY_GROUP: :class:`int`
        Represents a group for lobby packets.
    LOBBY_DATA: :class:`int`
        Represents a lobby data packet.
    LOBBY_DATA_REQUEST: :class:`int`
        Represents a lobby data request packet.
    GAME_STATE_GROUP: :class:`int`
        Represents a group for game state packets.
    GAME_STATE: :class:`int`
        Represents a game state packet.
    READY_TO_RECEIVE_GAME_STATE: :class:`int`
        Represents a ready to receive game state packet.
    PLAYER_RESPONSE_ACTION_GROUP: :class:`int`
        Represents a group for player response action packets.
    MOVEMENT: :class:`int`
        Represents a movement response packet.
    ROTATION: :class:`int`
        Represents a rotation response packet.
    ABILITY_USE: :class:`int`
        Represents an ability use response packet.
    CAPTURE_ZONE: :class:`int`
        Represents a capture zone response packet.
    GO_TO: :class:`int`
        Represents a go to response packet.
    PASS: :class:`int`
        Represents a pass response packet.
    GAME_STATUS_GROUP: :class:`int`
        Represents a group for game status packets.
    GAME_NOT_STARTED: :class:`int`
        Represents a game not started packet.
    GAME_STARTING: :class:`int`
        Represents a game starting packet.
    GAME_STARTED: :class:`int`
        Represents a game started packet.
    GAME_IN_PROGRESS: :class:`int`
        Represents a game in progress packet.
    GAME_ENDED: :class:`int`
        Represents a game ended packet.
    GAME_STATUS_REQUEST: :class:`int`
        Represents a game status request packet.
    WARNING_GROUP: :class:`int`
        Represents a 4-bit group for warning packets.
    CUSTOM_WARNING: :class:`int`
        Represents a custom warning packet.
    PLAYER_ALREADY_MADE_ACTION_WARNING: :class:`int`
        Represents a player already made action warning packet.
    ACTION_IGNORED_DUE_TO_DEAD_WARNING: :class:`int`
        Represents an action ignored due to dead warning packet.
    SLOW_RESPONSE_WARNING: :class:`int`
        Represents a slow response warning packet.
    ERROR_GROUP: :class:`int`
        Represents a 4-bit group for error packets.

    Notes
    -----
    The packet types are represented as follows
    (starting from the most significant bit):

    - The first 4 bits represent the group.
    - The 5th bit represents the payload flag.
    - The last 3 bits represent the type.
    """

    UNKNOWN = 0x0

    HAS_PAYLOAD = 0x8

    COMMUNICATION_GROUP = 0x10
    PING = COMMUNICATION_GROUP | 0x1
    PONG = COMMUNICATION_GROUP | 0x2
    CONNECTION_ACCEPTED = COMMUNICATION_GROUP | 0x3
    CONNECTION_REJECTED = COMMUNICATION_GROUP | HAS_PAYLOAD | 0x4

    LOBBY_GROUP = 0x20
    LOBBY_DATA = LOBBY_GROUP | HAS_PAYLOAD | 0x1
    LOBBY_DATA_REQUEST = LOBBY_GROUP | 0x2

    GAME_STATE_GROUP = 0x30
    GAME_STATE = GAME_STATE_GROUP | HAS_PAYLOAD | 0x2
    READY_TO_RECEIVE_GAME_STATE = GAME_STATE_GROUP | 0x5

    PLAYER_RESPONSE_ACTION_GROUP = 0x40
    MOVEMENT = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x1
    ROTATION = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x2
    ABILITY_USE = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x3
    CAPTURE_ZONE = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x4
    GO_TO = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x6
    PASS = PLAYER_RESPONSE_ACTION_GROUP | HAS_PAYLOAD | 0x7

    GAME_STATUS_GROUP = 0x50
    GAME_NOT_STARTED = GAME_STATUS_GROUP | 0x1
    GAME_STARTING = GAME_STATUS_GROUP | 0x2
    GAME_STARTED = GAME_STATUS_GROUP | 0x3
    GAME_IN_PROGRESS = GAME_STATUS_GROUP | 0x4
    GAME_ENDED = GAME_STATUS_GROUP | HAS_PAYLOAD | 0x5
    GAME_STATUS_REQUEST = GAME_STATUS_GROUP | 0x7

    WARNING_GROUP = 0xE0
    CUSTOM_WARNING = WARNING_GROUP | HAS_PAYLOAD | 0x1
    PLAYER_ALREADY_MADE_ACTION_WARNING = WARNING_GROUP | 0x2
    ACTION_IGNORED_DUE_TO_DEAD_WARNING = WARNING_GROUP | 0x3
    SLOW_RESPONSE_WARNING = WARNING_GROUP | 0x4

    ERROR_GROUP = 0xF0


class WarningType(IntEnum):
    """Represents a type of a warning.

    Attributes
    ----------
    CUSTOM: :class:`int`
        Represents a custom warning.
    PLAYER_ALREADY_MADE_ACTION: :class:`int`
        Represents a player already made action warning.
    ACTION_IGNORED_DUE_TO_DEAD: :class:`int`
        Represents an action ignored due to dead warning.
    SLOW_RESPONSE: :class:`int`
        Represents a slow response warning.
    """

    CUSTOM = PacketType.CUSTOM_WARNING
    PLAYER_ALREADY_MADE_ACTION = PacketType.PLAYER_ALREADY_MADE_ACTION_WARNING
    ACTION_IGNORED_DUE_TO_DEAD = PacketType.ACTION_IGNORED_DUE_TO_DEAD_WARNING
    SLOW_RESPONSE = PacketType.SLOW_RESPONSE_WARNING
