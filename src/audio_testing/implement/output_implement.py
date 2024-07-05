import os
import wfdb
import torch
import librosa
import numpy as np
import torch.nn as nn
# from audio_testing.implement.pytorch_model import MyModel

class ProcessInput:
    def __init__(self,root_dir:str,name:str,target_length:int) -> None:
        self.data_path = f"{root_dir}\{name}" if root_dir else name
        self.array = None
        self.target_length = target_length

    def reduce_array_with_average(self) -> np.array:
        factor = len(self.array) // self.target_length
        return np.mean(self.array[:factor * self.target_length].reshape(-1, factor), axis=1)
    
    def read_data(self) -> np.array:
        if self.data_path[-4:] == '.hea':
            """
            Read Header (.hea) file."""
            data = wfdb.rdrecord(self.data_path[:-4])
            print(f"The data {data.comments[0]}")
            self.array = data.p_signal.reshape(-1)
            
        elif self.data_path[-4:] == '.wav':
            """
            Read audio file..."""
            self.array,s = librosa.load(self.data_path) 
        else:
            """
            What if other format are provided."""
            g = -1
            assert g == 2, "Provide a Correct file with either .hea or .wav format.\n HACK: Try adding .wav and .hea at last of ur file." 
        
        return torch.tensor(self.reduce_array_with_average()).float()
        



class Loading_Testing:
    def __init__(self) -> None:
        self.model: nn.Module = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_model(self, name: str) -> nn.Module:
        # Check if the name ends with '.pth', otherwise add it
        model_path = name if name.endswith('.pth') else f'{name}.pth'
        
        # Ensure the file exists
        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model file {model_path} not found.")

        print("Model Loading------->")
        
        # Load the model onto the appropriate device
        self.model = torch.load(model_path, map_location=self.device)
        
        Model_Loaded = "Model Loaded"
        print(f"{Model_Loaded:-^30}")

        return self.model.eval()


"""    def test(self,model:nn.Module,test_dataloader, device='cpu')->float:
        print("Testing Started")
        self.model = model
        self.device = device
        self.model.to(self.device)
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in test_dataloader:
                inputs, labels = batch['input'].float().to(self.device), batch['label'].float().to(self.device)
                
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == torch.argmax(labels, dim=1)).sum().item()
    
        test_acc = correct / total
        print(f'Test Accuracy: {100*test_acc:.2f}%')
        return test_acc"""
    
    
    
"""         print("------------------------------------")
                print("Dictionary Type Model was unable to Load. Load with json type\n To load JSON type, add aurgment 'type=1'")
                print("------------------------------------")
                os.chdir("..")"""
        
''' path1 = os.getcwd()
        assert os.path.basename(path1) == 'LSTm_practise' , "Current directory is not correct"
        path2 = os.getcwd()
        if os.path.basename(path2) == 'LSTm_practise':
            os.chdir("saved_models")'''