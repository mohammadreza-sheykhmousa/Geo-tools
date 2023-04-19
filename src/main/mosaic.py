import os
from osgeo import gdal
import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import matplotlib

# Folder containing TIF files to mosaic
folder_path = r"C:\dataset"

# Get folder name and create output filename
folder_name = os.path.basename(folder_path)
output_filename = f'mosaic_{folder_name}.tif'

# Get a list of all TIF files in the folder above 2 MB
file_list = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.tif') and os.path.getsize(os.path.join(folder_path, f)) > 2000000]
# print(folder_name)
# print(output_filename)
# print(len(file_list))

# Read the CRS of the first input image
with rasterio.open(file_list[0]) as src:
    crs = src.crs

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
                   transform=out_trans,crs=crs) as dst:
    dst.write(mosaic,[3, 2, 1, 4])  # <-- reverse order of bands: red, green, blue, NIR

# Display the mosaic image
show(mosaic)
