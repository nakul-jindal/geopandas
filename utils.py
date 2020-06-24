import osmnx as ox
import matplotlib.pyplot as plt
import networkx as nx
from typing import List, Set, Dict, Tuple
import pandas as pd
import geopandas as gpd
import pyproj
from shapely.wkt import loads, dumps
from shapely.geometry import mapping, Point, LineString, MultiPolygon, MultiLineString, MultiPoint
from shapely.ops import split, snap, transform
from functools import partial
from fiona.crs import from_epsg

place_name = "Sector 28, Baba Nagar, Faridabád,Haryana,India"
graph = ox.graph_from_place(place_name)
graph_proj = ox.project_graph(graph)
nodes_proj, edges_proj = ox.graph_to_gdfs(graph_proj, nodes=True, edges=True)

pois = ox.pois_from_place(place_name)
pois_proj=ox.project_gdf(pois)    #project pois

# randomly pick poi
point=pois_proj.iloc[2].geometry 

def get_closest_point_on_line(line: LineString, point: Point) -> Point:
    #Finds the closest point on a line to given point and returns it as Point.
    
    projected = line.project(point)
    closest_point = line.interpolate(projected)
    return closest_point
   
def get_split_lines(line: LineString, point: Point) -> List[LineString]:
    """Splits a line at nearest intersecting point.
    Returns:
        A list containing two LineString objects.
    """
    snap_line = snap(line,point,0.01)
    result = split(snap_line, point)
    if (len(result) < 2): print('Error in splitting line at point: only one line in the result') 
    return result   


n_edge=ox.get_nearest_edge(graph_proj, (point.y ,point.x))   #get nearest edge to poi

n_node=get_closest_point_on_line(n_edge[0],point)          #get nearest node on that edge

split_line=get_split_lines(n_edge[0], n_node)            #split the edge at that node into 2 lines
         

fig, ax = ox.plot_graph(graph_proj, node_color='#999999', show=False, close=False)
ax.scatter(point.x, point.y, c='r', marker='x')
ax.scatter(nn.x, nn.y, c='g', marker='x')
  #un-comment any 1 of the 3 below to visualize that line
#x, y = n_edge[0].xy
#x, y = split_line[0].xy     
#x, y = split_line[1].xy
ax.plot(x, y, alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
plt.show()         
         
