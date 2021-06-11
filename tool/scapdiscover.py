from scapy.all  import *
import base64
import os ,sys
import networkx as nx
#net_data = sniff(iface="wlan0")
network_packets = rdpcap("../data/pcap/test.pcapng")
G = nx.Graph()
#G1 = nx.Graph()
connections = set()
nodes_udp = set()
#nodes_dns = set()
lable={}
with PcapReader("../data/pcap/test.pcapng") as pcap_reader:
  for p in pcap_reader:
    if IP in p:
      nodes_udp.add(p[IP].src)
      nodes_udp.add(p[IP].dst)
      lable[(p[IP].src,p[IP].dst)] = p[IP].mysummary().split()[3]
      connections.add((p[IP].src,p[IP].dst))
    if DNS in p :
      print(p[DNS].mysummary())
G.add_nodes_from(nodes_udp)
G.add_edges_from(connections)
pos = nx.spring_layout(G,scale = 0.05, iterations=10)
figure, axis = plt.subplots(1,1)
plt.tight_layout()
nx.draw(G, pos, labels= {node:node for node in G.nodes()},node_color='c',edge_color='k',with_labels=True)
nx.draw_networkx_edge_labels(G,pos,edge_labels=lable,font_color="red")
plt.show()
#self.draw_idle()

'''for d in network_packets:
  if d.haslayer(DNSRR):
    ancount = d[DNS].ancount
    i = ancount + 4
    while i > 4:
      print(d[0][i].rrname)'''
'''for d in network_packets:
  if d.haslayer(IP):
    if(d[IP].haslayer(ICMP)):
      print("Use")
    print(d[IP].mysummary().split())'''
