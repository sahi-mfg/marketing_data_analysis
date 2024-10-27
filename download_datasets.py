import os
from kaggle.api.kaggle_api_extended import KaggleApi  # type: ignore
import zipfile
import logging

logging.basicConfig(level=logging.INFO)

# Set your Kaggle username and API key
os.environ["KAGGLE_USERNAME"] = "mohamedfrancissahi"
os.environ["KAGGLE_KEY"] = "944e278fb6fefbc196054c66ff1ec988"


api = KaggleApi()
api.authenticate()

# Download the dataset
logging.info("Downloading the dataset")
api.dataset_download_files("rodsaldanha/arketing-campaign/", path=".")

# Unzip the dataset
logging.info("Unzipping the dataset")
zipfile.ZipFile("arketing-campaign.zip", "r").extractall("data")

# Remove the zip file
logging.info("Removing the zip file")
os.remove("arketing-campaign.zip")
