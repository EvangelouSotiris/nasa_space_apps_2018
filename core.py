import math
import gdal
import struct
import numpy
import requests
from geopy.geocoders import Nominatim
from pyproj import Proj

def convert_wgs84_2_sin(lon, lat):
    p_modis_grid = Proj('+proj=sinu +R=6371007.181 +nadgrids=@null +wktext')
    x, y = p_modis_grid(lon, lat)
    return x, y

def convert_sin_2_wgs84(x, y):
    p_modis_grid = Proj('+proj=sinu +R=6371007.181 +nadgrids=@null +wktext +init=epsg:3857')
    lon, lat = p_modis_grid(x, y, inverse=True)
    return lon, lat

def find_my_pixel(given_latlong, latlong_table, band):
    #current_min = (sum_diff, x, y)
    current_min = (1111111111, 0, 0)
    for i in range(band.XSize):
        for j in range(band.YSize):
            sum_diff = math.sqrt((given_latlong[0] - latlong_table[i][j][0]) ** 2 + (given_latlong[1] - latlong_table[i][j][1]) ** 2)
            if sum_diff < current_min[0]:
                current_min = (sum_diff, i, j)
    return current_min

def find_nearest_snow(latlong_table, location):
    if(latlong_table[location[0]][ location[1]][2] > 0 and latlong_table[location[0]][ location[1]][2] <= 100):
       return location
    depth = 1
    runner = (0,0)
    while (1):
        flag = 0
        runner = (location[0]-depth , location[1]+depth)
        for i in range(depth*2+1):
            if (runner[0] + i < 0 or runner[0] + i > band.XSize or runner[1] > band.YSize or runner[1] < 0):
                continue
            else:
                flag = 1
            if (latlong_table[runner[0] + i][ runner[1]][2]>0 and latlong_table[runner[0] + i][ runner[1]][2]<=100):
                print "snow found"
                return latlong_table[runner[0]+i][runner[1]]
#        runner[0] += i
        runner = (runner[0] + i, runner[1])
        for i in range(depth * 2 + 1):
            if (runner[0]  < 0 or runner[0] > band.XSize or runner[1] - i > band.YSize or runner[1] - i < 0):
                continue
            else:
                flag = 1
            if (latlong_table[runner[0]][ runner[1] - i][2]>0 and latlong_table[runner[0]][ runner[1] - i][2] <= 100):
                print "snow found"
                return latlong_table[runner[0]][runner[1]-i]
#        runner[1] -= i
        runner = (runner[0], runner[1] - i)
        for i in range(depth * 2 + 1):
            if (runner[0] - i < 0 or runner[0] - i > band.XSize or runner[1] > band.YSize or runner[1] < 0):
                continue
            else:
                flag = 1
            if (latlong_table[runner[0] - i][ runner[1]][2]>0 and latlong_table[runner[0] - i][ runner[1]][2] <= 100):
                print "snow found"
                return latlong_table[runner[0]-i][runner[1]]
#            runner[0] -= i
            runner = (runner[0] - i, runner[1])
        for i in range(depth * 2 + 1) :
            if (runner[0] < 0 or runner[0] > band.XSize or runner[1] + i > band.YSize or runner[1] + i < 0):
                continue
            else:
                flag = 1
            if (latlong_table[runner[0]][ runner[1] + i][2]>0 and latlong_table[runner[0]][ runner[1] + i][2] <= 100):
                print "snow found"
                return latlong_table[runner[0]][runner[1]+i]
        if(flag == 0):
            print "nosno"
            break
        depth += 1
def run_and_check_pixels(latlong_table, query):
    object_list = []
    runner = (0, 0)
    radius = raw_input("Enter Radius Parameter (Radius in Meters): ")
    MIN = raw_input("Enter Snow Tolerance (1 to 99): ")
    MIN = int(MIN)
    for i in range(2400):
        for j in range(2400):
            if(MIN <= latlong_table[i][j][2] <= 99):
                #print convert_sin_2_wgs84(latlong_table[i][j][0], latlong_table[i][j][1])
                coordinates = convert_sin_2_wgs84(latlong_table[i][j][0], latlong_table[i][j][1])
                r = requests.get("https://api.tomtom.com/search/2/poiSearch/"+ query +".json?key=sMiwluxXC46HdG5EWpNYaPtfZnl8AdS8&lat=" + str(coordinates[1]) +"&lon=" + str(coordinates[0]) + "&radius=" + radius)
                response = r.json()
                if(len(response['results']) > 0):
                    if(len(object_list) == 0):
                        object_list.append(response['results'][0]['poi']['name'])
                    else:
                        double_flag = 0
                        for i in range(len(object_list)):
                            if(object_list[i] == response['results'][0]['poi']['name']):
                                double_flag = 1
                        if(double_flag == 0):
                            object_list.append(response['results'][0]['poi']['name'])
                            print(response['results'][0]['poi']['name'])
nameraster = "/home/anon/Downloads/seattle.hdf"
tile_name = nameraster
print "1. Find nearest snow\n2. Find all POIs in slice with snow(We used hospital in demo)"
func_option = raw_input("Please enter your preferance: ")
hdl_file = gdal.Open(tile_name)
subDatasets = hdl_file.GetSubDatasets()
dataset = gdal.Open(subDatasets[0][0])
geotransform = dataset.GetGeoTransform()
band = dataset.GetRasterBand(1)
array = band.ReadAsArray()
fmttypes = {'Byte':'B', 'UInt16':'H', 'Int16':'h', 'UInt32':'I',
            'Int32':'i', 'Float32':'f', 'Float64':'d'}
BandType = gdal.GetDataTypeName(band.DataType)
print geotransform
X = geotransform[0] #top left x
Y = geotransform[3] #top left y
w = band.XSize 
h = band.YSize
latlong_table = [[0 for x in range(w)] for y in range(h)]

for y in range(band.YSize):
    scanline = band.ReadRaster(0, y, band.XSize, 1, band.XSize, 1, band.DataType)
    values = struct.unpack(fmttypes[BandType] * band.XSize, scanline)#
    x = 0
    for value in values:
        #print "%.4f %.4f %.2f" % (X, Y, value)
        latlong_table[x][y] = (X, Y, value)
        X += geotransform[1] #x pixel size
        x += 1
    X = geotransform[0]
    Y += geotransform[5] #y pixel size
if func_option == "1":
    location_name = raw_input("Please enter your location. \n")
    geolocator = Nominatim(user_agent="arcGIS")
    location = geolocator.geocode(location_name)
    latitude = location.latitude
    print latitude
    longitude = location.longitude
    print longitude
    seattle = convert_wgs84_2_sin(longitude, latitude)
    my_pixel = find_my_pixel(seattle, latlong_table, band)
    #print 'This is the weird part' + str(tuple(my_pixel))
    ma_location = (my_pixel[1], my_pixel[2])
    ma_snow = find_nearest_snow(latlong_table, ma_location)
    print ma_snow
    lon, lat = convert_sin_2_wgs84(ma_snow[0], ma_snow[1])
    print lon
    print lat
elif func_option == "2":
    poi = raw_input("Enter poi: ")
    run_and_check_pixels(latlong_table, poi)
else:
    print "Exiting. . . \n"
