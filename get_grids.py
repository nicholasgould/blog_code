import processing, os
from zipfile import ZipFile
outputFolder = "C:\\temp\\tiles"
rasterFileType = "asc" # this is the extension of the raster file
tileList = []
tileFiles = []
params = {'INPUT':'os_bng_grids 10km_grid','PREDICATE':'0','INTERSECT':'Buffered','METHOD':'0'}
processing.run("qgis:selectbylocation", params)
# get the layer (NB this returns a list so get first (and only) item...
my_layer = QgsProject.instance().mapLayersByName('os_bng_grids 10km_grid')[0]
# get the selected features...
selectedGridCells = my_layer.selectedFeatures()
# Add the selected grid cell names to a list...
for gridCell in selectedGridCells:    
    tileList.append(gridCell.attributes()[1])
print(str(len(tileList)) + "tiles required")
   
with ZipFile("C:\\temp\\terr50_gagg_gb.zip", 'r') as zObject:
    # for every file in the zip file, see if it has a name similar to any required tile names...
    for fileName in zObject.namelist(): 
        #check if the zipped file is in the list of required tiles...
        if any(tileName.lower() in fileName for tileName in tileList):                        
            # we don't want to preserve the folder structure so extract the filenames only
            fileInfo = zObject.getinfo(fileName)            
            fileInfo.filename = os.path.basename(fileInfo.filename)            
            zObject.extract(fileInfo, outputFolder)
            # now we have extracted the required zip file, extract everything from that...
            innerFileName = outputFolder + '\\' + fileInfo.filename            
            with ZipFile(innerFileName, 'r') as zObjectInner:                
                zObjectInner.extractall(outputFolder)
                # get the name of the .asc file for the tile...
            for innerFileFileName in zObjectInner.namelist():
                if innerFileFileName[-3:] == rasterFileType:
                    print (innerFileFileName)
                    tileFiles.append(outputFolder + '\\' + innerFileFileName)
            zObjectInner.close()
            # now delete the zipped zip file for the current tile...
            os.remove(innerFileName)
zObject.close()
# create a group for the tiles...
root = QgsProject.instance().layerTreeRoot()
tileGroup = root.addGroup("terrain50")
# Now add the tiles to the map in the new group...
for tileFile in tileFiles:    
    newTileLayer = QgsRasterLayer(tileFile)
    QgsProject.instance().addMapLayer(newTileLayer, False) # add but don't show layer
    tileGroup.addLayer(newTileLayer) # add the layer to the group

