"""A module that contains the payloads used in the library.

This module contains the payloads that are used to represent the data
that is sent and received between the client and the server.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

import humps

if TYPE_CHECKING:
    from .actions import GoTo

# pylint: disable=too-many-instance-attributes


@dataclass(slots=True, frozen=True)
class ServerSettings:
    """Represents the server settings."""

    grid_dimension: int
    number_of_players: int
    seed: int
    ticks: int | None
    broadcast_interval: int
    sandbox_mode: bool
    eager_broadcast: bool
    match_name: str | None
    version: str


@dataclass(slots=True, frozen=True)
class RawTeam:
    """Represents a raw team data."""

    name: str
    color: int
    score: int | None = None
    players: tuple[RawPlayer, ...] = field(default_factory=tuple)

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawTeam:
        """Creates a RawTeam from a JSON dictionary."""
        json_data["players"] = tuple(
            RawPlayer.from_json(p) for p in json_data["players"]
        )
        self = cls(**json_data)
        return self


@dataclass(slots=True, frozen=True)
class RawPlayer:
    """Represents a raw player data."""

    id: str
    kills: int | None = None
    ping: int | None = None
    ticks_to_regen: int | None = None
    tank_type: int | None = None

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawPlayer:
        """Creates a RawPlayer from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawMap:
    """Represents a raw map data."""

    tiles: tuple[tuple[tuple[RawTileObject, ...], ...], ...]
    zones: tuple[RawZone, ...]

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawMap:
        """Creates a RawMap from a JSON dictionary."""

        json_data["tiles"] = tuple(
            tuple(tuple(RawTileObject.from_json(obj) for obj in tile) for tile in row)
            for row in json_data["tiles"]
        )
        json_data["zones"] = tuple(
            RawZone.from_json(zone) for zone in json_data["zones"]
        )
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawTileObject:
    """Represents a raw tile object data."""

    type: str
    entity: RawTileEntity

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawTileObject:
        """Creates a RawTileObject from a JSON dictionary."""

        obj_type = json_data.pop("type")

        payload_class_name = f"Raw{humps.pascalize(obj_type)}"
        payload_class = globals().get(payload_class_name)

        if payload_class is None or not issubclass(payload_class, RawTileEntity):
            raise ValueError(f"Unknown tile object class: {payload_class_name}")

        entity = payload_class.from_json(json_data.get("payload", {}))

        return cls(obj_type, entity)


@dataclass(slots=True, frozen=True)
class RawTileEntity(ABC):
    """Represents a raw tile entity data."""

    @classmethod
    @abstractmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawTileEntity:
        """Creates a payload from a JSON dictionary."""


@dataclass(slots=True, frozen=True)
class RawWall(RawTileEntity):
    """Represents a raw wall data."""

    type: int

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawWall:
        """Creates a RawWall from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawBullet(RawTileEntity):
    """Represents a raw bullet data."""

    id: int
    speed: int | None
    direction: int | None
    type: int

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawBullet:
        """Creates a RawBullet from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawLaser(RawTileEntity):
    """Represents a raw laser data."""

    id: int
    orientation: int

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawLaser:
        """Creates a RawLaser from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawMine(RawTileEntity):
    """Represents a raw mine data."""

    id: int
    explosion_remaining_ticks: int | None = None

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawMine:
        """Creates a RawMine from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawTank(RawTileEntity):
    """Represents a raw tank data."""

    owner_id: str
    type: int
    direction: int
    turret: RawTurret
    health: int | None = None
    ticks_to_radar: int | None = None
    is_using_radar: bool | None = None
    ticks_to_mine: int | None = None
    visibility: tuple[str, ...] | None = None

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawTank:
        """Creates a RawTank from a JSON dictionary."""
        json_data["turret"] = RawTurret.from_json(json_data["turret"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawTurret:
    """Represents a raw turret data."""

    direction: int
    bullet_count: int | None = None
    ticks_to_bullet: int | None = None
    ticks_to_double_bullet: int | None = None
    ticks_to_laser: int | None = None
    ticks_to_healing_bullet: int | None = None
    ticks_to_stun_bullet: int | None = None

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawTurret:
        """Creates a RawTurret from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class RawZone:
    """Represents a raw zone data."""

    x: int
    y: int
    width: int
    height: int
    index: int
    shares: dict[str, float]

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> RawZone:
        """Creates a RawZone from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class Payload(dict[str, Any], ABC):  # pylint: disable=too-few-public-methods
    """Represents a payload that can be attached to a packet."""


@dataclass(slots=True, frozen=True)
class ConnectionRejectedPayload(Payload):
    """Represents a CONNECTION_REJECTED payload."""

    reason: str

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> ConnectionRejectedPayload:
        """Creates a ConnectionRejectedPayload from a JSON dictionary."""
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class LobbyDataPayload(Payload):
    """Represents a LOBBY_DATA payload."""

    player_id: str
    team_name: str
    teams: tuple[RawTeam, ...]
    server_settings: ServerSettings

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> LobbyDataPayload:
        """Creates a LobbyDataPayload from a JSON dictionary."""
        json_data["teams"] = tuple(RawTeam.from_json(t) for t in json_data["teams"])
        json_data["server_settings"] = ServerSettings(**json_data["server_settings"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class GameStatePayload(Payload):
    """Represents a GAME_STATE payload."""

    id: str
    tick: int
    player_id: str
    teams: tuple[RawTeam, ...]
    map: RawMap

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> GameStatePayload:
        """Creates a GameStatePayload from a JSON dictionary."""
        json_data["teams"] = tuple(RawTeam.from_json(t) for t in json_data["teams"])
        json_data["map"] = RawMap.from_json(json_data["map"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class GameEndPayload(Payload):
    """Represents a GAME_END payload."""

    teams: tuple[RawTeam, ...]

    @classmethod
    def from_json(cls, json_data: dict[str, Any]) -> GameEndPayload:
        """Creates a GameEndPayload from a JSON dictionary."""
        json_data["teams"] = tuple(RawTeam.from_json(t) for t in json_data["teams"])
        return cls(**json_data)


@dataclass(slots=True, frozen=True)
class ResponseActionPayload(Payload, ABC):
    """Represents a response action payload."""

    game_state_id: str


@dataclass(slots=True, frozen=True)
class MovementPayload(ResponseActionPayload):
    """Represents a MOVEMENT payload."""

    direction: int


@dataclass(slots=True, frozen=True)
class RotationPayload(ResponseActionPayload):
    """Represents a ROTATION payload."""

    tank_rotation: int | None
    turret_rotation: int | None


@dataclass(slots=True, frozen=True)
class AbilityUsePayload(ResponseActionPayload):
    """Represents an ABILITY_USE payload."""

    ability_type: int


@dataclass(slots=True, frozen=True)
class CaptureZonePayload(ResponseActionPayload):
    """Represents a CAPTURE_ZONE payload."""


@dataclass(slots=True, frozen=True)
class GoToPayload(ResponseActionPayload):
    """Represents a GO_TO payload."""

    x: int
    y: int
    turret_rotation: int | None
    costs: GoTo.Costs
    penalties: GoTo.Penalties


@dataclass(slots=True, frozen=True)
class PassPayload(ResponseActionPayload):
    """Represents a PASS payload."""
