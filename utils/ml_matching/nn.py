import torch
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
import pandas as pd

x = {
    "Eggplant": [0.301, 0.133, 0.306],
    "Sand": [0.957, 0.855, 0.710],
    "Mushroom": [0.486, 0.396, 0.333],
    "Mineral green": [0.251, 0.404, 0.325],
    "Deep burgundy": [0.376, 0.000, 0.125],
    "Carbon": [0.129, 0.129, 0.129],
    "Electric blue": [0.047, 0.427, 0.776],
    "Dijon": [0.784, 0.549, 0.259],
    "Olive oil": [0.745, 0.733, 0.541],
    "Cactus": [0.220, 0.435, 0.345],
    "Ivory": [1.000, 1.000, 0.941],
    "Sagebrush": [0.580, 0.616, 0.471],
    "Sunflower": [1.000, 0.855, 0.208],
    "Burnt sienna": [0.682, 0.306, 0.000],
    "Cadet": [0.325, 0.408, 0.447],
    "Seafoam": [0.498, 1.000, 0.831],
    "Stone": [0.584, 0.565, 0.545],
    "Mink": [0.514, 0.400, 0.388],
    "Eggshell": [0.941, 0.914, 0.827],
    "Olive grove": [0.478, 0.502, 0.286],
    "Pale lavender": [0.867, 0.816, 0.914],
    "Rustic brown": [0.521, 0.247, 0.149],
    "Coral": [1.0, 0.5, 0.31],
    "Navy": [0.0, 0.0, 0.5],
    "Emerald": [0.31, 0.78, 0.47],
    "Wine": [0.5, 0.0, 0.13],
    "Forest": [0.13, 0.55, 0.13],
    "Teal": [0.0, 0.5, 0.5],
    "Navy blue": [0.0, 0.0, 0.5],
    "Olive green": [0.33, 0.42, 0.18],
    "Rust": [0.8, 0.25, 0.15],
    "Eggplant": [0.38, 0.25, 0.32],
    "Forest green": [0.13, 0.55, 0.13],
    "Lavender": [0.9, 0.9, 0.98],
    "Beige": [0.96, 0.96, 0.86],
    "Sky blue": [0.53, 0.81, 0.92],
    "Charcoal gray": [0.21, 0.27, 0.31],
    "Taupe": [0.28, 0.24, 0.2],
    "Burgundy": [0.5, 0.0, 0.13],
    "Sand": [0.76, 0.7, 0.5],
    "Denim blue": [0.08, 0.38, 0.74],
    "Camel": [0.76, 0.6, 0.42],
    "Sage green": [0.44, 0.56, 0.44],
    "Mustard yellow": [1.0, 0.86, 0.35],
    "Cobalt blue": [0.0, 0.28, 0.67],
    "Tan": [0.82, 0.71, 0.55],
    "Dusty rose": [0.52, 0.39, 0.39],
    "Marigold": [0.99, 0.69, 0.19],
    "Mauve": [0.88, 0.69, 0.77],
    "Teal": [0.0, 0.5, 0.5],
    "Blush pink": [0.98, 0.52, 0.52],
    "Coral": [1.0, 0.5, 0.31],
    "Cobalt blue": [0.0, 0.28, 0.67],
    "Forest green": [0.13, 0.55, 0.13],
    "Lavender": [0.9, 0.9, 0.98],
    "Beige": [0.96, 0.96, 0.86],
    "Sky blue": [0.53, 0.81, 0.92],
    "Rust": [0.6627, 0.6353, 0.6431],
    "Moss": [0.3059, 0.1647, 0.3098],
    "Olive": [0.4667, 0.5098, 0.3176],
    "Sage": [0.5333, 0.5647, 0.4039],
    "Sand": [0.8980, 0.8392, 0.7412],
    "Camel": [0.7765, 0.6078, 0.4314],
    "Beige": [0.9569, 0.9255, 0.8392],
    "Cream": [1.0000, 0.9804, 0.9608],
    "Ivory": [1.0000, 1.0000, 0.9412],
    "Gold": [1.0000, 0.8431, 0.0000],
    "Bronze": [0.8039, 0.4980, 0.1961],
    "Champagne": [0.9686, 0.8941, 0.7725],
    "Pewter": [0.5569, 0.5569, 0.5569],
    "Silver": [0.7529, 0.7529, 0.7529],
    "Slate": [0.4392, 0.5019, 0.5647],
    "Charcoal": [0.2118, 0.2118, 0.2118],
    "Black": [0.0000, 0.0000, 0.0000],
    "White": [1.0000, 1.0000, 1.0000],
    "Blush": [0.8706, 0.6784, 0.6784],
    "Mauve": [0.7020, 0.5176, 0.5843],
    "Dusty Rose": [0.7137, 0.5216, 0.5451],
    "Taupe": [0.5686, 0.4627, 0.3804],
    "Mustard": [0.7451, 0.6510, 0.1490],
    "Maroon": [0.5020, 0.0000, 0.0000],
    "Lavender": [0.7059, 0.4902, 0.8627],
    "Plum": [0.5569, 0.2706, 0.5216],
    "Fuchsia": [1.0000, 0.0000, 1.0000],
    "Magenta": [1.0000, 0.0000, 1.0000],
    "Lilac": [0.7843, 0.6353, 0.7843],
    "Orchid": [0.8549, 0.4392, 0.8392],
    "Sky Blue": [0.5294, 0.8078, 0.9216],
    "Teal": [0.0000, 0.5020, 0.5020],
    "Forest Green": [0.133, 0.545, 0.133],}

