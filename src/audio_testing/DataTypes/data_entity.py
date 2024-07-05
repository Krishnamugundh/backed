from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataConfigBox:
    """
    This class is used to store the configuration of the data used.
    """
    data_url:Path
    download_path:Path

@dataclass
class DataReductionInfo:
    """
    This class is used to store the configuration of transformation of the data.
    """
    data_path:Path
    save_df_at:Path
    reduced_df:Path
    save_df_name:str
    save_format: str
    reduction_size:int
    df_key:str

@dataclass
class ModelTrainInfo:
    """
    This class is used to store the configuration of model training.
    """
    device:str
    epochs:int
    batch_size:int
    train_fraction:int
    valid_fraction:int
    test_fraction:int
    input_size:int


@dataclass
class ModelSaving:
    """
    This class is used to store config of where to save the model.
    """
    save_model:bool
    save_model_at:str
    # save_model_name:str

@dataclass
class OutputPaths:
    model_path:Path
    model_file:str
    data_path:Path
    data_file:str
    input_size:int