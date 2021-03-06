# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:03:12 2019
@author: Claude M. Schrader
"""
from __future__ import absolute_import, division, print_function

#import everything we need
import os

import arcpy
import urllib2
import zipfile

#get the path of the documents directory and build paths to create
documents_dir = os.path.expanduser("~\Documents")
newdir = "final_project_cschrader"
newpath = os.path.join(documents_dir, newdir)
downloads_dir = os.path.join(newpath, "data")
#list containing the four files to download
zips_to_dl = ["ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyHealth_Healthy_corner_stores.zip",\
              "ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyPlanning_Schools.zip",\
              "ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyPlanning_Neighborhoods.zip",\
              "https://github.com/nanotubing/python_gis/raw/master/arcpy_healthy_schools/PhillyPlanning_Schools.lyr"]

#create project and data directories if they don't exist.
#this is more elegant in later versions of python, but we're stuck with 2.7
if not os.path.exists(newpath):
    os.makedirs(newpath)
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)


def fetch_data(url, dl_dir):
    """function to download and unzip if necessary
    returns nothing    
    """
    download_url = urllib2.urlopen(url)
    zip_contents = download_url.read()
    download_url.close()
    out_file_name = os.path.join(dl_dir, os.path.basename(url))
    with open(out_file_name, 'wb') as outf:
        outf.write(zip_contents)
    
    #don't try to unzip the lyr file
    if(out_file_name[-4:]) == ".zip":
        with zipfile.ZipFile(out_file_name, 'r') as zipObj:
            zipObj.extractall(dl_dir)


def spatial_analysis(schools_file_full_loc, schools_buff_loc, corner_store_loc,\
                     stores_per_school_loc):
    """function that performs all the spatial analysis
    returns nothing
    """
    #set up basic arc options
    arcpy.env.workspace = newpath
    arcpy.env.overwriteOutput = True
    
    #set a 300M buffer in the next step
    buffer_dist = "300 Meters"
    #set a 300 meter buffer around each school
    arcpy.Buffer_analysis(schools_file_full_loc, schools_buff_loc, buffer_dist)
    #look for healthy corner stores within 300m school buffer
    arcpy.SpatialJoin_analysis(schools_buff_loc, corner_store_loc, stores_per_school_loc,\
                               "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "COMPLETELY_CONTAINS")
    #insert count of healthy stores back into the original school shp file
    arcpy.JoinField_management(schools_file_full_loc, "SCHOOL_NUM", stores_per_school_loc,\
                               "SCHOOL_NUM", "Join_Count")


def make_map(dl_dir, rootpath, schools_buff_loc, schools_file_full_loc,\
             schools_layer_loc, neighborhoods_loc):
    """create our map using the arc mapping module
    returns nothing
    """
    #set up basic arc options
    arcpy.env.workspace = newpath
    arcpy.env.overwriteOutput = True
    #initial mxd template we use
    mxd_path = os.path.join(os.getcwd(), "final.mxd")
    #name of PDF map we create
    output_pdf_name = "Healthy_Stores_per_School.pdf"
    
    #set up mxd object and data frames
    mxd = arcpy.mapping.MapDocument(mxd_path)
    data_frames = arcpy.mapping.ListDataFrames(mxd)
    data_frame = data_frames[0]

    #create layers from the neighborhood and schools shape files 
    layer0 = arcpy.mapping.Layer(neighborhoods_loc)
    layer1 = arcpy.mapping.Layer(schools_file_full_loc)
    #copy the symbology from the downloaded .lyr file. this is an inelegant
    #way to accomplish this, but here we are
    #this file was manually created in arcmap beforehand
    arcpy.ApplySymbologyFromLayer_management(layer1, schools_layer_loc)
    #add both layers into the map document we're about to export.
    #make sure the base layer is on the bottom
    arcpy.mapping.AddLayer(data_frame, layer0, "BOTTOM")
    arcpy.mapping.AddLayer(data_frame, layer1, "TOP")
    
    #export to PDF
    arcpy.mapping.ExportToPDF(mxd, os.path.join(rootpath, output_pdf_name))
    #also save out the modified mxd document for some manual prettying up
    mxd.saveACopy(os.path.join(rootpath, "Healthy_Stores_per_School.mxd"))


#path to the healthy corner stores shapefile
corner_store = os.path.join(downloads_dir, "PhillyHealth_Healthy_corner_stores.shp")
#set up files and paths for the schools shape file and buffer output file
schools_file_basename = "PhillyPlanning_Schools.shp"
schools_file_full = os.path.join(downloads_dir, schools_file_basename)
schools_buff = schools_file_basename[:-4] + "_buff.shp"
#downloaded lyr file containing schools symbology
schools_layer = os.path.join(downloads_dir, "PhillyPlanning_Schools.lyr")
#intermediate file from spatial analysis
#could be converted into a transient in-memory layer
stores_per_school = "Healthy_stores_per_school.shp"
# philadelphia neighborhoods basemap
neighborhoods = os.path.join(downloads_dir, "PhillyPlanning_Neighborhoods.shp")

#now lets actually run the functions
#list comprehension running the fetch_data( ) function for each item in zips_to_dl
[fetch_data(file, downloads_dir) for file in zips_to_dl]

#run the spatial_analysis() function and pass in all necessary data as args
spatial_analysis(schools_file_full, schools_buff, corner_store, stores_per_school )

#make our actual map and output PDF and modified MXD files
make_map(downloads_dir, newpath, schools_buff, schools_file_full, schools_layer, neighborhoods)

