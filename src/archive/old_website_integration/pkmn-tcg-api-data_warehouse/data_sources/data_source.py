import os
import urllib.request
import zipfile
from pathlib import Path


class DataSource:
    source_url = ""
    source_code_location = os.path.dirname(os.path.realpath(__file__))
    local_cache_name = ""
    local_cache_directory = ""
    local_download_location = ""
    local_cache_age = ""
    force_download = ""
    raw_data = {}
    data = {}

    def __init__(self, force_download=False):
        self.local_cache_parent_dir = os.path.join(self.source_code_location, "data_source_cache", self.local_cache_name)
        self.local_download_dir = os.path.join(self.local_cache_parent_dir, "download")
        self.local_cache_data_dir = os.path.join(self.local_cache_parent_dir, "data")
        self.local_download_location = os.path.join(self.local_download_dir, self.local_cache_name + ".zip")

        self.force_download = force_download

        Path(self.local_cache_parent_dir).mkdir(parents=True, exist_ok=True)
        Path(self.local_cache_data_dir).mkdir(parents=True, exist_ok=True)
        Path(self.local_download_dir).mkdir(parents=True, exist_ok=True)

        self.download_fresh_data()
        self.extract_data()
        self.load_data()

    def download_fresh_data(self):
        # Download fresh data
        if not Path(self.local_download_location).is_file() or (
                Path(self.local_download_location).is_file() and self.force_download):
            print(f"Downloading data for {self.local_cache_name}")
            Path(self.local_cache_directory).mkdir(parents=True, exist_ok=True)
            with urllib.request.urlopen(self.source_url) as downloaded_data:
                with open(self.local_download_location, 'wb') as output:
                    output.write(downloaded_data.read())
        else:
            print(f"Skipping data download for {self.local_cache_name}")

    def extract_data(self):
        if Path(self.local_download_location).suffix == ".zip":
            # If source directory empty
            if not os.listdir(self.local_cache_data_dir):
                with zipfile.ZipFile(self.local_download_location, 'r') as zip_ref:
                    zip_ref.extractall(self.local_cache_data_dir)

    def load_data(self):
        pass