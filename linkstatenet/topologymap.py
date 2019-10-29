'''
Generate topology database for link  state protocol.
The topology database can then be used to generate network diagram.
Pre-requisites:
    - Link type should be point-to-point links
    - For juniper equipment JunOS 11.4R9 or later is required
    
NB: If pre-requisites are not met diagram data will still be useful but just not very accurate
'''

import pprint
import subprocess
import binascii
import sys
import matplotlib.pyplot as matp
import networkx as nx
from colorama import init, deinit, Fore, Style
from pysnmp.entity.rfc3413.oneliner import cmdgen


__author__ = "Paul S.I. Basondole"
__credits__ = "Mihai Catalin Teodosiu"
__version__ = "1.0.1"
__maintainer__ = "Paul S.I. Basondole"
__email__ = "bassosimons@me.com"



def snmp_get(ip,comm,protocol):
    ''' Collect information from devices and return a dictionary of devices and their link state'''

    global devices_list
    nbridlist = []
    nbriplist = []
    _devices = {}
    

    hostname_oid = '1.3.6.1.2.1.1.5'
    interface_oid = '1.3.6.1.2.1.31.1.1.1.1'
    if protocol == 'ospf':
        router_id_oid = ['1.3.6.1.2.1.14.1.1']
        neighbor_router_id_oid = ['1.3.6.1.2.1.14.10.1.3']
        neighbor_router_ip_oid = ['1.3.6.1.2.1.14.10.1.1']

    if protocol == 'isis':
        ''' to match possible oids from
        juniper systemID, Cisco ciissysID and Juniper Ent systemID
        '''
        router_id_oid = ['1.3.6.1.2.1.138.1.1.1.3',
                         '1.3.6.1.4.1.4874.2.2.38.1.1.1.1.4',
                         '1.3.6.1.4.1.9.10.118.1.1.1.3']
        neighbor_router_id_oid = ['1.3.6.1.2.1.138.1.6.1.1.6',
                                  '1.3.6.1.4.1.9.10.118.1.6.1.1.6']

        neighbor_router_ip_oid = ['1.3.6.1.2.1.138.1.6.3.1.3',
                                  '1.3.6.1.4.1.9.10.118.1.6.3.1.3']
        protocol_ifindex_oid = ['1.3.6.1.2.1.138.1.3.2.1.2',
                                '1.3.6.1.4.1.9.10.118.1.3.2.1.2']


    #Creating command generator object
    cmdGen = cmdgen.CommandGenerator()
    
    '''
    Performing SNMP GETNEXT operations on the OIDs
    The basic syntax of nextCmd: nextCmd(authData, transportTarget, *varNames)
    The nextCmd method returns a tuple of (errorIndication, errorStatus, errorIndex, varBindTable)
    '''
    
    hostname = False
    errIndication,errStatus,errIndex, hostname = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                cmdgen.UdpTransportTarget((ip, 161)),                                                                  
                                                                hostname_oid)
    # print ip, hostname
    for item in hostname:
        for oid, host in item:
            _host = str(host)
            print('%s = %s' % (oid, host))

    # check if the hostname is already querried, if it is return
    for n in range(0, len(devices_list)):
        if devices_list[n]["Host"] == _host:
            #print(_host, "SKIPPED ALREADY POLLED")
            return

        
    interfaces = False
    errIndication,errStatus,errIndex, interfaces = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                  cmdgen.UdpTransportTarget((ip, 161)),                                                                  
                                                                  interface_oid)

    all_interfaces = {}
    for item in interfaces:
        for oid, iface in item:
            all_interfaces[str(oid)]=str(iface)
            #print('%s = %s' % (oid, iface))
    #print(all_interfaces)


    hostId = False
    for oid in router_id_oid:
        errIndication,errStatus,errIndex, hostId = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                  cmdgen.UdpTransportTarget((ip, 161)),
                                                                  oid)
        if hostId: break


    #print ip, hostId
    for item in hostId:
        for oid, hostid in item:
            hex_string = binascii.hexlify(str(hostid))
            octets = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            ip_ = [int(i, 16) for i in octets]
            _host_id = '.'.join(str(i) for i in ip_)
            print('%s = %s' % (oid, hostid))


    varBindNbrTable = False
    for oid in neighbor_router_id_oid:
        errIndication,errStatus,errIndex, varBindNbrTable = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                           cmdgen.UdpTransportTarget((ip, 161)),
                                                                           oid)
        if varBindNbrTable: break


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
            

    varBindNbrIpTable = False
    for oid in neighbor_router_ip_oid:
        errorIndication, errorStatus, errorIndex, varBindNbrIpTable = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                                     cmdgen.UdpTransportTarget((ip, 161)),
                                                                                     oid)
        if varBindNbrIpTable: break
    
    #print(varBindNbrIpTable)
    for varBindNbrIpTableRow in varBindNbrIpTable:
        for oid, nbrip in varBindNbrIpTableRow:
            hex_string = binascii.hexlify(str(nbrip))
            octets = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
            ip_ = [int(i, 16) for i in octets]
            nbr_ip = '.'.join(str(i) for i in ip_)
            if len(nbr_ip)<=15: # only take valid IP addresses
                nbriplist.append(nbr_ip)
                #print('%s = %s' % (oid, nbr_ip))


    varIfIndex = False
    for oid in protocol_ifindex_oid:
        errIndication,errStatus,errIndex, varIfIndex = cmdGen.nextCmd(cmdgen.CommunityData(comm),
                                                                      cmdgen.UdpTransportTarget((ip, 161)),
                                                                      oid)
        if varIfIndex: break

    if varIfIndex:
        ifnames = []
        for item in varIfIndex:
            for oid, ifindex in item:
                #print('%s = %s' % (oid, ifindex))
                if not 'lo0' in all_interfaces[interface_oid+'.'+str(ifindex)] or not 'Lo0' in all_interfaces[interface_oid+'.'+str(ifindex)]:
                    ifnames.append(all_interfaces[interface_oid+'.'+str(ifindex)])

        '''
        remove logical tunnel interfaces configured on the logical system side for junos
        this is to avoid polling the logical system if the adjacency is between logical and main system
        '''
        if ifnames:
            for x in range(len(ifnames)):
                try:
                  if ifnames[x].split('.')[0] == ifnames[x+1].split('.')[0]:
                     if 'lt' in ifnames[x]: ifnames.pop(x+1)
                except IndexError: pass


    querried_neighbors_names.append((_host,_host_id))

    #Adding data of the polled device in the _device dictionary
    _devices["Host"] = _host
    _devices["HostId"] = _host_id
    _devices["NbrRtrId"] = nbridlist
    _devices["NbrRtrIp"] = nbriplist
    _devices["Interface"] = ifnames
    
    devices_list.append(_devices)
    #pprint.pprint(devices_list)
    return devices_list




