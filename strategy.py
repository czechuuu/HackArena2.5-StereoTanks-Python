from hackathon_bot import *
from enum import Enum

class Objective(Enum):
    GO_TO_ZONE = 0

class Strategy:
    objective: Objective


    # CURRENTLY DEFAULT GO TO ZONE
    def __init__(self) -> None:
        self.objective = Objective.GO_TO_ZONE
        return None
    
    def get_objective(self) -> Objective:
        return self.objective
    
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
