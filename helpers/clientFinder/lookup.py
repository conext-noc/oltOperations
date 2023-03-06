from helpers.clientFinder.dataLookup import dataLookup
from helpers.clientFinder.nameLookup import nameLookup
from helpers.clientFinder.optical import opticalValues
from helpers.clientFinder.serialLookup import serialSearch
from helpers.clientFinder.wan import wan
from helpers.utils.printer import inp


def lookup(comm, command, olt, lookup_type):
    """
    This module retrieves the clients data from the cli
    
    comm        : connection client
    command     : fnc to send command with enter
    olt         : which olt belongs the client
    lookup_type : type of search, by sn, by name, by olt data
    
    """
    client = {
            "fail":None,
            "frame":None,
            "slot": None,
            "port": None,
            "onu_id":None,
            "sn":None,
            "name":None,
            "control_flag":None,
            "run_state":None,
            "device":None,
            "last_down_cause":None,
            "last_down_time":None,
            "last_down_date":None,
        }
    if lookup_type == "S":
        client["sn"] = inp("Ingrese el Serial del Cliente a buscar : ")
        client["olt"] = olt
        client = serialSearch(comm, command, client)

    if lookup_type == "D":
        client["olt"] = olt
        client["frame"] = inp("Ingrese frame de cliente        : ")
        client["slot"] = inp("Ingrese slot de cliente         : ")
        client["port"] = inp("Ingrese puerto de cliente       : ")
        client["onu_id"] = inp("Ingrese el onu id del cliente   : ")
        client = dataLookup(comm,command,client)
        
    if lookup_type == "N":
        client["olt"] = olt
        NAME = inp("Ingrese el Nombre del Cliente a buscar : ")
        client = nameLookup(comm,command,NAME)

    if client["fail"] == None and lookup_type != "N":
        (client["ip_address"], client["wan"]) = wan(comm, command, client)
        (client["temp"], client["pwr"]) = opticalValues(comm, command, client, False)
    
    return client