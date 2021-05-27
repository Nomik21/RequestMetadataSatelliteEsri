"""      Title of Programm :Request Metadata Polygons from ArcGIS Server
                              Author: Nomikos P.Nikolaos 
                               Last Modified 26/05/2021                    """
import csv
import requests
import geopandas
import fiona
import pandas
import os
from pathlib import Path

print('Welcome to the program of requesting metadata from ArcGIS Server!!')
print('Please remind to place the appropriate csv to the python script in order to run')
print('Thanks for your attention!!')

#OPEN THE CSV FILE AND DEFINES THE VARIABLES OF EXTENT OF POLYGONS
with open ('BundlesPolygon5k.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter= ',')
    Xmin=[]
    Ymin=[]
    Xmax=[]
    Ymax=[]
    line_count = 0

# REQUEST FROM ARCGIS ONLINE AND EXTRACT GEOJSONS.GEOJSONS CONVERTED TO SHAPEFILES
    for row in csv_reader:
            Xmin=float(row[2])
            Ymin=float(row[3])
            Xmax=float(row[4])
            Ymax=float(row[5])
            url= "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/4/query?where=&text=&objectIds=&time=&geometry="+str(Xmin)+","+str(Ymin)+","+str(Xmax)+","+str(Ymax)+"&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&returnTrueCurves=false&maxAllowableOffset=&geometryPrecision=&outSR=4326&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&resultOffset=&resultRecordCount=&queryByDistance=&returnExtentsOnly=false&datumTransformation=&parameterValues=&rangeValues=&f=geojson"
            response=(requests.get(url).text)
            file=open("Massive_test_10k"+str(line_count)+".json","w")
            file.write(response)
            file.close()
            mygeojsonfile=geopandas.read_file('Massive_test_10k' + str(line_count)+ '.json')
            mygeojsonfile.to_file('Massive_test_10k' + str(line_count)+ '.shp')
            print(f'The coordinates of Polygon {row[1]} are: Xmin:{row[2]},Ymin:{row[3]},Xmax:{row[4]},Ymax:{row[5]}.')
            print(f'The coordinates of the id {line_count} are {Xmin,Ymin,Xmax,Ymax} .')
            line_count += 1
    print(f'Processed {line_count} lines.')
    print(f'Code created {line_count} shapefiles')

# MERGE SHAPEFILES 
#Complete the path you saved all the exports.
folder=Path('C:\Projects\Metadata_SatelliteArcGIS')
shapefiles=folder.glob('Massive_test_10k*.shp')
gdf=pandas.concat([geopandas.read_file(shp) for shp in shapefiles]).pipe(geopandas.GeoDataFrame)# pipe unions the functions read_file and GeoDataFrame
gdf.to_file(folder/'compiled.shp')
print("The code merged the shapefiles to compiled.shp")

# CREATE A PROJECTION FILE FOR THE MERGED SHAPEFILE
def getWKT_PRJ():
    urlprj="https://spatialreference.org/ref/epsg/4326/esriwkt/"
    wkt=(requests.get(urlprj).text)
    #wkt=urllib.request.urlopen("https://spatialreference.org/ref/epsg/
    return wkt

prj=open("compiled.prj", "w")
epsg= getWKT_PRJ()
prj.write(epsg)
prj.close()
print('The code projected the compiled.shp')

# REMOVE DUPLICATES FROM MERGED AND PROJECTED SHAPEFILE AND CREATES THE FINAL SHP
metadata_attribute=geopandas.read_file(folder/'compiled.shp')
new_shp=metadata_attribute.drop_duplicates('OBJECTID')
new_shp.to_file(folder/'finalresult.shp')
print('The code removed the duplicates from compiled.shp and created the final compiled_new.shp')
print('The compiled_new.shp is ready for further geoprocessing')
print('Thanks for your valuable time')

