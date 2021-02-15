import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import copy
import random
import time

from util import *

SEED = 1234

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True

ROOT = 'data'

# Standaryzacja danych
train_data = datasets.MNIST(root=ROOT,
                            train=True,
                            download=True)

mean = train_data.data.float().mean() / 255
std = train_data.data.float().std() / 255

print(f'Calculated mean: {mean}')
print(f'Calculated std: {std}')

# Definicja transformacji zbioru testowego oraz treningowego
train_transforms = transforms.Compose([
  transforms.RandomRotation(5, fill=(0,)),
  transforms.RandomCrop(28, padding=2),
  transforms.ToTensor(),
  transforms.Normalize(mean=[mean], std=[std])
])

test_transforms = transforms.Compose([
  transforms.ToTensor(),
  transforms.Normalize(mean=[mean], std=[std])
])

train_data = datasets.MNIST(root=ROOT,
                            train=True,
                            download=True,
                            transform=train_transforms)

test_data = datasets.MNIST(root=ROOT,
                           train=False,
                           download=True,
                           transform=test_transforms)

# Tworzenie zbioru walidacyjnego
VALID_RATIO = 0.9
n_train_examples = int(len(train_data) * VALID_RATIO)
n_valid_examples = len(train_data) - n_train_examples
train_data, valid_data = data.random_split(train_data,
                                           [n_train_examples, n_valid_examples])
valid_data = copy.deepcopy(valid_data)
valid_data.dataset.transform = test_transforms
print(f'Number of training examples: {len(train_data)}')
print(f'Number of validation examples: {len(valid_data)}')
print(f'Number of testing examples: {len(test_data)}')

BATCH_SIZE = 64

train_iterator = data.DataLoader(train_data,
                                 shuffle=True,
                                 batch_size=BATCH_SIZE)

valid_iterator = data.DataLoader(valid_data,
                                 batch_size=BATCH_SIZE)

test_iterator = data.DataLoader(test_data,
                                batch_size=BATCH_SIZE)

N_IMAGES = 5

images = [image for image, label in [test_data[i] for i in range(N_IMAGES)]]

horizontal_filter = [[-1, -2, -1],
                     [0, 0, 0],
                     [1, 2, 1]]
plot_filter(images, horizontal_filter)

horizontal_filter = [[1, 2, 1],
                     [0, 0, 0],
                     [-1, -2, -1]]
plot_filter(images, horizontal_filter)

vertical_filter = [[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]]
plot_filter(images, vertical_filter)

vertical_filter = [[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]]
plot_filter(images, vertical_filter)

diagonal_filter = [[-2, -1, 0],
                   [-1, 0, 1],
                   [0, 1, 2]]
plot_filter(images, diagonal_filter)


plot_subsample(images, 'max', 2)

plot_subsample(images, 'max', 3)

plot_subsample(images, 'avg', 2)

plot_subsample(images, 'avg', 3)

OUTPUT_DIM = 10

model = LeNet(OUTPUT_DIM)


def count_parameters(model):
  return sum(p.numel() for p in model.parameters() if p.requires_grad)


print(f'The model has {count_parameters(model):,} trainable parameters')


# Trenowanie modelu

optimizer = optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = model.to(device)
criterion = criterion.to(device)

EPOCHS = 1

best_valid_loss = float('inf')

for epoch in range(EPOCHS):

  start_time = time.time()

  train_loss, train_acc = train(model, train_iterator, optimizer, criterion,
                                device)
  valid_loss, valid_acc = evaluate(model, valid_iterator, criterion, device)

  if valid_loss < best_valid_loss:
    best_valid_loss = valid_loss
    torch.save(model.state_dict(), 'cnn-model.pt')

  end_time = time.time()

  epoch_mins, epoch_secs = epoch_time(start_time, end_time)

  print(f'Epoch: {epoch + 1:02} | Epoch Time: {epoch_mins}m {epoch_secs}s')
  print(f'\tTrain Loss: {train_loss:.3f} | Train Acc: {train_acc * 100:.2f}%')
  print(f'\t Val. Loss: {valid_loss:.3f} |  Val. Acc: {valid_acc * 100:.2f}%')

model.load_state_dict(torch.load('cnn-model.pt'))
test_loss, test_acc = evaluate(model, test_iterator, criterion, device)
print(f'Test Loss: {test_loss:.3f} | Test Acc: {test_acc * 100:.2f}%')

# Weryfikacja modelu

images, labels, probs = get_predictions(model, test_iterator, device)
pred_labels = torch.argmax(probs, 1)
plot_confusion_matrix(labels, pred_labels)

corrects = torch.eq(labels, pred_labels)

incorrect_examples = []

for image, label, prob, correct in zip(images, labels, probs, corrects):
  if not correct:
    incorrect_examples.append((image, label, prob))

incorrect_examples.sort(reverse=True,
                        key=lambda x: torch.max(x[2], dim=0).values)

N_IMAGES = 25

plot_most_incorrect(incorrect_examples, N_IMAGES)
