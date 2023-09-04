####################             IN MAINTANCE             ####################
import json
from time import sleep
from helpers.utils.decoder import decoder, check
from helpers.handlers.file_formatter import file_to_dict
from helpers.utils.ssh import ssh

clients = file_to_dict("data.csv", "C")

clients_list = [
    {"contract": str(client["Referencia"]).zfill(10), "action": "S"}
    for client in clients
]

count = 1
(comm, command, quit_ssh) = ssh("181.232.180.7", True)
sleep(2)
result = decoder(comm)
real_deacts = []
real_actives = []
for client in clients_list:
    command(f"display ont info by-desc {client['contract']}")
    print(count, client)
    sleep(5)
    res = decoder(comm)
    result += res
    condition = check(res," deactivated ")
    if condition == None:
        print(client,"its active")
        real_actives.append(client)
        continue
    print(client,"its deactivated")
    real_deacts.append(client)
    count += 1
print(result, file=open('result_s.txt','w'))
print(json.dumps({"clients":real_deacts}), file=open('action_s_real.json','w'))
print(json.dumps({"clients":real_actives}), file=open('action_r_real.json','w'))


####################             IN MAINTANCE             ####################
