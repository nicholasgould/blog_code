from matplotlib import colors
import numpy as np
import matplotlib.pyplot as plt
from random import randint
#generate a 50x50 raster populated with random values 1 to 5
# first as a list...
all_rows = []
for row_num in range(50):
    row = []
    for col_num in range(50):
        row.append(randint(1,5))
    all_rows.append(row)
# ... then create a numpy array from the list...
land_cover_array = np.array(all_rows)
# generate a matplotlib listed color map...
cmap = colors.ListedColormap(['blue','white','gray','orange','green'])
# plot the raster using the color map...
plt.imshow(land_cover_array,cmap=cmap)
plt.show()
# iitialise the dictionary...
class_totals = {'water':0,'urban':0,'suburban':0,'arable':0,'woodland':0}
# determine the class of each cell
for row in range(50):
    for col in range(50):
        if all_rows[row][col] == 1:
            class_totals['water'] += 1
        elif all_rows[row][col] == 2:
            class_totals['urban'] += 1
        elif all_rows[row][col] == 3:
            class_totals['suburban'] += 1
        elif all_rows[row][col] == 4:
            class_totals['arable'] += 1
        elif all_rows[row][col] == 5:
            class_totals['woodland'] += 1    
print (class_totals)