y = {
    "Taupe": [0.282, 0.235, 0.196],
    "Burgundy": [0.502, 0, 0.125],
    "Mauve": [0.878, 0.69, 1],
    "Mustard": [1, 0.859, 0.345],
    "Blush": [0.871, 0.365, 0.514],
    "Dusty Rose": [0.71, 0.475, 0.475],
    "Maroon": [0.502, 0, 0],
    "Lavender": [0.902, 0.902, 0.98],
    "Plum": [0.867, 0.627, 0.867],
    "Fuchsia": [1, 0, 1],
    "Magenta": [1, 0, 0.502],
    "Lilac": [0.859, 0.678, 0.902],
    "Orchid": [0.855, 0.439, 0.839],
    "Sky Blue": [0.529, 0.808, 0.922],
    "Teal": [0, 0.502, 0.502],
    "Turquoise": [0.251, 0.878, 0.816],
    "Coral": [1, 0.498, 0.314],
    "Navy": [0, 0, 0.502],
    "Emerald": [0.125, 0.698, 0.408],
    "Wine": [0.502, 0, 0.251],
    "Forest Green": [0.133, 0.545, 0.133],
    "Sage": [0.502, 0.502, 0],
    "Olive": [0.502, 0.502, 0],
    "Champagne": [0.969, 0.906, 0.808],
    "Rust": [0.718, 0.255, 0.055],
    "Copper": [0.722, 0.451, 0.2],
    "Camel": [0.757, 0.604, 0.42],
    "Sand": [0.957, 0.643, 0.376],
    "Beige": [0.961, 0.961, 0.863],
    "Slate": [0.439, 0.502, 0.565],
    "Ivory": [1, 1, 0.941],
    "Cream": [1, 0.992, 0.816],
    "Gold": [1, 0.843, 0],
    "Bronze": [0.804, 0.498, 0.196],
    "Pewter": [0.467, 0.533, 0.6],
    "Silver": [0.753, 0.753, 0.753],
    "Charcoal": [0.212, 0.271, 0.31],
    "Black": [0, 0, 0],
    "White": [1, 1, 1],
    'Charcoal': (0.21, 0.27, 0.31),
    'Navy': (0.00, 0.00, 0.50),
    'Blush': (1.00, 0.75, 0.80),
    'Taupe': (0.28, 0.24, 0.20),
    'Dusty Rose': (0.71, 0.53, 0.56),
    'Mauve': (0.88, 0.69, 0.73),
    'Burgundy': (0.50, 0.00, 0.13),
    'Olive': (0.50, 0.50, 0.00),
    'Mustard': (1.00, 0.86, 0.35),
    'Sage': (0.44, 0.51, 0.38),
    'Beige': (0.96, 0.96, 0.86),
    'Ivory': (1.00, 1.00, 0.94),
    'Cream': (1.00, 0.99, 0.82),
    'Gold': (1.00, 0.84, 0.00),
    'Champagne': (0.97, 0.91, 0.81),
    'Camel': (0.76, 0.60, 0.42),
    'Rose': (1.00, 0.00, 0.50),
    'Dusty Pink': (0.69, 0.53, 0.53),
    'Terracotta': (0.80, 0.34, 0.28),
    'Rust': (0.80, 0.30, 0.18),
    'Burnt Orange': (0.80, 0.33, 0.00),
    'Teal': (0.00, 0.50, 0.50),
    'Wine': (0.50, 0.00, 0.25),
    'Lavender': (0.90, 0.90, 0.98),
    'Emerald': (0.31, 0.78, 0.47),
    'Slate': (0.44, 0.50, 0.56),
    'Sand': (0.76, 0.70, 0.50),
    'Bronze': (0.80, 0.50, 0.20),
    'Green': (0.00, 1.00, 0.00),
    'Rose Gold': (0.72, 0.43, 0.47),
    'Light Blue': (0.68, 0.85, 0.90),
    'Cranberry Red': (0.70, 0.13, 0.19),
    'Peach': (1.00, 0.90, 0.71),
    'Forest Green': (0.13, 0.55, 0.13),
    'Mustard Yellow': (1.00, 0.86, 0.35),
    'Burnt Orange': (0.80, 0.33, 0.00),
    "Mustard yellow": [0.769, 0.690, 0.129],
    "Light blue": [0.678, 0.847, 0.902],
    "Sage green": [0.557, 0.663, 0.498],
    "Cranberry red": [0.620, 0.149, 0.208],
    "Mauve": [0.788, 0.635, 0.678],
    "Peach": [1.000, 0.808, 0.667],
    "Rose gold": [0.718, 0.431, 0.475],
    "Dusty rose": [0.796, 0.502, 0.522],
    "Forest green": [0.133, 0.545, 0.133],
    "Coral": [1.000, 0.498, 0.314],
    "Rust": [0.804, 0.357, 0.157],
    "Terracotta": [0.804, 0.341, 0.133],
    "Olive green": [0.420, 0.557, 0.137],
    "Espresso": [0.157, 0.086, 0.062],
    "Oxford blue": [0.000, 0.129, 0.278],
    "Moss": [0.392, 0.486, 0.216],
    "Caviar": [0.082, 0.082, 0.082],
    "Royal blue": [0.255, 0.412, 0.882],
    "British khaki": [0.557, 0.537, 0.349],
    "Toffee": [0.588, 0.447, 0.329],
    "Concrete": [0.502, 0.502, 0.502],
    "Ballet pink": [0.973, 0.851, 0.859],
    "Aegean": [0.149, 0.545, 0.824],
    "Cameo pink": [0.937, 0.749, 0.808],
    "Flame": [0.855, 0.380, 0.153],
    "Patriot blue": [0.071, 0.149, 0.357],
    "Pine": [0.082, 0.392, 0.251],
    "Wisteria": [0.788, 0.643, 0.862],
    "Almond": [0.937, 0.871, 0.804],
    "Cognac": [0.557, 0.271, 0.090],
    "Harbor": [0.129, 0.180, 0.259],
    "Mulberry": [0.620, 0.259, 0.459],
    "Oatmeal": [0.871, 0.839, 0.784],
    "Caramel": [0.906, 0.588, 0.353],
    "Goldenrod": [0.855, 0.647, 0.125],
    'Asphalt': (0.16, 0.16, 0.16),
    'Peacock': (0.0, 0.34, 0.42),
    'Wheat': (0.96, 0.87, 0.7),
    'Portobello': (0.59, 0.51, 0.44),
    'Copper': (0.72, 0.45, 0.2),
    'Champagne': (0.97, 0.91, 0.81),
    'Adobe': (0.8, 0.6, 0.4),
    'Henna': (0.67, 0.31, 0.0),
    'Terracotta': (0.9, 0.45, 0.35),
    'French blue': (0.0, 0.45, 0.73),
    'Lilypad': (0.3, 0.5, 0.22),
    'Clay': (0.58, 0.38, 0.27),
    'Truffle': (0.34, 0.21, 0.16),
    'Marshmallow': (0.96, 0.96, 0.95),
    'Ivy': (0.0, 0.51, 0.29),
    'Blue haze': (0.62, 0.68, 0.75),
    'Mahogany': (0.75, 0.25, 0.0),
    'Burnt orange': (0.80, 0.33, 0.00),
    'Blush pink': (0.98, 0.81, 0.81),
    'Dusty pink': (0.69, 0.53, 0.53)
}

