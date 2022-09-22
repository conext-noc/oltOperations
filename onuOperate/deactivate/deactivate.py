def deactivate(actList, enter, commandToSend, comm, olt):
    for client in actList:
        print(client)
        commandToSend(
            "interface gpon {}/{}".format(client["frame"], client["slot"]))
        commandToSend("ont deactivate {} {}".format(
            client["port"], client["id"]))
        commandToSend("display ont info {} {} | include \"Control flag\" ".format(
            client["port"], client["id"]))
        enter()
        outputClient = comm.recv(65535)
        outputClient = outputClient.decode("latin-1")
        frame = client["frame"]
        slot = client["slot"]
        port = client["port"]
        clientID = client["id"]
        path = f"deactivate_{frame}-{slot}-{port}-{clientID}_OLT{olt}.txt"
        print(outputClient, file=open(path, "w"))
