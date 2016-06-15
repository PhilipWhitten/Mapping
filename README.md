# GPX to shapefile format with reprojection of data
Python code for converting a folder of gpx files to ESRI shapefiles.

This aim of this project is to take a collect of gpx files and produce a raster heatmap type image where different colors are used to indicate the number of times a gpx track is incident on a specific point.

The first step is to open a series of gpx files located in one folder, change their projection (in this case EPSG28355), and change their file type to one that is compatible with the GDAL python library (eg. shapefile).

Uses the GDAL python library.  Intructions for loading GDAL library: http://cartometric.com/blog/2011/10/17/install-gdal-on-windows/
