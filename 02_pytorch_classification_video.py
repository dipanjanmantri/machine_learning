# -*- coding: utf-8 -*-
"""02_pytorch_classification_video.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ptdiWA-IvOLAj2C8-d07PtJrPQyAb4C9

## Make classification data and get it ready
"""

import sklearn

from sklearn.datasets import make_circles

# Make 1000 samples
n_samples = 1000

# Create circles
X, y =  make_circles(n_samples,
                     noise=0.03, # creating some randomness
                     random_state=42) # setting a random seed)

print(len(X))
print(len(y))

print(f"First 5 samples of X:\n {X[:5]}\n")
print(f"First 5 samples of y:\n {y[:5]}")

# Make DataFrame of circle data
import pandas as pd


# X[:,0] represents 0th index and X[:,1] represents 1st index
circles = pd.DataFrame({"X1":X[:,0],
                        "X2":X[:,1],
                        "label": y})

circles.head(5)

# Visualize, visualize, visualize
import matplotlib.pyplot as plt

plt.scatter(x=X[:,0],
            y=X[:,1],
            c=y,
            cmap=plt.cm.RdYlBu);

"""## Check input and output shapes"""

X.shape, y.shape # X has 1000 samples and 2 features in each sample, y has 1000 samples and its a scalar that is why its showing as (1000,) because it does not have any features.
                 # 2 features of X equals 1 y

# View the first example of features and labels
X_sample = X[0]
y_sample = y[0]

X_sample, X_sample.shape, y_sample, y_sample.shape

"""## Turn data into tensors and create train and test splits"""

X.shape, y.shape

X

# View the 1st example of features and labels
X_sample = X[0]
y_sample = y[0]

X_sample, X_sample.shape, y_sample, y_sample.shape

# Turn data into tensors and create train and test splits
import torch
torch.__version__

type(X), X.dtype

# Turn data into tensors
import torch
import numpy

X = torch.from_numpy(X).type(torch.float)
y = torch.from_numpy(y).type(torch.float)

X[:5], y[:5]

type(X), X.dtype, y.dtype

# Split data into training and test sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

len(X_train), len(X_test), len(y_train), len(y_test)



"""## Build a model to classify our blue and red dots
## 1) Setup device agnostic code
## 2) Construct a model(by subclassing nn.Module)
## 3) Define a loss functon and a optimizer
## 4) Create a training and test loop
"""

import torch
from torch import nn

device = "cuda" if torch.cuda.is_available() else "cpu"
device

X_train.shape

class CircleModelV0(nn.Module):
  def __init__(self):
    super().__init__()

    # Create nn.Linear layers of handling the shapes of the data
    # self.layer_1 = nn.Linear(in_features=2, out_features=5) # takes 2 features and upscales to 5 features
    # self.layer_2 = nn.Linear(in_features=5, out_features=1)  # takes in 5 features from previous layer and outputs a single feature


    self.two_linear_layers = nn.Sequential(
    nn.Linear(in_features=2, out_features=5),
    nn.Linear(in_features=5, out_features=1)
    )


  # Defines a forward method that outlines the forward pass
  def forward(self, x):
    return two_linear_layers(x)
    # return self.layer_2(self.layer_1(x)) # x ----> layer_1 -----> layer_2 ----> output



# Instantiate an instance of our model class and send it to target device
model_0 = CircleModelV0().to(device)
model_0

device, next(model_0.parameters()).device

# Lets replicate the model above using nn.Sequential()

model_0 = nn.Sequential(
    nn.Linear(in_features=2, out_features=5),
    nn.Linear(in_features=5, out_features=1)
).to(device)

model_0

# Make some predictions with the model
with torch.inference_mode():
  untrained_preds = model_0(X_test.to(device))
print(f"Length of predictions: {len(untrained_preds)} | Shape of prediction: {untrained_preds.shape}")
print(f"Length of test sample: {len(X_test)} | Shape of test sample: {X_test.shape}")
print(f"\n First 10 predictions: {torch.round(untrained_preds[:10])}")
print(f"\n First 10 labels: {y_test[:10]}")

X_test[:10], y_test[:10]

## Setup loss function and optimizer

# This is problem specific

# For Regression use MAE(Mean absolute error) or MSE(Mean squared error)

# For classification use Binary Cross Entropy or Categorical Cross Entropy

# 2 most common optimizers are SGD and Adam, however PyTorch has many built in options

