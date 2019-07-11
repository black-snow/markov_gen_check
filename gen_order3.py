#!/usr/bin/env python
import markovify
from pathlib import Path
import sys
import random

path = Path(sys.argv[1])
files = path.glob('**/*.txt')

# build corpus
corpus = ''
for file in files:
    with open(file, 'r') as f:
        corpus += f.read() + '\n'

# model
text_model = markovify.NewlineText(corpus, state_size=3)

print(text_model.make_sentence())
print(text_model.make_sentence())
print(text_model.make_sentence())
print(text_model.make_sentence())
