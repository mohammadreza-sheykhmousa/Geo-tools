import os
from osgeo import gdal

def geotiff_to_png(input_path, output_path=None, return_object=False):
    """
    Converts a GeoTIFF file to a PNG file or object. Specific to Skysatimages with 4 bands (blue, green, red, nir).

    Args:
        input_path (str): The file path of the input GeoTIFF file.
        output_path (str, optional): The file path of the output PNG file. If not provided, PNG object is returned. Defaults to None.
        return_object (bool, optional): Whether to return the PNG data as an object. If True, the output_path parameter will be ignored. Defaults to False.

    Returns:
        numpy.ndarray or None: If output_path is not provided and return_object is True, returns a 3D numpy array representing the PNG image. Otherwise, returns None.

    """
    # Open input file
    dataset = gdal.Open(input_path)
    output_types = [gdal.GDT_Byte, gdal.GDT_UInt16, gdal.GDT_Float32]
    
    # Define output format and options
    options = gdal.TranslateOptions(format='PNG', bandList=[3,2,1], creationOptions=['WORLDFILE=YES'], outputType=output_types[0])
    
    # Translate to PNG
    if output_path is not None:
        gdal.Translate(output_path, dataset, options=options)
        print(f'Successfully saved PNG file to {output_path}')
    
    # Return PNG object
    if return_object:
        mem_driver = gdal.GetDriverByName('MEM')
        mem_dataset = mem_driver.CreateCopy('', dataset, 0)
        png_data = mem_dataset.ReadAsArray()
        return png_data
