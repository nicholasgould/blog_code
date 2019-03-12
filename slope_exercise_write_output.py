# reads in as ASCII grid file and generates, plots and outputs slope values
# for each cell (ino=put and output CRS are OSGB)
import math
import numpy as np
import os
if 'GDAL_DATA' not in os.environ:
    print("NO GDAL_DATA variable")
import osr
from osgeo import gdal
import matplotlib.pyplot as plt
# calculate the slope for a specific cell in a specified array:
def getSlope(my_array, my_cell, my_cell_size_x, my_cell_size_y):
    x = my_cell[0]
    y = my_cell[1]
    a = np.double(my_array[x-1,y-1])
    b = np.double(my_array[x-1,y])
    c = np.double(my_array[x-1,y+1])
    d = np.double(my_array[x,y-1])
    f = np.double(my_array[x,y+1])
    g = np.double(my_array[x+1,y-1])
    h = np.double(my_array[x+1,y])
    i = np.double(my_array[x+1,y+1])
    dzdx = ((c + 2*f + i) - (a + 2*d + g)) / (8*np.double(my_cell_size_x))
    dzdy = ((g + 2*h + i) - (a + 2*b + c)) / (8*np.double(my_cell_size_y))    
    rise_run = math.sqrt(dzdx**2 + dzdy**2)
    slope_degrees = math.atan(rise_run) * 57.29578        
    return slope_degrees

my_raster = gdal.Open("c:\\temp\\NN15.ASC")
cols = my_raster.RasterXSize
rows = my_raster.RasterYSize
gt = my_raster.GetGeoTransform()
top_left_x = gt[0]
top_left_y = gt[3]
cell_width = gt[1]
cell_height = gt[5]
dtm_array = my_raster.ReadAsArray()
output_rows = []
for row in range(1,dtm_array.shape[0]-1):
    new_row = []
    for col in range(1,dtm_array.shape[1]-1):
        cell_slope = getSlope(dtm_array, [row,col], cell_width, abs(cell_height))
        new_row.append(cell_slope)
    output_rows.append(new_row)
slope_array = np.array( output_rows )
plt.imshow(slope_array)
plt.show()
driver = gdal.GetDriverByName('GTiff')
output_raster = driver.Create('c:\\temp\\slope_of_NN15.tif', cols - 2, rows - 2, 1, gdal.GDT_Float32)
output_raster.SetGeoTransform((top_left_x + cell_width, cell_width, 0, top_left_y + cell_height, 0, cell_height))
output_band = output_raster.GetRasterBand(1).WriteArray(slope_array)
output_raster_SRS = osr.SpatialReference()
res = output_raster_SRS.ImportFromEPSG(27700)
if res != 0:
    raise RuntimeError(repr(res) + ': could not import from EPSG')
output_raster.SetProjection(output_raster_SRS.ExportToWkt())
output_raster = None

