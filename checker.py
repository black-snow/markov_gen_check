#!/usr/bin/env python
from pathlib import Path
import sys
import regex
from functools import reduce
# let's use this faster 3rd party lib instead of our own
import markovify

#
# Pass -e to score some examples.
# Otherwise examples will be read from the commandline.
# The input should be 3 words or more.
#

tests = []
if len(sys.argv) > 1 and sys.argv[1] == '-e':
    tests = [
        'go term(ch, float64(k))',
        'public static final String',
        'HashMap<String, String> map = new HashMap<>();',
        '$this->run()'
    ]

def split_code(text):
    '''Split given code (text) by newlines, braces, semicolons, white space, arrows'''
    return list(filter(lambda x: not x == '', regex.split(r'([\n()\[\];.]|=>|->|\s{4,})| ', text)))

def load_model(model, state_size=2):
    '''e.g. java, go, php'''
    path = Path('code') / model
    files = path.glob('**/*.' + model)
    corpus = []
    for file in files:
        try:
            with open(file, 'r') as f:
                corpus.append(f.read())
        except:
            print('skipping {0} due to error'.format(file))
    corpus = list(map(lambda x: split_code(x), corpus))
    return markovify.Text('', state_size=state_size, parsed_sentences=corpus, retain_original=False)

def has_words(model, words):
    '''Check whether given n-tuple appears in the model or not.'''
    return tuple(words) in model.chain.model

def any_match(model, word):
    for key_tuple in dict.keys(text_model.chain.model):
        if key_tuple[0] == word:
            return True
    return False

def get_touples_starting_with(model, word):
    tuples = []
    for key_tuple in dict.keys(text_model.chain.model):
        if key_tuple[0] == word:
            tuples.append(key_tuple)
    return tuples

# in order to check if the given string belongs to the model we'll
# walk through the tokens and see if and with what probability the
# model could've generated the sequence

# we'll use state size = 2
STATE_SIZE = 2

def compute_direct_match_score(model, words):
    '''Number of exact matches / number of checks.'''
    if type(words) == str:
        words = split_code(words)

    num_checks = len(words) - 1
    score = 0
    for i in range(0, len(words) - 1):
        if ((words[i], words[i + 1]) in model.chain.model):
            score += 1
    return score / num_checks

def compute_prob_score(model, words):
    '''Compute a probability score for given words.'''
    if type(words) == str:
        words = split_code(words)
    num_checks = len(words) - 1
    score = 0
    for i in range(0, len(words) - 1):
        local_score = 0
        local_checks = 0
        for tuples in dict.keys(model.chain.model):
            if tuples[STATE_SIZE - 1] == words[i] and words[i + 1] in model.chain.model[tuples]:
                local_sum = reduce(lambda a, b: a + b, dict.values(model.chain.model[tuples]))
                local_score += (model.chain.model[tuples][words[i + 1]] / local_sum)
                local_checks += 1
        if local_checks > 0:
            score += local_score / local_checks
    return score / num_checks

def score(models, text):
    '''Score given models {name: model}.'''
    results = {k: compute_prob_score(v, text) for k, v in models.items()}
    scores = sorted(results.items(), key=lambda x: x[1])
    top = scores.pop()
    print("That's probably -- {0} -- ({1:1.6f} %)".format(top[0], top[1] * 100))
    for score in sorted(scores, reverse=True, key=lambda x: x[1]):
        print("  or {0} ({1:1.6f} %)".format(score[0], score[1] * 100))


# compute the models
java_model = load_model('java', state_size=STATE_SIZE)
go_model = load_model('go', state_size=STATE_SIZE)
php_model = load_model('php', state_size=STATE_SIZE)

models = {'java': java_model, 'go': go_model, 'php': php_model}

if len(tests):
    for test in tests:
        print('\n', test)
        score(models, test)
else:
    try:
        while True:
            l = input(':')
            score(models, l)
    except KeyboardInterrupt:
        print('bb')
quit(0)
