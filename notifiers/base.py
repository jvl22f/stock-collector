from abc import ABC, abstractmethod


class BaseNotifier(ABC):
    """通知の基底クラス。メール・LINE等は本クラスを継承して実装する。"""

    @abstractmethod
    def send(self, subject: str, body: str) -> bool:
        pass
