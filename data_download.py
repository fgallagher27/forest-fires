# data download script
import os
from data_funcs import download_zip_from_url, extract_zip, download_data

mtbs_url = "https://edcintl.cr.usgs.gov/downloads/sciweb1/shared/MTBS_Fire/data/composite_data/burned_area_extent_shapefile/mtbs_perimeter_data.zip"
mtbs_folder = os.path.join("data","inputs", "mtbs_wildfires.zip")
shp_file = "mtbs_perims_DD.shp"
extract_location = os.path.join("data", "inputs")

# download_zip_from_url(mtbs_url, mtbs_folder)
# extract_zip(mtbs_folder)

download_data(mtbs_url, mtbs_folder, shp_file, extract_location)