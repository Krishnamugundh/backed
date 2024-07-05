import torch
import torch.nn as nn
from pathlib import Path
from torch.utils.data import DataLoader, TensorDataset
from audio_testing.implement.pytorch_model import MyModel 
from audio_testing.DataTypes.data_entity import OutputPaths
from audio_testing.config.all_config import Parameters_Configurations
from audio_testing.implement.output_implement import ProcessInput, Loading_Testing
class Output:
    def __init__(self):
        self.dataset = None
        self.single_dataloader = None
        self.device = None

    def testdata(self, data:torch.tensor, batch_size:int) -> DataLoader:
        """
        to Transform my data into dataset into dataloader.
        """
        self.dataset = TensorDataset(data.repeat(batch_size,1))
        self.single_dataloader = DataLoader(self.dataset, batch_size=batch_size)

    def Predict(self,model_path:Path, data:torch.tensor, batch_size:int, device:str) -> torch.tensor:
        """
        to Predict the output of the data provided using dataloader
        """
        model:nn.Module = MyModel()
        model:nn.Module = Loading_Testing().load_model(model_path)
        self.testdata(data,batch_size) # To get the dataloader
        predicted:torch.tensor = None
        """
        for Testing the model using the input.
        """
        for batch in self.single_dataloader:
            inputs= batch[0].float().to(device)
            
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
        """
        Returning the index of the predicted disease.
        """
        return predicted

class Output_Pipeline:
    def __init__(self):
        configs:OutputPaths = Parameters_Configurations().output_configurations()
        self.model_path = configs.model_path
        self.model_file = configs.model_file
        self.data_path = configs.data_path
        self.data_file = configs.data_file
        self.input_size = configs.input_size
    

    def main(self):
        """
        To get the data from the file.
        """
        obj1 = ProcessInput(self.data_path,self.data_file,self.input_size)
        data = obj1.read_data()
        data = torch.tensor(data)
        """
        To Predict the output of the data provided using dataloader
        """
        model_at = f"{self.model_path}/{self.model_file}"
        predicted = Output().Predict(model_at,data,1,'cpu')
        print(f"Here is the output of the following prediction: {predicted}")
        return predicted

        

if __name__ == "__main__":
    
    s = Output_Pipeline()

    s.main()

