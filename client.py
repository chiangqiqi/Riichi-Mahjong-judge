#!/usr/bin/env python3

import sys
import json
import fileinput
import random

from enum import Enum
from collections import namedtuple
from typing import List

def eprint(*args, **kwargs):
    """A simple function to eprint data to stderr"""
    print(*args, file=sys.stderr, **kwargs)

Tile = namedtuple("Tile", ["type", "num", "chibao"])

def tile_to_str(t):
    if t.chibao:
        return "{}0".format(t.type)
    else:
        return "{}{}".format(t.type, t.num)
Tile.__str__ = tile_to_str

def tiles_to_str(tiles):
    return " ".join([str(t)  for t in tiles ])

def is_same_tile(t1: Tile, t2: Tile) -> bool:
    return t1.type == t2.type and t1.num == t2.num

def parse_tile(tile_str: str):
    if isinstance(tile_str, Tile):
        return tile_str

    t, n = tile_str
    if n == '0':
        return Tile(t, 5, True)
    else:
        return Tile(t, int(n), False)

class HandTiles:
    def __init__(self, tiles: List[str]):
        self._tiles = list(map(parse_tile, tiles))

    def play_tile(self, tile:Tile):
        self._tiles.remove(tile)

    def draw_tile(self, tile:Tile):
        self._tiles.append(tile)

    def __repr__(self):
        return ",".join([str(t)  for t in self._tiles ])

    def sort(self):
        self._tiles.sort()
# ActionType = Enum("PLAY", "CHI", "GANG", "PENG")

class Action:
    def __init__(self, t: Tile):
        self._tile = t
        self._mianzi = None
        # self._mianzi = tiles
    # def parse_req(self, info: List[str]):
        # raise NotImplementedError("parse need to be implemented")
    def played(self):
        return self._tile

    def to_str(self):
        raise NotImplementedError("parse need to be implemented")

class PlayAction(Action):
    def __init__(self, t: List[str]):
        super().__init__(parse_tile(t[0]))
    def to_str(self):
        return "PLAY {}".format(self.played())
       
class DrawAction(Action):
    def __init__(self, t: List[str]):
        # 这个摸牌看不到
        if t[0] is None:
            super().__init__(t[0])
        else:
            super().__init__(parse_tile(t[0]))

    def to_str(self):
        return "DRAW"

class ChiAction(Action):
    def __init__(self, t: List[str]):
        super().__init__(parse_tile(t[-1]))
        self._mianzi = parse_mianzi(t[:-1])

    def to_str(self):
        return "CHI {} {}".format(self._mianzi, self.played())

class PengAction(Action):
    def __init__(self, t: List[str]):
        super().__init__(parse_tile(t[-1]))
        self._mianzi = parse_mianzi(t[:-1])

    def to_str(self):
        return "PENG {} {}".format(self._mianzi, self.played())

class GangAction(Action): # 暂时先不要管暗杠之类的了
    def __init__(self, t: List[str]):
        super().__init__(parse_tile(t[-1]))
        self._mianzi = parse_mianzi(t[:-1])
    def to_str(self):
        return "GANG {} {}".format(self._mianzi, self.played())

class RiichiAction(Action):
    def __init__(self ):
        super().__init__(None)

    def to_str(self):
        return "RIICHI"

class HuAction(Action):
    def __init__(self ):
        super().__init__(None)

    def to_str(self):
        return "HU"

class PassAction(Action):
    def __init__(self ):
        super().__init__(None)

    def to_str(self):
        return "PASS"

def parse_action(raw_action : List[str]) -> Action:
    name, tiles_str = raw_action[0], raw_action[1:]
    if name == "DRAW":
        return DrawAction([None])
    elif name == "PLAY":
        return PlayAction(tiles_str)
    elif name == "CHI":
        return ChiAction(tiles_str)
    elif name == "PENG":
        return PengAction(tiles_str)
    elif name == "GANG":
        return GangAction(tiles_str)
    elif name == "RIICHI":
        return RiichiAction()

class Mianzi:
    def __init__(self, tiles):
        self._tiles = tiles

    def get_tiles(self):
        return self._tiles

    def __str__(self):
        return tiles_to_str(self._tiles)

class Shunzi(Mianzi):
    def __init__(self, tiles: List[Tile]):
        super(Shunzi ,self).__init__(tiles)
        tmin = tiles[0]
        if (tmin.type == "Z"):
            raise ValueError("字牌 {} 不能组成顺子".format(tmin))

        # self._tmin = tmin
    # def get_tiles(self):
        # t,n,_ = self._tmin
        # return [Tile(t, n+i, False) for i in range(3)]

class Kezi(Mianzi):
    def __init__(self, tiles: List[Tile]):
        # self._tile = t
        super().__init__(tiles)

    # def get_tiles(self):
        # return [self._tile] * 3

