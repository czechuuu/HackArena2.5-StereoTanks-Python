"""This module contains the response actions that the bot can take.

The response actions are used to define the bot's next move in the game.

Classes
-------
ResponseAction
    Base class for response actions.
Movement
    Represents a movement response action.
Rotation
    Represents a rotation response action.
AbilityUse
    Represents an ability use response action.
Pass
    Represents a pass response action.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar, final

from .enums import Ability, MovementDirection, PacketType, RotationDirection
from .payloads import (
    AbilityUsePayload,
    CaptureZonePayload,
    GoToPayload,
    MovementPayload,
    PassPayload,
    ResponseActionPayload,
    RotationPayload,
)

__all__ = (
    "ResponseAction",
    "Movement",
    "Rotation",
    "AbilityUse",
    "CaptureZone",
    "GoTo",
    "Pass",
)


@dataclass(slots=True, frozen=True)
class ResponseAction(ABC):
    """Base class for response actions."""

    packet_type: ClassVar[PacketType]

    @abstractmethod
    def to_payload(self, game_state_id: str) -> ResponseActionPayload:
        """Converts the response action to a payload."""


@dataclass(slots=True, frozen=True)
class Movement(ResponseAction):
    """Represents a movement response action.

    Example
    -------

    ::

        movement = Movement(MovementDirection.FORWARD)
    """

    movement_direction: MovementDirection
    packet_type: ClassVar[PacketType] = PacketType.MOVEMENT

    @final
    def to_payload(self, game_state_id: str) -> MovementPayload:
        return MovementPayload(game_state_id, self.movement_direction)


@dataclass(slots=True, frozen=True)
class Rotation(ResponseAction):
    """Represents a rotation response action.

    Example
    -------

    ::

        rotation = Rotation(RotationDirection.LEFT, RotationDirection.RIGHT)
    """

    tank_rotation_direction: RotationDirection | None
    turret_rotation_direction: RotationDirection | None
    packet_type: ClassVar[PacketType] = PacketType.ROTATION

    @final
    def to_payload(self, game_state_id: str) -> RotationPayload:
        return RotationPayload(
            game_state_id,
            self.tank_rotation_direction,
            self.turret_rotation_direction,
        )


@dataclass(slots=True, frozen=True)
class AbilityUse(ResponseAction):
    """Represents an ability use response action.

    Example
    -------

    ::

        # Fire bullet (basic attack)
        ability_use = AbilityUse(Ability.FIRE_BULLET)

        # Fire double bullet
        ability_use = AbilityUse(Ability.FIRE_DOUBLE_BULLET)

        # Use laser
        ability_use = AbilityUse(Ability.USE_LASER)

        # Use radar
        ability_use = AbilityUse(Ability.USE_RADAR)

        # Drop mine
        ability_use = AbilityUse(Ability.DROP_MINE)
    """

    ability: Ability
    packet_type: ClassVar[PacketType] = PacketType.ABILITY_USE

    @final
    def to_payload(self, game_state_id: str) -> AbilityUsePayload:
        return AbilityUsePayload(game_state_id, self.ability)


@dataclass(slots=True, frozen=True)
class CaptureZone(ResponseAction):
    """Represents a pass response action.

    Example
    -------

    ::

        capture_zone = CaptureZone()
    """

    packet_type: ClassVar[PacketType] = PacketType.CAPTURE_ZONE

    @final
    def to_payload(self, game_state_id: str) -> ResponseActionPayload:
        return CaptureZonePayload(game_state_id)


@dataclass(slots=True, frozen=True)
class GoTo(ResponseAction):
    """Represents a pass response action.

    Example
    -------

    ::

        # just go to (x, y) coordinates
        go_to = GoTo(5, 10)


        # go to (x, y) coordinates with custom costs and penalties

        # prefer backward
        custom_costs = new Costs(forward=2, backward=1, rotate=2)
        # penalize for blindly and laser, don't care about mine
        custom_penalties = new Penalties(blindly=2, laser=5, mine=null)
        # add custom tiles to penalize (for example, to avoid cached mines)
        custom_penalties.per_tile.add(new PerTilePenalty(5, 10, 5.0))

        go_to = GoTo(5, 10, custom_costs, custom_penalties)
    """

    @dataclass(slots=True)
    class Costs:
        """Represents the costs of moving.

        Attributes
        ----------
        forward: :class:`float`
            The cost of moving forward. Defaults to 1.
        backward: :class:`float`
            The cost of moving backward. Defaults to 1.5.
        rotate: :class:`float`
            The cost of rotating. Defaults to 1.5.
        """

        forward: float = 1
        backward: float = 1.5
        rotate: float = 1.5

    @dataclass(slots=True)
    class Penalties:
        """Represents the penalties of moving.

        Attributes
        ----------
        blindly: :class:`float`
            The penalty for blindly moving. Defaults to None.
        tank: :class:`float`
            The penalty for moving into a tank. Defaults to None.
        bullet: :class:`float`
            The penalty for moving into a bullet. Defaults to None.
        mine: :class:`float`
            The penalty for moving into a mine. Defaults to None.
        laser: :class:`float`
            The penalty for moving into a laser. Defaults to None.
        per_tile: :class:`list[PerTile]`
            A list of penalties for specific tiles. Defaults to an empty list.
        """

        @dataclass(slots=True)
        class PerTile:
            """Represents a penalty for a specific tile.

            Attributes
            ----------
            x: :class:`int`
                The x coordinate of the tile.
            y: :class:`int`
                The y coordinate of the tile.
            penalty: :class:`float`
                The penalty for the tile.
            """

            x: int
            y: int
            penalty: float

        blindly: float | None = None
        tank: float | None = None
        bullet: float | None = None
        mine: float | None = None
        laser: float | None = None
        per_tile: list[PerTile] = field(default_factory=list)

    x: int
    y: int
    costs: Costs = field(default_factory=Costs)
    penalties: Penalties = field(default_factory=Penalties)
    packet_type: ClassVar[PacketType] = PacketType.GO_TO

    @final
    def to_payload(self, game_state_id: str) -> ResponseActionPayload:
        return GoToPayload(game_state_id, self.x, self.y, self.costs, self.penalties)


@dataclass(slots=True, frozen=True)
class Pass(ResponseAction):
    """Represents a pass response action.

    Example
    -------

    ::

        pass_ = Pass()
    """

    packet_type: ClassVar[PacketType] = PacketType.PASS

    @final
    def to_payload(self, game_state_id: str) -> ResponseActionPayload:
        return PassPayload(game_state_id)