x_key = set(x)
y_key = set(y)

unique_x = {}
unique_y = {}

for item in x_key: unique_x[item] = x[item]
for item in y_key: unique_y[item] = y[item]

model_x = []
model_y = []

def list_creation(path):
    # Example table with dress recommendations
    xls = pd.ExcelFile(path)
    df_color = pd.read_excel(xls, 'Sheet4')
    df_dress = pd.read_excel(xls, 'Sheet5')

    color_input = []
    dress_input = []

    color_output = []
    dress_output = []

    for i, row in df_color.iterrows():  
        color_input.append(row['Colour 1'])
        color_output.append(row['Colour 2'])

    for i, row in df_dress.iterrows(): 
        dress_input.append(row['Dress 1'])
        dress_output.append(row['Dress 2'])

    print(color_input)
    print(color_output)
    print(dress_input)
    print(dress_output)

    input_dresses = []
    output_dresses = []
    for color in color_input:
        for dress in dress_input:
            input_dresses.append(color + ' ' + dress)

    for color in color_output:
        for dress in dress_output:
            output_dresses.append(color + ' ' + dress)

    return color_input, color_output, dress_input, dress_output

file_path = '/content/Fashion Recommendation Table.xlsx'
color_input, color_output, dress_input, dress_output = list_creation(file_path)

