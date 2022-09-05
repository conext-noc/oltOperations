import paramiko
import time


def activate(deactList, username, password, port, delay, ip):
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, port, username, password)
    comm = conn.invoke_shell()

    def enter():
        comm.send(" \n")
        time.sleep(delay)

    def commandToSend(command):
        comm.send("{} \n".format(command))
        time.sleep(delay)

    def exitInfo():
        comm.send("Q")
        time.sleep(delay)

    commandToSend("enable")
    commandToSend("config")
    for client in deactList:
        # print(client)
        commandToSend(
            "interface gpon {}/{}".format(client["frame"], client["slot"]))
        commandToSend("ont activate {} {}".format(
            client["port"], client["id"]))
        commandToSend("display ont info {} {}".format(
            client["port"], client["id"]))
        enter()
        exitInfo()
        output = comm.recv(100000000000)
        output = output.decode("utf-8")
        print(output, file=open("activateResultOLT.txt", "a"))
    conn.close()
