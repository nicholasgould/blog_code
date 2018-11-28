#reads street point data and calculates length of streets
import sys
import math
#define a function that calculates the distance between a pair of points
#the input will be two tuples and the output a distance(m)
def pointDistance(point1,point2):
    X1 = int(point1[0])
    Y1 = int(point1[1])
    X2 = int(point2[0])
    Y2 = int(point2[1])
    sumsq = (X2 - X1)**2 + (Y2 - Y1)**2
    distance = math.sqrt(sumsq)
    return distance
    
#read each row of file into a dictionary element
#the dictionary element name will be the street name
#the value will be a LIST of point tuples
try:
    street_file = open("streets.txt", "r")
except Exception as e: 
    print("Error: " + str(e))
    sys.exit()
allStreets = {} #define dictionary
for street in street_file: #street is 1 line
    myStreet = street.rstrip("\n").split(";")
    myStreetName = ""
    myStreetPoints = []
    for element in myStreet:
        if element.find(",") == -1:
            myStreetName = element
            print(myStreetName)
        else:
            myPointValues = element.split(",")
            myPoint = (myPointValues[0],myPointValues[1]) #create tuple for point
            print(myPointValues[0],myPointValues[1]) 
            myStreetPoints.append(myPoint)
    allStreets[myStreetName] = myStreetPoints
street_file.close()
    
#now have a dictionary of the streets
for streetName,points in allStreets.items():    
    count = 0
    lineDist = 0
    while count < len(points) - 1:
        lineDist += pointDistance(points[count], points[count+1])
        count += 1
    print("street:", streetName, "points:", len(points), "distance:", int(lineDist))