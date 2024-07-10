import yaml
from pathlib import Path
from box import ConfigBox
from ensure import ensure_annotations
from audio_testing.config import config_path, params_path
from audio_testing.DataTypes.data_entity import DataConfigBox, DataReductionInfo, ModelTrainInfo, ModelSaving, OutputPaths

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox type
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            return ConfigBox(content)
    
    except Exception as e:
        raise e
    '''except BoxValueError as e:
        raise ValueError("yaml file is empty") from e'''


class Parameters_Configurations:
    def __init__(self, config_path = config_path, params_path = params_path) -> None:
        '''
        To get the config info from yaml files.
        '''
        self.config_detail = read_yaml(config_path)
        self.param_detail = read_yaml(params_path)


    def data_download_configuration(self) -> DataConfigBox:
        data_paths_config = self.config_detail.data_download

        return DataConfigBox(
            data_url = data_paths_config.data_url,
            download_path = data_paths_config.data_path,
        )
    
    def data_redemption_configuration(self) -> DataReductionInfo:
        data_redem_path = self.config_detail.data_redemption

        return DataReductionInfo(
                data_path = data_redem_path.data_path,
                save_df_at = data_redem_path.save_df_at,
                reduced_df = data_redem_path.save_reduced_data,
                save_df_name = data_redem_path.save_df_name,
                save_format = data_redem_path.save_format,
                org_key = data_redem_path.df_original_key,
                red_key = data_redem_path.df_reduced_key,
                reduction_size = data_redem_path.reduction_size,
        )

    def model_training_configuration(self) -> ModelTrainInfo:
        model_train_params = self.param_detail.model_training

        return ModelTrainInfo(
            batch_size = model_train_params.batch_size,
            epochs = model_train_params.num_epochs,
            device = model_train_params.device,
            train_fraction = model_train_params.train_fraction,
            valid_fraction = model_train_params.valid_fraction,
            test_fraction = model_train_params.test_fraction,
            input_size = model_train_params.input_size,
        )

    def model_saving_configruation(self) -> ModelSaving:
        model_sav = self.config_detail.model_saving

        return ModelSaving(
            save_model = model_sav.save_model,
            save_model_at = model_sav.save_model_at,
            # save_model_with_name = model_train_params.save_model_with_name,
        )

    def output_configurations(self) -> OutputPaths:
        config = self.config_detail.output_file

        return OutputPaths(
            model_path = config.model_path,
            model_file = config.model_file,
            data_path = config.data_path,
            data_file = config.data_file,
            input_size = config.input_size,
        )