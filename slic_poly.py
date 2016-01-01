import glob
from osgeo import gdal, ogr, osr
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
from osgeo import gdal
import numpy as num

seg=sorted(glob.glob('*****.tif'))
#seg=[i for i in reversed(seg)]
myname=[i[i.find('*****'):i.find('.tif')] for i in seg]

#rasteter to polygon
for i in range(len(seg)):
	adata = gdal.Open(seg[i])
	data = adata.GetRasterBand(1)
	spatialReference = osr.SpatialReference()
	spatialReference.ImportFromProj4('+proj=utm +zone=14 +ellps=GRS80 +datum=NAD83 +units=m +no_defs')
	driver_v = ogr.GetDriverByName("ESRI Shapefile")
	outfile='*****.shp'
	outdataset = driver_v.CreateDataSource(outfile)
	outlayer = outdataset.CreateLayer(outfile, spatialReference, geom_type=ogr.wkbMultiPolygon)#, srs = None)
	categories = ogr.FieldDefn('categories', ogr.OFTInteger)
	outlayer.CreateField(categories)
	gdal.Polygonize( data, data, outlayer, 0, [], callback=None )
	outlayer = None