def find_unqueried_neighbors(ip,comm,protocol):
    ''' Uses the snmp_get function to querry found neighbors'''

    global devices_list, querried_neighbors, querried_neighbors_names
    
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

    #Running the snmp_get() function for each unqueried neighbor
    print("lenght of devices_list",len(devices_list))

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
                        snmp_get(new_ip,comm,protocol)
                        querried_neighbors.append(s)
                        print("    ",q,r,s, "DONE")
                    except Exception as e:
                       print(e)
                       querried_neighbors.append(s)
                       print("    ",q,r,s,new_ip, "SKIPPED FAIL POLL")


    return all_nbr_ids, devices_list



def neighborship(final_devices_list):
    '''
    Creating list of neighborships
    '''
    neighborship_dict = {}
    for each_dictionary in final_devices_list:
        for index, each_neighbor in enumerate(each_dictionary["NbrRtrId"]):
            each_tuple = (each_dictionary["HostId"], each_neighbor)
            neighborship_dict[each_tuple] = each_dictionary["NbrRtrIp"][index]
    return neighborship_dict



def id_to_name(final_devices_list):
    ''' The SNMP poll will return router id. This function maps the id to hostnames
    '''
    id_host = {}
    for item in final_devices_list: id_host[item['HostId']] = item['Host']
    return id_host


def ip_to_name(final_devices_list,neighborship_dict):
    ''' Maps link IP address to the interface name
    '''
    ip_iface = {}
    for item in final_devices_list:
        for index, each_neighbor in enumerate(item["NbrRtrId"]):
            each_tuple = (each_neighbor,item["HostId"])
            ip_iface[each_tuple] = item['Interface'][index] + '\n'+ item["NbrRtrIp"][index]
            try: neighborship_dict[each_tuple]= item['Interface'][index] + '\n'+ neighborship_dict[each_tuple]
            except KeyError: pass
    
    return neighborship_dict




