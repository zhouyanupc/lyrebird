import requests
import re
import numpy as np
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict

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
            stations_info= dict(zip(station,x_y))
        line_list = re.findall('"kn":"(\w+)"',line)
        for i in range(len(line_list)):
            lines_info[line_list[i]]=stations_info
    for i in lines_info.keys():
        for j in lines_info[i].keys():
            x_y = tuple(map(float,list(lines_info[i][j])))
            lines_info[i][j] = x_y
    return lines_info

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

def my_search(graph, from_station, to_station):

    pathes_need_to_check = [[from_station]]
    already_checked = set()

    while pathes_need_to_check:
        path = pathes_need_to_check.pop(0)  # BFS
        #         path = pathes_need_to_check.pop(-1) #DFS
        froniter = path[-1]

        if froniter in already_checked: continue

        new_expanded = graph[froniter]

        for station in new_expanded:
            if station in path: continue

            new_path = path + [station]

            pathes_need_to_check.append(new_path)

            #             print('当前路径是:----')
            #             for p in pathes_need_to_check:
            #                 print('\t {}'.format(p))

            if station == to_station:
                return new_path
        already_checked.add(froniter)

lines_info = get_lines_stations_info(r.text)
stations_info = {}
for i in lines_info.keys():
    stations_info.update(lines_info.get(i))
# print(lines_info)
# print(stations_info)

# 画地铁图
stations_info_graph = nx.Graph()
stations_info_graph.add_nodes_from(list(stations_info.keys()))
nx.draw(stations_info_graph, stations_info, with_labels=True,font_size=3, node_size=2)
# plt.show()
neighbor_info = get_neighbor_info(lines_info)
neighbor_info_graph = nx.Graph(neighbor_info)
nx.draw(neighbor_info_graph,stations_info,with_labels=True,font_size=3, node_size=2)
plt.show()

search1 = my_search(neighbor_info,'金安桥','万寿路')
search2 = my_search(neighbor_info,'朝阳门','西单')
search3 = my_search(neighbor_info,'芍药居','望京')
print(search1)
print(search2)
print(search3)

