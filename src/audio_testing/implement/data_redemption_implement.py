#Data extraction
import os
import re
import wfdb
import warnings
import numpy as np 
import pandas as pd
# from pathlib import Path
from audio_testing.DataTypes.data_entity import DataReductionInfo




class DataRedemption():
    def __init__(
        self,
        config_detail:DataReductionInfo
    ):
        # #creating new DIrectory
        '''
        l = os.path.basename(os.path.normpath(os.getcwd()))
        if(l == "Final_csv_data"):
            os.chdir("..")'''
            
        #defining Dataframe
        self.df1 = pd.DataFrame()
        
        # Change directory
        '''
        self.home = os.getcwd()
        self.csv_dir = os.path.join(os.getcwd(), "Final_csv_data")
        self.main_data_dir =  os.path.join(os.getcwd(), "voice-icar-federico-ii-database-1.0.0") '''

        # self.curr_home = 
        self.curr_data_dir = config_detail.data_path
        self.save_dir = config_detail.save_df_at
        self.save_name = config_detail.save_df_name
        self.format = config_detail.save_format
        self.df_save_key = config_detail.df_key

        # If dir not exists, create it
        if not os.path.exists(self.save_dir):
            print(f"Creating directory:{os.getcwd()+self.save_dir}")
            os.makedirs(self.save_dir)



    # To identify the diagnoses the patient has undergone.
    def parse_comments(self,comments:str):  # sourcery skip: use-named-expression
        pattern = r'<age>: (\d+)\s+<sex>: (\w+)\s+<diagnoses>: ([^<]+)\s+<medications>: ([^<]+)'
        match = re.search(pattern, comments)
        if match:
            age, sex, diagnoses, medications = match.groups()
            return diagnoses.strip()
        else:
            return None

    #To get the details about the patient.
    def parse_patient_info(self, text) -> dict:
        # Use regex to extract the information
        patient_info = {}

        # Define regex patterns
        patterns = {
            'ID': r'ID\s+(\S+)',
            'Age': r'Age:\s+(\d+)',
            'Gender': r'Gender:\s+(\w+)',
            # 'Diagnosis': r'Diagnosis:\s+(.+)',
            'Occupation status': r'Occupation status:\s+(.+)',
            'VHI Score': r'Voice Handicap Index \(VHI\) Score:\s+(\d+)',
            'RSI Score': r'Reflux Symptom Index \(RSI\) Score:\s+(\d+)',
            'Smoker': r'Smoker:\s+(\w+)',
            'Cigarettes per day': r'Number of cigarettes smoked per day:\s+(\S+)',
            'Alcohol consumption': r'Alcohol consumption:\s+(.+)',
            'Glasses of alcohol per day': r'Number of glasses containing alcoholic beverage drinked in a day\s+(\S+)',
            'Water consumption per day': r'Amount of water\'s litres drink every day:\s+([\d,]+)',
            'Carbonated beverages': r'Carbonated beverages:\s+(.+)',
            'Glasses of carbonated beverages per day': r'Amount of glasses drinked in a day\s+(\S+)',
            'Tomatoes': r'Tomatoes:\s+(\w+)',
            'Coffee': r'Coffee:\s+(.+)',
            'Cups of coffee per day': r'Number of cups of coffee drinked in a day\s+(\d+)',
            'Chocolate': r'Chocolate:\s+(.+)',
            'Gramme of chocolate per day': r'Gramme of chocolate eaten in a day\s+(\S+)',
            'Soft cheese': r'Soft cheese:\s+(.+)',
            'Gramme of soft cheese per day': r'Gramme of soft cheese eaten in a day\s+(\S+)',
            'Citrus fruits': r'Citrus fruits:\s+(.+)',
            'Citrus fruits per day': r'Number of citrus fruits eaten in a day\s+(\S+)',
        }

        # Extract each field using regex and handle missing fields
        for key, pattern in patterns.items():
            if match := re.search(pattern, text):
                patient_info[key] = match[1]
                if key in ['Age', 'VHI Score', 'RSI Score', 'Cups of coffee per day']:
                    patient_info[key] = int(patient_info[key])
            else:
                patient_info[key] = None

        return patient_info

    # ------------------------------------------------------------------- #
    def retreive_data(self) -> pd.DataFrame:
        # os.chdir(self.curr_home)
        # print("curr dir:",os.getcwd())
        try:
            # To get the .text files from dir and stire the audio amplitudes for each sample seperately.
            # List to store records information

            all_patients_info = []

            
            for filename in os.listdir(self.curr_data_dir):
                if filename.endswith('.hea'):
                    record_path = os.path.join(self.curr_data_dir, filename.replace('.hea',''))
                    
                    # Read the record
                    record = wfdb.rdrecord(record_path)
                    
                    # diagnoses of Patient
                    diagnose = self.parse_comments(record.comments[0])
                    
                    # Converts the signals into a single array for processing
                    signal_array = record.p_signal.reshape(-1)

                    # Extracting the corresponding patient's other details from txt file.
                    # Construct the full path to the file
                    
                    file_path = os.path.join(self.curr_data_dir, filename.replace('.hea','-info.txt'))
                    
                    # Read the text file
                    with open(file_path, 'r') as file:
                        text_content = file.read()
                    

                    # Parse the text content
                    patient_info = self.parse_patient_info(text_content)

                    #adding the signal details to the 
                    patient_info['Signal'] = np.array(signal_array)
                    patient_info['diagnoses'] = diagnose
                    
                    
                    # Append the parsed information to the list
                    all_patients_info.append(patient_info)
                
                    
            # print("All data has been Successfully loaded into All_records")
            self.df1 = pd.DataFrame(all_patients_info)
            # print("Data has been stored into a dataframe and returned to the variable assigned")
        except Exception as F:
            print(f"<--------------Something is wrong - msg:{F}--------------------->")

        with warnings.catch_warnings(action="ignore"):
            self.df1['Alcohol consumption'][self.df1['Alcohol consumption']=='habitual drinker '] = "habitual drinker"
            self.df1['diagnoses'][self.df1['diagnoses']=='hyperkineti dysphonia'] = "hyperkinetic dysphonia"
        return self.df1
        
        # --------------------------------------------------------------- #
    
    def store_dataframe(self):
        # Defining the dataframe path.
        self.save_name += f".{self.format}"
            
        saving_dir = os.path.join(self.save_dir + self.save_name)
        
        # If dir not exists, create it
        if not os.path.exists(self.save_dir):
            print(f"Creating directory:{os.getcwd()+self.save_dir}")
            os.makedirs(self.save_dir)
        
        # Save DataFrame
        self.df1.to_hdf(saving_dir,key=self.df_save_key, mode='w')

        print(f"saved the data from All_records as {self.format} : {self.save_name}")
        