def build(ip,comm,protocol):
    ''' Collect devices data and build the neighbourship database
    '''
    global devices_list, querried_neighbors, querried_neighbors_names

    devices_list = snmp_get(ip,comm,protocol)
    querried_neighbors.append(devices_list[0]["HostId"])
    pprint.pprint(devices_list)

    while True:
        all_nbr_ids, devices_list = find_unqueried_neighbors(ip,comm,protocol)
        if len(all_nbr_ids)==0: break

    final_devices_list = devices_list
    #pprint.pprint(final_devices_list)

    neighborship_dict = neighborship(final_devices_list)
    #pprint.pprint(neighborship_dict)

    neighborship_dict = ip_to_name(final_devices_list,neighborship_dict)
    #pprint.pprint(neighborship_dict)

    return final_devices_list,neighborship_dict



def get_input():
    ''' Collect information from user
    '''

    ip = raw_input(Fore.BLUE + Style.BRIGHT + "\n* Enter device IP: ")
    comm = raw_input(Fore.BLUE + Style.BRIGHT + "\n* Enter SNMP community: ")
    protocol = raw_input(Fore.BLUE + Style.BRIGHT + "\n* Specify link protocol (isis or ospf): ").lower()

    if protocol != 'ospf' and protocol != 'isis':
        print('Wrong protocol choice')
        sys.exit(1)

    return ip,comm,protocol



if __name__ == '__main__':

    devices_list = []
    querried_neighbors = []
    querried_neighbors_names = []

     #Initialize colorama
    init()
    ip,comm,protocol = get_input()

    final_devices_list,neighborship_dict = build(ip,comm,protocol)


    while True:
        try:
            # User actions
            print(Fore.BLUE + Style.BRIGHT + "* Please choose an action:\
                1 - Display devices on the screen\
                2 - Export devices to CSV file\
                3 - Generate network topology\
                4 - Generate interactive network topology\
                5 - Generate GEFX file to use with Gephi\
                e - Exit")
            user_choice = raw_input("\n* Enter your choice: ")
            print("\n")


            if user_choice == "1":
                
                for each_dict in final_devices_list:
                    print("Hostname: " + Fore.YELLOW + Style.BRIGHT + "%s" % each_dict["Host"] + Fore.BLUE + Style.BRIGHT)
                    print("RID: " + Fore.YELLOW + Style.BRIGHT + "%s" % each_dict["HostId"] + Fore.BLUE + Style.BRIGHT)
                    print("Neighbors by ID: " + Fore.YELLOW + Style.BRIGHT + "%s" % ', '.join(each_dict["NbrRtrId"]) + Fore.BLUE + Style.BRIGHT)
                    print("Neighbors by IP: " + Fore.YELLOW + Style.BRIGHT + "%s" % ', '.join(each_dict["NbrRtrIp"]) + Fore.BLUE + Style.BRIGHT)
                    print("\n")
                    
                continue
            
            # Printing devices to CSV file
            elif user_choice == "2":
                print(Fore.CYAN + Style.BRIGHT + "* Generating " + Fore.YELLOW + Style.BRIGHT + "DEVICES" + Fore.CYAN + Style.BRIGHT + " file...\n")
                print(Fore.CYAN + Style.BRIGHT + "* Check the script folder. Import the file into Excel for a better view of the devices.\n")
                
                csv_file = open("DEVICES.txt", "w")
                
                print >>csv_file, "Hostname" + ";" + "RouterID" + ";" + "NeighborRouterID" + ";" + "NeighborIP"
                
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
                
                # add blank labels for nodes that could not be querried by SNMP
                for node in node_positions.keys():
                    if node not in node_labels.keys(): node_labels[node]=''
                edge_labels = {key:neighborship_dict[key] for key in neighborship_dict.keys() if key in edge_list}

                interactive_graph.draw_node_labels(node_labels, node_positions,node_label_font_size=9)

                matp.show()

            elif user_choice == "5":
                import os
                G = nx.Graph()
                G.add_edges_from(neighborship_dict.keys())
                
                #loop through and add label for edges
                for edge in neighborship_dict.keys(): 
                  G.edges[edge]['label'] = neighborship_dict[edge]

                nodes =id_to_name(final_devices_list)
        
                #loop through and add label attribute for nodes
                for node in nodes.keys(): 
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
