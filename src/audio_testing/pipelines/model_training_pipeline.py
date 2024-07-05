from audio_testing.implement.dataloader import DataTransformation
from audio_testing.implement.model_training_implement import ModelTrainEvalPredictSave
from audio_testing.config.all_config import Parameters_Configurations

pipeline_name = "Model Training Pipeline"

class Train_Model():
    """
    Used to create a pipeline for loading the dataloader configuration.
    """
    def __init__(self):
        self.train_data = None
        self.val_data = None
        self.test_data = None
        self.data_configs = Parameters_Configurations().data_redemption_configuration()
        self.params = Parameters_Configurations().model_training_configuration()
        self.save_config = Parameters_Configurations().model_saving_configruation()
    
    def get_data(self) -> None:

        class_obj = DataTransformation(self.data_configs,self.params)

        obj1 = class_obj.MyDataLoader()

        self.train_data = obj1.train_data
        self.val_data = obj1.val_data
        self.test_data = obj1.test_data

    def model_training(self):
        obj2 = ModelTrainEvalPredictSave(self.train_data, self.params, self.save_config)

        obj2.training()



if __name__ == '__main__':
    print(f"{pipeline_name:*^100}")
    obj1 = Train_Model()

    obj1.get_data()
    obj1.model_training()


        