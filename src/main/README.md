**mosaic.py** is a Python script for mosaicking multiple TIF files into a single seamless image using the rasterio and osgeo modules. Here is a breakdown of what the script does:

Import necessary modules:

os module for working with file paths and directories
gdal module from osgeo for reading TIF files
rasterio module for reading and writing raster data
merge function from rasterio.plot module for merging TIF files
show function from rasterio.plot module for displaying the resulting mosaic
Set the path to the folder containing TIF files to mosaic.

- Get the folder name and create an output filename for the resulting mosaic.

- Get a list of all TIF files in the folder that are above 2 MB.

- Read all TIF files from the list using rasterio and put them in a list.

- Merge all TIF files into a single seamless image using merge function from rasterio.plot module.

- Write the mosaic image to a new TIF file using rasterio.

- Display the mosaic image using show function from rasterio.plot module.
