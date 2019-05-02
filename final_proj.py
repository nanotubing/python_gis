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
    stores_per_school = "Healthy_stores_per_school.shp"
    arcpy.SpatialJoin_analysis(buffer_suffix, papi_store, stores_per_school,\
                               "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "COMPLETELY_CONTAINS")

#def make_map():
        

[fetch_data(file) for file in zips_to_dl]
spatial_analysis()

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "PhillyPlanning_Schools_buff", "PhillyHealth_Healthy_corner_stores"
#arcpy.SpatialJoin_analysis(target_features="PhillyPlanning_Schools_buff",\
#                           join_features="PhillyHealth_Healthy_corner_stores", out_feature_class="C:/Users/tuj53509/Documents/final_project_cschrader/test2.shp", join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL", field_mapping='AUN "AUN" true true false 19 Double 0 0 ,First,#,PhillyPlanning_Schools_buff,AUN,-1,-1;SCHOOL_NUM "SCHOOL_NUM" true true false 10 Long 0 10 ,First,#,PhillyPlanning_Schools_buff,SCHOOL_NUM,-1,-1;LOCATION_I "LOCATION_I" true true false 50 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,LOCATION_I,-1,-1;FACIL_NAME "FACIL_NAME" true true false 64 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,FACIL_NAME,-1,-1;FACILNAME_ "FACILNAME_" true true false 50 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,FACILNAME_,-1,-1;FACIL_ADDR "FACIL_ADDR" true true false 56 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,FACIL_ADDR,-1,-1;ZIPCODE "ZIPCODE" true true false 16 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,ZIPCODE,-1,-1;FACIL_TELE "FACIL_TELE" true true false 16 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,FACIL_TELE,-1,-1;ACTIVE "ACTIVE" true true false 1 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,ACTIVE,-1,-1;GRADE_LEVE "GRADE_LEVE" true true false 24 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,GRADE_LEVE,-1,-1;GRADE_ORG "GRADE_ORG" true true false 8 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,GRADE_ORG,-1,-1;ENROLLMENT "ENROLLMENT" true true false 5 Long 0 5 ,First,#,PhillyPlanning_Schools_buff,ENROLLMENT,-1,-1;TYPE "TYPE" true true false 10 Long 0 10 ,First,#,PhillyPlanning_Schools_buff,TYPE,-1,-1;TYPE_SPECI "TYPE_SPECI" true true false 50 Text 0 0 ,First,#,PhillyPlanning_Schools_buff,TYPE_SPECI,-1,-1;BUFF_DIST "BUFF_DIST" true true false 19 Double 0 0 ,First,#,PhillyPlanning_Schools_buff,BUFF_DIST,-1,-1;ORIG_FID "ORIG_FID" true true false 10 Long 0 10 ,First,#,PhillyPlanning_Schools_buff,ORIG_FID,-1,-1;OFFICIAL_S "OFFICIAL_S" true true false 254 Text 0 0 ,First,#,PhillyHealth_Healthy_corner_stores,OFFICIAL_S,-1,-1;STORE_ADDR "STORE_ADDR" true true false 254 Text 0 0 ,First,#,PhillyHealth_Healthy_corner_stores,STORE_ADDR,-1,-1;CDC_STORE_ "CDC_STORE_" true true false 19 Double 0 0 ,First,#,PhillyHealth_Healthy_corner_stores,CDC_STORE_,-1,-1;CATEGORY "CATEGORY" true true false 254 Text 0 0 ,First,#,PhillyHealth_Healthy_corner_stores,CATEGORY,-1,-1;ZIP "ZIP" true true false 50 Text 0 0 ,First,#,PhillyHealth_Healthy_corner_stores,ZIP,-1,-1', match_option="COMPLETELY_CONTAINS", search_radius="", distance_field_name="")
#                           
#arcpy.SpatialJoin_analysis(target_features="PhillyPlanning_Schools_buff", \
#                           join_features="PhillyHealth_Healthy_corner_stores",\
#                           out_feature_class="C:/Users/tuj53509/Documents/final_project_cschrader/test2.shp",\
#                           join_operation="JOIN_ONE_TO_ONE", join_type="KEEP_ALL",\
#match_option="COMPLETELY_CONTAINS", search_radius="", distance_field_name="")