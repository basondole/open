# talkToUs

> As in network devices saying "talk to us"

Talk to us allows a user to send commands to remote devices via SSH.
User has a flexibility of sending a single command or multiple commands or better yet refer commands from a text file.
These commands will can be run against a singel device whose ip address will be specified by the user,
similarly multiple ip addresses can used also with the flexibility of getting the ip addresses from a text file.

# Supported platforms
- Linux  
- Cisco IOS  
- Cisco IOSXE  
- Cisco IOSXR  
- JunOS  
- Arista EOS  
- Mikrotik RouterOS  

Hoppefully any device with a shell and SSH server :wink:


# Usage

### Checking the version
<pre>
C:\Users\u>talktous -version
talkToUs
Version: 2.0
Developer: Paul S.I. Basondole

C:\Users\u>
</pre>

### Running a single command on one device

Note on the output
> INFO: username and password auto-retrieved  
This is because my login credentials have already been saved (encypted) and the program just loads and decrypt the credentials without user having to re-enter the credential on each run

<pre>
C:\Users\u>talktous -commands "show bgp summary" -ipaddress "192.168.56.36"

INFO: username and password auto-retrieved

[192.168.56.36]


   show bgp summary
   ----------------
   Groups: 4 Peers: 6 Down peers: 6
   Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending
   inet.0                 0          0          0          0          0          0
   bgp.l3vpn.0            0          0          0          0          0          0
   bgp.l2vpn.0            0          0          0          0          0          0
   inetflow.0             0          0          0          0          0          0
   Peer                  AS     InPkt   OutPkt  OutQ  Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
   10.36.100.2           64512   0        0      0     0        6:49 Connect
   10.36.100.2           64518   0        0      0     0        6:49 Connect
   192.168.0.15          64512   0        0      0     0        6:49 Connect
   192.168.56.2          64512   0        0      0     0        6:49 Connect
   192.168.56.18         64512   0        0      0     0        6:49 Connect
   192.168.56.26         64512   0        0      0     0        6:49 Connect




INFO: Developed by Paul S.I. Basondole

C:\Users\u>
</pre>


### Running a multiple commands on one device
<pre>
C:\Users\u>talktous -commands "show version brief:show system alarms" -ipaddress "192.168.56.36"

INFO: username and password auto-retrieved

[192.168.56.36]


   show version brief
   ------------------
   Hostname: big
   Model: olive
   JUNOS Base OS boot [12.1R1.9]
   JUNOS Base OS Software Suite [12.1R1.9]
   JUNOS Kernel Software Suite [12.1R1.9]
   JUNOS Crypto Software Suite [12.1R1.9]
   JUNOS Packet Forwarding Engine Support (M/T Common) [12.1R1.9]
   JUNOS Packet Forwarding Engine Support (M20/M40) [12.1R1.9]
   JUNOS Online Documentation [12.1R1.9]
   JUNOS Voice Services Container package [12.1R1.9]
   JUNOS Border Gateway Function package [12.1R1.9]
   JUNOS Services AACL Container package [12.1R1.9]
   JUNOS Services LL-PDF Container package [12.1R1.9]
   JUNOS Services PTSP Container package [12.1R1.9]
   JUNOS Services Stateful Firewall [12.1R1.9]
   JUNOS Services NAT [12.1R1.9]
   JUNOS Services Application Level Gateways [12.1R1.9]
   JUNOS Services Captive Portal and Content Delivery Container package [12.1R1.9]
   JUNOS Services RPM [12.1R1.9]
   JUNOS Services HTTP Content Management package [12.1R1.9]
   JUNOS AppId Services [12.1R1.9]
   JUNOS IDP Services [12.1R1.9]
   JUNOS Services Crypto [12.1R1.9]
   JUNOS Services SSL [12.1R1.9]
   JUNOS Services IPSec [12.1R1.9]
   JUNOS Runtime Software Suite [12.1R1.9]
   JUNOS Routing Software Suite [12.1R1.9]


   show system alarms
   ------------------
   No alarms currently active




INFO: Developed by Paul S.I. Basondole

C:\Users\u>
</pre>

### Running multiple commands on multiple devices

<pre>
C:\Users\u>talktous -commands "show version:show bgp summary" -ipaddress "192.168.56.36:192.168.56.63"

INFO: username and password auto-retrieved

