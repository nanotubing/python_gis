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
    papi_store = "PhillyHealth_Healthy_corner_stores.shp"
    buffer_file = "PhillyPlanning_Schools.shp"
    buffer_suffix = buffer_file[:-4] + '_buff.shp'
    buffer_dist = "300 Meters"
#    print(buffer_file)
#    print(buffer_suffix)
    arcpy.Buffer_analysis(buffer_file, buffer_suffix, buffer_dist)
    
    arcpy.SpatialJoin_analysis(buffer_suffix, papi_store,"in_memory/points_SpatialJoin",\
                               "JOIN_ONE_TO_MANY", "KEEP_ALL", "", "INTERSECT")

#def make_map():
        

[fetch_data(file) for file in zips_to_dl]
spatial_analysis()