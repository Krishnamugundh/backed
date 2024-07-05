from audio_testing.config.all_config import Parameters_Configurations
from audio_testing.implement.data_reduction_implement import Dimension_Reduction
# from audio_testing.DataTypes import DataReduction


pipeline_name = "Data Reduction Pipeline"

class DataReductionPipeline:

    def Pipeline():
        # print(f"{pipeline_name:*^100}")
        configs = Parameters_Configurations().data_redemption_configuration()

        obj1 = Dimension_Reduction(configs)

        obj1.reduction()
        obj1.display_df()


if __name__ == "__main__":
    print(f'{pipeline_name:*^100}')

    DataReductionPipeline.Pipeline()