[192.168.56.63]


   show version
   ------------
   Cisco IOS Software, 7200 Software (C7200-ADVIPSERVICESK9-M), Version 15.2(4)S5, RELEASE SOFTWARE (fc1)
   Technical Support: http://www.cisco.com/techsupport
   Copyright (c) 1986-2014 by Cisco Systems, Inc.
   Compiled Thu 20-Feb-14 06:51 by prod_rel_team

   ROM: ROMMON Emulation Microcode
   BOOTLDR: 7200 Software (C7200-ADVIPSERVICESK9-M), Version 15.2(4)S5, RELEASE SOFTWARE (fc1)

   router-1 uptime is 11 minutes
   System returned to ROM by unknown reload cause - suspect boot_data[BOOT_COUNT] 0x0, BOOT_COUNT 0, BOOTDATA 19
   System image file is "tftp://255.255.255.255/unknown"
   Last reload reason: Unknown reason



   This product contains cryptographic features and is subject to United
   States and local country laws governing import, export, transfer and
   use. Delivery of Cisco cryptographic products does not imply
   third-party authority to import, export, distribute or use encryption.
   Importers, exporters, distributors and users are responsible for
   compliance with U.S. and local country laws. By using this product you
   agree to comply with applicable laws and regulations. If you are unable
   to comply with U.S. and local laws, return this product immediately.

   A summary of U.S. laws governing Cisco cryptographic products may be found at:
   http://www.cisco.com/wwl/export/crypto/tool/stqrg.html

   If you require further assistance please contact us by sending email to
   export@cisco.com.

   Cisco 7206VXR (NPE400) processor (revision A) with 491520K/32768K bytes of memory.
   Processor board ID 4279256517
   R7000 CPU at 150MHz, Implementation 39, Rev 2.1, 256KB L2 Cache
   6 slot VXR midplane, Version 2.1

   Last reset from power-on

   PCI bus mb0_mb1 (Slots 0, 1, 3 and 5) has a capacity of 600 bandwidth points.
   Current configuration on bus mb0_mb1 has a total of 400 bandwidth points.
   This configuration is within the PCI bus capacity and is supported.

   PCI bus mb2 (Slots 2, 4, 6) has a capacity of 600 bandwidth points.
   Current configuration on bus mb2 has a total of 0 bandwidth points
   This configuration is within the PCI bus capacity and is supported.

   Please refer to the following document "Cisco 7200 Series Port Adaptor
   Hardware Configuration Guidelines" on Cisco.com <http://www.cisco.com>
   for c7200 bandwidth points oversubscription and usage guidelines.


   2 FastEthernet interfaces
   509K bytes of NVRAM.

   8192K bytes of Flash internal SIMM (Sector size 256K).
   Configuration register is 0x2102


   show bgp summary
   ----------------
   BGP router identifier 192.168.142.63, local AS number 64512
   BGP table version is 2, main routing table version 2
   1 network entries using 144 bytes of memory
   1 path entries using 80 bytes of memory
   1/1 BGP path/bestpath attribute entries using 136 bytes of memory
   0 BGP route-map cache entries using 0 bytes of memory
   0 BGP filter-list cache entries using 0 bytes of memory
   BGP using 360 total bytes of memory
   BGP activity 1/0 prefixes, 1/0 paths, scan interval 60 secs

   Neighbor        V           AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
   192.168.56.15   4        64512       0       0        1    0    0 never    Idle
   192.168.56.26   4        64512       0       0        1    0    0 never    Idle



[192.168.56.36]


   show version
   ------------
   Hostname: big
   Model: olive
   JUNOS Base OS boot [12.1R1.9]
   JUNOS Base OS Software Suite [12.1R1.9]
   JUNOS Kernel Software Suite [12.1R1.9]
   JUNOS Crypto Software Suite [12.1R1.9]
   JUNOS Packet Forwarding Engine Support (M/T Common) [12.1R1.9]
   JUNOS Packet Forwarding Engine Support (M20/M40) [12.1R1.9]
   JUNOS Online Documentation [12.1R1.9]
   JUNOS Voice Services Container package [12.1R1.9]
   JUNOS Border Gateway Function package [12.1R1.9]
   JUNOS Services AACL Container package [12.1R1.9]
   JUNOS Services LL-PDF Container package [12.1R1.9]
   JUNOS Services PTSP Container package [12.1R1.9]
   JUNOS Services Stateful Firewall [12.1R1.9]
   JUNOS Services NAT [12.1R1.9]
   JUNOS Services Application Level Gateways [12.1R1.9]
   JUNOS Services Captive Portal and Content Delivery Container package [12.1R1.9]
   JUNOS Services RPM [12.1R1.9]
   JUNOS Services HTTP Content Management package [12.1R1.9]
   JUNOS AppId Services [12.1R1.9]
   JUNOS IDP Services [12.1R1.9]
   JUNOS Services Crypto [12.1R1.9]
   JUNOS Services SSL [12.1R1.9]
   JUNOS Services IPSec [12.1R1.9]
   JUNOS Runtime Software Suite [12.1R1.9]
   JUNOS Routing Software Suite [12.1R1.9]


   show bgp summary
   ----------------
   Groups: 4 Peers: 6 Down peers: 6
   Table          Tot Paths  Act Paths Suppressed    History Damp State    Pending
   inet.0                 0          0          0          0          0          0
   bgp.l3vpn.0            0          0          0          0          0          0
   bgp.l2vpn.0            0          0          0          0          0          0
   inetflow.0             0          0          0          0          0          0
   Peer                  AS     InPkt   OutPkt  OutQ  Flaps Last Up/Dwn State|#Active/Received/Accepted/Damped...
   10.36.100.2           64512   0        0      0     0        6:49 Connect
   10.36.100.2           64518   0        0      0     0        6:49 Connect
   192.168.0.15          64512   0        0      0     0        6:49 Connect
   192.168.56.2          64512   0        0      0     0        6:49 Connect
   192.168.56.18         64512   0        0      0     0        6:49 Connect
   192.168.56.26         64512   0        0      0     0        6:49 Connect




