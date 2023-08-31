####################             IN MAINTANCE             ####################
# import json
# from time import sleep
# from helpers.utils.decoder import decoder
# from helpers.handlers.file_formatter import file_to_dict
# from helpers.utils.ssh import ssh

# clients = file_to_dict("data.csv", "C")

# clients_list = [
#     {"contract": str(client["Referencia"]).zfill(10), "action": "S"}
#     for client in clients
# ]

# count = 1
# (comm, command, quit_ssh) = ssh("181.232.180.7", True)
# for client in clients_list:
#     print(count, client)
#     command(f"display ont info by-desc {client['contract']}")
#     sleep(5)
#     count += 1
# result = decoder(comm)
# print(result, file=open('result_s.txt','w'))


####################             IN MAINTANCE             ####################
