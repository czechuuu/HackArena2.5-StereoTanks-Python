"""This module contains the models used in the library.

For streamlined versions with better documentation
and only essential fields, refer to the protocols
which serve as interfaces for these models with enhanced clarity.

Some of the models contain weird attributes like __instancecheck_something__.
These are used to distinguish between different classes that have the same
data structure. This is necessary to allow using isinstance() with protocols.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING, Any

from .enums import BulletType, Direction, Orientation, TankType, WallType
from .payloads import (
    GameEndPayload,
    GameStatePayload,
    LobbyDataPayload,
    RawBullet,
    RawLaser,
    RawMap,
    RawMine,
    RawPlayer,
    RawTank,
    RawTeam,
    RawTurret,
    RawWall,
    RawZone,
    ServerSettings,
)


@dataclass(slots=True, frozen=True)
class TeamModel:
    """Represents a team model."""

    name: str
    color: int
    players: list[PlayerModel]
    score: int | None = None

    @classmethod
    def from_raw(cls, raw: RawTeam) -> TeamModel:
        """Creates a team from a raw team payload."""
        data = asdict(raw)
        players = [PlayerModel.from_raw(p) for p in raw.players]
        return cls(data["name"], data["color"], players, data.get("score", None))


@dataclass(slots=True, frozen=True)
class PlayerModel:  # pylint: disable=too-many-instance-attributes
    """Represents a player model."""

    id: str
    tank_type: TankType
    kills: int | None = None
    ping: int | None = None
    ticks_to_regenerate: int | None = None

    @classmethod
    def from_raw(cls, raw: RawPlayer) -> PlayerModel:
        """Creates a player from a raw player payload."""
        data = asdict(raw)
        data["ticks_to_regenerate"] = data.pop("ticks_to_regen", None)
        return cls(**data)


@dataclass(slots=True, frozen=True)
class TurretModel:
    """Represents a turret model."""

    direction: Direction
    bullet_count: int | None = None
    ticks_to_bullet: int | None = None
    ticks_to_double_bullet: int | None = None
    ticks_to_healing_bullet: int | None = None
    ticks_to_stun_bullet: int | None = None
    ticks_to_laser: int | None = None

    @classmethod
    def from_raw(cls, raw: RawTurret) -> TurretModel:
        """Creates a turret from a raw turret payload."""
        data = asdict(raw)
        data["direction"] = Direction(data["direction"])
        return cls(**data)


@dataclass(slots=True, frozen=True)
class TankModel:  # pylint: disable=too-many-instance-attributes
    """Represents a tank model."""

    __instancecheck_tank__ = True

    owner_id: str
    type: TankType
    direction: Direction
    turret: TurretModel
    health: int | None = None
    ticks_to_mine: int | None = None
    ticks_to_radar: int | None = None
    is_using_radar: bool | None = None
    visibility: tuple[tuple[bool, ...], ...] | None = None

    @classmethod
    def from_raw(cls, raw: RawTank) -> TankModel:
        """Creates a tank from a raw tank payload."""
        data = asdict(raw)
        data["type"] = TankType(data["type"])
        data["direction"] = Direction(data["direction"])
        data["turret"] = TurretModel.from_raw(raw.turret)
        if raw.visibility is not None:
            data["visibility"] = tuple(
                tuple(c == "1" for c in row) for row in raw.visibility
            )
        return cls(**data)


@dataclass(slots=True, frozen=True)
class WallModel:
    """Represents a wall model."""

    __instancecheck_wall__ = True

    type: WallType

    @classmethod
    def from_raw(cls, raw: RawWall) -> WallModel:
        """Creates a wall from a wall model payload."""
        data = asdict(raw)
        data["type"] = WallType(data["type"])
        return cls(**data)


@dataclass(slots=True, frozen=True)
class BulletModel:
    """Represents a bullet model."""

    __instancecheck_bullet__ = True

    id: int
    speed: float
    direction: Direction
    type: BulletType

    @classmethod
    def from_raw(cls, raw: RawBullet) -> BulletModel:
        """Creates a bullet from a raw bullet payload."""

        data = asdict(raw)
        data["direction"] = Direction(data["direction"])
        data["type"] = BulletType(data["type"])
        return cls(**data)


@dataclass(slots=True, frozen=True)
class LaserModel:
    """Represents a laser model."""

    __instancecheck_laser__ = True

    id: int
    orientation: Orientation

    @classmethod
    def from_raw(cls, raw: RawLaser) -> LaserModel:
        """Creates a laser from a raw laser payload."""
        data = asdict(raw)
        data["orientation"] = Orientation(data["orientation"])
        return cls(**data)


@dataclass(slots=True, frozen=True)
class MineModel:
    """Represents a mine model."""

    __instancecheck_mine__ = True

    id: int
    explosion_remaining_ticks: int | None

    @property
    def exploded(self) -> bool:
        """Whether the mine has exploded."""
        return self.explosion_remaining_ticks is not None

    @classmethod
    def from_raw(cls, raw: RawMine) -> MineModel:
        """Creates a mine from a raw mine payload."""
        return cls(**asdict(raw))


@dataclass(slots=True, frozen=True)
class ZoneModel(ABC):  # pylint: disable=too-many-instance-attributes
    """Represents a zone model."""

    x: int
    y: int
    width: int
    height: int
    index: int
    shares: dict[str, float]

    @classmethod
    def from_raw(cls, raw: RawZone) -> ZoneModel:
        """Creates a zone from a raw zone payload."""
        data = asdict(raw)
        data["shares"] = data.get("shares", {})
        return ZoneModel(**data)


@dataclass(slots=True, frozen=True)
class LobbyDataModel:
    """Represents the lobby data model."""

    player_id: str
    team_name: str
    teams: tuple[TeamModel, ...]
    server_settings: ServerSettings

    @property
    def my_id(self) -> str:
        """Your player ID."""
        return self.player_id

    @classmethod
    def from_payload(cls, payload: LobbyDataPayload) -> LobbyDataModel:
        """Creates a lobby data from a lobby data payload."""
        teams = tuple(TeamModel.from_raw(t) for t in payload.teams)
        return cls(payload.player_id, payload.team_name, teams, payload.server_settings)


if TYPE_CHECKING:
    TileEntity = TankModel | WallModel | BulletModel | LaserModel | MineModel


@dataclass(slots=True, frozen=True)
class TileModel:
    """Represents a tile model on the map."""

    entities: list[TileEntity]
    zone: ZoneModel | None


@dataclass(slots=True, frozen=True)
class MapModel:
    """Represents a map model."""

    tiles: tuple[tuple[TileModel, ...], ...]
    zones: tuple[ZoneModel, ...]

    @classmethod
    def from_raw(cls, raw: RawMap) -> MapModel:  # pylint: disable=too-many-locals
        """Creates a map from a raw map payload."""
        zones = tuple(ZoneModel.from_raw(z) for z in raw.zones)

        tiles: list[tuple[TileModel, ...]] = []
        for x, row in enumerate(raw.tiles):
            tab: list[TileModel] = []
            for y, raw_tile in enumerate(row):
                objects: list[Any] = []
                for obj in raw_tile:
                    entity = obj.entity
                    if isinstance(entity, RawTank):
                        objects.append(TankModel.from_raw(entity))
                    elif isinstance(entity, RawWall):
                        objects.append(WallModel.from_raw(entity))
                    elif isinstance(entity, RawBullet):
                        objects.append(BulletModel.from_raw(entity))
                    elif isinstance(entity, RawLaser):
                        objects.append(LaserModel.from_raw(entity))
                    elif isinstance(entity, RawMine):
                        objects.append(MineModel.from_raw(entity))
                    else:
                        raise ValueError(f"Unknown tile type: {obj.type}")

                zone = next(
                    (
                        z
                        for z in zones
                        if z.x <= x < z.x + z.width and z.y <= y < z.y + z.height
                    ),
                    None,
                )

                tab.append(TileModel(objects, zone))
            tiles.append(tuple(tab))

        tiles = [
            tuple(tiles[y][x] for y in range(len(tiles))) for x in range(len(tiles[0]))
        ]

        return MapModel(tuple(tiles), tuple(zones))


@dataclass(slots=True, frozen=True)
class GameStateModel:
    """Represents a game state model."""

    id: str
    tick: int
    player_id: str
    teams: tuple[TeamModel, ...]
    map: MapModel

    @property
    def my_id(self) -> str:
        """Your player ID."""
        return self.player_id

    @classmethod
    def from_payload(cls, payload: GameStatePayload) -> GameStateModel:
        """Creates a game state from a game state payload."""

        teams = tuple(TeamModel.from_raw(t) for t in payload.teams)

        return cls(
            id=payload.id,
            tick=payload.tick,
            player_id=payload.player_id,
            teams=teams,
            map=MapModel.from_raw(payload.map),
        )


@dataclass(slots=True, frozen=True)
class GameResultModel:
    """Represents the game results model."""

    teams: tuple[TeamModel, ...]

    @classmethod
    def from_payload(cls, payload: GameEndPayload) -> GameResultModel:
        """Creates game results from a game end payload."""
        teams = tuple(TeamModel.from_raw(t) for t in payload.teams)
        return cls(teams)
