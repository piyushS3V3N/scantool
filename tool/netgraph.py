import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from scapy.all import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
matplotlib.use('Qt5Agg')
class PlotCanvas(FigureCanvas):

    def __init__(self,filepath,parent=None, width=10, height=8, dpi=100):
        #fig = Figure(figsize=(width, height), dpi=dpi)
        fig = plt.figure(figsize=(width, height), dpi=dpi)
        self.filepath = filepath
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.netgraph()
    def netgraph(self):
      G = nx.Graph()
      connections = set()
      nodes = set()
      lable= {}
      with PcapReader(self.filepath) as pcap_reader:
        for p in pcap_reader:
          if IP in p:
            nodes.add(p[IP].src)
            nodes.add(p[IP].dst)
            lable[p[IP].mysummary().split()[0],p[IP].mysummary().split()[2]] = p[IP].mysummary().split()[3]
            connections.add((p[IP].src,p[IP].dst))
      G.add_nodes_from(nodes)
      G.add_edges_from(connections)
      pos = nx.planar_layout(G)
      #pos = nx.spring_layout(G,scale = 0.05, iterations=10)
      plt.tight_layout()

      nx.draw(G, pos, node_color='c',edge_color='k',with_labels=True)
      nx.draw_networkx_edge_labels(G,pos,edge_labels=lable,font_color="red")
      self.draw_idle()
