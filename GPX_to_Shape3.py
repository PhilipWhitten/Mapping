# This script opens all the gpx files in a folder and saves their track point layers in a shapefile.
# Script uses Try-Finally structure to reduce lock's on datasets.

import os
import ogr
import osr
import sys

fn = '6HR_Rogain_Tarlo_NP.gpx'
os.chdir(r'C:\Users\pipi\Documents\Rogaine\Tarlo\gpx')  #folder containing gpx files
EPSG = 28355 #EPSG of desired spatial reference system. 28355 if for GDA94, 54.
# in future might automate the selection of EPSG or use a world system.

shfn = 'gpxcollection.shp'  # produce a shapefile to contain all of the gpx files, with the same fields

driverName = "ESRI Shapefile"
driver = ogr.GetDriverByName(driverName)

if os.path.isfile(shfn): #deletes file shfn if it already exists
    driver.DeleteDataSource(shfn)

# change spatial reference system
SR = osr.SpatialReference()  # TO DO: automate the selection of UTM zone or similar
SR.ImportFromEPSG(EPSG)

# constructs an empty shapefile
if driver is None:
    print "%s driver not available.\n" % driverName
    sys.exit( 1 )

try:
    OutDs = driver.CreateDataSource(shfn)  #does this command leave the created file open?
    if OutDs is None:
        print "Creation of output file failed.\n"
        sys.exit( 1 )
    # creates a layer in the shapefile with the appropriate spatial reference (SR) and geometry.
    outlyr = OutDs.CreateLayer(fn[:-4], SR, geom_type=ogr.wkbMultiPoint)
    outlyrDefn = outlyr.GetLayerDefn()
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)

    # open all gpx files in a folder
    files = os.listdir(os.curdir)
    for file in files:
        if file[-3:] == 'gpx':
            # opens a single gpx file
            try:
                ds = ogr.GetDriverByName('GPX').Open(file, 0)  #by stating driver, the code does not have to find it.
                #0 means read only mode, 1 would allow editing
                if ds is None:
                    sys.exit('Could not open {0}.'.format(file))
                lyr = ds.GetLayer('track_points')  #get's the layer containing tarck points
                multipoint.Empty()

                for feature in lyr:  #reads each point in the gpx file and converts to a multipoint with new SR
                    geom = feature.GetGeometryRef()
                    pt = feature.geometry()
                    pt.TransformTo(SR)  #TransformTo must be done on each point, not the layer
                    multipoint.AddGeometry(pt)

            finally:
                del ds

            # NEED TO ADD FIELD TO SHAPEFILE FOR EACH GPX FILENAME

            # add's multipoint to shapefile.
            # code might be much faster if multipoint data sets are put into temporary Python dictionary.
            outFeature = ogr.Feature(outlyrDefn)
            outFeature.SetGeometry(multipoint)  #adds the multipoint data to outFeature
            outlyr.CreateFeature(outFeature)  #add outFeature to the shapefile
            outFeature.Destroy()
finally:
    del OutDs


