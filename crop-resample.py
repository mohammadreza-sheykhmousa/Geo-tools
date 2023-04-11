import os
from osgeo import gdal
import rasterio
from rasterio.windows import Window
from rasterio.enums import Resampling
from rasterio.transform import Affine
from shapely.geometry import box

def crop_images(image_path1, image_path2, output_dir):
    # Open the two satellite images
    src1 = rasterio.open(image_path1)
    src2 = rasterio.open(image_path2)
    
    # Check if the spatial resolutions of the two images are the same
    if src1.res != src2.res:
        print("Warning: The spatial resolutions of the two images are different. Resampling to the bigger resolution...")
        if src1.res[0] > src2.res[0]:
            bigger_res = src1.res
            smaller_res = src2.res
            bigger_src = src1
            smaller_src = src2
        else:
            bigger_res = src2.res
            smaller_res = src1.res
            bigger_src = src2
            smaller_src = src1
        
        # Compute the new dimensions for the smaller source based on the bigger resolution
        new_height = round(smaller_src.height * smaller_res[0] / bigger_res[0])
        new_width = round(smaller_src.width * smaller_res[1] / bigger_res[1])
        new_transform = Affine(bigger_res[0], 0, smaller_src.transform[2], 0, bigger_res[1], smaller_src.transform[5])
        
        # Resample the smaller source to the bigger resolution
        smaller_data = smaller_src.read(out_shape=(smaller_src.count, new_height, new_width), resampling=Resampling.bilinear, 
                                         transform=new_transform)
        smaller_meta = smaller_src.meta
        smaller_meta.update({"transform": new_transform, "height": new_height, "width": new_width})
        smaller_src = rasterio.open(os.path.join(output_dir, "resampled_" + os.path.basename(image_path1)), 'w', **smaller_meta)
        smaller_src.write(smaller_data)
        
    # Check if the spectral resolutions of the two images are the same
    if src1.count != src2.count:
        print("Warning: The spectral resolutions of the two images are different.")
    
    # Get the overlapping area of the two satellite images
    bounds = box(*src1.bounds).intersection(box(*src2.bounds))
    window1 = src1.window(*bounds.bounds)
    window2 = src2.window(*bounds.bounds)
    
    # Crop the two images to the overlapping area
    data1 = src1.read(window=window1)
    data2 = src2.read(window=window2)
    
    # Write the cropped images to disk
    cropped1_path = os.path.join(output_dir, "cropped_" + os.path.basename(image_path1))
    cropped2_path = os.path.join(output_dir, "cropped_" + os.path.basename(image_path2))
    
    meta1 = src1.meta
    meta1.update({"transform": src1.window_transform(window1), "height": window1.height, "width": window1.width})
    with rasterio.open(cropped1_path, 'w', **meta1) as dst:
        dst.write(data1)
        
    meta2 = src2.meta
    meta2.update({"transform": src2.window_transform(window2), "height": window2.height, "width": window2.width})
    with rasterio.open(cropped2_path, 'w', **meta2) as dst:
        dst.write(data2)
