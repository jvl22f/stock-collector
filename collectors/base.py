from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StockData:
    code: str
    name: str
    timestamp: datetime = field(default_factory=datetime.now)
    price: float = None
    change_pct: float = None
    volume: int = None
    news: list = field(default_factory=list)


class BaseCollector(ABC):
    @abstractmethod
    def collect(self, stock: dict) -> StockData:
        pass
