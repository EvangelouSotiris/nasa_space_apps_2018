import gdal
import struct

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
