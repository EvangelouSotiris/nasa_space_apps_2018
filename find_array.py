import math
import gdal
import struct
import numpy

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
    if(latlong_table(location[0], location[1]) > 0 and latlong_table(location[0], location[1]) <= 100):
       return location
    
nameraster = "/home/anon/Downloads/MOD10A1.A2018284.h18v05.006.2018286033502.hdf"
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
my_pixel = find_my_pixel((1024387.4162, 4398692.9307), latlong_table, band)
print my_pixel
