optical_values = """interface  gpon  0/1   

MARLLM01(config-if-gpon-0/1)# 

MARLLM01(config-if-gpon-0/1)#  display  ont  optical-info  2  0  |  no-more 
{ <cr>||<K> }:  

  Command:
            display  ont  optical-info  2  0  |  no-more
  -----------------------------------------------------------------------------
  ONU NNI port ID                        : 0
  Module type                            : GPON
  Module sub-type                        : CLASS B+
  Used type                              : ONU
  Encapsulation Type                     : BOSA ON BOARD
  Optical power precision(dBm)           : 3.0
  Vendor name                            : HUAWEI          
  Vendor rev                             : -
  Vendor PN                              : HW-BOB-0007     
  Vendor SN                              : 1943WJ830108S   
  Date Code                              : 19-12-22
  Rx optical power(dBm)                  : -18.18
  Rx power current warning threshold(dBm): [-,-]
  Rx power current alarm threshold(dBm)  : [-29.0,-7.0]
  Tx optical power(dBm)                  : 2.27
  Tx power current warning threshold(dBm): [-,-]
  Tx power current alarm threshold(dBm)  : [0.0,5.0]
  Laser bias current(mA)                 : 16
  Tx bias current warning threshold(mA)  : [-,-]
  Tx bias current alarm threshold(mA)    : [2.000,100.000]
  Temperature(C)                         : 58
  Temperature warning threshold(C)       : [-,-]
  Temperature alarm threshold(C)         : [-61,95]
  Voltage(V)                             : 3.360
  Supply voltage warning threshold(V)    : [-,-]
  Supply voltage alarm threshold(V)      : [3.000,3.600]
  OLT Rx ONT optical power(dBm)          : -22.22
  CATV Rx optical power(dBm)             : -
  CATV Rx power alarm threshold(dBm)     : [-,-]
  -----------------------------------------------------------------------------

MARLLM01(config-if-gpon-0/1)#quit 

MARLLM01(config)# 

MARLLM01(config)#"""
