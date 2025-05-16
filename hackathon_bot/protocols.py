"""A module that contains the protocols used in the library.

Some of the protocols contain weird attributes like __instancecheck_something__.
These are used to distinguish between different classes that have the same
data structure. This is necessary to enable isinstance() to be used with protocols.
To take advantage of this, the models should have the same weird attribute as the protocol.

Notes
-----
Protocols are used to provide type hints for the classes
in the game state, lobby data, and game result.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Sequence, runtime_checkable

from hackathon_bot.enums import TankType, WallType

if TYPE_CHECKING:
    from hackathon_bot.enums import BulletType, Direction, Orientation


# pylint: disable=too-few-public-methods

__all__ = (
    "ServerSettings",
    "GameStatePlayer",
    "LobbyPlayer",
    "GameEndPlayer",
    "Turret",
    "Tank",
    "Wall",
    "Bullet",
    "Laser",
    "Mine",
    "Tile",
    "LobbyData",
    "Zone",
    "Map",
    "GameState",
    "GameResult",
    "GameStateTeam",
    "LobbyTeam",
    "GameEndTeam",
)


class ServerSettings(Protocol):
    """Represents the server settings.

    Attributes
    ----------
    grid_dimension: :class:`int`
        The grid dimension.
    number_of_players: :class:`int`
        The number of players.
    seed: :class:`int`
        The seed of the game.
    ticks: :class:`int` | `None`
        The number of game ticks.
    broadcast_interval: :class:`int`
        The broadcast interval in milliseconds.
    sandbox_mode: :class:`bool`
        Whether the game is in sandbox mode.
    match_name: :class:`str` | `None`
        The name of the match.
    eager_broadcast: :class:`bool`
        Whether to eager broadcast is enabled.
    version: :class:`str`
        The version of the server.
    """

    @property
    def grid_dimension(self) -> int:
        """The grid dimension."""
        raise NotImplementedError

    @property
    def number_of_players(self) -> int:
        """The number of players."""
        raise NotImplementedError

    @property
    def seed(self) -> int:
        """The seed of the game."""
        raise NotImplementedError

    @property
    def ticks(self) -> int | None:
        """The number of game ticks.

        For example, if the number of ticks is 2000,
        and the broadcast interval is 50 milliseconds,
        the game will last for 100 seconds (2000 / (1000 / 50))

        If sandbox mode is enabled, this value is `None`.
        """
        raise NotImplementedError

    @property
    def broadcast_interval(self) -> int:
        """The broadcast interval.

        The interval in milliseconds between
        each broadcast game state.
        """
        raise NotImplementedError

    @property
    def sandbox_mode(self) -> bool:
        """Whether the game is in sandbox mode."""
        raise NotImplementedError

    @property
    def eager_broadcast(self) -> bool:
        """Whether eager broadcast is enabled.

        If `True`, the server will broadcast the game state
        immediately after all players respond to the latest game state.

        If `False`, the server will broadcast the game state
        after the broadcast interval.

        This allows for a shorter waiting time for the next broadcast
        if all players respond to the latest game state.

        As a **participant of Hackathon**, you can **ignore this**.
        """
        raise NotImplementedError

    @property
    def match_name(self) -> str | None:
        """The name of the match."""
        raise NotImplementedError

    @property
    def version(self) -> str:
        """The version of the server."""
        raise NotImplementedError


class GameStateTeam(Protocol):
    """Represents a team.

    Attributes
    ----------
    name: :class:`str`
        The name of the team.
    color: :class:`int`
        The color of the team in format `0xAABBGGRR`.
    players: Sequence[:class:`GameStatePlayer`]
        The sequence of players in the team.
    """

    @property
    def name(self) -> str:
        """The name of the team."""
        raise NotImplementedError

    @property
    def color(self) -> int:
        """The color of the team in format `0xAABBGGRR`."""
        raise NotImplementedError

    @property
    def players(self) -> Sequence[GameStatePlayer]:
        """The players in the team."""
        raise NotImplementedError


class GameStatePlayer(Protocol):
    """Represents a player in the game.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    ping: :class:`int`
        The ping of the player.
    ticks_to_regenerate: :class:`int` | `None`
        The number of ticks to regenerate the player's tank.
        It is `None` for players in opposition team.
        If `None` for your team, the player is not dead.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""
        raise NotImplementedError

    @property
    def ping(self) -> int:
        """The ping of the player."""
        raise NotImplementedError

    @property
    def ticks_to_regenerate(self) -> int | None:
        """The number of ticks to regenerate the player's tank.

        It is `None` for players in opposition team.

        If `None` for your team, the player is not dead.
        """
        raise NotImplementedError


