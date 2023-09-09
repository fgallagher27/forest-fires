import pandas as pd
import geopandas as gpd
from data_funcs import *

wildfire_shp = "mtbs_perims_DD.shp"
check_inputs(wildfire_shp)

# read in shapefile of fires and filter for wildfires
wildfire_df = gpd.read_file(os.path.join("data", "inputs", wildfire_shp))
wildfire_df = filter_df(wildfire_df, "Incid_Type", ["Wildfire", "Out of area response"])

# BurnBndAc - acres mapped