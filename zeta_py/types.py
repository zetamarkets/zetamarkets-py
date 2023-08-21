from enum import Enum


class Side(Enum):
    BID = 0
    ASK = 1


class Asset(Enum):
    SOL = 0
    BTC = 1
    ETH = 2
    APT = 3
    ARB = 4
    UNDEFINED = 5

    def to_index(self):
        return self.value

    def to_string(self):
        return self.name

    @staticmethod
    def all():
        return [a for a in Asset if a != Asset.UNDEFINED]


class Network(Enum):
    LOCALNET = "localnet"
    DEVNET = "devnet"
    TESTNET = "testnet"
    MAINNET = "mainnet_beta"
