import numpy as num
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
from osgeo import gdal
from scipy import stats

from skimage.segmentation import felzenszwalb, slic, quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

adata = gdal.Open( "*****.tif", GA_ReadOnly)
data1 = img_as_float(adata.GetRasterBand(1).ReadAsArray().astype(num.float64))
#data1=stats.zscore(data1)
data2 = img_as_float(adata.GetRasterBand(2).ReadAsArray().astype(num.float64))
#data2=stats.zscore(data2)
data3 = img_as_float(adata.GetRasterBand(3).ReadAsArray().astype(num.float64))
#data3=stats.zscore(data3)
data4 = img_as_float(adata.GetRasterBand(4).ReadAsArray().astype(num.float64))
#data4=stats.zscore(data4)
data5 = img_as_float(adata.GetRasterBand(5).ReadAsArray().astype(num.float64))
#data5=stats.zscore(data5)
data=num.array([data1, data2, data3,data4,data5]) #data1,data2,
dataT=num.array([data[:,i].transpose() for i in  range(data.shape[1])])
#num.vstack([test[i][j] for j in range(test.shape[1]) for i in range(test.shape[0])])

#segments_fz = felzenszwalb(dataT, scale=600, sigma=2, min_size=60) 
#band 3, 4, 5 (R, NIR and NDVI) plus transfer to the Z values
#segments_slic = slic(dataT, n_segments=5, compactness=10, sigma=1) 
#band 1-5 (RGB, NIR, NDVI) no using the Z values for segmentation
segments_slic = slic(dataT, n_segments=10, compactness=10, sigma=1)
segments_slic=segments_slic+1
#10, 5, 1
#5, 10, 1
#segments_quick = quickshift(dataT, kernel_size=3, max_dist=25, ratio=0.5)


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
dataset.GetRasterBand(1).WriteArray(segments_slic)
dataset.FlushCache()  # Write to disk.