class Gangzi(Mianzi):
    def __init__(self, tiles: List[Tile]):
        super().__init__(tiles)

    # def get_tiles(self):
        # return [self._tile] * 4

def parse_mianzi(tiles: List[str]) -> Mianzi:
    """Be sure these tiles form a mianzi before
    """
    tiles = sorted([parse_tile(t) for t in tiles])
    tiles_count = len(tiles)
    t1, t2 = tiles[:2]
    if is_same_tile(t1, t2):
        if tiles_count == 3:
            return Kezi(tiles)
        else:
            assert(tiles_count == 4)
            return Gangzi(tiles)
    else:
        return Shunzi(tiles)

class PlayerPublic:
    """A public player contains the info that is shown to all
    the players in the game
    Including the played cards,
    """
    def __init__(self, pos: int):
        self._pos = int(pos)
        self._ming_mian = []  # 放明的面子
        self._played_tiles = []
        self._riichi = False # 是否立直

    def do_action(self, a: Action):
        if isinstance(a, DrawAction):
            # 别的玩家无法观察到摸牌的操作
            pass
        elif isinstance(a,RiichiAction):
            self._riichi = True
        elif isinstance(a, Action):
            # 先打出牌

            if isinstance(a, PlayAction):
                self._played_tiles.append(a.played())
            else:
                self._played_tiles.append(a.played())
                self.show_mianzi(a._mianzi)

    def play_tile(self, t: Tile):
        self._played_tiles.append(t)

    def show_mianzi(self, m: Mianzi):
        self._ming_mian.append(m)

# State MO ，打牌
class Player(PlayerPublic):

    def __init__(self, pos):
        super().__init__(pos)
        self._state = "MO"
        self._players = [None] * 4

        # 初始化玩家
        for i in range(4):
            if i != self._pos:
                self._players[i] = PlayerPublic(i)
            else:
                self._players[i] = self
        self._last_player = None
        self._last_action = None

    def set_tiles(self, tiles):
        self._hand_tiles = HandTiles(tiles)

    def draw_tile(self, tile):
        self._hand_tiles.draw_tile(tile)

    def play_tile(self, tile):
        self._hand_tiles.play_tile(tile)

    def hand_tile_num(self):
        return len(self._hand_tiles._tiles)

    def do_action(self, a: Action):
        self._hand_tiles.sort()
        if isinstance(a, DrawAction):
            self.draw_tile(a.played())
        else:
            self.play_tile(a.played())
            # 把要亮明的面子从手牌中拿出去
            if a._mianzi is not None:
                # 面子里的第一张需要从上一个玩家的牌堆中拿出来
                self._players[self._last_player]._played_tiles.remove(a._mianzi.get_tiles()[0])

                for _t in a._mianzi.get_tiles()[1:]: # 第一张牌不是手里的
                    self._hand_tiles.play_tile(_t)

            # super(Player, self).do_action(a)
            PlayerPublic.do_action(self, a)
        self._last_player = self._pos
        self._last_action = a

    def witness(self, player_idx: int, action: Action):
        p = self._players[player_idx]
        # import pdb; pdb.set_trace()
        # try:
        if isinstance(p, Player):
            eprint(p._hand_tiles._tiles)
        eprint(action)
        p.do_action(action)

        self._last_player = player_idx
        self._last_action = action


    def should_play(self):
        """上一个请求是摸牌，所以应该打出一张
        """
        return self._last_player == self._pos and isinstance( self._last_action, DrawAction )

    def select_play_tile(self, tiles):
        """选择一张牌打出
        如果有副露应该一般不能打出副露中出现的牌
        """

        for pos,mz in find_mianzis(tiles, 0, len(tiles)):
            del tiles[pos[0]:pos[1]]
        return random.choice(tiles)

    def legal_actions(self):
        """latest request is of form

        {
        "doraIndicators": "T8",
        "state": "2 W4",
        "validact": null
        },
        """
        if "validact" not in self._last_request:
            return [PassAction()]
        validact = self._last_request["validact"]
        # which move can the agent do
        if self.should_play():
            # 摸牌之后只能打牌
            return [ PlayAction([t]) for t in self._hand_tiles._tiles ]
        elif validact is not None:
            validacts = self._last_request["validact"].split(",")
            # 碰杠 > 吃 吃牌可以吃上家的牌，
            played_tile = self._last_action.played()
            actions = []
            for validact in validacts:
                fulu_action = self.generate_fulu_action(self._hand_tiles._tiles, played_tile , validact)
                if fulu_action is not None: actions.append(fulu_action)

            return actions
        else:
            return [PassAction()]

    def legal_actions_output(self):
        """
        """
        return [ a.to_str() for a in self.legal_actions()]


    def generate_fulu_action(self, hand_tiles: List[Tile], played_tile: Tile, fulu_type):
        """输入分别是手牌，别的玩家打出的牌以及 fulu 的种类
        返回一个面子
        比如如果输入是
        "W1 W2 ", "W3", "CHI"
        返回应该是

        W3 W1 W2,

        TODO 如果和牌了返回和牌
        """
        hand_tiles_num = len(hand_tiles)
        if fulu_type == "HU":
            return HuAction()
        else:
            # 先将牌插入
            # 这里需要确保 hand_tiles 是排好序的
            hand_tiles_copy = hand_tiles[:]
            for i in range(hand_tiles_num + 1):
                # 插入在第一个
                if  i == hand_tiles_num or played_tile < hand_tiles[i]:
                    hand_tiles_copy.insert(i, played_tile)
                    insert_pos = i
                    break

            # 面子需要是包含当前这张牌
            # TODO 需要考虑4张的杠子
            # 需要考虑边缘因素
            mianzis = find_mianzis(hand_tiles_copy, insert_pos-2, insert_pos+1)
            if len(mianzis) == 0:
                return PassAction()

            pos, selected_mianzi = mianzis[0]

            # TODO 这个地方写的有点丑
            # 应该把吃牌之类的拿到的别人的牌放到一个副露的最前面
            selected_mianzi._tiles.remove(played_tile)
            selected_mianzi._tiles = [played_tile] + selected_mianzi._tiles
            # play a tile from left tiles
            del hand_tiles_copy[pos[0]:pos[1]]

            should_play = self.select_play_tile(hand_tiles_copy)
            if fulu_type == "CHI":
                return ChiAction(selected_mianzi._tiles + [should_play])
            if fulu_type == "PENG":
                return PengAction(selected_mianzi._tiles + [should_play])

    def process_input(self, content):
        parsed_content = json.loads(content)
        reqs = parsed_content["requests"]
        resps = parsed_content["responses"]
        eprint(parsed_content["requests"])
        self._last_request = reqs[-1]
        for i,req in enumerate( reqs  ):
            if "state" in req:
                req_cont = req["state"].split()
            else:
                req_cont = req["handTiles"].split()

            if i == 0:
                self._pos = req_cont[1]
            elif i == 1:
                self.set_tiles(req_cont[1:])
            else:
                # first process request
                if req_cont[0] == "2":
                    # 自己摸牌
                    action = DrawAction([parse_tile(req_cont[1])])
                    self.do_action(action)

                elif req_cont[0] == "3":
                    # 看到的别人行动
                    action_player = int(req_cont[1])
                    self.witness(action_player, parse_action(req_cont[2:]))

                eprint(req_cont)


