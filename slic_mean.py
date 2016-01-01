from osgeo import gdal  
from osgeo.gdalnumeric import *  
from osgeo.gdalconst import *
import gdal, ogr, osr
import numpy as num
import sys
import os, glob
import pysal
from rasterstats import raster_stats
from osgeo import ogr
import pandas as pd

polyshp=glob.glob('*****.shp')
polydbf=glob.glob('*****.dbf')
#polyshp=sorted(glob.glob('*****.shp'))[32:36]
#polydbf=sorted(glob.glob('*****.dbf'))[32:36]
tif=glob.glob('*****.tif')

scalepara=sorted([i[i.find('NDVI'):i.find('_s.shp')-4].replace('NDVI','N').replace('07','') for i in polyshp])
scaletif=sorted([i[i.find('clipNDVI'):i.find('.tif')].replace('NDVI','N').replace('clip','').replace('19','').replace('181','18')[:-8]+'_'+i[i.find('clipNDVI'):i.find('.tif')][-1] for i in tif])

for i, l in zip(polyshp, polydbf): #two loops for each shape with different parameters on different layers
	source = ogr.Open(i, 1) #add fields to each shape files
	layer = source.GetLayer()
	layer_defn = layer.GetLayerDefn()
	field_names = [layer_defn.GetFieldDefn(u).GetName() for u in range(layer_defn.GetFieldCount())]
	
	for k in scaletif:
		new_mean = ogr.FieldDefn(k, ogr.OFTReal) #add field names to the shape files
		layer.CreateField(new_mean)
	
	source = None

	for j, g in zip (tif,  range(1, len(scaletif)+1)):
		highstats=raster_stats(i,j, stats="mean", copy_properties=True)
		
		mymean = [] #get the mean from the dictionary
		for p in highstats:
			mymean.append(p.values()[0])
			
		#change the dbf file
		#db = pysal.open(l, 'r')
		db= pysal.open(l, 'r')
		#d = {col: db.by_col(col) for col in db.header}
		#dtable=pd.DataFrame(d).fillna(0)
		#dtable[list(dtable.columns)[g]]=mymean
		meansave = []
		for t, u in zip (db, mymean):
			t[g] = u
			meansave.append(t)

		x=db.header
		y=db.field_spec
		db1 = pysal.open(l, 'w')
		db1.header=x
		db1.field_spec=y

		for s in range(len(db)):
			db1.write(meansave[s])

		db1.close()
		db.close()
