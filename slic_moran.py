import pysal
import numpy as num
import os, glob
import csv

poly=glob.glob('*****.shp')

scalepara=sorted([i[i.find('NDVI'):i.find('_s.shp')].replace('NDVI','N')[:i[i.find('NDVI'):i.find('_s.shp')].replace('NDVI','N').find('_')+5] for i in poly])
#scalepara=sorted([i[i.find('NDVI'):i.find('.shp')].replace('NDVI','N')[:i[i.find('NDVI'):i.find('.shp')].replace('NDVI','N').find('_')+5]+'_'+i[i.find('NDVI'):i.find('.shp')][-4:] for i in poly])
#scaletif=sorted([i[i.find('slicNDVI'):i.find('.tif')] for i in tif])
newMoran = []	
for i in range(len(poly)): 
	#create weight files
	wh = pysal.queen_from_shapefile(poly[i])
	
	MoransI = []
	#Moran's I
	db = pysal.open(poly[i].replace('.shp','.dbf'),'r')
	#a=[p for p in db.header[1:] if '2014' in p]
	for g in db.header[1:]:
		db1 = num.array(db.by_col[g])
		#if g == 'N_2014_5':
		for p in range(len(db1)):
			if str(db1[p]) == 'None':
				db1[p]=0
		db1=db1.astype(float)
		mi = pysal.Moran(db1, wh)
		MoransI.append(mi.z_norm)
		#MoransI.append(mi.I)
		#print mi.I
	
	newMoran.append(MoransI)

dy=range(len(scalepara)) #scale parameter label
for i, j in zip(range(len(scalepara)), scalepara):
	dy[i]=j

newlist=[]
for p, q in zip(dy, newMoran):
	newlist.append([p]+q)

with open('*****.txt', 'wb') as f:
	writer = csv.writer(f)
	writer.writerows([db.header])
	writer.writerows(newlist)
db.close()
