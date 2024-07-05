# Download data from github.
import os
import zipfile
from pathlib import Path
import urllib.request as request
from audio_testing.DataTypes.data_entity import DataConfigBox


class DataDownload:
    def __init__(self, paths:DataConfigBox) -> None:
        self.paths = paths

    def download_data(self):
        # assert os.path.basename(self.curr_dir) == "LSTm_practise", f"The current dir is not right, its in {self.curr_dir}!! Change it to 'LSTm_practise to proceed.'"
        print(f"Fetching data from {self.paths.data_url}......")
        '''
        if not os.path.exists(self.download_path):
            os.makedirs(, exist_ok=True)
            print(f"Making directory {Path(os.getcwd()+chr(92)+)}")'''
            
        filename, headers = request.urlretrieve(
            url=self.paths.data_url, 
            filename=f'{self.paths.download_path}.zip',
        )
        print(f"Downloaded data from GITHUB and stored inside {Path(os.getcwd()+chr(92)+self.paths.download_path)}")
        return filename, headers
        
    def extract_zip_file(self) -> None:
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.paths.download_path
        print(f"Extracting data into {Path(os.getcwd()+chr(92)+unzip_path)}......")
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(f'{self.paths.download_path}.zip', 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        print("Stored data after unzipping!!!")

        '''After unzipping the data, immediately 
        delete the parent zip file to save storage.
        '''

        if os.path.exists(f'{self.paths.download_path}.zip'):
            os.remove(f'{self.paths.download_path}.zip')
            print(f"{f'{self.paths.download_path}.zip'} has been deleted successfully.")
        else:
            print(f"{f'{self.paths.download_path}.zip'} does not exist.")
                