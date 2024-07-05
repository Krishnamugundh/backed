import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from .pytorch_model import MyModel
from audio_testing.DataTypes.data_entity import ModelTrainInfo, ModelSaving

# from .dataloader import DataTransformation


class ModelTrainEvalPredictSave:
    def __init__(self, train_dataloader, params:ModelTrainInfo, configs:ModelSaving):
        self.train_dataloader = train_dataloader
        self.num_epochs = params.epochs
        self.device = params.device
        self.model = MyModel(params.input_size).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.CrossEntropyLoss()
        # self.scheduler = ReduceLROnPlateau(self.optimizer, 'min')
        self.save_model = configs.save_model
        self.save_model_at = configs.save_model_at
        self.save_model_with_name = f"Model_no-{time.strftime('%d-%m-%Y_%H-%M-%S')}.pth"
        self.max_accuracy = 0
    
    def training(self):
        print("Training Started")
        self.model.to(self.device)
        for epoch in range(self.num_epochs):
            running_loss = 0.0
            correct = 0
            total = 0
            for batch in self.train_dataloader:
                inputs, labels = batch['input'].float().to(self.device), batch['label'].float().to(self.device)
                
                # Zero the parameter gradients
                self.optimizer.zero_grad()
                
                # Forward pass
                outputs = self.model(inputs)
                loss = self.criterion(outputs, torch.argmax(labels, dim=1))
                
                # Backward pass and optimize
                loss.backward()
                self.optimizer.step()
                
                # Calculate accuracy
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == torch.argmax(labels, dim=1)).sum().item()
        
                running_loss += loss.item()
        
            epoch_loss = running_loss / len(self.train_dataloader)
            epoch_acc = correct / total
            self.max_accuracy = max(self.max_accuracy,epoch_acc*100)
            print(f'Epoch [{epoch+1}/{self.num_epochs}], Loss: {epoch_loss:.4f}, Accuracy: {100*epoch_acc:.2f}%')
            
            # Step the scheduler
            # self.scheduler.step(epoch_loss)
        
        print("Training completed. Returning Model for future Use.")
        if self.save_model:
            if not os.path.exists(self.save_model_at):
                os.makedirs(self.save_model_at, exist_ok=True)
            
            model_path = os.path.join(self.save_model_at,self.save_model_with_name)
            torch.save(self.model, model_path)
            print(f"Model saved at {model_path}")
        return self.model

    def evaluate(self,*args):
        print("Evaluation Started")
        # If the evaluation has to be done seperately then, It should be passed seperately.
        if args:
            self.eval_dataloader = args[0]

        self.model.to(self.device)
        self.model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for batch in self.eval_dataloader:
                inputs, labels = batch['input'].float().to(self.device), batch['label'].float().to(self.device)
                
                outputs = self.model(inputs)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == torch.argmax(labels, dim=1)).sum().item()

        eval_acc = correct / total
        print(f'Evaluation Accuracy: {100*eval_acc:.2f}%')
        return eval_acc
