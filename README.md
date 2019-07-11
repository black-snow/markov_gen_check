# Markov Chain lyrics generator and programming language classifier

## Requirements

* python 3.4 or higher
* pipenv
* lyrics in the lyrics folder (possibly crawled via the cralwer)
* code examples in the code/language-name folder (e.g. ./code/java) named *.language-name (e.g. chain.java)

## Installation

```bash
$ pipenv install
```

Fetch some lyrics examples via the crawler and put some code examples in the code folder. The structure for the code folder is:

```
- code
- |- java
- - |- example_code_at_any_depth.java
- - |- more_examples.java
- |- php
- - |- example.php
- |- go
- - |- example.go
```

I can't share the lyrics / code with you for they might be constrained by copyright laws. Please get your own.

## Usage

```bash
# always go into the virtualenv first
$ pipenv shell
# run the crawler
$ python crawl.py 'https://www.songtexte.com/artist/coldplay-3d6bde3.html' ./lyrics/coldplay
# run the generator
$ python generator.py ./lyrics/coldplay
# run the classifier reading from the command line
$ python checker.py
```
