import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from torch.optim.lr_scheduler import _LRScheduler

"""
  Reprezentacja obrazka w PyTorch - [channels, height, width]
  Reprezentacja obrazka w matplotlib - [height, width, channels]
  Stąd zmiana kolejności wymiarów obrazka
"""
def plot_images(images, labels, classes, normalize = False):
  n_images = len(images)
  rows = int(np.sqrt(n_images))
  cols = int(np.sqrt(n_images))
  fig = plt.figure(figsize = (10, 10))
  for i in range(rows*cols):

    ax = fig.add_subplot(rows, cols, i+1)

    image = images[i]

    if normalize:
      image = normalize_image(image)

    ax.imshow(image.permute(1, 2, 0).cpu().numpy())
    ax.set_title(classes[labels[i]])
    ax.axis('off')
  fig.show()


"""
  Matplotlib wymaga wartości pixela z przedziału [0,1]. Po naszej normalizacji wartości są inne
"""
def normalize_image(image):
  image_min = image.min()
  image_max = image.max()
  image.clamp_(min = image_min, max = image_max)
  image.add_(-image_min).div_(image_max - image_min + 1e-5)
  return image
"""
  Model LeNet:
  - opisać użyte funkcje oraz dodać komentarze nad każdą linijką
"""


def plot_filter(images, filter, normalize = True):
  images = torch.cat([i.unsqueeze(0) for i in images], dim = 0).cpu()
  filter = torch.FloatTensor(filter).unsqueeze(0).unsqueeze(0).cpu()
  filter = filter.repeat(3, 3, 1, 1)
  n_images = images.shape[0]
  filtered_images = F.conv2d(images, filter)
  images = images.permute(0, 2, 3, 1)
  filtered_images = filtered_images.permute(0, 2, 3, 1)
  fig = plt.figure(figsize = (25, 5))

  for i in range(n_images):
    image = images[i]
    if normalize:
      image = normalize_image(image)
    ax = fig.add_subplot(2, n_images, i+1)
    ax.imshow(image)
    ax.set_title('Original')
    ax.axis('off')
    image = filtered_images[i]

    if normalize:
      image = normalize_image(image)

    ax = fig.add_subplot(2, n_images, n_images+i+1)
    ax.imshow(image)
    ax.set_title(f'Filtered')
    ax.axis('off')


"""
Model AlexNet
"""
class AlexNet(nn.Module):
  # output_dim - liczba klas
  def __init__(self, output_dim):
    super().__init__()

    self.features = nn.Sequential(
      # Kod
    )

    self.classifier = nn.Sequential(
      # Kod
    )

  def forward(self, x):
    x = self.features(x)
    h = x.view(x.shape[0], -1)
    x = self.classifier(h)
    return x, h


"""
  Znajdowanie learning rate
"""
class LRFinder:
  def __init__(self, model, optimizer, criterion, device):
    self.optimizer = optimizer
    self.model = model
    self.criterion = criterion
    self.device = device
    torch.save(model.state_dict(), 'init_params.pt')

  def range_test(self, iterator, end_lr = 10, num_iter = 100,
      smooth_f = 0.05, diverge_th = 5):
    lrs = []
    losses = []
    best_loss = float('inf')
    lr_scheduler = ExponentialLR(self.optimizer, end_lr, num_iter)
    iterator = IteratorWrapper(iterator)

    for iteration in range(num_iter):
      loss = self._train_batch(iterator)
      lrs.append(lr_scheduler.get_last_lr()[0])
      # Aktualizacja learning rate
      lr_scheduler.step()
      if iteration > 0:
        loss = smooth_f * loss + (1 - smooth_f) * losses[-1]

      if loss < best_loss:
        best_loss = loss

      losses.append(loss)

      if loss > diverge_th * best_loss:
        print("Stopping early, the loss has diverged")
        break

    # Reset modelu do wartości początkowych
    self.model.load_state_dict(torch.load('init_params.pt'))

    return lrs, losses

  def _train_batch(self, iterator):
    self.model.train()
    self.optimizer.zero_grad()
    x, y = iterator.get_batch()
    x = x.to(self.device)
    y = y.to(self.device)
    y_pred, _ = self.model(x)
    loss = self.criterion(y_pred, y)
    loss.backward()
    self.optimizer.step()
    return loss.item()


class ExponentialLR(_LRScheduler):
  def __init__(self, optimizer, end_lr, num_iter, last_epoch=-1):
    self.end_lr = end_lr
    self.num_iter = num_iter
    super(ExponentialLR, self).__init__(optimizer, last_epoch)

  def get_lr(self):
    curr_iter = self.last_epoch
    r = curr_iter / self.num_iter
    return [base_lr * (self.end_lr / base_lr) ** r for base_lr in self.base_lrs]

class IteratorWrapper:
  def __init__(self, iterator):
    self.iterator = iterator
    self._iterator = iter(iterator)

  def __next__(self):
    try:
      inputs, labels = next(self._iterator)
    except StopIteration:
      self._iterator = iter(self.iterator)
      inputs, labels, *_ = next(self._iterator)

    return inputs, labels

  def get_batch(self):
    return next(self)


"""
  Wyrysowanie szukania learning rate
"""
def plot_lr_finder(lrs, losses, skip_start = 5, skip_end = 5):
  if skip_end == 0:
    lrs = lrs[skip_start:]
    losses = losses[skip_start:]
  else:
    lrs = lrs[skip_start:-skip_end]
    losses = losses[skip_start:-skip_end]

  fig = plt.figure(figsize = (16,8))
  ax = fig.add_subplot(1,1,1)
  ax.plot(lrs, losses)
  ax.set_xscale('log')
  ax.set_xlabel('Learning rate')
  ax.set_ylabel('Loss')
  ax.grid(True, 'both', 'x')
  plt.show()