class LobbyTeam(Protocol):
    """Represents a team in the lobby.

    Attributes
    ----------
    name: :class:`str`
        The name of the team.
    color: :class:`int`
        The color of the team in format `0xAABBGGRR`.
    players: Sequence[:class:`LobbyPlayer`]
        The sequence of players in the team.
    """

    @property
    def name(self) -> str:
        """The name of the team."""
        raise NotImplementedError

    @property
    def color(self) -> int:
        """The color of the team in format `0xAABBGGRR`."""
        raise NotImplementedError

    @property
    def players(self) -> Sequence[LobbyPlayer]:
        """The players in the team."""
        raise NotImplementedError


class LobbyPlayer(Protocol):
    """Represents a player in the lobby.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    tank_type: :class:`str`
        The type of the tank.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""
        raise NotImplementedError

    @property
    def tank_type(self) -> TankType:
        """The type of the tank."""
        raise NotImplementedError


class GameEndTeam(Protocol):
    """Represents a team in the game result.

    Attributes
    ----------
    name: :class:`str`
        The name of the team.
    color: :class:`int`
        The color of the team in format `0xAABBGGRR`.
    score: :class:`int`
        The score of the team.
    players: Sequence[:class:`GameEndPlayer`]
        The sequence of players in the team.
    """

    @property
    def name(self) -> str:
        """The name of the team."""
        raise NotImplementedError

    @property
    def color(self) -> int:
        """The color of the team in format `0xAABBGGRR`."""
        raise NotImplementedError

    @property
    def score(self) -> int:
        """The score of the team."""
        raise NotImplementedError

    @property
    def players(self) -> Sequence[GameEndPlayer]:
        """The players in the team."""
        raise NotImplementedError


class GameEndPlayer(Protocol):
    """Represents a player in the game result.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the player.
    kills: :class:`int`
        The number of players killed by the player.
    tank_type: :class:`str`
        The type of the tank.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the player."""
        raise NotImplementedError

    @property
    def kills(self) -> int:
        """The number of players killed by the player."""
        raise NotImplementedError

    @property
    def tank_type(self) -> TankType:
        """The type of the tank."""
        raise NotImplementedError


class Turret(Protocol):
    """Represents a turret of a player's tank.

    Attributes
    ----------
    direction: :class:`Direction`
        The direction of the turret.
    """

    @property
    def direction(self) -> Direction:
        """The direction of the turret."""
        raise NotImplementedError

    @property
    def bullet_count(self) -> int | None:
        """The number of bullets in the turret.

        It is `None` for players in opposition team.
        """
        raise NotImplementedError

    @property
    def ticks_to_bullet(self) -> int | None:
        """The number of ticks to regenerate a bullet in the turret.

        It is `None` for players in opposition team.

        If `None` for your team, the turret has full bullets.
        """
        raise NotImplementedError

    @property
    def ticks_to_double_bullet(self) -> int | None:
        """The number of ticks to regenerate a double bullet ability in the turret.

        It is `None` for players in opposition team.

        It is `None` for heavy tank.

        If `None` for your team, the turret has double bullet ability.
        """
        raise NotImplementedError

    @property
    def ticks_to_healing_bullet(self) -> int | None:
        """The number of ticks to regenerate a healing bullet ability in the turret.

        It is `None` for players in opposition team.

        If `None` for your team, the turret has healing bullet ability.
        """
        raise NotImplementedError

    @property
    def ticks_to_stun_bullet(self) -> int | None:
        """The number of ticks to regenerate a stun bullet ability in the turret.

        It is `None` for players in opposition team.

        If `None` for your team, the turret has stun bullet ability.
        """
        raise NotImplementedError

    @property
    def ticks_to_laser(self) -> int | None:
        """The number of ticks to regenerate a laser ability in the turret.

        It is `None` for players in opposition team.

        It is `None` for light tank.

        If `None` for your team, the turret has laser ability.
        """
        raise NotImplementedError


@runtime_checkable
class Tank(Protocol):
    """Represents a tank of a player.

    Attributes
    ----------
    owner_id: :class:`str`
        The unique identifier of the owner.
    direction: :class:`Direction`
        The direction of the tank.
    turret: :class:`Turret`
        The turret of the tank.
    """

    __instancecheck_tank__: bool

    @property
    def owner_id(self) -> str:
        """The unique identifier of the owner."""
        raise NotImplementedError

    @property
    def type(self) -> TankType:
        """The type of the tank."""
        raise NotImplementedError

    @property
    def direction(self) -> Direction:
        """The direction of the tank."""
        raise NotImplementedError

    @property
    def turret(self) -> Turret:
        """The turret of the tank."""
        raise NotImplementedError

    @property
    def health(self) -> int | None:
        """The health of the tank.

        It is `None` for players in opposition team.

        If `None` for your team, the tank is dead.
        """
        raise NotImplementedError

    @property
    def ticks_to_mine(self) -> int | None:
        """The number of ticks to regenerate a mine ability in the tank.

        It is `None` for players in opposition team.

        It is `None` for light tank.

        If `None` for your team, the tank has mine ability.
        """
        raise NotImplementedError

    @property
    def ticks_to_radar(self) -> int | None:
        """The number of ticks to regenerate a radar ability in the tank.

        It is `None` for players in opposition team.

        It is `None` for heavy tank.

        If `None` for your team, the tank has radar ability.
        """
        raise NotImplementedError

    @property
    def is_using_radar(self) -> bool | None:
        """Whether the tank is using radar ability.

        It is `None` for players in opposition team.

        It is `None` for heavy tank.

        If `None` for your team, the tank is not using radar ability.
        """
        raise NotImplementedError

    @property
    def visibility(self) -> tuple[tuple[bool, ...], ...] | None:
        """The visibility of the tank.

        It is `None` for players in opposition team.
        """
        raise NotImplementedError


@runtime_checkable
class Wall(Protocol):
    """Represents a wall in the game.

    Attributes
    ----------
    type: :class:`WallType`
        The type of the wall.
    """

    __instancecheck_wall__: bool

    @property
    def type(self) -> WallType:
        """The type of the wall."""
        raise NotImplementedError


@runtime_checkable
class Bullet(Protocol):
    """Represents a bullet in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the bullet.
    speed: :class:`float`
        The speed of the bullet.
    direction: :class:`Direction`
        The direction of the bullet.
    type: :class:`BulletType`
        The type of the bullet.
    """

    __instancecheck_bullet__: bool

    @property
    def id(self) -> int:
        """The unique identifier of the bullet."""
        raise NotImplementedError

    @property
    def speed(self) -> float:
        """The speed of the bullet."""
        raise NotImplementedError

    @property
    def direction(self) -> Direction:
        """The direction of the bullet."""
        raise NotImplementedError

    @property
    def type(self) -> BulletType:
        """The type of the bullet."""
        raise NotImplementedError


@runtime_checkable
class Laser(Protocol):
    """Represents a laser in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the laser.
    orientation: :class:`Orientation`
        The orientation of the laser.
    """

    __instancecheck_laser__: bool

    @property
    def id(self) -> int:
        """The unique identifier of the laser."""
        raise NotImplementedError

    @property
    def orientation(self) -> Orientation:
        """The orientation of the laser."""
        raise NotImplementedError


@runtime_checkable
class Mine(Protocol):
    """Represents a mine in the game.

    Attributes
    ----------
    id: :class:`int`
        The unique identifier of the mine.
    explosion_remaining_ticks: :class:`int`
        The remaining ticks to animate the mine explosion.
    exploded: :class:`bool`
        Whether the mine has exploded.
    """

    __instancecheck_mine__: bool

    @property
    def id(self) -> int:
        """The unique identifier of the mine."""
        raise NotImplementedError

    @property
    def explosion_remaining_ticks(self) -> int | None:
        """The remaining ticks to animate the mine explosion.

        This value is mainly used for visualization purposes,
        but you can use it if you have a strategy that depends on it.

        Take note that the mine explodes immediately after
        a tank enters the tile containing the mine.
        Then the remaining ticks start counting down.

        If `None`, the mine has not exploded yet.
        """
        raise NotImplementedError

    @property
    def exploded(self) -> bool:
        """Whether the mine has exploded.

        If `True`, the mine has exploded
        and only the explosion animation is visible.
        You can enter the tile containing the mine safely.
        """
        raise NotImplementedError


class Zone(Protocol):
    """Represents a zone in the game.

    Attributes
    ----------
    x: :class:`int`
        The x-coordinate of the zone.
    y: :class:`int`
        The y-coordinate of the zone.
    width: :class:`int`
        The width of the zone.
    height: :class:`int`
        The height of the zone.
    index: :class:`int`
        The index of the zone.
    shares: dict[:class:`str`, :class:`float`]
        The shares of the zone.
    """

    @property
    def x(self) -> int:
        """The x-coordinate of the zone."""
        raise NotImplementedError

    @property
    def y(self) -> int:
        """The y-coordinate of the zone."""
        raise NotImplementedError

    @property
    def width(self) -> int:
        """The width of the zone."""
        raise NotImplementedError

    @property
    def height(self) -> int:
        """The height of the zone."""
        raise NotImplementedError

    @property
    def index(self) -> int:
        """The index of the zone."""
        raise NotImplementedError

    @property
    def shares(self) -> dict[str, float]:
        """The shares of the zone.

        The keys are the names of the teams
        and the values are the shares of the zone (0.0 to 1.0).
        """
        raise NotImplementedError


class LobbyData(Protocol):
    """Represents the lobby data.

    Attributes
    ----------
    my_id: :class:`str`
        Your unique identifier.
    teams: Sequence[:class:`LobbyTeam`]
        The sequence of teams in the lobby.
    server_settings: :class:`ServerSettings`
        The server settings.
    """

    @property
    def my_id(self) -> str:
        """Your unique identifier."""
        raise NotImplementedError

    @property
    def teams(self) -> Sequence[LobbyTeam]:
        """The sequence of teams in the lobby."""
        raise NotImplementedError

    @property
    def server_settings(self) -> ServerSettings:
        """The server settings."""
        raise NotImplementedError


if TYPE_CHECKING:
    TileEntity = Tank | Wall | Bullet | Laser | Mine


class Tile(Protocol):
    """Represents a tile of the map.

    Attributes
    ----------
    entities: list[:class:`TileEntity`]
        The entities present on the tile.
    zone: :class:`Zone` | `None`
        The zone in the tile.
    """

    @property
    def entities(self) -> list[TileEntity]:
        """The entities present on the tile.

        The entity can be one of the following types:
        - :class:`Wall`
        - :class:`Bullet`
        - :class:`Laser`
        - :class:`Mine`
        - :class:`Tank`

        Examples
        --------

        To check the type of the entity in the tile,
        use the `isinstance` function.

        ::

            for entity in tile.entities:
                if isinstance(entity, Wall):
                    # The entity is a wall.
                elif isinstance(entity, Bullet):
                    # The entity is a bullet.
                elif isinstance(entity, Mine):
                    # The entity is a mine.
                elif isinstance(entity, Tank):
                    # The entity is a tank.

        If you have checked the type of the entity, you can easily access its attributes.

        ::

            for entity in tile.entities:
                if isinstance(entity, Mine):
                    >>> entity.exploded
                elif isinstance(entity, Tank):
                    >>> entity.owner_id
                    >>> entity.direction
                    >>> entity.turret.direction

        Without checking the type of the entity, the linter may suggest
        all attributes of the entities in the tile, which can be misleading.
        """
        raise NotImplementedError

    @property
    def zone(self) -> Zone | None:
        """The zone in the tile.

        If the tile does not contain a zone,
        this property is `None`.
        """
        raise NotImplementedError


class Map(Protocol):
    """Represents the map of the game state.

    Attributes
    ----------
    tiles: tuple[tuple[:class:`Tile`]]
        The tiles of the map in a 2D tuple,
        where the first index is the y-coordinate
        and the second index is the x-coordinate.
    zones: Sequence[:class:`Zone`]
        The zones on the map.
    """

    @property
    def tiles(self) -> tuple[tuple[Tile, ...], ...]:
        """The tiles of the map in a 2D tuple.

        The first index is the y-coordinate
        and the second index is the x-coordinate.
        """
        raise NotImplementedError

    @property
    def zones(self) -> tuple[Zone]:
        """The zones on the map."""
        raise NotImplementedError


class GameState(Protocol):
    """Represents the game state.

    Attributes
    ----------
    id: :class:`str`
        The unique identifier of the game state.
    tick: :class:`int`
        The tick of the game state.
    my_id: :class:`str`
        The unique identifier of your agent.
    teams: Sequence[:class:`GameStateTeam`]
        The sequence of teams in the game state.
    map: :class:`Map`
        The map of the game state.
    """

    @property
    def id(self) -> str:
        """The unique identifier of the game state.

        This identifier is required by the server when
        sending the response payload of your action.
        This allows for a shorter waiting time for the next
        broadcast if all players respond to the latest game state.

        As a **participant of Hackathon**, you can **ignore this**.
        Attaching the identifier to the response payload is done by
        this library automatically.
        """
        raise NotImplementedError

    @property
    def tick(self) -> int:
        """The tick of the game state."""
        raise NotImplementedError

    @property
    def my_id(self) -> str:
        """The unique identifier of your agent."""
        raise NotImplementedError

    @property
    def teams(self) -> Sequence[GameStateTeam]:
        """The sequence of teams in the game state."""
        raise NotImplementedError

    @property
    def map(self) -> Map:
        """The map of the game state."""
        raise NotImplementedError


class GameResult(Protocol):
    """Represents the game result.

    Attributes
    ----------
    teams: Sequence[:class:`GameEndTeam`]
        The sequence of teams in the game result.
    """

    @property
    def teams(self) -> Sequence[GameEndTeam]:
        """The sequence of teams in the game result."""
        raise NotImplementedError
