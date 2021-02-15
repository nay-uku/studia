from util import *
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
# torchvision - zbiory danych dotyczące computer vision
import torchvision.transforms as transforms
import torchvision.datasets as datasets

import numpy as np

import copy
import random
import time

"""
Zadania:
1.Eksperymentalnie:
 - wybrać liczbę neuronów oraz warstw sieci
 - wybrać liczbę epok uczenia
 - znaleźć miejsca na przyspieszenie oraz propozycje zmiany (mając na uwadze, że pętle 'for' są bardzo wolne)
 - jak długo trwa uczenie dla różnych konfiguracji liczby neuronów oraz warstw?

2. Wypisać funkcje biblioteki PyTorch użyte w programie wraz z krótki opis działania
 oraz dlaczego zostały zastosowane

3. Odpowiedzieć na pytania zadane w komentarzach.
"""
SEED = 1234

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True

"""
 PRZYGOTOWANIE DANYCH
"""

# Ładowanie zbioru danych MNIST do folderu 'data'
ROOT = 'data'

train_data = datasets.MNIST(root = ROOT,
                            train = True,
                            download = True)
# Normalizacja danych
mean = train_data.data.float().mean() / 255
std = train_data.data.float().std() / 255
print(f'Calculated mean: {mean}')
print(f'Calculated std: {std}')

# Transformacje - najpierw wykonujemy transformacje na obrazie PIL (Python Imaging Library, Pillow)
# Normalizacje wykonujemy na tensorze
# https://pytorch.org/docs/stable/torchvision/transforms.html#transforms-on-pil-image
# https://pytorch.org/docs/stable/torchvision/transforms.html#transforms-on-torch-tensor

# Co dokładnie wykonują transformacje?
train_transforms = transforms.Compose([
  transforms.RandomRotation(5, fill=(0,)),
  transforms.RandomCrop(28, padding = 2),
  transforms.ToTensor(),
  transforms.Normalize(mean = [mean], std = [std])
])

test_transforms = transforms.Compose([
  transforms.ToTensor(),
  transforms.Normalize(mean = [mean], std = [std])
])

train_data = datasets.MNIST(root = ROOT,
                            train = True,
                            download = True,
                            transform = train_transforms)

test_data = datasets.MNIST(root = ROOT,
                           train = False,
                           download = True,
                           transform = test_transforms)

print(f'Number of training examples: {len(train_data)}')
print(f'Number of testing examples: {len(test_data)}')

# Prezentacja kliku zdjęć ze zbioru danych
N_IMAGES = 25

images = [image for image, label in [train_data[i] for i in range(N_IMAGES)]]
plot_images(images)

# Zbiór danych MNIST nie zawiera zbioru walidacyjnego.
# Zabieramy 10% zbioru treningowego na zbiór walidacyjny

VALIDATION_SET_RATIO = 0.9
n_train_examples = int(len(train_data) * VALIDATION_SET_RATIO)
n_valid_examples = len(train_data) - n_train_examples

train_data, valid_data = data.random_split(train_data,
                                           [n_train_examples, n_valid_examples])
print(f'Number of training examples: {len(train_data)}')
print(f'Number of validation examples: {len(valid_data)}')
print(f'Number of testing examples: {len(test_data)}')

# Zbiór walidacyjny zawiera transformacje zbioru treningowego
images = [image for image, label in [valid_data[i] for i in range(N_IMAGES)]]
plot_images(images)

# Zamiana transformacji
valid_data = copy.deepcopy(valid_data)
valid_data.dataset.transform = test_transforms

# Porównanie obrazków po transformacji (bardziej zcentrowane)
images = [image for image, label in [valid_data[i] for i in range(N_IMAGES)]]
plot_images(images)

# Definicja DataLoader'ów (czym są DataLoader'y)?
# Co oznacza i do czego jest używany parametr shuffle = True w zbiorze treningowym?
BATCH_SIZE = 64
train_iterator = data.DataLoader(train_data,
                                 shuffle = True,
                                 batch_size = BATCH_SIZE)

valid_iterator = data.DataLoader(valid_data,
                                 batch_size = BATCH_SIZE)

test_iterator = data.DataLoader(test_data,
                                batch_size = BATCH_SIZE)

"""
 DEFINICJA MODELU
"""

# Obrazek jest jednokolorowy o wymiarach 28 x 28
INPUT_DIM = 28 * 28
OUTPUT_DIM = 10

model = MLP(INPUT_DIM, OUTPUT_DIM)

# Wyliczenie liczby parametrów modelu
def count_parameters(model):
  return sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f'The model has {count_parameters(model):,} trainable parameters')


"""
 UCZENIE
"""

optimizer = optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()
# Umieszczenie modelu oraz danych na GPU (jeśli jest dostępne)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
criterion = criterion.to(device)

EPOCHS = 1  # Ustawione na 1, gdyż uczenie może zająć chwilę czasu...

best_valid_loss = float('inf')

for epoch in range(EPOCHS):
  start_time = time.time()
  train_loss, train_acc = train(model, train_iterator, optimizer, criterion, device)
  # ewaluacja modelu na zbiorze walidacyjnym
  valid_loss, valid_acc = evaluate(model, valid_iterator, criterion, device)
  if valid_loss < best_valid_loss:
    best_valid_loss = valid_loss
    torch.save(model.state_dict(), 'nn_model.pt')

  end_time = time.time()
  epoch_mins, epoch_secs = epoch_time(start_time, end_time)

  print(f'Epoch: {epoch+1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
  print(f'\tTrain Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}%')
  print(f'\t Val. Loss: {valid_loss:.3f} |  Val. Acc: {valid_acc*100:.2f}%')

# Jaki model został zapisany w pliku 'nn_model'?
model.load_state_dict(torch.load('nn_model.pt'))
test_loss, test_acc = evaluate(model, test_iterator, criterion, device)
print(f'Test Loss: {test_loss:.3f} | Test Acc: {test_acc*100:.2f}%')


"""
 ANALIZA MODELU
"""

images, labels, probs = get_predictions(model, test_iterator, device)
pred_labels = torch.argmax(probs, 1)

plot_confusion_matrix(labels, pred_labels)
corrects = torch.eq(labels, pred_labels)
incorrect_examples = []

for image, label, prob, correct in zip(images, labels, probs, corrects):
  if not correct:
    incorrect_examples.append((image, label, prob))

incorrect_examples.sort(reverse = True, key = lambda x: torch.max(x[2], dim = 0).values)
plot_most_incorrect(incorrect_examples, N_IMAGES)
# Dlaczego te obrazki mogły zostać nieprawidłowo sklasyfikowane?

N_WEIGHTS = 25
weights = model.input_fc.weight.data
plot_weights(weights, N_WEIGHTS)