class RandomPlayer(Player):
    def choose_action(self):
        return random.choice(self.legal_actions_output())


def generate_mianzi(tiles):
    """能否组成一个面子
    比如顺子，刻子或者杠子
    """
    tiles_num = len(tiles)

    tiles = sorted(tiles)
    # 顺子或者刻子
    if tiles_num == 3:
        t1,t2,t3=tiles
        if (t2.num- t1.num) == 1 and (t3.num - t2.num) == 1:
            return Shunzi(tiles)
        if is_same_tile(t1, t2) and is_same_tile(t2, t3):
            return Kezi(tiles)
    elif tiles_num == 4:
        # 四张牌只能组成 杠子
        t1 = tiles[0]
        if all(lambda x: is_same_tile(x,t1), tiles):
            return Gangzi(tiles)

def find_mianzis(tiles_list, idx1, idx2):
    """给一个 tiles 的列表，返回一个去掉所有面子的列表
    需要输入的数组是排好序的
    """
    to_be_removed = []
    mianzis = []
    begin_pos = idx1
    while begin_pos < idx2:
        end_pos = begin_pos + 3
        if begin_pos < 0:
            continue
        if end_pos > len(tiles_list):
            break
        m = generate_mianzi(tiles_list[begin_pos:end_pos])

        if m is not None:
            # 还需要标记位置
            # 格式是 (2,5), Kezi(W1,W2,W3)
            mianzis.append( ((begin_pos,end_pos),m) )
            begin_pos = end_pos
        else:
            begin_pos += 1

    # pos, selected_mianzi = mianzis[0]
    return mianzis

def main():
    # while 1:
    # if len(sys.argv) < 2:
    #     eprint("Should give a filename as argument")
    #     return;

    # with open(sys.argv[1]) as fp:
    #     content = fp.read()
    #     parsed_content = json.loads(content)
    #     reqs = parsed_content["requests"]
    #     resps = parsed_content["responses"]

    content = sys.stdin.read()
    p = RandomPlayer(0)
    p.process_input(content)
    action_cmd = p.choose_action()


    print( json.dumps({"response":action_cmd}) )
   

if __name__ == '__main__':
    main()
