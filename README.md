# netgrapher
Tool for auto generation of link state such as OSPF and IS-IS network topologies using SNMP. The code will take a base IP address and SNMP community string then poll each adjacent device for protocol specific OIDs to gather neighborship details that will be used to generate the network diagram.


# OIDs
Different vendor implement different MIB OIDs in their software below are generic and may not work with your equipment. For more specifi OIDs for your environment refer your equipment vendor OID library

### OSPF
 OSPF RouterId
 ```
 1.3.6.1.2.1.14.1.1
 ```
 OSPF Neighbor routerID
```
1.3.6.1.2.1.14.10.1.3
```
 OSPF Neighbor IPAddress  
```
1.3.6.1.2.1.14.10.1.1
```
### ISIS
ISIS systemID Junos  
```
1.3.6.1.2.1.138.1.1.1.3
```
ISIS SysID Juniper enterprise OID 
```
1.3.6.1.4.1.4874.2.2.38.1.1.1.1.4
```
ISIS sysID cisco
```
1.3.6.1.4.1.9.10.118.1.1.1.3
```
ISIS Neighbor sytemID Junos
```
1.3.6.1.2.1.138.1.6.1.1.6
```
ISIS Neighbor sytemID Cisco
```
1.3.6.1.4.1.9.10.118.1.6.1.1.6
```
ISIS Neighbor IPAddress Junos 
```
1.3.6.1.2.1.138.1.6.3.1.3
```
ISIS Neighbor IPAddress Cisco
```
1.3.6.1.4.1.9.10.118.1.6.3.1.3
```
