#!pip install osmnx
import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
import geopandas as gpd
import pandas as pd

place_name = "Sector 28, Baba Nagar, Faridabád,Haryana,India"
graph = ox.graph_from_place(place_name)
graph_proj = ox.project_graph(graph)

pois = ox.pois_from_place(place_name)

fig, ax = ox.plot_graph(graph)

nodes,edges = ox.graph_to_gdfs(graph)
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj)    #projected nodes and edges

#just to see the dataframe
nodes.head()
edges.head()
nodes_proj.head()
edges_proj.head()

#pick 2 random nodes for routing
origin=nodes_proj.iloc[1]       #returns dictionary
destination=nodes_proj.iloc[4]

#!git clone https://github.com/dsaidgovsg/k-shortest-path.git
# cd k-shortest-path
from kspath.deviation_path.mps import SingleTargetDeviationPathAlgorithm
n_paths=10   # no. of top shortest paths

dpa_mps = SingleTargetDeviationPathAlgorithm.create_from_graph(G=graph_proj, target=destination['osmid'], weight='length')
paths = []
for path_count, path in enumerate(dpa_mps.shortest_simple_paths(source=origin['osmid']), 1):
    paths.append(path)
    if path_count == n_paths:
        break
      
from shapely.geometry import LineString, Point
route_line=[]
route_geom=gpd.GeoDataFrame(geometry='geometry', crs=edges_proj.crs, columns=['geometry','length_m'])      

for i in range(len(paths)):    
    fig, ax = ox.plot_graph_route(graph_proj, paths[i], origin_point= (origin['x'] , origin['y']) , destination_point= (origin['x'] , origin['y']))
    route_nodes=nodes_proj.loc[paths[i]]
    route_line.append(LineString(list(route_nodes.geometry.values)))
    temp= gpd.GeoDataFrame([[route_line[i]]], geometry='geometry', crs=edges_proj.crs, columns=['geometry'])
    temp['length_m'] = temp.length
    route_geom=route_geom.append(temp, ignore_index=True)
print(route_geom)
         

  
