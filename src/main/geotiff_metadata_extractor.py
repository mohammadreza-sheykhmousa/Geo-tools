"""
This module provides a function to extract metadata from a GeoTIFF file, including the bounding box and CRS, and output the information to a JSON file.

The module requires the following packages to be installed:
    - rasterio
    - osgeo (part of the GDAL library)
    - json

Example usage:
    import geotiff_metadata_extractor

    # extract metadata and output to JSON file
    geotiff_metadata_extractor.get_metadata(src='example.tif', output_file='metadata.json')

    # extract metadata without writing to file
    metadata = geotiff_metadata_extractor.get_metadata(src='example.tif', write=False)

"""

from osgeo import gdal
import rasterio
import json

def get_metadata(src, output_file=None, write=True):
    """
    Extracts metadata from a GeoTIFF file, including the bounding box and CRS.

    Args:
        src (str or path-like object): The file path of the GeoTIFF file to extract metadata from.
        output_file (str, optional): The file path to output the metadata as a JSON file. If not provided, the metadata is not written to file.
        write (bool, optional): A flag indicating whether to write the metadata to file. If False, the metadata is returned as a dictionary. Default is True.

    Returns:
        dict: A dictionary containing the metadata information, including the bounding box and CRS. Only returned if write=False.

    Raises:
        Exception: If the GeoTIFF file cannot be opened or if an error occurs during metadata extraction.

    """
    try:
        # Open the GeoTIFF file
        with rasterio.open(src) as dataset:
            # Get the bounding box and CRS
            bbox = dataset.bounds
            crs = dataset.crs.to_dict()
            tags = dataset.tags()
            meta = dataset.meta.copy()
            print(bbox, crs)

        # Create a dictionary with the values
        data = {
            "bbox": bbox,
            "crs": crs,
            "tags": tags,
            "meta": meta
        }

        # If output file not provided, use the same filename as the input file
        if not output_file:
            output_file = os.path.splitext(str(src))[0] + '.json'

        # Write the dictionary to a JSON file
        if write:
            with open(output_file, "w") as f:
                json.dump(data, f)

        else:
            return data

    except Exception as e:
        raise Exception(f"Error extracting metadata from GeoTIFF file: {e}")