#loss_fn = BCELoss()  # requires the input data to have already gone thrpugh sigmoid function
loss_fn = nn.BCEWithLogitsLoss() # built in sigmoid function

optimizer = torch.optim.SGD(params=model_0.parameters(),lr=0.1)


model_0.state_dict()

# Calculate accuracy - out of 100 examples, what percentage does our model get right?

def accuracy_fn(y_true, y_pred):
  correct = torch.eq(y_true, y_pred).sum().item()
  acc = (correct/ len(y_pred)) * 100
  return acc

"""## Train a model - Build a training loop

1. Forward Pass
2. Calculate Loss
3. Optimizer zero grad
4. Loss backward (backpropagation)
5. Optimizer step (gradient descent)

## Going from raw logits -> prediction probabilities -> prediction labels
## Our model output will be raw logits
## We can convert the logits into prediction probabilities by passing them through an activation function
## Then we can convert our model's prediction probabilities to prediction labels by either rounding them or taking them....
"""

# View the first 5 outputs of the forward pass on the test data
model_0.eval()
with torch.inference_mode():
  y_logits = model_0(X_test.to(device))[:5]
y_logits, y_test

# Pass the logits through the sigmoid activation function
y_pred_probs = torch.sigmoid(y_logits)
y_pred_probs, torch.round(y_pred_probs)

"""## y_pred_probs>=0.5 then 1 else 0"""

# Find the predicted labels
y_preds = torch.round(y_pred_probs)

# In full (logits -> pred probs -> pred labels)
y_pred_labels = torch.round(torch.sigmoid(model_0(X_test.to(device))[:5]))

# Check for equality
print(torch.eq(y_preds.squeeze(), y_pred_labels.squeeze()))

# Get rid of extra dimension
y_preds.squeeze()

## Building a training and a test loop

torch.manual_seed(42)

# Set the number of epochs
epochs=1000

# Put data to target device
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

# Build a training and a evaluation loop
for epoch in range(epochs):
  ## Training
  model_0.train()

  # Forward Pass
  y_logits = model_0(X_train).squeeze()
  y_pred = torch.round(torch.sigmoid(y_logits)) # logits -> pred_probs -> pred_labels

  # Calculate the loss/accuracy
  # loss = loss_fn(torch.sigmoid(y_logits), y_train) # nn.BCELoss expects prediction probabilities as input

  loss = loss_fn(y_logits, y_train) # nn.BCEWithLogitsLoss expects raw logits as input
  acc = accuracy_fn(y_true=y_train,
                    y_pred=y_pred)


  # Optimizer zero grad
  optimizer.zero_grad()

  # Loss backward (backpropagation)
  loss.backward()

  # Optimizer step (gradient descent)
  optimizer.step()


  ### Testing

  model_0.eval()

  with torch.inference_mode():
    # Forward pass
    test_logits = model_0(X_test).squeeze()
    test_pred = torch.round(torch.sigmoid(test_logits))


    # Calculate the test loss/acc
    test_loss = loss_fn(test_logits, y_test)
    test_acc = accuracy_fn(y_true=y_test,
                           y_pred=test_pred)

    # Print out what's happening

  if epoch % 10 == 0:
    print(f"Epoch: {epoch} | Loss: {loss: .2f} | Acc: {acc: .2f}% | Test Loss: {test_loss: .2f} | Test Accuracy: {test_acc: .2f}%")

# Make predictions and evaluate the model

import requests
from pathlib import Path


# download helper functions from Learn PyTorch repo( if its not already downloaded)
if Path("helper_functions.py").is_file():
  print("file exists")
else:
  request = requests.get("https://raw.githubusercontent.com/mrdbourke/pytorch-deep-learning/main/helper_functions.py")
  with open("helper_functions.py", "wb") as f:
    f.write(request.content)



from helper_functions import plot_predictions, plot_decision_boundary

# Plot decision boundary of the model
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.title("Train")
plot_decision_boundary(model_0, X_train, y_train)
plt.subplot(1,2,2)
plt.title("Test")
plot_decision_boundary(model_0, X_test, y_test)

# Improve the model by
# 1. adding more layers
# 2. adding more hidden units , go from 5 hidden units to 10 hidden units
# 3. fit for longer, more epochs
# 4. changing the activation functions
# 5. change the learning rate
# 6. change the loss function

