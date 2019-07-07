#Forked from Mihai Catalin Teodosiu work on "OSPF Network Discovery via SNMP"
#Author: Paul S.I. Basondole
#E-mail: bassosimons@me.com

import pprint
import subprocess
import binascii
import sys

import matplotlib.pyplot as matp
import networkx as nx

from colorama import init, deinit, Fore, Style
from pysnmp.entity.rfc3413.oneliner import cmdgen

# Pre requisite
# all link running IGP should be point-to-point links
# for juniper equipment JunOS 11.4R9 or later is required
# if the above arent met diagram data will still be useful just not very accurate


#SNMP function
def snmp_get(ip):
    print "\n---------BEGIN---------------"
    nbridlist = []
    nbriplist = []
    _devices = {}
    
    #Creating command generator object
    cmdGen = cmdgen.CommandGenerator()
    
    #Performing SNMP GETNEXT operations on the OIDs
    #The basic syntax of nextCmd: nextCmd(authData, transportTarget, *varNames)
    #The nextCmd method returns a tuple of (errorIndication, errorStatus, errorIndex, varBindTable)

    hostname = False
    errIndication,errStatus,errIndex, hostname = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                   cmdgen.UdpTransportTarget((ip, 161)),                                                                  
                                                                    '1.3.6.1.2.1.1.5')
    #print ip, hostname
    for item in hostname:
        for oid, host in item:
            _host = str(host)
            if 'SNET-' in _host: _host=_host.lstrip('SNET').lstrip('-')
            _host = _host.rstrip('simbanet.co.tz')
            print('%s = %s' % (oid, host))

    # check if the hostname is already querried, if it is return
    for n in range(0, len(devices_list)):
        if devices_list[n]["Host"] == _host:
            print(_host, "SKIPPED ALREADY POLLED")
            return

        
    interfaces = False
    errIndication,errStatus,errIndex, interfaces = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                   cmdgen.UdpTransportTarget((ip, 161)),                                                                  
                                                                    '1.3.6.1.2.1.31.1.1.1.1')
    #print ip, interfaces
    all_interfaces = {}
    for item in interfaces:
        for oid, iface in item:
            all_interfaces[str(oid)]=str(iface)
            #print('%s = %s' % (oid, iface))
    #print(all_interfaces)
    #sys.exit()

    hostId = False
    errIndication,errStatus,errIndex, hostId = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                     cmdgen.UdpTransportTarget((ip, 161)),
                                                                     '1.3.6.1.2.1.138.1.1.1.3') #isis systemID Junos
                                                                     #'1.3.6.1.2.1.14.1.1') #ospf RouterId

    if not hostId:
        errIndication,errStatus,errIndex, hostId = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                         cmdgen.UdpTransportTarget((ip, 161)),
                                                                     '1.3.6.1.4.1.4874.2.2.38.1.1.1.1.4')
        
    if not hostId: 
        errIndication,errStatus,errIndex, hostId = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                     cmdgen.UdpTransportTarget((ip, 161)),
                                                                     '1.3.6.1.4.1.9.10.118.1.1.1.3')#isis sysID cisco ciiSysID from CISCO-IETF-ISIS-MIB

    #print ip, hostId
    for item in hostId:
        for oid, hostid in item:
            hex_string = binascii.hexlify(str(hostid))
            octets = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            ip_ = [int(i, 16) for i in octets]
            _host_id = '.'.join(str(i) for i in ip_)
            print('%s = %s' % (oid, hostid))
    #sys.exit()

    varBindNbrTable = False
    errIndication,errStatus,errIndex, varBindNbrTable = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                       cmdgen.UdpTransportTarget((ip, 161)),
                                                                       '1.3.6.1.2.1.138.1.6.1.1.6') #isis Neighbor sytemID Junos
                                                                       #'1.3.6.1.2.1.14.10.1.3') #ospf Neighbor routerID

    if not varBindNbrTable:
        errIndication,errStatus,errIndex, varBindNbrTable = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                       cmdgen.UdpTransportTarget((ip, 161)),
                                                                       '1.3.6.1.4.1.9.10.118.1.6.1.1.6') #isis Neighbor sytemID Cisco

    #print(varBindNbrTable)
    for varBindNbrTableRow in varBindNbrTable:
        for oid, nbrid in varBindNbrTableRow:
            hex_string = binascii.hexlify(str(nbrid))
            #print(hex_string)
            octets = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            #print(octets)
            ip_ = [int(i, 16) for i in octets]
            #print(ip)
            nbr_r_id = '.'.join(str(i) for i in ip_)
            #print(nbr_r_id)
            nbridlist.append(nbr_r_id)
            #print('%s = %s' % (oid, nbr_r_id))
            
    #sys.exit()

    varBindNbrIpTable = False
    errorIndication, errorStatus, errorIndex, varBindNbrIpTable = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                                 cmdgen.UdpTransportTarget((ip, 161)),
                                                                                 '1.3.6.1.2.1.138.1.6.3.1.3') #isis Neighbor IPAddress Junos
                                                                                 #'1.3.6.1.2.1.14.10.1.1') #ospf Neighbor IPAddress

    if not varBindNbrIpTable:
        errorIndication, errorStatus, errorIndex, varBindNbrIpTable = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                                 cmdgen.UdpTransportTarget((ip, 161)),
                                                                                 '1.3.6.1.4.1.9.10.118.1.6.3.1.3') #isis Neighbor IPAddress Cisco

    
    #print(varBindNbrIpTable)
    for varBindNbrIpTableRow in varBindNbrIpTable:
        for oid, nbrip in varBindNbrIpTableRow:
            hex_string = binascii.hexlify(str(nbrip))
            octets = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            ip_ = [int(i, 16) for i in octets]
            nbr_ip = '.'.join(str(i) for i in ip_)
            if len(nbr_ip)<=15: #only take valid IP addresses
                nbriplist.append(nbr_ip)
                #print('%s = %s' % (oid, nbr_ip))
    #sys.exit()

    varIfIndex = False
    errIndication,errStatus,errIndex, varIfIndex = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                     cmdgen.UdpTransportTarget((ip, 161)),
                                                                     '1.3.6.1.2.1.138.1.3.2.1.2') #get ifindex for isis interfaces junos
    if varIfIndex:
        ifnames = []
        for item in varIfIndex:
            for oid, ifindex in item:
                #print('%s = %s' % (oid, ifindex))
                if not 'lo0' in all_interfaces['1.3.6.1.2.1.31.1.1.1.1.'+str(ifindex)]:
                    ifnames.append(all_interfaces['1.3.6.1.2.1.31.1.1.1.1.'+str(ifindex)])
                    
        if ifnames: # remove logical tunnel interfaces configured on the logical system side junos
            for x in range(len(ifnames)):
                try:
                  if ifnames[x].split('.')[0] == ifnames[x+1].split('.')[0]:
                     if 'lt' in ifnames[x]: ifnames.pop(x+1)
                except IndexError: pass
                
    if not varIfIndex:
            errIndication,errStatus,errIndex, varIfIndex = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                     cmdgen.UdpTransportTarget((ip, 161)),
                                                                    '1.3.6.1.4.1.9.10.118.1.3.2.1.2') #get ifindex for isis interfaces cisco

            ifnames = []
            for item in varIfIndex:
                for oid, ifindex in item:
                    #print('%s = %s' % (oid, ifindex))
                    if not 'Lo0' in all_interfaces['1.3.6.1.2.1.31.1.1.1.1.'+str(ifindex)]:
                        ifnames.append(all_interfaces['1.3.6.1.2.1.31.1.1.1.1.'+str(ifindex)])



    querried_neighbors_names.append((_host,_host_id))

    #sys.exit()
    
    #Adding OSPF data by device in the ospf_device dictionary
    _devices["Host"] = _host
    _devices["HostId"] = _host_id
    _devices["NbrRtrId"] = nbridlist
    _devices["NbrRtrIp"] = nbriplist
    _devices["Interface"] = ifnames
    
    devices_list.append(_devices)
    #pprint.pprint(devices_list)
    return devices_list




	############# Application #5 - Part #3 #############

