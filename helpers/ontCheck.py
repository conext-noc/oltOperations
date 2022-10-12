from helpers.outputDecoder import decoder,parser,check

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power\(dBm\)                  : "
conditionFail = "Failure: "

def verifyValues(comm, command, enter, SLOT, PORT, ID):
    enter()
    decoder(comm)
    command(f"interface gpon 0/{SLOT}")
    enter()

    command(
        f"""display ont optical-info {PORT} {ID} | include Temperature""")
    enter()
    (value,re) = parser(comm,conditionTemp,"s")
    if(re == None):
        reFail = check(value,conditionFail)
        (_,e) = reFail.span()
        print(valueFail[e:e+22]) 
        return ("NA", "NA")
    endTemp = re.span()[1]
    temp = value[endTemp:endTemp+4]

    command(f"display ont optical-info {PORT} {ID} | include Rx")
    enter()
    (value,re) = parser(comm,conditionPwr,"s")
    if(re == None):
        (valueFail,reFail) = parser(comm,conditionFail,"s")
        (_,e) = reFail.span()
        print(valueFail[e:e+22]) 
        return ("NA", "NA")
    endPwr = re.span()[1]
    pwr = value[endPwr:endPwr+6]

    command("quit")
    enter()
    return (temp, pwr)
