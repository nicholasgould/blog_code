# For each road accident, identify its nearest road junction (within a distance threshold)
# This script must be run from the QGIS Python Console
# tested on QGIS 3.2.0
# Shapefiles required are OSMnodes.shp (road junctions) and OSMaccidents.shp (accidents)
# The accident and junction layers must be open in QGIS before running this script
layers = iface.mapCanvas().layers()
for layer in layers:
    if layer.name() == "OSMaccidents":
        accident_layer = layer
    if layer.name() == "OSMnodes":
        node_layer = layer
junction_threshold = 30 #metres
accident_node = {} # dictionary for accident ID and nearest node ID

# Add an attribute (if not already present) to the accident layer to store nearest node ID
pr = accident_layer.dataProvider()
if accident_layer.fields().indexFromName("node_id") == -1:
    pr.addAttributes([QgsField("node_id",QVariant.String)])
    accident_layer.updateFields()

# enumerate the accidents to determine nearest node
for accident in accident_layer.getFeatures():
    accident_ID = accident['ACCIDENTID']    
    nearest_neighbour_ID = 0
    nearest_neighbour_distance = 1000000
    for node in node_layer.getFeatures():
        dist = accident.geometry().distance(node.geometry())
        if dist < nearest_neighbour_distance:
            nearest_neighbour_distance = dist
            nearest_neighbour_ID = node['osmid']
    if nearest_neighbour_distance < junction_threshold:
        #this accident is near to a junction, record it
        accident_node[accident_ID] = nearest_neighbour_ID
    else:
        #not met threshold - set the nearest node ID to null
        accident_node[accident_ID] = None
       
# print results for debugging      
for accident_id, node_id in accident_node.items():  
    print ("for accident ", accident_id, "nearest node is", node_id)
    
# write results to new attribute    
accident_layer.startEditing()
for accident in accident_layer.getFeatures():
    # find the key for this accident in the dictionary...
    if accident['ACCIDENTID'] in accident_node:
        #we've found the accident now set its node id (the 10th attribute)
        accident_layer.changeAttributeValue(accident.id(),9,accident_node[accident['ACCIDENTID']])
accident_layer.commitChanges()


