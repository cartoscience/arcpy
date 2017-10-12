#--- Bulk raster processing (MODIS NDVI sample)
#--- execfile(r'c:\path_to_code\bulk_raster_processing.py')

import sys, string, os, os.path, arcgisscripting, arcpy, datetime
from arcpy.sa import *
gp = arcgisscripting.create()
gp.CheckOutExtension("spatial")
arcpy.env.overwriteOutput = True
arcpy.env.resamplingMethod = "BILINEAR"

gp.cellSize = "250"
scaleFactor = "0.0001"

startTime = datetime.datetime.now()
print(u"\u2022" + " Start time: " + str(startTime))

extent = arcpy.env.snapRaster = "c:\\path_to_mask_raster\\mask_raster.tif"
inFolder = arcpy.env.workspace = "V:\\path_to_folder_containing_rasters\\"
outFolder = str(arcpy.CreateFolder_management(inFolder, "processing_results"))

rasterList = arcpy.ListRasters()
for raster in rasterList:
    outName = os.path.basename(raster).rstrip(os.path.splitext(raster)[1])
    print(u"\u2022" + " Processing raster: " + str(outName) + "...")
    arcpy.gp.Times_sa(raster, scaleFactor, "in_memory/ndvi")
    arcpy.gp.ExtractByMask_sa("in_memory/ndvi", extent, outFolder + "\\" + outName + "_p.tif")

print(u"\u2022" + " Cleaning workspace...")
arcpy.env.workspace = outFolder
itemList = arcpy.ListFiles()
for item in itemList:
    if str(os.path.splitext(item)[1].lstrip(".")) != str("tif"):
        arcpy.gp.Delete_management(item)

endTime = datetime.datetime.now()
print(u"\u2022" + " End time: " + str(endTime))
elapsedTime = endTime - startTime
print(u"\u2022" + " Elapsed time: " + str(elapsedTime))
countFiles = len(os.listdir(outFolder))
print(u"\u2022" + " " + str(countFiles) + " raster files processed")
print(u"\u2022" + " Folder containing output files: " + str(outFolder))
print(u"\u2022" + " Processing complete!")

arcpy.RefreshCatalog(inFolder)
arcpy.RefreshCatalog(outFolder)

arcpy.gp.Delete_management("in_memory")
arcpy.ClearWorkspaceCache_management()
