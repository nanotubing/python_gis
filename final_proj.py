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
zips_to_dl = ["ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyHealth_Healthy_corner_stores.zip",\
              "ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyPlanning_Schools.zip",\
              "ftp://ftp.pasda.psu.edu/pub/pasda/philacity/data/PhillyPlanning_Neighborhoods.zip"]

if not os.path.exists(newpath):
    os.makedirs(newpath)
    

def fetch_data(url):
    download_url = urllib2.urlopen(url)
    zip_contents = download_url.read()
    download_url.close()
    out_file_name = os.path.join(newpath, os.path.basename(url))
    with open(out_file_name, 'wb') as outf:
        outf.write(zip_contents)
        
    with zipfile.ZipFile(out_file_name, 'r') as zipObj:
        zipObj.extractall(newpath)

def spatial_analysis():
    arcpy.env.workspace = newpath
    arcpy.env.overwriteOutput = True
    corner_store = "PhillyHealth_Healthy_corner_stores.shp"
    schools_file = "PhillyPlanning_Schools.shp"
    schools_buff = schools_file[:-4] + '_buff.shp'
    buffer_dist = "300 Meters"

    arcpy.Buffer_analysis(schools_file, schools_buff, buffer_dist)
    stores_per_school = "Healthy_stores_per_school.shp"
    arcpy.SpatialJoin_analysis(schools_buff, corner_store, stores_per_school,\
                               "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "COMPLETELY_CONTAINS")
    arcpy.JoinField_management(schools_file, "SCHOOL_NUM", stores_per_school, "SCHOOL_NUM", "Join_Count")


def make_map():
    neighborhoods_shp = "PhillyPlanning_Neighborhoods.shp"
    mxd_path = os.path.join(os.getcwd(), "final.mxd")
    output_pdf_name = "Healthy_Stores_PerSchool.pdf"
    print(mxd_path)
    mxd = arcpy.mapping.MapDocument(mxd_path)
    data_frames = arcpy.mapping.ListDataFrames(mxd)
    data_frame = data_frames[0]
    
    arcpy.mapping.AddLayer(data_frame, neighborhoods_shp, "BOTTOM" )
    
    #export to PDF
    arcpy.mapping.ExportToPDF(mxd, "output_pdf_name")

[fetch_data(file) for file in zips_to_dl]

spatial_analysis()

make_map()
