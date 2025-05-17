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