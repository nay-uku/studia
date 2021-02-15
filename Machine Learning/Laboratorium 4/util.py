import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

"""
  Wyrysowuje filter nałożony na obrazy
"""
def plot_filter(images, filter):
  images = images = torch.cat([i.unsqueeze(0) for i in images], dim=0).cpu()
  filter = torch.FloatTensor(filter).unsqueeze(0).unsqueeze(0).cpu()
  n_images = images.shape[0]
  filtered_images = F.conv2d(images, filter)
  fig = plt.figure(figsize=(20, 5))
  for i in range(n_images):
    ax = fig.add_subplot(2, n_images, i + 1)
    ax.imshow(images[i].squeeze(0), cmap='bone')
    ax.set_title('Original')
    ax.axis('off')
    image = filtered_images[i].squeeze(0)
    ax = fig.add_subplot(2, n_images, n_images + i + 1)
    ax.imshow(image, cmap='bone')
    ax.set_title(f'Filtered')
    ax.axis('off')
  fig.show()

"""
  Model LeNet:
  - opisać użyte funkcje oraz dodać komentarze nad każdą linijką
"""
class LeNet(nn.Module):
  def __init__(self, output_dim):
    super().__init__()

    self.conv1 = nn.Conv2d(in_channels=1,
                           out_channels=6,
                           kernel_size=5)

    self.conv2 = nn.Conv2d(in_channels=6,
                           out_channels=16,
                           kernel_size=5)

    self.fc_1 = nn.Linear(16 * 4 * 4, 120)
    self.fc_2 = nn.Linear(120, 84)
    self.fc_3 = nn.Linear(84, output_dim)

  def forward(self, x):
    x = self.conv1(x)
    x = F.max_pool2d(x, kernel_size=2)
    x = F.relu(x)
    x = self.conv2(x)
    x = F.max_pool2d(x, kernel_size=2)
    x = F.relu(x)
    x = x.view(x.shape[0], -1)
    h = x
    x = self.fc_1(x)
    x = F.relu(x)
    x = self.fc_2(x)
    x = F.relu(x)
    x = self.fc_3(x)
    return x, h


def calculate_accuracy(y_pred, y):
  top_pred = y_pred.argmax(1, keepdim=True)
  correct = top_pred.eq(y.view_as(top_pred)).sum()
  acc = correct.float() / y.shape[0]
  return acc


def train(model, iterator, optimizer, criterion, device):
  epoch_loss = 0
  epoch_acc = 0

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
      y_prob = F.softmax(y_pred, dim=-1)
      top_pred = y_prob.argmax(1, keepdim=True)
      images.append(x.cpu())
      labels.append(y.cpu())
      probs.append(y_prob.cpu())

  images = torch.cat(images, dim=0)
  labels = torch.cat(labels, dim=0)
  probs = torch.cat(probs, dim=0)

  return images, labels, probs


def plot_confusion_matrix(labels, pred_labels):
  fig = plt.figure(figsize=(10, 10))
  ax = fig.add_subplot(1, 1, 1)
  cm = confusion_matrix(labels, pred_labels)
  cm = ConfusionMatrixDisplay(cm)
  cm.plot(values_format='d', cmap='Blues', ax=ax)
  fig.show()


def plot_most_incorrect(incorrect, n_images):
  rows = int(np.sqrt(n_images))
  cols = int(np.sqrt(n_images))
  fig = plt.figure(figsize=(20, 10))
  for i in range(rows * cols):
    ax = fig.add_subplot(rows, cols, i + 1)
    image, true_label, probs = incorrect[i]
    true_prob = probs[true_label]
    incorrect_prob, incorrect_label = torch.max(probs, dim=0)
    ax.imshow(image.view(28, 28).cpu().numpy(), cmap='bone')
    ax.set_title(f'true label: {true_label} ({true_prob:.3f})\n' \
                 f'pred label: {incorrect_label} ({incorrect_prob:.3f})')
    ax.axis('off')
  fig.subplots_adjust(hspace=0.5)
  fig.show()


def plot_subsample(images, pool_type, pool_size):
  images = torch.cat([i.unsqueeze(0) for i in images], dim=0).cpu()
  if pool_type.lower() == 'max':
    pool = F.max_pool2d
  elif pool_type.lower() in ['mean', 'avg']:
    pool = F.avg_pool2d
  else:
    raise ValueError(f'pool_type must be either max or mean, got: {pool_type}')

  n_images = images.shape[0]
  pooled_images = pool(images, kernel_size=pool_size)
  fig = plt.figure(figsize=(20, 5))
  for i in range(n_images):
    ax = fig.add_subplot(2, n_images, i + 1)
    ax.imshow(images[i].squeeze(0), cmap='bone')
    ax.set_title('Original')
    ax.axis('off')
    image = pooled_images[i].squeeze(0)
    ax = fig.add_subplot(2, n_images, n_images + i + 1)
    ax.imshow(image, cmap='bone')
    ax.set_title(f'Subsampled')
    ax.axis('off');
