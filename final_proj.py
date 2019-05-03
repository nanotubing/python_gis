# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:03:12 2019

@author: tuj53509
"""
from __future__ import absolute_import, division, print_function

import arcpy, os, urllib2, zipfile

documents_dir = os.path.expanduser("~\Documents")
newdir = "final_project_cschrader"
newpath = os.path.join(documents_dir, newdir)
downloads_dir = os.path.join(newpath, "data")
zips_to_dl = ["ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyHealth_Healthy_corner_stores.zip",\
              "ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyPlanning_Schools.zip",\
              "ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyPlanning_Neighborhoods.zip"]

if not os.path.exists(newpath):
    os.makedirs(newpath)
if not os.path.exists(downloads_dir):
    os.makedirs(downloads_dir)


def fetch_data(url, dl_dir):
    download_url = urllib2.urlopen(url)
    zip_contents = download_url.read()
    download_url.close()
    out_file_name = os.path.join(dl_dir, os.path.basename(url))
    with open(out_file_name, 'wb') as outf:
        outf.write(zip_contents)
        
    with zipfile.ZipFile(out_file_name, 'r') as zipObj:
        zipObj.extractall(dl_dir)

def spatial_analysis(schools_file_full_loc, schools_buff_loc, corner_store_loc,\
                     stores_per_school_loc):
    arcpy.env.workspace = newpath
    arcpy.env.overwriteOutput = True
    
    buffer_dist = "300 Meters"

    arcpy.Buffer_analysis(schools_file_full_loc, schools_buff_loc, buffer_dist)
    arcpy.SpatialJoin_analysis(schools_buff_loc, corner_store_loc, stores_per_school_loc,\
                               "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "COMPLETELY_CONTAINS")
    arcpy.JoinField_management(schools_file_full_loc, "SCHOOL_NUM", stores_per_school_loc,\
                               "SCHOOL_NUM", "Join_Count")


def make_map(dl_dir, rootpath, schools_buff_loc, schools_file_full_loc, neighborhoods_loc):
    arcpy.env.workspace = newpath
    arcpy.env.overwriteOutput = True
    
    
    mxd_path = os.path.join(os.getcwd(), "final.mxd")
    output_pdf_name = "Healthy_Stores.pdf"
#    layer_list = [schools_buff_loc, schools_file_full_loc, neighborhoods_loc]
    
    mxd = arcpy.mapping.MapDocument(mxd_path)
    data_frames = arcpy.mapping.ListDataFrames(mxd)
    data_frame = data_frames[0]
    
    layer0 = arcpy.mapping.Layer(neighborhoods_loc)
    arcpy.mapping.AddLayer(data_frame, layer0, "BOTTOM")
#    layer1 = arcpy.mapping.Layer(schools_buff_loc)
#    arcpy.mapping.AddLayer(data_frame, layer1)
    layer2 = arcpy.mapping.Layer(schools_file_full_loc)
    arcpy.mapping.AddLayer(data_frame, layer2, "TOP")

        
    #export to PDF
    arcpy.mapping.ExportToPDF(mxd, os.path.join(rootpath, output_pdf_name))


corner_store = os.path.join(downloads_dir, "PhillyHealth_Healthy_corner_stores.shp")
schools_file_basename = "PhillyPlanning_Schools.shp"
schools_file_full = os.path.join(downloads_dir, schools_file_basename)
schools_buff = schools_file_basename[:-4] + "_buff.shp"
stores_per_school = "Healthy_stores_per_school.shp"
neighborhoods = os.path.join(downloads_dir, "PhillyPlanning_Neighborhoods.shp")

[fetch_data(file, downloads_dir) for file in zips_to_dl]

spatial_analysis(schools_file_full, schools_buff, corner_store, stores_per_school )

make_map(downloads_dir, newpath, schools_buff, schools_file_full, neighborhoods)
