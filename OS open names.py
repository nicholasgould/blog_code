#generates a Shapefile of towns and cities within GM using OS Open Names dataset
import os
import csv
import glob
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
boundaryDataPath = "C:/test/"
boundaryDataFile = "GM boundary.shp"
dataFilePath = "C:/test/"
headerFileName = "C:/test/OS_Open_Names_Header.csv"
OSnationalGridSquares = ("SD","SE","SJ","SK")

# read the header file
with open(headerFileName, 'r') as headerFile:
    header = csv.reader(headerFile)
    for row in header:
        headers = row

# get a list of relevant files i.e. those that are in the specified grid squares
files = list()
for square in OSnationalGridSquares:
    files.extend(glob.glob(os.path.join(dataFilePath, square +'*.csv')))
    
# get the GM boundary as a polygon...
boundaryTable = gpd.read_file(boundaryDataPath + boundaryDataFile)
GMgeometry = boundaryTable['geometry'][[0]] # this is a GeoPandas GeoSeries...
GMpolygon = Polygon(GMgeometry[0]) # ... we need it as a Shapely polygon

# loop through relevant Open Names CSV files and extract Towns and Cities
townsCities = pd.DataFrame(columns=['NAME1','TYPE','LOCAL_TYPE','GEOMETRY_X','GEOMETRY_Y'])
for filename in files:
    dfPlaces = pd.read_csv(filename,names=headers)
    dfPlaces = dfPlaces[['NAME1','TYPE','LOCAL_TYPE','GEOMETRY_X','GEOMETRY_Y']]        
    townsCities = townsCities.append(dfPlaces[(dfPlaces['LOCAL_TYPE'] == 'Town') | (dfPlaces['LOCAL_TYPE'] == 'City')])

# loop through the Towns and Cities and create a list of those within the GM boundary
listGMplaces = list()
for place in townsCities.itertuples(index=True, name='Pandas'):
    townCityPoint = Point(place.GEOMETRY_X, place.GEOMETRY_Y)
    if townCityPoint.within(GMpolygon):
        print ( place.NAME1 + " is within GM" )
        listGMplaces.append([place.NAME1,place.TYPE,place.LOCAL_TYPE,townCityPoint])
        
# create a Shapefile of the Towns and Cities within GM
dfGMplaces = pd.DataFrame(listGMplaces,columns=['NAME1','TYPE','LOCAL_TYPE','GEOMETRY'])
crsOSGB = {'init': 'epsg:27700'}
gpdfGMplaces = gpd.GeoDataFrame(dfGMplaces, crs=crsOSGB, geometry='GEOMETRY')
gpdfGMplaces.to_file(boundaryDataPath + 'GMplaces.shp', driver='ESRI Shapefile')

        
