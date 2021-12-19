from abc import ABC
from typing import ClassVar
from dataclasses import dataclass
from data.upgrade import Upgrade


@dataclass
class MonkeyTemplate(ABC):
    clas: str
    name: str
    cost: int
    hotkey: str
    upgrades: list
