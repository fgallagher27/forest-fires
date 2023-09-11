# data download script
import os
from data_funcs import load_data_catalogue, download_data

data_catalogue = load_data_catalogue()

mtbs_url = data_catalogue['downloads']['wildfires']['url']
mtbs_folder = os.path.join("data","inputs", "mtbs_wildfires.zip")
shp_file = "mtbs_perims_DD.shp"
extract_location = os.path.join("data", "inputs")

# download_zip_from_url(mtbs_url, mtbs_folder)
# extract_zip(mtbs_folder)

download_data(mtbs_url, mtbs_folder, shp_file, extract_location)