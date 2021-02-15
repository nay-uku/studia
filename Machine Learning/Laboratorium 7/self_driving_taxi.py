import random

import gym
from IPython.core.display import clear_output
from pandas import np

# załadowanie środowiska
env = gym.make("Taxi-v3").env
# reset środowiska do losowego stanu
env.reset()

print("Przestrzeń akcji {}".format(env.action_space))
print("Przestrzeń stanów {}".format(env.observation_space))

# (taxi row, taxi column, passenger index, destination index)
state = env.encode(3, 1, 2, 0)
print("State:", state)
env.s = state
env.render()

# P - tablica nagród środowiska
# {action: [(probability, nextstate, reward, done)]}
# W tym środowisku 'probability' zawsze = 1
# nextstate - stan po wykonaniu akcji 'action'
# done - czy pasażer został odstawiony do odpowiedniej lokacji
print(env.P[328])

# Q-table
q_table = np.zeros([env.observation_space.n, env.action_space.n])

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

for i in range(1, 100001):
  state = env.reset()
  done = False

  while not done:
    if random.uniform(0, 1) < epsilon:
      action = env.action_space.sample()  # Eksploracja
    else:
      action = np.argmax(q_table[state])  # Eksploitacja

    next_state, reward, done, info = env.step(action)

    old_value = q_table[state, action]

    # równanie bellmana
    new_value = (1 - alpha) * old_value + alpha * \
                (reward + gamma * np.max(q_table[next_state]))
    # aktualizacja q-table
    q_table[state, action] = new_value
    # aktualizacja stanu
    state = next_state

  if i % 1000 == 0:
    clear_output(wait=True)
    print(f"Episode: {i}")

print("Training finished.\n")

"""
Ewaluacja agenta po uczeniu
"""

total_epochs, total_penalties = 0, 0
episodes = 100

for _ in range(episodes):
  state = env.reset()
  epochs, penalties, reward = 0, 0, 0

  done = False

  while not done:
    action = np.argmax(q_table[state])
    state, reward, done, info = env.step(action)

    if reward == -10:
      penalties += 1

    epochs += 1

  total_penalties += penalties
  total_epochs += epochs

print(f"Results after {episodes} episodes:")
print(f"Average timesteps per episode: {total_epochs / episodes}")
print(f"Average penalties per episode: {total_penalties / episodes}")


'''
  Wizualizacja
'''

state = env.reset()
done = False
while not done:
  env.render()
  action = np.argmax(q_table[state])
  state, reward, done, info = env.step(action)


