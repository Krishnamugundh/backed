# Class definition for dimension reduction
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.signal import resample
from ensure import ensure_annotations
from audio_testing.DataTypes.data_entity import DataReductionInfo




class Dimension_Reduction():
    def __init__(self, configs:DataReductionInfo ):
        self.data_saved_at = f"{configs.save_df_at + configs.save_df_name + '.' +configs.save_format}"
        self.reduced_df_dir = configs.reduced_df
        self.org_key = configs.org_key
        self.red_key = configs.red_key
        self.save_reduced_data = f"{self.reduced_df_dir + configs.save_df_name + '.' +configs.save_format}"
        self.df:pd.DataFrame = pd.read_hdf(Path(self.data_saved_at),self.org_key)
        self.target_length = configs.reduction_size
        
    def __str__(self) -> str:
        return (
            f"This function adds a extra column to the dataframe that contains the reduced input size to {self.target_length}\n"
            + "Also If any other information are needed about data, Follow these instruction & add necessary arguments into utility function \n--------------------------------'object.util(*args)' --------------------------------\n"
            + "1.) For diff lengths of Signal Present in the data include: 'signal_lengths:bool = True'\n"
            + "2.) For diff types of diseases in the data, include: 'diff_diseases:bool = True'\n"
            + "3.) For displaying the Graphical display of the original Signal from the Reduced Signal: 'graph_display:bool = True' & the data U need 'data_point_graph:int'"
        )

    @ensure_annotations
    def util(self,signal_lengths:bool=False, diff_diseases:bool = False, graph_display:bool = False, data_point_graph:int = None)->None:
        if graph_display and data_point_graph:
            print(f"You need to enter the datapoint to display the graph using 'data_point_graph:int= [0,{len(self.df['Signal'])}]'")
        try:
            if signal_lengths:
                print("Different lengths of Signal Present")
                different_sets = self.df['Signal'].apply(lambda x:len(x))
                print(f"There are {len(set(different_sets))} diff lengths in dataset")
                print(set(different_sets),"\n-------------------------")
            if diff_diseases:
                print("Different types of diseases in the data",self.df['diagnoses'].value_counts().sort_index(),"\n-------------------------")
            if graph_display:
                print("Graphs:")
                original_array = self.df.loc[self.data_point_graph, 'Signal']
                reduced_array = self.df.loc[self.data_point_graph, 'Reduced_Signal']
                plt.figure(figsize=(12, 6))
                plt.plot(original_array, label='Original Array (Length: 30880)', alpha=0.7)
                plt.plot(np.linspace(0, len(original_array), len(reduced_array)), reduced_array, label='Reduced Array (Length: 5000)', alpha=0.7)
                plt.legend()
                plt.xlabel('Index')
                plt.ylabel('Value')
                plt.title('Original and Reduced Arrays')
                plt.show()
                print("\n-------------------------")
        except Exception as E:
            print(f"You encounter an error\n-------------------- \n{E}\n --------------------")
    
    # Define the function to reduce array length using resample from signal
    @ensure_annotations
    def reduce_array_with_resample(self, array: np.array)->np.array:
        return resample(array, self.target_length)
    
    # Define the function to reduce array length using linear interpolation
    @ensure_annotations
    def reduce_array_with_interpolation(self, array: np.array)->np.array:
        original_indices = np.linspace(0, len(array) - 1, num=len(array))
        target_indices = np.linspace(0, len(array) - 1, num=self.target_length)
        reduced_array = np.interp(target_indices, original_indices, array)
        return reduced_array
        
    # Define the function to reduce array length by averaging chunks
    def reduce_array_with_average(self, array: np.array)->np.array:
        # print(type(array), type(self.target_length))
        factor = len(array) // self.target_length
        reduced_array = np.mean(array[:factor * self.target_length].reshape(-1, factor), axis=1)
        return reduced_array

    def display_df(self):
        print(self.df.sample(5))

    def reduction(self):
        # Apply the reduction function to the 'Signal' column
        self.df['Reduced_Signal'] = self.df['Signal'].apply(lambda x: self.reduce_array_with_average(x))

        if not os.path.exists(self.reduced_df_dir):
            os.makedirs(self.reduced_df_dir)
            print(f"{self.reduced_df_dir} doesn't not exist. Thus creating it.")
        
        self.df.to_hdf(self.save_reduced_data, key=self.red_key, mode='w')
        # os.subprocess(['python'])
        print(f"The Reduced_Signal has been created and saved to {self.save_reduced_data}")

        print("Pushing my data into dvc")
        os.chdir("artifacts/reduced_data/")
        os.system("dvc push -v --remote all_artifacts final_data_001.h5.dvc")
        print("Completed pushing")
