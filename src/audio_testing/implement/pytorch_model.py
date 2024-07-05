import torch
import torch.nn as nn


class MyModel(nn.Module):
    def __init__(self, input_size=15000, hidden_size=64, num_classes=6):
        super(MyModel, self).__init__()
        
        # Convolutional layer
        self.conv1 = nn.Conv1d(1, 16, kernel_size=5, stride=2, padding=2)
        
        # Linear layer to reduce input size
        self.linear1 = nn.Linear(16 * (input_size // 2), hidden_size)
        
        # LSTM layer
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        
        # Linear layer1
        self.linear2 = nn.Linear(hidden_size, hidden_size)
        
        # Output layer (softmax)
        self.output_layer = nn.Linear(hidden_size, num_classes)
        
        # Activation functions
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        # Reshape input for convolution
        x = x.float()
        x = x.view(x.size(0), 1, -1)
        
        # Convolutional layer
        x = self.conv1(x)
        x = self.relu(x)
        
        # Flatten for linear layer
        x = x.view(x.size(0), -1)
        
        # Linear layer to reduce input size
        x = self.linear1(x)
        x = self.relu(x)
        return x
        
        # LSTM layer
        h_0 = torch.zeros(1, x.size(0), self.lstm.hidden_size).to(x.device)
        c_0 = torch.zeros(1, x.size(0), self.lstm.hidden_size).to(x.device)
        x, _ = self.lstm(x.unsqueeze(1), (h_0, c_0))  # LSTM expects input of shape (batch_size, seq_len, input_size)
        
        # Linear layer
        x = self.linear2(x.squeeze(1))
        x = self.relu(x)
        
        # Output layer
        x = self.output_layer(x)
        x = self.softmax(x)
        