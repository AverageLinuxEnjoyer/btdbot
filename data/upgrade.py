from dataclasses import dataclass

@dataclass
class Upgrade:
    name: str
    cost: int
    tier: int
    path: int