from hackathon_bot import *
from enum import Enum

class Objective(Enum):
    GO_TO_ZONE = 0
    DEFEND_AREA = 1
class Strategy:
    objective: dict[TankType: Objective]
    apache_timeout: int = None  # time for apache to stay on target
    defend_area_coords: list[int, int, int] = None  # coordinates, length
    attack_mode: bool = False
    dip_mode: bool = False
    bullets_left_in_attack_mode: int = 3
    where_to_escape: tuple[int, int] = (0, 0)  # (x, y)
    
    def __init__(self) -> None:
        self.objective = Objective.GO_TO_ZONE
        self.defend_area_coords = (0, 0, 0)
        self.apache_timeout = 10
        return None
    
    def get_objective(self) -> Objective:
        return self.objective
    
    def set_objective(self, new_objective: Objective) -> None:
        self.objective = new_objective
        return None
    
    def get_penalties(self) -> GoTo.Penalties:
        """Returns the penalties for the GoTo action."""
        # In the future, can change the penalties based on the objective etc.
        default_costs = GoTo.Penalties(
            blindly=1,
            tank=1,
            bullet=99,
            mine=999,
            laser=9999
        ) 
        return default_costs

    def set_defend_area_coords(self, coords: tuple[int, int, int]) -> None:
        """Sets the coordinates of the defend area."""
        self.defend_area_coords = coords
        return None
    
    def get_defend_area_coords(self) -> tuple[int, int, int]:
        """Returns the coordinates of the defend area."""
        return self.defend_area_coords