def find_unqueried_neighbors():

    global querried_neighbors
    
    querried_neighbors = list(set(querried_neighbors))
    
    #Neighbor OSPF Router IDs
    all_nbr_ids = []

    #print len(devices_list)
    for n in range(0, len(devices_list)):
        for each_nid in devices_list[n]["NbrRtrId"]:
	    
            if each_nid == "0.0.0.0": pass
	    
            else:
                if each_nid not in querried_neighbors:
                    all_nbr_ids.append(each_nid)
                    
    all_nbr_ids = list(set(all_nbr_ids))
    print("Neighbors of the host, these neighbors need to be polled")
    print(all_nbr_ids)
    #sys.exit()
    
    #Running the snmp_get() function for each unqueried neighbor
    print "lenght of devices_list",len(devices_list)

    for q in all_nbr_ids:
        for r in range(0, len(devices_list)):
            for index,s in enumerate(devices_list[r]["NbrRtrId"]):
                #print(q+'/'+str(len(all_nbr_ids)), str(r)+'/'+str(len(ospf)), s+'/'+str(len(ospf[r]["NbrRtrId"])))
                if q == s:
                    print('    found router-id that matches neighbor ID')
                    try: new_ip = devices_list[r]["NbrRtrIp"][index]
                    except IndexError: continue
                    print("    NEW_IP",new_ip)
                    try:
                        snmp_get(new_ip)
                        querried_neighbors.append(s)
                        print("    ",q,r,s, "DONE")
                    except Exception as e:
                       print(e)
                       querried_neighbors.append(s)
                       print("    ",q,r,s,new_ip, "SKIPPED FAIL POLL")


    return all_nbr_ids, devices_list

