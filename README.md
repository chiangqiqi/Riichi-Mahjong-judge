# Riichi Mahjong 裁判代码

## Dependence
  * Boost
  * [jsoncpp](https://github.com/open-source-parsers/jsoncpp)

`jsoncpp` 的 include 路径默认为 `json/json.h` 可以在 `mahjong.h` 中更改。

## Build

```shell
# 编译
g++ --std=c++11 Mahjong2.cpp Yizhong.cpp Player.cpp Tools.cpp -ljsoncpp -o mahjong

# 之后可以执行
./mahjong
```

## TODO
1. 吃牌的计算有问题，当手牌中有多余牌时无法识别
2. 可以用强化学习的方式来做一下打牌


