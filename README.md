Explanation of Code for Requesting Metadata for Satellite Images via ArcGISOnline.

The purpose of this script, is a mulptiple request in ArcGIS Server for downloading metadata polygons which are related to Satellite Images which are used in ArcGIS Online.

First of all, the user should have installed Python version 3 and some modules such as Pandas,Fiona,Geopandas,Csv,Requests,Os,Pathlib.

The code takes as input a csv file which is produced by an attribute table from polygon shapefile.The conversion from attribute table to a csv file takes place in a GIS program such as QGIS which is open software. Note!!! The last four columns of the csv file are the spatial extent of each polygon.(XMIN,YMIN,XMAX,YMAX).The csv file is taken as input in line 17 in code.

The final result is multiple shapefiles which contain the metadata polygons.After this, all shapefiles are merged to one which is projected.
Finally the merged shapefile has duplicate values which are checked and deleted from the script and as a result it is saved as compiled_new.shp.

Note: The whole code runs in Visual Studio Code which has as Python Interpreter a Miniconda Environment with the appropriate modules installed.

Author : Nomikos Nikolaos
