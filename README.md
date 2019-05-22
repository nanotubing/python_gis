## GIS analyses performed in python
### arcpy_healthy_schools - Number of Healthy Corner stores per School
This analysis was created using Python 2.7 and the arcpy interface to ArcMap 10.5.1

This script downloads a few shape files from [PASDA](http://www.pasda.psu.edu) and a template layer file. 
It then performs a spatial analyis, calculating the number of healthy corner stores within 300 Meters of 
each school in Philadelphia, and creates a map based on that data. The visualization was limited pretty 
heavily by arcpy's mapping capabilities.  