# The above points are some of the strategies to improve a model(from a model's perspective)
# These are also called hyperparameters
# Parameters are the values within a model
# Hyperparameters are the values that we can change in a model


### When experimenting to improve the model add/change one at a time and track the results
    # else we can't know which one is improving and which one is degrading the model

class CircleModelV1(nn.Module):
  def __init__(self):
    super().__init__()
    self.layer_1 = nn.Linear(in_features=2, out_features=10)
    self.layer_2 = nn.Linear(in_features=10, out_features=10)
    self.layer_3 = nn.Linear(in_features=10, out_features=1)


  def forward(self, x):
    # z = self.layer_1(x)
    # z = self.layer_2(z)
    # z = self.layer_3(z)
    return self.layer_3(self.layer_2(self.layer_1(x))) # speeds up the operation behind the scenes




model_1 = CircleModelV1().to(device)

model_1.state_dict()

# Create a loss function
loss_fn = nn.BCEWithLogitsLoss()

# Create an optimizer
optimizer = torch.optim.SGD(params=model_1.parameters(),
                            lr=0.1)

# Creating a training and evaluation loop for model_1
torch.manual_seed(42)
torch.cuda.manual_seed(42)


# Train for longer
epochs = 1000


# Put data into the target device
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)


for epoch in range(epochs):
  ## Training
  model_1.train()

  ## Forward pass
  y_logits = model_1(X_train).squeeze()
  y_pred = torch.round(torch.sigmoid(y_logits)) # logits -> pred probabilities -> prediction labels

  # Calculate the loss/accuracy, loss is mandatory but accuracy is optional
  loss = loss_fn(y_logits, y_train)
  acc = accuracy_fn(y_true=y_train,
                    y_pred=y_pred)

  # Optimizer zero grad
  optimizer.zero_grad()

  # Loss backwards (backpropagation)
  loss.backward()

  # Optimizer step (gradient descent)
  optimizer.step()



  ### Testing
  model_1.eval()
  with torch.inference_mode():
    # Forward pass
    test_logits = model_1(X_test).squeeze()  # squeeze is used to get rid of extra dimension
    test_pred = torch.round(torch.sigmoid(test_logits))

    # Calculate the loss
    test_loss = loss_fn(test_logits,
                        y_test)
    test_acc = accuracy_fn(y_true=y_test,
                           y_pred=test_pred)


  # Print out what is happening
  if epoch % 100 == 0:
    print(f"Epoch: {epoch} | Loss: {loss: .5f}, Acc: {acc: .2f}% | Test Loss: {test_loss: .5f}, Test Acc: {test_acc: .2f}%")

# Plot the decision boundary
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.title("Train")
plot_decision_boundary(model_1, X_train, y_train)
plt.subplot(1,2,2)
plt.title("Test")
plot_decision_boundary(model_1, X_test, y_test)

### Preparing data to see if our model can fit a straight line

# One way to troubleshoot a larger problem is to test out a smaller problem

# Create some data(same as notebook 01)
weight = 0.7
bias = 0.3
start = 0
end = 1
step = 0.01


# Create data
# torch.arange(start, end, step), torch.arange(start, end, step).unsqueeze(dim=0),  torch.arange(start, end, step).unsqueeze(dim=1)

X_regression = torch.arange(start, end, step).unsqueeze(dim=1)
y_regression = weight * X_regression + bias # linear regression formula



# Check the data
print(len(X_regression))
X_regression[:5], y_regression[:5]

# Create train and test splits
# len(X_regression), train_split - checking the length of X_regression and train_split


train_split = int(0.8 * len(X_regression))
X_train_regression, y_train_regression = X_regression[:train_split], y_regression[:train_split]
X_test_regression, y_test_regression = X_regression[train_split:], y_regression[train_split:]

# Check the lengths of each
len(X_train_regression), len(y_train_regression), len(X_test_regression), len(y_test_regression)

plot_predictions(train_data=X_train_regression,
                 train_labels=y_train_regression,
                 test_data=X_test_regression,
                 test_labels=y_test_regression)

X_train_regression[:10], y_train_regression[:10] # Here 1 feature is mappped to 1 label

model_1

"""## Adjusting model_1 to fit a straight line"""

