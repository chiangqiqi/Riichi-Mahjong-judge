#!/usr/bin/env python3

from subprocess import Popen, PIPE
import json

with open('init.json', 'rb') as fp:
    msg = fp.read()

init_data = json.loads(msg)
init_data['log'] = []

client_input = [
    {"requests": [], "responses": []},
    {"requests": [], "responses": []},
    {"requests": [], "responses": []},
    {"requests": [], "responses": []}
]

def one_step():
    # 先发牌
    pserver = Popen(['./mahjong'], stdout=PIPE, stdin=PIPE)

    # client_input['requests'].append(init_data)
    msg,_ = pserver.communicate(input= json.dumps(init_data).encode())
    import pdb; pdb.set_trace()
    msg_decoded = json.loads(msg.decode())
    # client_input['responses'].append(msg_decoded)

    if msg_decoded['command'] == 'finish':
        return True

    # in mahjong, each response data contains 4 person
    # so it needed to be dealt carefully
    init_data['log'].append({"output":  msg_decoded})

    round_data = {}
    # a round data contains each of the four players on
    # the table
    req_content = msg_decoded['content']

    for i in range(4):
        client_input[i]['requests'].append(req_content[str(i)])

        pclient = Popen(['./client'], stdout=PIPE, stdin=PIPE)
        client_output,_ = pclient.communicate(input=json.dumps(client_input[i]).encode())
        rec = json.loads(client_output.decode())

        rec['verdict'] = "OK"
        client_input[i]['responses'].append(rec['response'])
        print("player {} with response {}".format(i,rec['response']) )
        round_data[str(i)] = rec
    init_data['log'].append(round_data)
    return False

while one_step() is False:
    print("run one step ");
