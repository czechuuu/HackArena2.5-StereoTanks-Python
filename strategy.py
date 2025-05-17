from hackathon_bot import *
from enum import Enum

class Objective(Enum):
    GO_TO_ZONE = 0
    DEFEND_AREA = 1
class Strategy:
    objective: dict[TankType: Objective]
    defend_area_coords: dict[TankType: tuple[int, int, int]] = {}

    # CURRENTLY DEFAULT GO TO ZONE
    def __init__(self) -> None:
        self.objective[TankType.LIGHT] = Objective.GO_TO_ZONE
        self.objective[TankType.HEAVY] = Objective.GO_TO_ZONE
        self.defend_area_coords[TankType.LIGHT] = (0, 0, 0)
        self.defend_area_coords[TankType.HEAVY] = (0, 0, 0)
        return None
    
    def get_objective(self, type: TankType) -> Objective:
        return self.objective[type]
    
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
