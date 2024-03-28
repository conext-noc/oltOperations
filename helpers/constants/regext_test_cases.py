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

install_new_values = """

  Huawei Integrated Access Software (MA5800).
  Copyright(C) Huawei Technologies Co., Ltd. 2002-2021. All rights reserved.

  -----------------------------------------------------------------------------
  User last login information:
  -----------------------------------------------------------------------------
  Access Type : SSH
  IP-Address  : 54.149.142.43
  Login  Time : 2024-03-12 23:20:20-04:00
  Logout Time : 2024-03-12 23:20:44-04:00
  -----------------------------------------------------------------------------
  -----------------------------------------------------------------------------
  All user fail login information:
  -----------------------------------------------------------------------------
  Access Type IP-Address           Time                          Login Times
  -----------------------------------------------------------------------------
  SSH         10.7.110.233         2024-03-12 12:29:42-04:00              37
  SSH         10.3.172.67          2024-01-19 14:17:59-04:00              23
  SSH         54.149.142.43        2024-02-03 15:03:28-04:00              22
  SSH         10.3.172.66          2024-01-16 13:40:12-04:00              21
  SSH         10.6.111.99          2024-03-08 11:42:33-04:00              10
  SSH         52.36.152.69         2024-01-05 23:59:43-04:00               6
  SSH         181.232.180.78       2024-02-14 17:30:20-04:00               5
  SSH         181.232.180.77       2023-12-24 13:28:41-04:00               2
  -----------------------------------------------------------------------------

MARLLM01>
  Warning: The user password is set by other administrator or NMS, it is
recommended to change the password.

MARLLM01>enable

MARLLM01#

MARLLM01#config

MARLLM01(config)#

MARLLM01(config)#scroll 512

MARLLM01(config)#

MARLLM01(config)#display ont autofind all | no-more
{ <cr>||<K> }:

  Command:
          display ont autofind all | no-more
   ----------------------------------------------------------------------------
   Number              : 1
   F/S/P               : 0/1/3
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754430B086EA9 (HWTC-0B086EA9)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 260F.A
   Ont SoftwareVersion : V5R020C10S035
   Ont EquipmentID     : EG8010Hv6
   Ont Customized Info : COMMON
   Ont MAC             : B85F-B0E0-61DE
   Ont Equipment SN    : 2150084674LDN3000737
   Ont autofind time   : 2024-03-12 02:33:42-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 2
   F/S/P               : 0/1/3
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754430B0A58A9 (HWTC-0B0A58A9)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 260F.A
   Ont SoftwareVersion : V5R020C10S035
   Ont EquipmentID     : EG8010Hv6
   Ont Customized Info : COMMON
   Ont MAC             : B85F-B0E0-7318
   Ont Equipment SN    : 2150084674LDN3001227
   Ont autofind time   : 2024-03-12 20:40:54-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 3
   F/S/P               : 0/1/3
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544399483DA5 (HWTC-99483DA5)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S350
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : A4BD-C436-D3EE
   Ont Equipment SN    : 2150083877EGM3002227
   Ont autofind time   : 2024-03-12 02:33:42-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 4
   F/S/P               : 0/1/4
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443EF11ED9F (HWTC-EF11ED9F)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S115
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 01:08:21-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 5
   F/S/P               : 0/1/5
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544393CCB9A4 (HWTC-93CCB9A4)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S270
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : 7CD9-A0B0-3D29
   Ont Equipment SN    : 2150083877EGLB027373
   Ont autofind time   : 2024-03-08 15:50:14-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 6
   F/S/P               : 0/1/10
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443929FE29D (HWTC-929FE29D)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 22AD.A
   Ont SoftwareVersion : V5R020C00S035
   Ont EquipmentID     : EG8145X6
   Ont Customized Info : COMMON
   Ont MAC             : 4482-E6B0-9515
   Ont Equipment SN    : 2150083684LDK2095290
   Ont autofind time   : 2024-03-11 23:26:47-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 7
   F/S/P               : 0/2/1
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443F17509A6 (HWTC-F17509A6)
   Password            : 0x61697274656B00000000(airtek)
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S385
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : E813-6E6F-FD5B
   Ont Equipment SN    : 2150083877EGM8019184
   Ont autofind time   : 2024-03-12 02:03:58-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 8
   F/S/P               : 0/2/5
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544393CB86A4 (HWTC-93CB86A4)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S270
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : 7CD9-A0B0-28C6
   Ont Equipment SN    : 2150083877EGLB027066
   Ont autofind time   : 2024-03-10 22:17:39-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 9
   F/S/P               : 0/2/5
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544393CCE6A4 (HWTC-93CCE6A4)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S270
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : 7CD9-A0B0-4026
   Ont Equipment SN    : 2150083877EGLB027418
   Ont autofind time   : 2024-03-10 19:06:57-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 10
   F/S/P               : 0/2/6
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544393CBEDA4 (HWTC-93CBEDA4)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S270
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : 7CD9-A0B0-2F9D
   Ont Equipment SN    : 2150083877EGLB027169
   Ont autofind time   : 2024-03-12 11:07:16-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 11
   F/S/P               : 0/2/8
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754430B0A25A9 (HWTC-0B0A25A9)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 260F.A
   Ont SoftwareVersion : V5R020C10S035
   Ont EquipmentID     : EG8010Hv6
   Ont Customized Info : COMMON
   Ont MAC             : B85F-B0E0-714D
   Ont Equipment SN    : 2150084674LDN3001176
   Ont autofind time   : 2024-03-11 22:42:34-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 12
   F/S/P               : 0/2/9
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754439E1AB09D (HWTC-9E1AB09D)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : AF6.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8120L
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 16:22:49-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 13
   F/S/P               : 0/2/11
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443F17C02A6 (HWTC-F17C02A6)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S385
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : E813-6E70-73E4
   Ont Equipment SN    : 2150083877EGM8020969
   Ont autofind time   : 2024-03-12 00:23:34-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 14
   F/S/P               : 0/2/12
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754430B0853A9 (HWTC-0B0853A9)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 260F.A
   Ont SoftwareVersion : V5R020C10S035
   Ont EquipmentID     : EG8010Hv6
   Ont Customized Info : COMMON
   Ont MAC             : B85F-B0E0-60EB
   Ont Equipment SN    : 2150084674LDN3000710
   Ont autofind time   : 2023-05-16 18:15:51-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 15
   F/S/P               : 0/2/12
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754430B0A97A9 (HWTC-0B0A97A9)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 260F.A
   Ont SoftwareVersion : V5R020C10S035
   Ont EquipmentID     : EG8010Hv6
   Ont Customized Info : COMMON
   Ont MAC             : B85F-B0E0-754F
   Ont Equipment SN    : 2150084674LDN3001290
   Ont autofind time   : 2024-03-10 22:17:44-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 16
   F/S/P               : 0/2/12
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443EF11E49F (HWTC-EF11E49F)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S115
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 11:06:26-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 17
   F/S/P               : 0/2/14
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443EF0E609F (HWTC-EF0E609F)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S115
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 02:03:59-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 18
   F/S/P               : 0/2/15
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443EF13549F (HWTC-EF13549F)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S115
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-10 22:18:45-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 19
   F/S/P               : 0/3/1
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544393CC0AA4 (HWTC-93CC0AA4)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S270
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : 7CD9-A0B0-318A
   Ont Equipment SN    : 2150083877EGLB027198
   Ont autofind time   : 2024-03-12 00:00:29-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 20
   F/S/P               : 0/3/1
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544393CC64A4 (HWTC-93CC64A4)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S270
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : 7CD9-A0B0-3784
   Ont Equipment SN    : 2150083877EGLB027288
   Ont autofind time   : 2024-02-01 19:09:22-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 21
   F/S/P               : 0/3/5
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754430B096AA9 (HWTC-0B096AA9)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 260F.A
   Ont SoftwareVersion : V5R020C10S035
   Ont EquipmentID     : EG8010Hv6
   Ont Customized Info : COMMON
   Ont MAC             : B85F-B0E0-6ABA
   Ont Equipment SN    : 2150084674LDN3000989
   Ont autofind time   : 2024-03-11 17:58:34-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 22
   F/S/P               : 0/3/5
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544393DB67A4 (HWTC-93DB67A4)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S270
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : 7CD9-A0B1-36B7
   Ont Equipment SN    : 2150083877EGLB019031
   Ont autofind time   : 2024-03-11 18:01:17-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 23
   F/S/P               : 0/3/9
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443EF11A29F (HWTC-EF11A29F)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S115
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 17:47:43-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 24
   F/S/P               : 0/4/4
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754439E12827D (HWTC-9E12827D)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 20:37:53-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 25
   F/S/P               : 0/4/11
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443A5592D9B (HWTC-A5592D9B)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 1746.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8120L
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 23:14:50-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 26
   F/S/P               : 0/5/7
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443A54A789B (HWTC-A54A789B)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : 70C7-F357-DC00
   Ont Equipment SN    : 2150083615EGJ6088392
   Ont autofind time   : 2024-03-12 20:35:22-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 27
   F/S/P               : 0/5/8
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754436F1349A7 (HWTC-6F1349A7)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 03:44:06-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 28
   F/S/P               : 0/5/8
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754437A0DB339 (HWTC-7A0DB339)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 03:44:24-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 29
   F/S/P               : 0/5/8
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443FA063E42 (HWTC-FA063E42)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 635.A
   Ont SoftwareVersion : V3R015C10S150
   Ont EquipmentID     : HG8010H
   Ont Customized Info : -
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 13:45:01-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 30
   F/S/P               : 0/5/10
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443199A0D9B (HWTC-199A0D9B)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 1746.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8120L
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 21:53:41-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 31
   F/S/P               : 0/6/2
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443922A4C9D (HWTC-922A4C9D)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 1746.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8120L
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 03:43:55-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 32
   F/S/P               : 0/6/11
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754431A2AE939 (HWTC-1A2AE939)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 00:49:23-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 33
   F/S/P               : 0/6/12
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754439E06B8A6 (HWTC-9E06B8A6)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 22AD.A
   Ont SoftwareVersion : V5R020C00S080
   Ont EquipmentID     : EG8145X6
   Ont Customized Info : COMMON
   Ont MAC             : 30C5-0F9E-06B8
   Ont Equipment SN    : 2150084405HYM7056537
   Ont autofind time   : 2024-03-12 02:34:44-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 34
   F/S/P               : 0/7/0
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754435D81AC39 (HWTC-5D81AC39)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 04:09:13-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 35
   F/S/P               : 0/7/2
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443B841429D (HWTC-B841429D)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : C88D-84D8-9998
   Ont Equipment SN    : 2150083414AGH6022303
   Ont autofind time   : 2024-03-12 04:09:08-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 36
   F/S/P               : 0/7/4
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443A59E169B (HWTC-A59E169B)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : 70C7-F333-9755
   Ont Equipment SN    : 2150083615EGJ6037211
   Ont autofind time   : 2024-03-12 05:32:40-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 37
   F/S/P               : 0/7/7
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443C7E30C39 (HWTC-C7E30C39)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 12:24:38-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 38
   F/S/P               : 0/10/4
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 485754436F1146A7 (HWTC-6F1146A7)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V3R017C10S102
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 02:37:29-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 39
   F/S/P               : 0/10/12
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544349364D39 (HWTC-49364D39)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 07:43:51-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 40
   F/S/P               : 0/11/2
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544392AB049D (HWTC-92AB049D)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 147C.A
   Ont SoftwareVersion : V5R019C20S050
   Ont EquipmentID     : HS8545M5
   Ont Customized Info : COMMON
   Ont MAC             : 4482-E6AE-E810
   Ont Equipment SN    : 2150083684LDK2054062
   Ont autofind time   : 2024-03-12 21:17:40-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 41
   F/S/P               : 0/11/8
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544399477EA5 (HWTC-99477EA5)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 159D.A
   Ont SoftwareVersion : V5R019C10S350
   Ont EquipmentID     : EG8145V5
   Ont Customized Info : COMMON
   Ont MAC             : A4BD-C436-C73F
   Ont Equipment SN    : 2150083877EGM3002036
   Ont autofind time   : 2024-03-11 17:58:32-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 42
   F/S/P               : 0/11/9
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 4857544385694939 (HWTC-85694939)
   Password            : 0x00000000000000000000
   Loid                :
   Checkcode           :
   VendorID            : HWTC
   Ont Version         : 16FC.A
   Ont SoftwareVersion : V5R019C00S050
   Ont EquipmentID     : EG8141A5
   Ont Customized Info : COMMON
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 02:38:00-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   Number              : 43
   F/S/P               : 0/11/9
   ONT NNI type        : 2.5G/1.25G
   Ont SN              : 48575443B1E24D7C (HWTC-B1E24D7C)
   Password            : 0x31323334353637383930(1234567890)
   Loid                : user
   Checkcode           :
   VendorID            : BDCM
   Ont Version         : V1.0
   Ont SoftwareVersion : 10.10.27G_26
   Ont EquipmentID     : 1126
   Ont Customized Info : -
   Ont MAC             : -
   Ont Equipment SN    : -
   Ont autofind time   : 2024-03-12 02:37:30-04:00
   Multi channel       : -
   ----------------------------------------------------------------------------
   The number of GPON autofind ONT is 43

MARLLM01(config)#"""

version_values = """
MARLLM01(config)#display ont version 0  1 3 7
{ <cr>||<K> }:

  Command:
          display ont version 0  1 3 7
  --------------------------------------------------------------------------
  F/S/P                    : 0/1/3
  ONT-ID                   : 7
  Vendor-ID                : HWTC
  ONT Version              : 22AD.A
  Product-ID               : 22a
  Equipment-ID             : EG8145X6
  Main Software Version    : V5R020C00S080
  Standby Software Version : V5R020C00S070
  OntProductDescription    : OptiXstar EG8145X6 GPON Terminal (CLASS B+/PROD
                             UCT ID:2150084405HYM7076782/CHIP:00000020210603
                             )
  Support XML Version      : 1.3.0.0
  Ont MAC                  : 30C5-0F51-AC92
  Ont Equipment SN         : 2150084405HYM7076782
  --------------------------------------------------------------------------

MARLLM01(config)#"""

