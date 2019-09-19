# This version uses the Major Towns and Cities (December 2015) Boundaries instead of OSM town/city boundaries,...
# ...which do not always match the actual town boundaries (e.g. Harrogate, Ashford)
# Therefore, uses graph_from_polygon instead of graph_from_place
# Need to read in and loop through the Major_Towns_and_Cities_December_2015_Boundaries.shp

import os
import osmnx as ox
import geopandas as gpd
import time
import shutil
import pickle
import pyproj
import shapely.ops as ops
from functools import partial
def get_town_area(geom):
    #converts geometry of town into AEA projection and calculates its area in metres squared
    # see https://gis.stackexchange.com/questions/127607/area-in-km-from-polygon-of-coordinates
    geom_area = ops.transform(
    partial(
        pyproj.transform,
        pyproj.Proj(init='EPSG:4326'),
        pyproj.Proj(
            proj='aea',
            lat1=geom.bounds[1],
            lat2=geom.bounds[3])),
    geom)
    return geom_area.area

target_folder = "C:\\networks"
start_time = int(time.time())
#open the Shapefile of all ONS town boundaries
#places_gdf = gpd.read_file(target_folder + '\\Major_Towns_and_Cities_December_2015_Boundaries.shp')
places_gdf = gpd.read_file(target_folder + '\\towns_subset.shp')

total_towns = len(places_gdf)
# CRS needs to be 4326 for graph_from_polygon
places_gdf_ll = places_gdf.to_crs(epsg=4326)
i = 0
try:
    networks = pickle.load( open( target_folder + "\\networks_stats.pkl", "rb" ) )
except Exception as e:
    print (e)
    networks = {}
for index,place in places_gdf_ll.iterrows():    
    town_name = place['tcity15nm']
    town_area_m2 = get_town_area(place.geometry)
    # check we haven't already processed this town...
    if not os.path.isdir(target_folder + '\\' + town_name):
        place_polygon = place['geometry']
        # extract network for specified polygon...
        G = ox.graph_from_polygon(place_polygon, network_type='walk') 
        graphML_folder = target_folder + '\\' + town_name   
        ox.save_load.save_graphml(G,filename=town_name +'_graph.xml',folder=graphML_folder) 
        ox.save_load.save_graph_shapefile(G, filename=town_name, folder=target_folder, encoding='utf-8')
        networks[town_name] = ox.basic_stats(G,area=town_area_m2)
        # append the area of the town to the stats dictionary (network is a dictionary of dictionaries)...
        networks[town_name]['areakm2'] = town_area_m2/1000000
        # can't save direct from graph to shapefile in a specific CRS
        # could convert the graph to two GDFs and convert them to new CRS but there are problems with that:
        # see https://stackoverflow.com/questions/42221358/saving-dataframe-to-shapefile-using-geopandas-in-python-raises-valueerror-for-bo
        # So read in node/edge shapefiles...
        node_gdf = gpd.read_file(target_folder + '\\' + town_name +'\\nodes\\nodes.shp')
        edge_gdf = gpd.read_file(target_folder + '\\' + town_name +'\\edges\\edges.shp')
        # ... and convert to OSGB... 
        node_gdf_OSGB = node_gdf.to_crs(epsg=27700)
        edge_gdf_OSGB = edge_gdf.to_crs(epsg=27700)
        #.. and save...
        node_gdf_OSGB.to_file(target_folder + '\\' + town_name + '\\' + town_name + "_nodes_OSGB.shp") #defaults to Shapefile
        edge_gdf_OSGB.to_file(target_folder + '\\' + town_name + '\\' + town_name + "_edges_OSGB.shp") 
        #...delete source...
        shutil.rmtree(target_folder + '\\' + town_name +'\\nodes')
        shutil.rmtree(target_folder + '\\' + town_name +'\\edges')            
        print (town_name + " nodes:" + str(len(G.nodes)) + " edges:" + str(len(G.edges)))
        i+=1
        print(i, "towns of", total_towns, "processed")
pickle.dump(networks,open( target_folder + "\\networks_stats.pkl", "wb" ))
print ( "Total processing time:" + str(int(time.time() - start_time)) + " seconds" )

