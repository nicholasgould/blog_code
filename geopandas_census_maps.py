import geopandas as gpd
import matplotlib.pyplot as plt
import pysal
sourceDataPath = "C:/test/"
sourceDataFile = "GM_MSOA_deprivation_2011.shp"
# create a geopandas geodataframe...
sourceTable = gpd.read_file(sourceDataPath + sourceDataFile)
attributes = {'Total households':'F996','Household is deprived in 4 dimensions':'F1001'}
print ( sourceDataFile + " has " + str(len(sourceTable)) + " records" )
sourceTable['area'] = sourceTable['geometry'].area / 10**6 # area in km squared
for attribute in attributes:
    sourceTable[attributes[attribute] + '_density'] = sourceTable[attributes[attribute]] / sourceTable['area']
sourceTable['district'] = sourceTable['geo_label'].str.split(" ").str[0] 
districts = sourceTable['district'].unique()
plotNum = 1
for district in districts:
    # get data for this district only
    districtTable = sourceTable[sourceTable['district'] == district]    
    for attribute in attributes:    
        districtTable.plot(column=attributes[attribute] + '_density',cmap='Reds',scheme='fisher_jenks',edgecolor='black') 
        title = attribute + " in " + district
        plt.title(title)
        plt.figure(plotNum)
        plt.savefig("c:/test/" + title + ".png")
        plotNum += 1
plt.show() # NB: call this just once

