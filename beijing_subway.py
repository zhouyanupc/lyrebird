import requests
import re
import numpy as np

r = requests.get('http://map.amap.com/service/subway?_1469083453978&srhdata=1100_drw_beijing.json')
r.text


def get_lines_stations_info(text):
    lines_info = {}
    stations_info = {}
    for line in r.text.split('st'):
        if line.startswith('{"s"'): continue
        if line.strip() == "": continue
        for station in line:
            station = re.findall('"n":"(\w+)"', line)
            x_y = re.findall('"sl":\"(\d+.\d+),(\d+.\d+)\"', line)
            stations_info = dict(zip(station, x_y))
        line_list = re.findall('"kn":"(\w+)"', line)
        for i in range(len(line_list)):
            lines_info[line_list[i]] = stations_info
    for i in lines_info.keys():
        for j in lines_info[i].keys():
            x_y = tuple(map(float, list(lines_info[i][j])))
            lines_info[i][j] = x_y
        stations_info.update(lines_info.get(i))
    return lines_info , stations_info
lines_info , stations_info = get_lines_stations_info(r.text)

# print(lines_info)
# print(stations_info)
# 画地铁图
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt

stations_info_graph = nx.Graph()
stations_info_graph.add_nodes_from(list(stations_info.keys()))
nx.draw(stations_info_graph, stations_info, with_labels=True,font_size=3, node_size=2)
# plt.show()



from collections import defaultdict
def get_neighbor_info(lines_info):
    neighbor_info = defaultdict(list)
    for i in lines_info.keys():
        stations = list(lines_info[i].keys())
        for s1 in stations:
            for s2 in stations:
                if s1 == s2 :continue
                if abs(stations.index(s1) - stations.index(s2)) == 1:
                    neighbor_info[s1].append(s2)
    return neighbor_info
neighbor_info = get_neighbor_info(lines_info)

neighbor_info_graph = nx.Graph(neighbor_info)
nx.draw(neighbor_info_graph,stations_info,with_labels=True,font_size=3, node_size=2)
plt.show()