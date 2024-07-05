import pandas as pd
from audio_testing.config.all_config import Parameters_Configurations
from audio_testing.implement.data_redemption_implement import DataRedemption

pipeline_name = "Data Redemption Pipeline"

class DataRedemptionPipeline():
    def data_in_dataframe()->pd.DataFrame:
        # print(f"{pipeline_name:*^100}")

        configs = Parameters_Configurations().data_redemption_configuration()

        object1 =  DataRedemption(configs)

        dataframe = object1.retreive_data()
        object1.store_dataframe()

        return dataframe




if __name__ == '__main__':
    print(f"{pipeline_name:*^100}")

    x: pd.DataFrame = DataRedemptionPipeline.data_in_dataframe()
