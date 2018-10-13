import gdal

nameraster = "/home/anon/Downloads/MOD10A1.A2018284.h18v05.006.2018286033502.hdf"
hdl_file = gdal.Open(nameraster)
subDatasets = hdl_file.GetSubDatasets()
dataset = gdal.Open(subDatasets[0][0])
geotransform = dataset.GetGeoTransform()
band = dataset.GetRasterBand(1)
array = band.ReadAsArray()
print array
