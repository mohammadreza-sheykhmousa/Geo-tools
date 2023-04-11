import os
from osgeo import gdal
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import matplotlib

# Folder containing TIF files to mosaic
folder_path = r'C:\datasets\'

# Get folder name and create output filename
folder_name = os.path.basename(folder_path)
output_filename = f'mosaic_{folder_name}.tif'

# Get a list of all TIF files in the folder above 10 MB
file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.tif') and os.path.getsize(os.path.join(folder_path, f)) > 10000000]

# Read all TIF files and put them in a list
src_files_to_mosaic = []
for file in file_list:
    src = rasterio.open(file)
    src_files_to_mosaic.append(src)

# Merge all TIF files into a single seamless image
mosaic, out_trans = merge(src_files_to_mosaic)

# Write the mosaic image to a new TIF file
output_path = os.path.join(folder_path, output_filename)
with rasterio.open(output_path, 'w', driver='GTiff', 
                   width=mosaic.shape[2], height=mosaic.shape[1], 
                   count=mosaic.shape[0], dtype=mosaic.dtype, 
                   transform=out_trans) as dst:
    dst.write(mosaic)

# Display the mosaic image
show(mosaic)
