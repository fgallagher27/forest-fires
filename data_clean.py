import pandas as pd
import geopandas as gpd
from data_funcs import *

data_catalogue = load_data_catalogue()

wildfire_shp = data_catalogue['files']['wildfires']['input']['wildfire_shp']
file = wildfire_shp['file_name']
location = wildfire_shp['location']
check_inputs(location, file)

# read in shapefile of fires and filter for wildfires
wildfire_df = gpd.read_file(os.path.join(location, file))
wildfire_df = filter_df(wildfire_df, "Incid_Type", ["Wildfire", "Out of area response"])

# BurnBndAc - acres mapped
