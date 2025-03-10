import torch
import torch.nn as nn
import torch.nn.functional as f


class GCA(nn.Module):
    SOBEL_X = torch.tensor([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=torch.float32)
    SOBEL_Y = SOBEL_X.T
    IDENTITY = torch.tensor([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=torch.float32)
    GRID_SIZE = 32

    def __init__(self, n_channels=16, hidden_channels=128, input_channels = 3):
        ## Hidden channels are the number of channels in the linear layer in network
        ## Hidden channels are the number of channels in the linear layer in network
        super().__init__()
        self.input_channels = input_channels
        self.n_channels = n_channels

        ## Represent the update step as a submodule
        ## Represent the update step as a submodule
        self.update_network = (
            nn.Sequential(  # pytorch Conv2d layers automatically parallelize
                nn.Conv2d(3 * n_channels, hidden_channels, kernel_size=1),
                nn.ReLU(),
                nn.Conv2d(hidden_channels, n_channels-input_channels, kernel_size=1, bias=False),
                nn.Dropout(0.5)
            )
        )

        ## Initialise model parameters as much smaller numbers
        torch.nn.init.normal_(self.update_network[0].weight, mean=0.0, std=0.0001)
        torch.nn.init.normal_(self.update_network[0].bias, mean=0.0, std=0.0001)
        torch.nn.init.normal_(self.update_network[2].weight, mean=0.0, std=0.0001)
        ## Initialise model parameters as much smaller numbers
        torch.nn.init.normal_(self.update_network[0].weight, mean=0.0, std=0.0001)
        torch.nn.init.normal_(self.update_network[0].bias, mean=0.0, std=0.0001)
        torch.nn.init.normal_(self.update_network[2].weight, mean=0.0, std=0.0001)

    def to(self, device):
        """
        Overrides parent nn.Module to method for sending resources to GPU
        Move the model and constant tensors to the device (GPU)"""
        """
        Overrides parent nn.Module to method for sending resources to GPU
        Move the model and constant tensors to the device (GPU)"""
        self.SOBEL_X = self.SOBEL_X.to(device)
        self.SOBEL_Y = self.SOBEL_Y.to(device)
        self.IDENTITY = self.IDENTITY.to(device)
        return super().to(device)

    def forward(self, input_grid, pad = True):
        """
        Input_grid is tensor with dims: (batch, in_channels, height, width)
        1. Construct `perception_grid` by replacing each cell in input_grid with its feature vector
        2. Apply update to each `perception_vector` in `perception_grid` to obtain `ds_grid`, the grid of changes
        3. Apply stochastic update mask to `ds_grid` to filter out some changes
        Input_grid is tensor with dims: (batch, in_channels, height, width)
        1. Construct `perception_grid` by replacing each cell in input_grid with its feature vector
        2. Apply update to each `perception_vector` in `perception_grid` to obtain `ds_grid`, the grid of changes
        3. Apply stochastic update mask to `ds_grid` to filter out some changes
        4. Obtain next state of grid from `ds_grid` + `state_grid`
        5. Apply alive cell masking to `state_grid` to kill of cells with alpha < 0.1
        This yields output_filtered_grid, a tensor with dims: (batch, in_channels, height, width)
        5. Apply alive cell masking to `state_grid` to kill of cells with alpha < 0.1
        This yields output_filtered_grid, a tensor with dims: (batch, in_channels, height, width)
        """

        ## Add input grid to the device model parameters are on
        x = input_grid.to(next(self.parameters()).device)
        x = self.calculate_perception_grid(x, pad = pad)
        output_grid = x[:, :self.n_channels]

        x = self.calculate_ds_grid(x)
        output_grid[:, 3:] = output_grid[:, 3:] + x

        return output_grid
    

    def calculate_perception_grid(self, state_grid, pad = True):
        """
        Calculates 1x48 perception vector for each cell in grid, returns as grid of perception vectors.
        Perception vectors are 4 dimensional. Unsqueeze used to add dimension of size 1 at index
        """
        if (pad):
            state_grid_processed = f.pad(state_grid, (1, 1, 1, 1), mode="circular")
        else: 
            state_grid_processed = state_grid
            state_grid = state_grid[:,:, 1:-1, 1:-1]


        grad_x = f.conv2d(
            state_grid_processed,
            self.SOBEL_X.unsqueeze(0).repeat(state_grid.size(1), 1, 1, 1),
            stride=1,
            padding=0,
            groups=state_grid_processed.size(1),
        )  
        grad_y = f.conv2d(
            state_grid_processed,
            self.SOBEL_Y.unsqueeze(0).repeat(state_grid.size(1), 1, 1, 1),
            stride=1,
            padding=0,
            groups=state_grid_processed.size(1),
        )  
        perception_grid = torch.cat([state_grid, grad_x, grad_y], dim=1)

        return perception_grid

    def calculate_ds_grid(self, perception_grid):
        """Updates each perception vector in perception grid, return
        We can apply the submodule network like a function"""
        return self.update_network(perception_grid)