for i in range(len(color_input)):
  model_x.append(list(unique_x[color_input[i]]))
  model_y.append(list(unique_y[color_output[i]]))

for i in range(len(color_input)):
  model_x.append(list(unique_y[color_output[i]]))
  model_y.append(list(unique_x[color_input[i]]))

# Define a custom dataset to wrap the input/output pairs
class ColorMatchingDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __len__(self):
        return len(self.x)
    
    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]

# Define the neural network architecture
class ColorMatchingModel(nn.Module):
    def __init__(self):
        super(ColorMatchingModel, self).__init__()
        self.fc1 = nn.Linear(3, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 3)
        self.relu = nn.ReLU()
        
    def forward(self, x):
        out = self.relu(self.fc1(x))
        out = self.relu(self.fc2(out))
        out = self.fc3(out)
        return out

def train(model, train_loader, criterion, optimizer, epochs):
  for epoch in range(epochs):
    running_loss = 0.0
    for inputs, labels in train_loader:
      optimizer.zero_grad()
      outputs = model(inputs)
      loss = criterion(outputs, labels)
      loss.backward()
      optimizer.step()
      running_loss += loss.item()
      print(f"Epoch {epoch + 1} loss: {running_loss / len(train_loader)}")


def validate(model, val_loader, criterion):
  running_loss = 0.0
  with torch.no_grad():
    for inputs, labels in val_loader:
      outputs = model(inputs)
      loss = criterion(outputs, labels)
      running_loss += loss.item()
      print(f"Validation loss: {running_loss / len(val_loader)}")

model = ColorMatchingModel()

# Create dataloaders for the training and validation sets
dataset = ColorMatchingDataset(torch.tensor(model_x), torch.tensor(model_y))
train_size = int(len(dataset) * 0.8)

train_set, val_set = torch.utils.data.random_split(dataset, [train_size, len(dataset) - train_size])

train_loader = DataLoader(train_set, batch_size=16, shuffle=True)
val_loader = DataLoader(val_set, batch_size=16, shuffle=True)

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

train(model, train_loader, criterion, optimizer, 100)

test_x = torch.tensor([
[0.8157, 0.7294, 0.6078], # Tan
[0.3725, 0.3098, 0.2902], # Dark gray
[0.9412, 0.9020, 0.5490], # Light yellow
], dtype=torch.float32)

test_y = torch.tensor([
[0.5686, 0.5098, 0.5020], # Taupe
[0.0000, 0.0000, 0.0000], # Black
[1.0000, 1.0000, 0.8784], # Creamy
], dtype=torch.float32)

test_dataset = ColorMatchingDataset(test_x, test_y)
test_loader = DataLoader(test_dataset, batch_size=1)

model.eval()
with torch.no_grad():
  for inputs, labels in test_loader:
    outputs = model(inputs)
    print(f"Input color: {inputs.squeeze()} -> Predicted color: {outputs.squeeze()} -> Actual color: {labels.squeeze()}")