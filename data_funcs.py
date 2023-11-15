"""
This script contains the functions needed to download, check and clean the mtbs wildfires dataset
It can be imported as a module into the data download and clean scripts
It contains the following functions:

    * download_zip_from_url 
    * extract_zi
    * download_data
    * check_inputs
    * load_data_catalogue
    * count_nas
    * filter_df
    * extract_state
    * calc_area
    * normalise_values
    * normalise_cols

"""

import os
import pandas as pd
import geopandas as gpd
import zipfile
import yaml
import requests
from typing import List, Union


### Download files ----

def download_zip_from_url(url: str, file_path: str):
    """
    This function downloads a zip file from a url and places into file_path

    Args:
        url (str): url address of the zip folder to download
        file_path (str): folder path to save the zip file to including the name of the zip

    """
    print("Downloading data...")
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"File '{file_path}' downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


def extract_zip(zip_file_path: str, extract_location: str):
    """
    This function extracts the contents of a zipfile to extract_location.
    """
    print(f"Extracting data from {zip_file_path}")
    try:
        if not os.path.isfile(zip_file_path):
            raise FileNotFoundError(f"The file '{zip_file_path}' does not exist.")
        
        # Create the extraction directory if it doesn't exist
        os.makedirs(extract_location, exist_ok=True)

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_location)

        print(f"Successfully extracted {zip_file_path} to {extract_location}")

    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# maybe at some point refactor as a module/class structure
def download_data():
    """
    This function checks if the required data has already been downloaded.
    If it has not, it downloads and extracts it.
    """

    data_catalogue = load_data_catalogue()

    for input in data_catalogue['inputs']:

        print(f"Accessing information for {input} input")
        catalogue = data_catalogue['inputs'][input]
        folder_path = catalogue['location']
        file_name = catalogue['file_name']
        zip = catalogue['zip_folder']
        url = catalogue['url']
        input_path = os.path.join(folder_path, file_name)

        if os.path.exists(input_path):
            print(f"{file_name} is already downloaded in the subdirectory 'data'")
        elif os.path.exists(zip):
            print(f"Extracting data from {folder_path}...")
            extract_zip(zip, folder_path)
        elif url is not None:
            print(f"Downloading and extracting data from {url}...")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            download_zip_from_url(url, zip)
            extract_zip(zip, folder_path)
        else:
            raise ValueError("Invalid paths specified in data catalogue")


def check_inputs(folder: str, file: str):
    """
    Checks whether appropriate files are downloaded
    """
    # if path to wildfire shp does not exist, source download script
    # else do nothing
    file_path = os.path.join(folder, file)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'The file path "{file_path}" does not exist. Please run data_download.py to download required data')


### Data Catalogue ----

def load_data_catalogue():
    """
    Loads data catalogue
    """
    # Load the YAML data from the file
    with open('data_catalogue.yml', 'r') as file:
        data_catalogue = yaml.safe_load(file)
    return data_catalogue


### Data cleaning ----

def count_nas(df: pd.DataFrame):
    """
    Counts the number of missing values (NAs) in each column of a dataframe object
    """
    return df.isna().sum()


def filter_df(df: pd.DataFrame, column: str, values: List[str]):
    """
    This function filters a df so that column only contains the values in values
    """
    orig = len(df)
    new_df = df[df[column].isin(values)]

    new = len(new_df)
    diff = orig - new
    print(f"Filtering {column} for values in {values} has dropped {diff} rows from the dataframe")

    return new_df


def extract_state(df: Union[pd.DataFrame, gpd.GeoDataFrame]):
    """
    Creates a state column by extracting the leading 2 letter state code from the Event_ID
    """
    df['state'] = df.Event_ID.str[:2]
    return df


def calc_area(gpd_df: gpd.GeoDataFrame):
    """
    Creates an area column on a geopandas dataframe holding the area of each polygon
    """
    gpd_df['area'] = gpd_df['geometry'].area
    return gpd_df


def normalise_values(numbers: List[Union[float, int]]):
    """
    This function takes in a list of numbers and normalises the data to lie between 0 and 1

    Args:
        numbers (list): A list of numbers to normalise.
    
    Returns:
        list: list of numbers normalised between 0 and 1
    """
    min_val = min(numbers)
    max_val = max(numbers)

    # avoid division by zero if all numbers are the same
    if min_val == max_val:
        return [0.0] * len(numbers)
    else:
        return [(x - min_val) / (max_val - min_val) for x in numbers]


def normalise_cols(df: pd.DataFrame, cols_to_normalise: List[str]):
    """
    This applies normalise values to columns in a dataframe
    """
    df_copy = df.copy()

    # Apply the normalize_list function to the specified columns using .applymap()
    df_copy[cols_to_normalise] = df_copy[cols_to_normalise].map(normalise_values)
    
    return df_copy
