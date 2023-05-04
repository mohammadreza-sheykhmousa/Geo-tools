import os
import rasterio
from rasterio.windows import Window
from shapely.geometry import box
import numpy as np
import matplotlib.pyplot as plt


def mask_images(image_path1, image_path2, output_dir):
    """
    Mask two satellite images to the overlapping area based on a condition that values in both images are
    non-zero. If a pixel value is zero or not available in one image, then the corresponding pixel value in the other
    image is also masked out. Finally, the cropped images are written to disk and visualized.

    Parameters:
        image_path1 (str): The file path of the first image (TIFF file).
        image_path2 (str): The file path of the second image (TIFF file).
        output_dir (str): The directory where the cropped images will be saved.

    Returns:
        None
    """
    with rasterio.open(image_path1) as src1, rasterio.open(image_path2) as src2:
        # Read the data and mask values equal to 0 for the first file
        data1 = src1.read()
        mask1 = data1 != 0

        # Read the data and mask values equal to 0 for the second file
        data2 = src2.read(1)
        mask2 = data2 != 0

        # Create the third mask based on the condition mentioned in the question
        mask3 = np.logical_and(mask1, mask2)

        # Get the overlapping area of the two satellite images based on mask3
        bounds = box(*src1.bounds).intersection(box(*src2.bounds))
        window = src1.window(*bounds.bounds)
        mask3 = mask3[int(window.row_off):int(window.row_off + window.height), int(window.col_off):int(window.col_off + window.width)]

        # Crop the two images to the overlapping area based on mask3
        data1 = src1.read(1, window=window, masked=True)
        data2 = src2.read(1, window=window, masked=True)

        # Mask out corresponding pixel values in the other image if one pixel value is zero or not available based on mask3
        data1[~mask3] = 0
        data2[~mask3] = 0

        # Write the cropped images to disk
        cropped1_path = os.path.join(output_dir, "cropped_" + os.path.basename(image_path1))
        cropped2_path = os.path.join(output_dir, "cropped_" + os.path.basename(image_path2))

        meta1 = src1.meta
        meta1.update({"transform": src1.window_transform(window), "height": mask3.shape[0], "width": mask3.shape[1]})
        with rasterio.open(cropped1_path, 'w', **meta1) as dst:
            dst.write(data1, 1, window=Window(0, 0, mask3.shape[1], mask3.shape[0]))

        meta2 = src2.meta
        meta2.update({"transform": src2.window_transform(window), "height": mask3.shape[0], "width": mask3.shape[1]})
        with rasterio.open(cropped2_path, 'w', **meta2) as dst:
            dst.write(data2, 1, window=Window(0, 0, mask3.shape[1], mask3.shape[0]))

        # Visualize the two images based on mask3
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        axs[0].imshow(np.ma.masked_array(data1, mask=~mask3))
        axs[0].set_title("Image 1")
        axs[1].imshow(np.ma.masked_array(data2, mask=~mask3))
        axs[1].set_title("Image 2")
        plt.show()

