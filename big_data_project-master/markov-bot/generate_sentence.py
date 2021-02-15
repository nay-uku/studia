#!/usr/bin/python3
import argparse
import random
from model import *


def get_random_first_word():
    words = Word.nodes.filter(name__regex='^[A-Z].*')
    return random.choice(words)


def get_random_next_word(word):
    return random.choice(word.next_words)


def generate_sentence(n_words):
    word = get_random_first_word()
    text = word.name
    for i in range(1, n_words):
        word = get_random_next_word(word)
        text += ' ' + word.name
        if word.next_words is None:
            return text
    return text


parser = argparse.ArgumentParser(description='Markov-bot')
parser.add_argument('n_words', nargs='?', type=int, default=20,
                    help='Maksymalna długość generowanej sentencji.')
args = parser.parse_args()

print(generate_sentence(args.n_words))
