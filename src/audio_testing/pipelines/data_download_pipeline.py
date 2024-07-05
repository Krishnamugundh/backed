from audio_testing.config.all_config import Parameters_Configurations
from audio_testing.implement.data_download_implement import DataDownload

pipeline_name = "Data Download Pipeline"

class DataDownloadPipeline:
    def pipeflow() -> None:
        # print(f'{pipeline_name:*^100}')
        data_config = Parameters_Configurations().data_download_configuration()

        datum = DataDownload(data_config)

        datum.download_data()
        datum.extract_zip_file()    
    


if __name__ == "__main__":
    print(f'{pipeline_name:*^100}')
    
    d_002 = DataDownloadPipeline.pipeflow()
    # data_config = Parameters_Configurations().data_download_configuration()

    # datum = DataDownload(data_config)

    # datum.download_data()
    # datum.extract_zip_file()