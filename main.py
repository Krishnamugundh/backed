from audio_testing.pipelines.data_download_pipeline import DataDownloadPipeline
from audio_testing.pipelines.data_redemption_pipeline import DataRedemptionPipeline
from audio_testing.pipelines.data_reduction_pipeline import DataReductionPipeline
from audio_testing.pipelines.model_training_pipeline import Train_Model
from audio_testing.pipelines.output_pipeline import Output_Pipeline


if __name__ == "__main__":

    pipeline_name_01 = "Data Download Pipeline"
    try:
        print(f'{pipeline_name_01:*^100}')
        """
        Downloading data from the specified GUTHUB repo.
        """
        DataDownloadPipeline.pipeflow()
    except Exception as e:
        print(e)

# "********************************************************************************"

    pipeline_name_02 = "Data Redemption Pipeline"
    try:
        print(f"{pipeline_name_02:*^100}")
        """
        Saving the dataframe for future reference
        """

        Total_training_data = DataRedemptionPipeline.data_in_dataframe()

    except Exception as e:
        print(e)   

# "************************************************************************************************"

    pipeline_name_03 = "Data Reduction Pipeline"
    try:
        print(f"{pipeline_name_03:*^100}")
        """
        It is used to reduce the size of the dimensions of training data.
        """
        DataReductionPipeline.Pipeline()
    except Exception as e:
        print(e)

# "************************************************************************************************"

    pipeline_name_04 = "Model Training Pipeline"
    try:
        print(f"{pipeline_name_04:*^100}")
        Train_001 = Train_Model()
        """
        It is used to get the DATALOADER.
        """
        Train_001.get_data()
        """
        It is used to train the model.
        """
        Train_001.model_training()
    except Exception as e:
        print(e)

# "************************************************************************************************"

    pipeline_name_05 = "Output Pipeline"
    try:
        print(f"{pipeline_name_05:*^100}") 
        get_out = Output_Pipeline()

        get_out.main()
    except Exception as e:
        print(e)
 
# "************************************************************************************************"