# netgrapher
Tool fo auto generation of link state network topologies using SNMP. The code will take a base IP address and SNMP community string then poll each adjacennt device to generate the network diagram


# OID
Different vendor implement different MIB OIDs in their software below are generic and may not work with your equipment. Refer vendor OID library

'1.3.6.1.2.1.14.1.1' #ospf RouterId  
'1.3.6.1.2.1.14.10.1.3' #ospf Neighbor routerID  
'1.3.6.1.2.1.14.10.1.1' #ospf Neighbor IPAddress  

'1.3.6.1.2.1.138.1.1.1.3' #isis systemID Junos  
'1.3.6.1.4.1.4874.2.2.38.1.1.1.1.4' #isis SysID Juniper enterprise OID  
'1.3.6.1.4.1.9.10.118.1.1.1.3' #isis sysID cisco 

'1.3.6.1.2.1.138.1.6.1.1.6' #isis Neighbor sytemID Junos  
'1.3.6.1.4.1.9.10.118.1.6.1.1.6' #isis Neighbor sytemID Cisco

'1.3.6.1.2.1.138.1.6.3.1.3' #isis Neighbor IPAddress Junos  
'1.3.6.1.4.1.9.10.118.1.6.3.1.3' #isis Neighbor IPAddress Cisco
