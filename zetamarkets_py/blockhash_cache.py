import collections
from typing import Tuple

from solders.hash import Hash


class BlockhashCache:
    """
    A recent blockhash cache that expires after a given number of seconds.
    We grab the oldest cached blockhash in get(), without popping it

    Args:
        ttl: Slots until cached blockhash expires.
    """

    def __init__(self, ttl: int = 60) -> None:
        """Instantiate the cache (you only need to do this once)."""
        self.ttl_slots = 60
        self.blockhashes = collections.deque(maxlen=ttl * 10)

    def set(self, slot: int, blockhash: Hash, last_valid_block_height: int, used_immediately: bool = False) -> None:
        """
        Update the cache.

        Args:
            slot: the slot which the blockhash came from.
            blockhash: new blockhash value.
            last_valid_block_height: last block height at which the blockhash will be valid.
            (unused) used_immediately: unused param, exists in the solana BlockhashCache and just guarantees syntax compatibility

        """
        self.blockhashes.append(
            {"slot": slot, "blockhash": blockhash, "last_valid_block_height": last_valid_block_height}
        )

        # Keep only N slots of blockhashes
        pops = 0
        for item in self.blockhashes:
            if item["slot"] < slot - self.ttl_slots:
                pops += 1
            else:
                break

        for i in range(pops):
            self.blockhashes.popleft()

    def get(self) -> Tuple[Hash, int]:
        """
        Get the oldest cached blockhash without popping

        Returns:
            blockhash: cached blockhash.
            last_valid_block_height: last block height at which the blockhash will be valid.

        """
        if len(self.blockhashes) > 0:
            return self.blockhashes[0]["blockhash"], self.blockhashes[0]["last_valid_block_height"]
        else:
            raise ValueError
