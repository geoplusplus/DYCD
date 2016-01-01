import numpy as num
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
from skimage import data, io, segmentation, color
from skimage.future import graph
from osgeo import gdal
from skimage.segmentation import random_walker
import skimage
from scipy import ndimage

adata = gdal.Open( "*****.tif", GA_ReadOnly)
data1 = adata.GetRasterBand(1).ReadAsArray()
data1 = num.array(data1, dtype=numpy.float64)
data1 = ndimage.gaussian_filter1d(data1,5)
markers = num.zeros(data1.shape, dtype=num.uint)
markers[data1 < 63.16895369] = 1
markers[data1 > 335.826927] = 2

# Run random walker algorithm
labels = random_walker(data1, markers, beta=10, mode='bf')

data=data1*1
data1[labels==1]=0
markers1 = num.zeros(data1.shape, dtype=num.uint)
markers1[data1 < 295.3176796] = 1
markers1[data1 > 433.0834366] = 2
labels1 = random_walker(data1, markers1, beta=10, mode='bf')
labels1=num.array(labels1-1, dtype=num.uint)

com=labels+labels1

standtwd = gdal.Open( "*****.tif", GA_ReadOnly)
stand_proj = standtwd.GetProjection()
stand_geotrans = standtwd.GetGeoTransform()
wide = standtwd.RasterXSize
high = standtwd.RasterYSize

driver = gdal.GetDriverByName('GTiff')
#for i in zip (db1.by_col('Satellite'), num.arange(len(newdata))):
dst_filename = '*****.tif'
dataset = driver.Create(dst_filename, wide, high, 1, GDT_UInt32,) #gdal.GDT_Float64, )
dataset.SetGeoTransform(stand_geotrans) 
dataset.SetProjection(stand_proj) 
#for i in range(len(out2.shape[2])):
dataset.GetRasterBand(1).WriteArray(com)
dataset.FlushCache()  # Write to disk.