## Same architecture as model_1 but using nn.Sequential(), the only that is gonna change is the number of input features
model_2 = nn.Sequential(
    # when it goes through linear layers it triggers forward method
    nn.Linear(in_features=1, out_features=10), # 10 hidden units
    nn.Linear(in_features=10, out_features=10),
    nn.Linear(in_features=10, out_features=1)
).to(device)


model_2

# Loss and optimizer
loss_fn = nn.L1Loss() # MAE Loss with regression data
optimizer = torch.optim.SGD(model_2.parameters(), lr=0.01)

# Train the model
torch.manual_seed(42)
torch.cuda.manual_seed(42)

# Set the epochs
epochs = 1000


# Put the data on the target device
X_train_regression, y_train_regression = X_train_regression.to(device), y_train_regression.to(device)
X_test_regression, y_test_regression = X_test_regression.to(device), y_test_regression.to(device)


# Training
for epoch in range(epochs):
  y_pred = model_2(X_train_regression)
  loss = loss_fn(y_pred, y_train_regression)
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

  # Testing
  model_2.eval()
  with torch.inference_mode():
    test_pred = model_2(X_test_regression)
    test_loss = loss_fn(test_pred, y_test_regression)

  # Print out what is happening
  if epoch % 100 ==0:
    print(f"Epoch: {epoch} | Loss: {loss: .5f} | Test Loss: {test_loss: .5f}")

# Turn on evaluation mode
model_2.eval()

# Make predictions
with torch.inference_mode():
  y_preds = model_2(X_test_regression)


# Plot data and predictions
plot_predictions(train_data=X_train_regression,
                 train_labels=y_train_regression,
                 test_data=X_test_regression,
                 test_labels=y_test_regression,
                 predictions=y_preds);

"""## The missing piece: non-linearity
What patterns could you draw if you were given infinite number of straight and non-straight lines.

In terms of machine learning an infinite number of linear and non-linear functions.
"""

# Recreating non-linear data (red and blue circles)

import matplotlib.pyplot as plt
from sklearn.datasets import make_circles

n_samples = 1000

X, y = make_circles(n_samples,
                    noise=.03,
                    random_state=42)

# X[:10], y[:10]

plt.scatter(X[:,0], X[:,1], c=y, cmap=plt.cm.RdYlBu)

# Convert data to tensors and then to train and test splits
import torch
from sklearn.model_selection import train_test_split



# Turn data to tensors
X = torch.from_numpy(X).type(torch.float)
y = torch.from_numpy(y).type(torch.float)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)
X_train[:5], y_train[:5]

# Building a model with non-linearity

# Linear = straight line
# Non-Linear = non straight line

"""## Build a model with non-linear activation function

Artificial neural networks are large combinations of linear and non-linear functions
"""

from torch import nn

class CircleModelV2(nn.Module):
  def __init__(self):
    super().__init__()
    self.layer_1 = nn.Linear(in_features=2, out_features=10)
    self.layer_2 = nn.Linear(in_features=10, out_features=10)
    self.layer_3 = nn.Linear(in_features=10, out_features=1)
    self.relu = nn.ReLU() # relu is a non-linear activation function


  def forward(self, x):
    # Where should we put our non-linear activation function
    return self.layer_3(self.relu(self.layer_2(self.relu(self.layer_1(x)))))


model_3 = CircleModelV2().to(device)
model_3

## Setup Loss and Optimizer
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(model_3.parameters(),
                            lr=0.1)

# spam or not spam
# credit cards = fraud or not fraud
# insurance claims = fault or not at fault

"""## Train a model with non-linearity"""

from mmap import MAP_DENYWRITE
# Random seeds
torch.manual_seed(42)
torch.cuda.manual_seed(42)


# Put all data on target device
X_train, y_train = X_train.to(device), y_train.to(device)
X_test, y_test = X_test.to(device), y_test.to(device)

# Loop through data
epochs = 1000

for epoch in range(epochs):
  ### Training code
  model_3.train()

  # Forward pass
  y_logits = model_3(X_train).squeeze()
  y_pred = torch.round(torch.sigmoid(y_logits)) # logits -> pred probabilities -> pred labels

  # Calculate the loss
  loss = loss_fn(y_logits, y_train) # BCEWithLogitsLoss
  acc = accuracy_fn(y_true=y_train,
                    y_pred=y_pred)

  # Optimizer zero grad
  optimizer.zero_grad()


  # Backpropagation (gradient descent)
  loss.backward()

  # Optimizer step
  optimizer.step()


  # Testing
  model_3.eval()
  with torch.inference_mode():
    test_logits = model_3(X_test).squeeze()
    test_pred = torch.round(torch.sigmoid(test_logits))

    test_loss = loss_fn(test_logits,
                        y_test)
    test_acc = accuracy_fn(y_true=y_test,
                    y_pred=test_pred)

  # Print out whats happening
  if epoch % 100 == 0:
    print(f"Epoch: {epoch} | Loss: {loss: .4f}, loss_acc: {acc: .2f}% | Test Loss: {test_loss: .4f}, test_loss_acc: {test_acc: .2f}%")

