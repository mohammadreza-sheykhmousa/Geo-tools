import os
import numpy as np
from osgeo import gdal
import rasterio
from rasterio.windows import Window
from shapely.geometry import box
from rasterio.plot import show
import matplotlib.pyplot as plt
from rasterio.features import geometry_mask
from rasterio.mask import mask
from rasterio.enums import Resampling
from rasterio import features

def crop_images(image_path1, image_path2, output_dir):
    """
    Crops two satellite images to their overlapping area and writes them to disk. The function first opens the two images
    using the rasterio library, then calculates the overlapping area of the images using the shapely library. It defines
    a window for each image that covers the overlapping area and reads only the data within these windows. The function
    then writes the cropped images to disk in the specified output directory using the metadata of the original images.
    Finally, the function visualizes the cropped images side by side using matplotlib.

    Parameters:
        image_path1 (str): The file path of the first image (TIFF file).
        image_path2 (str): The file path of the second image (TIFF file).
        output_dir (str): The directory where the cropped images will be saved.

    Returns:
        Tuple[rasterio.DatasetReader, rasterio.DatasetReader]: A tuple containing the rasterio dataset readers for the
        two original images.
    """
    # Open the two satellite images
    src1 = rasterio.open(image_path1)
    src2 = rasterio.open(image_path2)

    # Get the overlapping area of the two satellite images
    bounds = box(*src1.bounds).intersection(box(*src2.bounds))

    # Define a window that covers the area of the polygon
    window1 = src1.window(*bounds.bounds)
    window2 = src2.window(*bounds.bounds)

    # Read only the data within the window
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

    # Visualize the two images
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    show(data1, ax=axs[0], title="Image 1")
    show(data2, ax=axs[1], title="Image 2")
    plt.show()

    with rasterio.open(image_path1) as src1, rasterio.open(image_path2) as src2:
        return src1, src2
