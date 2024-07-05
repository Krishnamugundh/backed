import os.path
import random
import numpy as np
import pandas as pd
from box import ConfigBox
from ensure import ensure_annotations
from sklearn.preprocessing import OneHotEncoder
from torch.utils.data import Dataset, DataLoader
from audio_testing.DataTypes.data_entity import DataReductionInfo, ModelTrainInfo



class MyDataset(Dataset):
    def __init__(self, df: pd.DataFrame, outputs: np.array = None, transform=None):
        self.transform = transform
        self.data = df['Reduced_Signal'].values
        self.labels = outputs  # Call the method from DataTransformation
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sample = {'input': self.data[idx], 'label': self.labels[idx]}
        if self.transform:
            sample = self.transform(sample)
        return sample


class DataTransformation:
    def __init__(self, configs:DataReductionInfo, params:ModelTrainInfo ):
        self.df_loc = os.path.join(configs.reduced_df,f"{configs.save_df_name}.{configs.save_format}")
        self.df:pd.DataFrame = pd.read_hdf(self.df_loc,configs.df_key)
        self.train_df = None
        self.val_df = None
        self.test_df = None
        self.ges = 0
        self.batch_size = params.batch_size
        self.train_frac = params.train_fraction
        self.valid_frac = params.valid_fraction
        self.test_frac = params.test_fraction

    def encode_diagnoses(self, df: pd.DataFrame):
        self.ges += 1
        encoder = OneHotEncoder()
        diagnoses_encoded = encoder.fit_transform(df[['diagnoses']]).toarray()
        assert self.ges <=3, "SELFMADE ERROR: The DataTransformation has been called more than once. Recall it again!!!"
        if self.ges == 1:
            print("Training Categories:")
        elif self.ges == 2:
            print("Validation Categories:")
        elif self.ges ==3:
            print("Testing Categories:")
        print("                 ",encoder.categories_[0])
        return diagnoses_encoded

    @ensure_annotations
    def MyDataLoader(self, shuffle=True) -> ConfigBox:
        assert self.train_frac + self.valid_frac + self.test_frac == 1.0, "Fractions must sum to 1."
    
        # Shuffle the indices
        indices = list(self.df.index)
        if shuffle:
            random.shuffle(indices)
        
        # Calculate the number of samples for each set
        total_samples = len(self.df)
        train_end = int(self.train_frac * total_samples)
        valid_end = train_end + int(self.valid_frac * total_samples)
    
        # Split the indices
        print("Splitting the dataframe......")
        train_indices = indices[:train_end]
        valid_indices = indices[train_end:valid_end]
        test_indices = indices[valid_end:]
    
        # Create the split dataframes
        self.train_df = self.df.loc[train_indices]
        self.val_df = self.df.loc[valid_indices]
        self.test_df = self.df.loc[test_indices]
        print("Size of:\nTraining data: ", self.train_df.shape, " \nTesting data: ", self.test_df.shape, "\nValidation data: ", self.val_df.shape)

        # Defining the datasets.
        print("Converting them into DATASETS.......")
        train_dataset = MyDataset(self.train_df, self.encode_diagnoses(self.train_df))
        val_dataset = MyDataset(self.val_df, self.encode_diagnoses(self.val_df))
        test_dataset = MyDataset(self.test_df, self.encode_diagnoses(self.test_df))

        # Converting them into dataloader
        print(f"Converting them into DATALOADER......, with parameters batch_size: {self.batch_size}")
        train_dataloader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=shuffle)
        val_dataloader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=shuffle)
        test_dataloader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=shuffle)

        return ConfigBox({"train_data":train_dataloader, "val_data":val_dataloader, "test_data":test_dataloader})