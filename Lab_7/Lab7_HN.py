import arcpy

# Assign source directory
source = r"H:\ArcGIS\GEOS676\Lab_07\Data\Lab7_Data"

# Assign band rasters
band1 = arcpy.sa.Raster(source + r"\band1.tif")  # Blue band
band2 = arcpy.sa.Raster(source + r"\band2.tif")  # Green band
band3 = arcpy.sa.Raster(source + r"\band3.tif")  # Red band
band4 = arcpy.sa.Raster(source + r"\band4.tif")  # NIR band

# Combine the bands into a single raster
combined = arcpy.CompositeBands_management([band1, band2, band3, band4], source + r"\output_combined.tif")

# Hillshade parameters
azimuth = 315
altitude = 45
shadows = 'NO_SHADOWS'
z_factor = 1

# Generate Hillshade raster
arcpy.ddd.Hillshade(source + r"\DEM.tif", source + r"\output_Hillshade.tif", azimuth, altitude, shadows, z_factor)

# Slope parameters
output_measurement = "DEGREE"
z_factor = 1

# Generate Slope raster
arcpy.ddd.Slope(source + r"\DEM.tif", source + r"\output_Slope.tif", output_measurement, z_factor)

print("Success!")