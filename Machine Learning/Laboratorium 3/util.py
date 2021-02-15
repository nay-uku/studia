import matplotlib.pyplot as plt
import numpy as np
import torch.nn.functional as F
import torch.nn as nn
import torch
from sklearn import metrics

def plot_images(images):
  n_images = len(images)
  rows = int(np.sqrt(n_images))
  cols = int(np.sqrt(n_images))
  fig = plt.figure()
  for i in range(rows*cols):
    ax = fig.add_subplot(rows, cols, i+1)
    ax.imshow(images[i].view(28, 28).cpu().numpy(), cmap = 'bone')
    ax.axis('off')
  fig.show()
"""
Defaultowe wartości:
 - 1 warstwa ukryta - 100 neuronów
 - 2 warstwa ukryta - 50 neuronów
 - funkcje aktywacji - ReLU
 
 Jak zmiana ma wpływ na wyniki?
 Czym jest nn.Linear?
"""

class MLP(nn.Module):
  def __init__(self, input_dim, output_dim):
    super().__init__()
    self.input_fc = nn.Linear(input_dim, 100)
    self.hidden_fc = nn.Linear(100, 50)
    self.output_fc = nn.Linear(50, output_dim)

  def forward(self, x):
    batch_size = x.shape[0]
    x = x.view(batch_size, -1)
    h_1 = F.relu(self.input_fc(x))
    h_2 = F.relu(self.hidden_fc(h_1))
    y_pred = self.output_fc(h_2)
    return y_pred, h_2

"""
Jak działa obliczanie dokładności modelu?
"""
def calculate_accuracy(y_pred, y):
  top_pred = y_pred.argmax(1, keepdim = True)
  correct = top_pred.eq(y.view_as(top_pred)).sum()
  acc = correct.float() / y.shape[0]
  return acc

"""
Opisać algorytm uczący - co można poprawić i jak?
"""
def train(model, iterator, optimizer, criterion, device):
  epoch_loss = 0
  epoch_acc = 0

  # Niektóre warstwy inaczej zachowują się podczas treningu a inaczej podczas ewaluacji.
  # Dobrą praktyką jest zaznaczenie, że sieć jest w "trybie uczenia"
  model.train()
  for (x, y) in iterator:
    x = x.to(device)
    y = y.to(device)
    optimizer.zero_grad()
    y_pred, _ = model(x)
    loss = criterion(y_pred, y)
    acc = calculate_accuracy(y_pred, y)
    loss.backward()
    optimizer.step()
    epoch_loss += loss.item()
    epoch_acc += acc.item()
  return epoch_loss / len(iterator), epoch_acc / len(iterator)


"""
Na czym polega ewaluacja modelu?
"""
def evaluate(model, iterator, criterion, device):
  epoch_loss = 0
  epoch_acc = 0
  model.eval()
  with torch.no_grad():
    for (x, y) in iterator:
      x = x.to(device)
      y = y.to(device)
      y_pred, _ = model(x)
      loss = criterion(y_pred, y)
      acc = calculate_accuracy(y_pred, y)
      epoch_loss += loss.item()
      epoch_acc += acc.item()
  return epoch_loss / len(iterator), epoch_acc / len(iterator)


def epoch_time(start_time, end_time):
  elapsed_time = end_time - start_time
  elapsed_mins = int(elapsed_time / 60)
  elapsed_secs = int(elapsed_time - (elapsed_mins * 60))
  return elapsed_mins, elapsed_secs


def get_predictions(model, iterator, device):
  model.eval()
  images = []
  labels = []
  probs = []
  with torch.no_grad():
    for (x, y) in iterator:
      x = x.to(device)
      y_pred, _ = model(x)
      y_prob = F.softmax(y_pred, dim = -1)

      images.append(x.cpu())
      labels.append(y.cpu())
      probs.append(y_prob.cpu())

  images = torch.cat(images, dim = 0)
  labels = torch.cat(labels, dim = 0)
  probs = torch.cat(probs, dim = 0)
  return images, labels, probs

"""
 Czym jest "Confusion matrix"? Opisać dla wyników modelu.
"""
def plot_confusion_matrix(labels, pred_labels):
  fig = plt.figure(figsize = (10, 10))
  ax = fig.add_subplot(1, 1, 1)
  cm = metrics.confusion_matrix(labels, pred_labels)
  cm = metrics.ConfusionMatrixDisplay(cm, range(10))
  cm.plot(values_format = 'd', cmap = 'Blues', ax = ax)
  fig.show()


def plot_most_incorrect(incorrect, n_images):
  rows = int(np.sqrt(n_images))
  cols = int(np.sqrt(n_images))
  fig = plt.figure(figsize = (20, 10))
  for i in range(rows*cols):
    ax = fig.add_subplot(rows, cols, i+1)
    image, true_label, probs = incorrect[i]
    true_prob = probs[true_label]
    incorrect_prob, incorrect_label = torch.max(probs, dim = 0)
    ax.imshow(image.view(28, 28).cpu().numpy(), cmap='bone')
    ax.set_title(f'true label: {true_label} ({true_prob:.3f})\n' \
                 f'pred label: {incorrect_label} ({incorrect_prob:.3f})')
    ax.axis('off')
  fig.subplots_adjust(hspace= 0.5)
  fig.show()

"""
 Zobrazowanie wag pierwszej warstwy modelu.
 Może jakiś neuron nauczył się rozpoznawać konkretny wzór?
 Podać przykład.
"""
def plot_weights(weights, n_weights):
  rows = int(np.sqrt(n_weights))
  cols = int(np.sqrt(n_weights))
  fig = plt.figure(figsize = (20, 10))
  for i in range(rows*cols):
    ax = fig.add_subplot(rows, cols, i+1)
    ax.imshow(weights[i].view(28, 28).cpu().numpy(), cmap = 'bone')
    ax.axis('off')
  fig.show()
