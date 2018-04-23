import geopandas as gpd
import matplotlib.pyplot as plt
import pysal
import rtree 
from shapely.geometry import Point
from shapely.geometry import Polygon
sourceDataPath = "C:/test/"
sourceDataFile = "GM_MSOA_deprivation_2011.shp"
placeDataFile = "GMplaces.shp"
# create a geopandas geodataframe...
sourceTable = gpd.read_file(sourceDataPath + sourceDataFile)
placeTable = gpd.read_file(sourceDataPath + placeDataFile)
attributes = {'Total households':'F996','Household is deprived in 4 dimensions':'F1001'}
print ( sourceDataFile + " has " + str(len(sourceTable)) + " records" )
sourceTable['area'] = sourceTable['geometry'].area / 10**6 # area in km squared
for attribute in attributes:
    sourceTable[attributes[attribute] + '_density'] = sourceTable[attributes[attribute]] / sourceTable['area']
sourceTable['district'] = sourceTable['name'].str.split(" ").str[0] 
districts = sourceTable['district'].unique()
plotNum = 1
for district in districts:
    # get data for this district only
    districtTable = sourceTable[sourceTable['district'] == district]
    print ( str(len(districtTable)) + " MSOAs in " + district )
    # get places in this district only using a GeoPandas spatial join
    placesInDistrict = gpd.sjoin(placeTable, districtTable, how='inner', op="within")
    # the join returns all columns in both tables, so trim down...
    placesInDistrict = placesInDistrict[['NAME1','TYPE','LOCAL_TYPE','geometry']]
    print ( str(len(placesInDistrict)) + " places in " + district )
    for attribute in attributes:    
        myMap = districtTable.plot(column=attributes[attribute] + '_density',cmap='Reds',scheme='fisher_jenks',edgecolor='black') 
        placesInDistrict.plot(ax=myMap, marker='o', color='blue', markersize=16) # add places layer to myMap
        # add labels to places
        for place in placesInDistrict.itertuples(index=True, name='Pandas'):
            plt.text(place.geometry.x + 300, place.geometry.y, place.NAME1,  bbox=dict(boxstyle='square,pad=0.1', fc='white', ec='none')) # 300m x offset added.
        title = attribute + " in " + district
        plt.title(title)
        plt.figure(plotNum)
        plt.savefig(sourceDataPath + title + ".png")
        plotNum += 1
plt.show() # NB: call this just once

