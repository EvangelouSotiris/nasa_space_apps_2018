import math
import gdal
import struct
import numpy
from pyproj import Proj

def convert_sin_2_wgs84(x, y):
    p_modis_grid = Proj('+proj=sinu +R=6371007.181 +nadgrids=@null +wktext')
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
    

        
nameraster = "/home/anon/Downloads/sweden.hdf"
tile_name = nameraster
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
my_pixel = find_my_pixel((698215.2638, 7743812.7440), latlong_table, band)
print my_pixel
ma_location = (my_pixel[1], my_pixel[2])
ma_snow = find_nearest_snow(latlong_table, ma_location)
print ma_snow
lon, lat = convert_sin_2_wgs84(ma_snow[0], ma_snow[1])
print lon
print lat