"""## Evaluating a model trained with non-linear activation functions

"""

# Make predictions
model_3.eval()
with torch.inference_mode():
  y_preds = torch.round(torch.sigmoid(model_3(X_test))).squeeze()



y_preds[:10], y_test[:10]

# Plot decision boundaries
plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.title("Train")
plot_decision_boundary(model_3, X_train, y_train)
plt.subplot(1,2,2)
plt.title("Test")
plot_decision_boundary(model_3, X_test, y_test)

"""## Replicate the non-linear activation functions

Neural networks, rather than us telling the model what to learn, we give it the tools to discover patterns in data and it tries to figure out the patterns on its own.

And these tools are linear and non-linear activation functions.


"""

# Create a tensor
A = torch.arange(-10,10,1, dtype=torch.float)
A.dtype

plt.plot(A)

plt.plot(A), plt.plot(torch.relu(A))

# Lets do the same for sigmoid
def sigmoid(x):
  return 1/(1+torch.exp(-x))



plt.plot(torch.sigmoid(A))

plt.plot(sigmoid(A))

"""## Putting it all together with a multi-class classification problem.
1. Binary classification = one thing or another(fraud or not fraud, dog or cat, spam or not spam and similar types)
2. Multi-class classification = more than one thing or another(dog or cat or sheep, pizza or burger or sushi)

## Create a toy multi-class dataset.
"""

# Import dependencies
import torch
from matplotlib import pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split

# Set the hyper-parameters for data creation
NUM_CLASSES = 4
NUM_FEATURES = 2
RANDOM_SEED = 42

# 1. Create multi-class data
X_blob, y_blob = make_blobs(n_samples=1000,
                            n_features=NUM_FEATURES,
                            centers=NUM_CLASSES,
                            cluster_std=1.5, # give the clusters a little shakeup
                            random_state=RANDOM_SEED)

# 2. Turn data into tensors
X_blob = torch.from_numpy(X_blob).type(torch.float)
y_blob = torch.from_numpy(y_blob).type(torch.LongTensor)


# 3. Split into train and test
X_blob_train, X_blob_test, y_blob_train, y_blob_test = train_test_split(X_blob,
                                                                        y_blob,
                                                                        test_size=0.2,
                                                                        random_state=RANDOM_SEED)

# 4. Plot data (Visualize, visualize, visualize)
plt.figure(figsize=(10,7))
plt.scatter(X_blob[:,0], X_blob[:,1], c=y_blob, cmap=plt.cm.RdYlBu)

"""## Building a multi-class classification model in PyTorch"""

# Create device agnostic code
device = "cuda" if torch.cuda.is_available() else "cpu"
device

# Build a multi-class classification model
class BlobModel(nn.Module):
  def __init__(self, input_features, out_features, hidden_units=8):
    super().__init__()
    self.linear_layer_stack = nn.Sequential(
        nn.Linear(in_features=input_features, out_features=hidden_units),
        nn.ReLU(),
        nn.Linear(in_features=hidden_units, out_features=hidden_units),
        nn.ReLU(),
        nn.Linear(in_features=hidden_units, out_features=out_features)
    )


  def forward(self, x):
    return self.linear_layer_stack(x)




# Create an instance of BlobModel and send it to the target device
model_4 = BlobModel(input_features=2,
                    out_features=4,
                    hidden_units=8).to(device)


model_4

X_blob_train.shape, y_blob_train[:100]

torch.unique(X_blob_train)

"""## Cross entropy loss is a loss function used in unbalanced datasets in multi-classification problem."""

# Create a loss function for multi-class classification
loss_fn = nn.CrossEntropyLoss()


# Create an optimizer for multi-class classfication
optimizer = torch.optim.SGD(params=model_4.parameters(),
                            lr=0.1)

