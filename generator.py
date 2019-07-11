#!/usr/bin/env python
import markovify
from pathlib import Path
import sys
import random

#
# Genrate a song text.
# Usage: python generator.py /path/to/lyrics
# Example: python generator.py ./lyrics/coldplay
#

path = Path(sys.argv[1])
files = path.glob('**/*.txt')

# build corpus
corpus = ''
for file in files:
    with open(file, 'r') as f:
        corpus += f.read() + '\n'

# model
text_model = markovify.NewlineText(corpus, state_size=2)

# let's play

verse_len = random.randint(8, 15)
chorus_len = random.randint(4, 10)

def gen_lines(n, model):
    return '\n'.join([model.make_sentence() for x in range(n)])

verses = [gen_lines(verse_len, text_model) for x in range(2)]
chorus = gen_lines(chorus_len, text_model)

# go
for verse in verses:
    print(verse, '\n\n', chorus, '\n\n')
