import click

import pandas as pd
from typing import Tuple


class Sieve:
    """Sieve. Use value True for non-prime"""

    sieve: bytearray
    n_init: int

    def __index_for(self, number) -> Tuple[int, int]:
        """calculate the index in the bytearray for a number"""
        cell = number // 8
        pos = number % 8
        return (cell, pos)

    def __init__(self, up_to: int) -> None:
        self.sieve = bytearray([0xFF] * (up_to // 8 + 1))
        assert up_to > 2
        for i in range(2, up_to + 1):
            if self[i] == True:
                for j in range(2 * i, up_to + 1, i):
                    self[j] = False

    def __getitem__(self, idx) -> bool:
        cell, pos = self.__index_for(idx)
        # any bit non-zero after the mask means it's a prime.
        return self.sieve[cell] & (1 << pos) != 0

    def __setitem__(self, idx, val) -> bool:
        cell, pos = self.__index_for(idx)
        # Bit fiddle
        old = self.sieve[cell]
        old = old & ~(1 << pos)
        self.sieve[cell] = old ^ (1 if val else 0 << pos)


@click.command()
@click.option(
    "--url",
    default="https://ftp.ripe.net/pub/stats/ripencc/2021/delegated-ripencc-extended-20211122.bz2",
    help="URL to delegated extended file, such as 'https://ftp.ripe.net/pub/stats/ripencc/2021/delegated-ripencc-extended-20211122.bz2'",
)
def main(url):
    # do work
    df = pd.read_csv(
        url,
        delimiter="|",
        skiprows=5,
        names=[
            "registry",
            "cc",
            "type",
            "start",
            "value",
            "date",
            "status",
            "extensions",
        ],
    )

    free_as = df[(df.type == "asn") & (df.status == "available")].start.astype(int)
    free = free_as.tolist()

    sieve = Sieve(free_as.max())
    primes = [p for p in free if sieve[p]]

    print("Prime ASNs that are available:")
    print(primes)


if __name__ == "__main__":
    main()