"""## Getting prediction probablities for multi-class PyTorch model.
In order to evaluate and train & test our model, we need to convert our model's outputs(logits) to prediction probabilities and then to prediction labels.

Logits (raw output of the model) -> Pred Probs (use torch.softmax())-> Pred Labels (take the argmax of the prediction probabilities)
"""

model_4.eval()
with torch.inference_mode():
  y_logits=model_4(X_blob_test.to(device))


y_preds.shape

y_blob_test[:5], X_blob_test[:5], y_logits[:5]

# Convert our model's logit outputs to prediction probabilities
y_pred_probs=torch.softmax(y_logits, dim=1)
print(y_logits[:5])
print(y_pred_probs[:5])

# Total sum of all the tensor values in the zeroth index,  max tensor value of the zeroth index
torch.sum(y_pred_probs[1]), torch.max(y_pred_probs[1])

# Convert our prediction probabilties to prediction labels
y_preds = torch.argmax(y_pred_probs, dim=1)
y_preds

y_blob_test

"""## Create a Training and a Testing loop for a multi-class classification model in PyTorch"""

y_logits.dtype, y_blob_train.dtype

# Fit the multi-class model to the data
torch.manual_seed(42)
torch.cuda.manual_seed(42)

# Set the number of epochs
epochs = 100

# Put the data to the target device
X_blob_train, y_blob_train = X_blob_train.to(device), y_blob_train.to(device)
X_blob_test, y_blob_test = X_blob_test.to(device), y_blob_test.to(device)

# Loop through data
for epoch in range(epochs):
  ### Training
  model_4.train()

  y_logits = model_4(X_blob_train)
  y_pred = torch.softmax(y_logits, dim=1).argmax(dim=1)
  loss = loss_fn(y_logits, y_blob_train)
  acc = accuracy_fn(y_true=y_blob_train,
                    y_pred=y_pred
                   )

  optimizer.zero_grad()

  loss.backward()

  optimizer.step()


  ### Testing
  model_4.eval()
  with torch.inference_mode():
    test_logits = model_4(X_blob_test)
    test_preds = torch.softmax(test_logits, dim=1).argmax(dim=1)

    test_loss = loss_fn(test_logits, y_blob_test)
    test_acc = accuracy_fn(y_true=y_blob_test,
                           y_pred=test_preds)


    # Print out what's happening
    if epoch % 10 == 0:
      print(f"Epoch: {epoch} | Loss: {loss: .4f}, Acc: {acc: .2f}% | Test Loss: {test_loss: .4f}, Test Loss Acc: {test_acc: .2f}%")

"""### Making and evaluating predictions with a PyTorch multi-class model"""

# Make predictions
model_4.eval()
with torch.inference_mode():
  y_logits = model_4(X_blob_test)



# View the first 10 predictions
y_logits[:10]

# Go from logits -> prediction probabilities
y_pred_probs = torch.softmax(y_logits, dim=1) # It spreads out the data evenly so that the sum of the data in each row for all the rows equals to 1
y_pred_probs[:10]

# Pred probs -> pred labels
y_preds = torch.argmax(y_pred_probs, dim=1)
y_preds[:10]

y_blob_test[:10]

plt.figure(figsize=(12,6))
plt.subplot(1,2,1)
plt.title("Train")
plot_decision_boundary(model_4, X_blob_train, y_blob_train)
plt.subplot(1,2,2)
plt.title("Test")
plot_decision_boundary(model_4, X_blob_test, y_blob_test)

"""## A few more classification metrics.....(to evaluate our classification model)

* Accuracy - out of 100 samples, how many does our model get right?
* Precision
* Recall
* F1-score
* Confusion matrix
* Classification report

See this article for reference:
https://towardsdatascience.com/beyond-accuracy-precision-and-recall-3da06bea9f6c


To access PyTorch metrics see TorchMetrics - https://torchmetrics.readthedocs.io/en/stable/




"""

!pip install torchmetrics

from torchmetrics import Accuracy

# Setup metric
torchmetric_accuracy = Accuracy(task="multiclass", num_classes=4).to(device)

# Calculate accuracy
torchmetric_accuracy(y_preds, y_blob_test)

"""## Excercises and extras - https://www.learnpytorch.io/02_pytorch_classification/#exercises

https://github.com/mrdbourke/pytorch-deep-learning/tree/main/extras/exercises


"""

