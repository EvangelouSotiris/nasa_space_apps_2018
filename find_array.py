import gdal

def produce_array(tile_name):
    nameraster = "/home/anon/Downloads/MOD10A1.A2018284.h18v05.006.2018286033502.hdf"
    tile_name = nameraster
    hdl_file = gdal.Open(tile_name)
    subDatasets = hdl_file.GetSubDatasets()
    dataset = gdal.Open(subDatasets[0][0])
    geotransform = dataset.GetGeoTransform()
    band = dataset.GetRasterBand(1)
    array = band.ReadAsArray()
    print array
    return array
