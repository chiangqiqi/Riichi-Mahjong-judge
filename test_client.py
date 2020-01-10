#!/usr/bin/env python3

import json

from client import *


def parse_tiles(s):
    tiles_str = s.split(" ")
    return [ parse_tile(s) for s in tiles_str ]

def test_tiles():
    t1 = parse_tile("W2")
    assert str(t1) == "W2"

    t1 = parse_tile("W0")
    assert str(t1) == "W0"
    t1 = parse_tile("Z2")
    assert str(t1) == "Z2"

def test_generate_fulu():
    played = parse_tile("W3")
    tiles = sorted(parse_tiles("W1 W2 B3 B3"))
    p = Player(0)
    fulus = p.generate_fulu_action(tiles, played, "CHI")
    print(fulus)

    # assert len(fulus) == 1
    assert isinstance( fulus._mianzi, Shunzi )

    fulus = p.generate_fulu_action(tiles, parse_tile("B3"), "CHI")
    # assert len(fulus) == 1
    assert isinstance( fulus._mianzi, Kezi )


def test_generate_mianzi():
    tiles1 = parse_tiles("W0 W5 W5")
    mianzi = generate_mianzi(tiles1)
    assert isinstance(mianzi, Kezi)

    tiles1 = parse_tiles("W1 W5 W5")
    mianzi = generate_mianzi(tiles1)
    assert mianzi is None

    tiles1 = parse_tiles("W1 W2 W3")
    mianzi = generate_mianzi(tiles1)

    assert isinstance(mianzi, Shunzi)


def test_find_mianzi():
    # 这个找下来应该是两个顺子
    tiles = parse_tiles("W1 W2 W3 W4 W5 W6")
    mianzi = find_mianzis(tiles, 0, 6)
    assert len(mianzi) == 2
