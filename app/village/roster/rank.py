from dataclasses import dataclass


@dataclass
class Rank:
    CITIZEN = 'Citizen'
    PEER = 'Peer'
    LORD = 'Lord'
    DEPUTY = 'Deputy'
    MAYOR = 'Mayor'

    name: str
    custom_name: str

    @property
    def order(self) -> int:
        if self.name == self.CITIZEN:
            return 5
        elif self.name == self.PEER:
            return 4
        elif self.name == self.LORD:
            return 3
        elif self.name == self.DEPUTY:
            return 2
        elif self.name == self.MAYOR:
            return 1

    @classmethod
    def get_names(cls):
        return [cls.CITIZEN, cls.PEER, cls.LORD, cls.DEPUTY, cls.MAYOR]
