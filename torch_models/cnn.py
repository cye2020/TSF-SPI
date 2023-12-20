import torch
import torch.nn as nn
import torch.nn.functional as F

class CNN(nn.Module):
    def __init__(self, conv_layers, fc_layers):
        super(CNN, self).__init__()

        self.convs = nn.ModuleList()
        self.pools = nn.ModuleList()
        self.activations = nn.ModuleList()
        for conv_layer in conv_layers:
            self.convs.append(nn.Conv1d(conv_layer['input_channels'], conv_layer['output_channels'], conv_layer['kernel_size']))
            self.pools.append(nn.MaxPool1d(conv_layer['pool_size']))
            self.activations.append(nn.ReLU() if conv_layer['activation'] == 'relu' else nn.Linear())

        self.flatten = nn.Flatten()
        
        self.fcs = nn.ModuleList()
        self.dropouts = nn.ModuleList()
        self.fc_activations = nn.ModuleList()
        for fc_layer in fc_layers:
            self.fcs.append(nn.Linear(fc_layer['input_size'], fc_layer['output_size']))
            self.dropouts.append(nn.Dropout(fc_layer['dropout_rate']))
            self.fc_activations.append(nn.ReLU() if fc_layer['activation'] == 'relu' else nn.Linear())

        self.out = nn.Linear(fc_layers[-1]['output_size'], 1)

    def forward(self, x):
        for conv, pool, activation in zip(self.convs, self.pools, self.activations):
            x = activation(conv(x))
            x = pool(x)

        x = self.flatten(x)

        for fc, dropout, activation in zip(self.fcs, self.dropouts, self.fc_activations):
            x = activation(fc(x))
            x = dropout(x)

        x = self.out(x)
        return x


conv_layers = [
    {'input_channels': 7, 'output_channels': 64, 'kernel_size': 2, 'pool_size': 2, 'activation': 'relu'}
]

fc_layers = [
    {'input_size': None, 'output_size': 100, 'activation': 'relu', 'dropout_rate': 0.25},
    {'input_size': 100, 'output_size': 30, 'activation': 'linear'}
]


model = CNN(conv_layers, fc_layers)