#Creating list of neighborships
def neighborship(final_devices_list):
    neighborship_dict = {}
    for each_dictionary in final_devices_list:
        for index, each_neighbor in enumerate(each_dictionary["NbrRtrId"]):
            each_tuple = (each_dictionary["HostId"], each_neighbor)
            neighborship_dict[each_tuple] = each_dictionary["NbrRtrIp"][index]
    return neighborship_dict

#function to map hostname and sysID by paul
def id_to_name(final_devices_list):
    id_host = {}
    for item in final_devices_list: id_host[item['HostId']] = item['Host']
    return id_host

#function to map link ipaddress and interface by paul
def ip_to_name(final_devices_list):
    ip_iface = {}
    for item in final_devices_list:
        for index, each_neighbor in enumerate(item["NbrRtrId"]):
            each_tuple = (each_neighbor,item["HostId"])
            ip_iface[each_tuple] = item['Interface'][index] + '\n'+ item["NbrRtrIp"][index]
            try: neighborship_dict[each_tuple]= item['Interface'][index] + '\n'+ neighborship_dict[each_tuple]
            except KeyError: pass
    return neighborship_dict




if __name__ == '__main__':

    #Prompting user for input
    ip = raw_input(Fore.BLUE + Style.BRIGHT + "\n* Please enter root device IP: ")
    comm = raw_input(Fore.BLUE + Style.BRIGHT + "\n* Please enter SNMP community: ")


    querried_neighbors = []
    querried_neighbors_names = []
    devices_list = []

    devices_list = snmp_get(ip)
    querried_neighbors.append(devices_list[0]["HostId"])
    pprint.pprint(devices_list)
    #sys.exit()

    while True:
        all_nbr_ids, devices_list = find_unqueried_neighbors()
        if len(all_nbr_ids)==0: break


    final_devices_list = devices_list
    #pprint.pprint(final_devices_list)

    neighborship_dict = neighborship(final_devices_list)
    #pprint.pprint(neighborship_dict)

    neighborship_dict = ip_to_name(final_devices_list)
    #pprint.pprint(neighborship_dict)


    #Initialize colorama
    init()

    while True:
        try:
            #User defined actions
            print(Fore.BLUE + Style.BRIGHT + "* Please choose an action:\n\n1 - Display OSPF devices on the screen\n2 - Export OSPF devices to CSV file\n3 - Generate OSPF network topology\n4 - Generate interactive network topology\n5 - Generate GEFX file to use with Gephi\ne - Exit")
            user_choice = raw_input("\n* Enter your choice: ")
            print("\n")

            #Defining actions
            if user_choice == "1":
                
                for each_dict in final_devices_list:
                    print("Hostname: " + Fore.YELLOW + Style.BRIGHT + "%s" % each_dict["Host"] + Fore.BLUE + Style.BRIGHT)
                    print("OSFP RID: " + Fore.YELLOW + Style.BRIGHT + "%s" % each_dict["HostId"] + Fore.BLUE + Style.BRIGHT)
                    print("OSPF Neighbors by ID: " + Fore.YELLOW + Style.BRIGHT + "%s" % ', '.join(each_dict["NbrRtrId"]) + Fore.BLUE + Style.BRIGHT)
                    print("OSPF Neighbors by IP: " + Fore.YELLOW + Style.BRIGHT + "%s" % ', '.join(each_dict["NbrRtrIp"]) + Fore.BLUE + Style.BRIGHT)
                    print("\n")
                    
                continue
            
            #Printing devices to CSV file
            elif user_choice == "2":
                print(Fore.CYAN + Style.BRIGHT + "* Generating " + Fore.YELLOW + Style.BRIGHT + "OSPF_DEVICES" + Fore.CYAN + Style.BRIGHT + " file...\n")
                print(Fore.CYAN + Style.BRIGHT + "* Check the script folder. Import the file into Excel for a better view of the devices.\n")
                
                csv_file = open("OSPF_DEVICES.txt", "w")
                
                print >>csv_file, "Hostname" + ";" + "OSPFRouterID" + ";" + "OSPFNeighborRouterID" + ";" + "OSPFNeighborIP"
                
                for each_dict in final_devices_list:
                    print >>csv_file, each_dict["Host"] + ";" + each_dict["HostId"] + ";" + ', '.join(each_dict["NbrRtrId"] + ";" + ', '.join(each_dict["NbrRtrIp"]))
                    
                csv_file.close()
                    
                continue
                    
            #Generating network topology   
            elif user_choice == "3":
                print(Fore.CYAN + Style.BRIGHT + "* Generating network topology...\n" + Fore.BLUE + Style.BRIGHT)
                
                #Drawing the topology using the list of neighborships
                G = nx.Graph()
                G.add_edges_from(neighborship_dict.keys())
                pos = nx.spring_layout(G, k = 0.5, iterations = 70)
                #pos = nx.bipartite_layout(G,neighborship_dict.keys())
                #pos = nx.circular_layout(G)
                #pos = nx.shell_layout(G)
                #pos = nx.random_layout(G)
                #pos = nx.spectral_layout(G)
                #pos = nx.kamada_kawai_layout(G)
                #pos = nx.fruchterman_reingold_layout(G)
                nx.draw_networkx_labels(G, pos,labels=id_to_name(final_devices_list), font_size = 9, font_family = "sans-serif", font_weight = "bold")
                nx.draw_networkx_edges(G, pos, width = 4, alpha = 0.4, edge_color = 'black')
                nx.draw_networkx_edge_labels(G, pos, neighborship_dict, label_pos = 0.3, font_size = 6)
                nx.draw(G, pos, node_size = 700, with_labels = False, node_color = 'red')
                matp.show()
                
                continue

            elif user_choice == "4":
                import netgraph
                G = nx.Graph()
                G.add_edges_from(neighborship_dict.keys())
                interactive_graph = netgraph.InteractiveGraph(G)

                node_positions = interactive_graph.node_positions
                edge_list = interactive_graph.edge_list
                node_labels = id_to_name(final_devices_list)
                
                # add nodes that could not be querried by SNMP
                for node in node_positions.keys():
                    if node not in node_labels.keys(): node_labels[node]=''
                edge_labels = {key:neighborship_dict[key] for key in neighborship_dict.keys() if key in edge_list}

                #print.pprint(node_positions)
                #print(node_labels)
                #print(node_positions.keys())
                #print(edge_labels)

                interactive_graph.draw_node_labels(node_labels, node_positions,node_label_font_size=9)

                matp.show()

            elif user_choice == "5":
                import os
                G = nx.Graph()
                G.add_edges_from(neighborship_dict.keys())
                
                for edge in neighborship_dict.keys(): #loop through and add label for edges
                  G.edges[edge]['label'] = neighborship_dict[edge]

                nodes =id_to_name(final_devices_list)

                for node in nodes.keys(): #loop through and add label attribute for nodes
                  G.add_node(node)
                  G.node[node]['label'] = nodes[node]

                nx.write_gexf(G, "Network_Diagram.gexf")
                print(Fore.RED + Style.BRIGHT + "File saved as <Network_Diagram.gexf> location "+ os.getcwd())
                
            elif user_choice == "e":
                print(Fore.RED + Style.BRIGHT + "* Exiting... Bye!\n")
                sys.exit()
                
            else:
                print(Fore.RED + Style.BRIGHT + "* Invalid option. Please retry.\n")
                continue
            
        except KeyboardInterrupt:
            print(Fore.RED + Style.BRIGHT + "\n\n* Program aborted by user. Exiting...\n")
            sys.exit()

        #De-initialize colorama
        deinit()
