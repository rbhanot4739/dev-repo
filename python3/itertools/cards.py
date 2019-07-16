import itertools as it
import random

suits = ("Club", "Spade", "Diamond", "Heart")
cards = ("A", "K", "Q", "J", "2", "3", "4", "5", "6", "7", "8", "9", "10")
deck = it.product(cards, suits)


def shuffle_deck(deck):
    deck = list(deck)
    for _ in range(10):
        random.shuffle(deck)
    return iter(deck)


def cut_cards(shuffled, index):
    iter1, iter2 = it.tee(shuffled, 2)
    top = it.islice(iter1, index)
    bottom = it.islice(iter2, index, None)
    new_deck = it.chain(bottom, top)
    return new_deck


shuffled = shuffle_deck(deck)
n = 30
print(*cut_cards(shuffled, n))
