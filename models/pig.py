from dataclasses import dataclass

@dataclass
class Pig:
    user_id: int
    name: str = "Безіменний"
    weight: int = 10
    strength: int = 5
    health: int = 100
    level: int = 1
    xp: int = 0
