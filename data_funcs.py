import os
import yaml
import zipfile
import requests

def download_zip_from_url(url, file_path):
    """
    This function downloads a zip file from a url and places into file_path
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


def extract_zip(zip_file_path, extract_location):
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


def download_data(url, folder, file, extract_location):
    """
    This function checks if the data has already been downloaded and if not, downloads and extracts it
    """
    if os.path.exists(os.path.join("data", "inputs", file)):
        print(f"{file} is already downloaded in the subdirectoy 'data'")
    elif os.path.exists(folder):
        print(f"Extracting data from {folder}...")
        extract_zip(folder, extract_location)
    else:
        print(f"Downloading and extracting data from {url}...")
        download_zip_from_url(url, folder)
        extract_zip(folder, extract_location)


def check_inputs(folder, file):
    """
    Checks whether appropriate files are downloaded
    """
    # if path to wildfire shp does not exist, source download script
    # else do nothing
    file_path = os.path.join(folder, file)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'The file path "{file_path}" does not exist. Please run data_download.py to download required data')
    

def load_data_catalogue():
    """
    Loads data catalogue
    """
    # Load the YAML data from the file
    with open('data_catalogue.yml', 'r') as file:
        data_catalogue = yaml.safe_load(file)
    return data_catalogue


def count_nas(df):
    """
    Counts the number of missing values (NAs) in each column of a dataframe object
    """
    return df.isna().sum()


def filter_df(df, column, values):
    orig = len(df)
    new_df = df[df[column].isin(values)]

    new = len(new_df)
    diff = orig - new
    print(f"Filtering {column} for values in {values} has dropped {diff} rows from the dataframe")

    return new_df


def extract_state(df):
    """
    Creates a state column by extracting the leading 2 letter state code from the Event_ID
    """
    df['state'] = df.Event_ID.str[:1]
    return df


def calc_area(gpd_df):
    """
    Creates an area column on a geopandas dataframe holding the area of each polygon
    """
    gpd_df['area'] = gpd_df['geometry'].area
    return gpd_df