INFO: Developed by Paul S.I. Basondole

C:\Users\u>
</pre>

### Getting commands from a text file

<pre>
C:\Users\u>cat mycommands.txt
show system alarms
show system reboot

C:\Users\u>

C:\Users\u>talktous -commandsFile "mycommands.txt" -ipaddress 192.168.56.36

INFO: username and password auto-retrieved

[192.168.56.36]


   show system alarms
   ------------------
   No alarms currently active


   show system reboot
   ------------------
   No shutdown/reboot scheduled.




INFO: Developed by Paul S.I. Basondole

C:\Users\u>
</pre>

### Getting commands and ip addresses from text files
<pre>
C:\Users\u>cat mycommands.txt
show vrrp
show interface lo0

C:\Users\u>cat mydevices.txt
192.168.56.36
192.168.56.63

C:\Users\u>talktous.py -commandsFile mycommands.txt -ipaddressFile mydevices.txt

INFO: username and password auto-retrieved

[192.168.56.63]


   show vrrp
   ---------

   show interface lo0
   ------------------
   Loopback0 is up, line protocol is up
     Hardware is Loopback
     MTU 1514 bytes, BW 8000000 Kbit/sec, DLY 5000 usec,
        reliability 255/255, txload 1/255, rxload 1/255
     Encapsulation LOOPBACK, loopback not set
     Keepalive set (10 sec)
     Last input never, output never, output hang never
     Last clearing of "show interface" counters never
     Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
     Queueing strategy: fifo
     Output queue: 0/0 (size/max)
     5 minute input rate 0 bits/sec, 0 packets/sec
     5 minute output rate 0 bits/sec, 0 packets/sec
        0 packets input, 0 bytes, 0 no buffer
        Received 0 broadcasts (0 IP multicasts)
        0 runts, 0 giants, 0 throttles
        0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
        0 packets output, 0 bytes, 0 underruns
        0 output errors, 0 collisions, 0 interface resets
        0 unknown protocol drops
        0 output buffer failures, 0 output buffers swapped out



[192.168.56.36]


   show vrrp
   ---------
   warning: vrrp subsystem not running - not needed by configuration.


   show interfaces lo0
   -------------------
   Physical interface: lo0, Enabled, Physical link is Up
     Interface index: 6, SNMP ifIndex: 6
     Type: Loopback, MTU: Unlimited
     Device flags   : Present Running Loopback
     Interface flags: SNMP-Traps
     Link flags     : None
     Last flapped   : Never
       Input packets : 22
       Output packets: 22

     Logical interface lo0.0 (Index 99) (SNMP ifIndex 16)
       Flags: SNMP-Traps Encapsulation: Unspecified
       Input packets : 0
       Output packets: 0
       Protocol inet, MTU: Unlimited
         Flags: Sendbcast-pkt-to-re
       Protocol iso, MTU: Unlimited
         Flags: None
         Addresses, Flags: Is-Default Is-Primary
           Local: 49.1921.6813.3600

     Logical interface lo0.16384 (Index 98) (SNMP ifIndex 21)
       Flags: SNMP-Traps Encapsulation: Unspecified
       Input packets : 0
       Output packets: 0
       Protocol inet, MTU: Unlimited
         Flags: None
         Addresses
           Local: 127.0.0.1

     Logical interface lo0.16385 (Index 100) (SNMP ifIndex 22)
       Flags: SNMP-Traps Encapsulation: Unspecified
       Input packets : 22
       Output packets: 22
       Protocol inet, MTU: Unlimited
         Flags: None
         Addresses, Flags: Is-Default Is-Primary
           Local: 128.0.0.4
       Protocol inet6, MTU: Unlimited
         Flags: None
           Local: fe80::a00:270f:fcc6:60f8




INFO: Developed by Paul S.I. Basondole

C:\Users\u>
</pre>
