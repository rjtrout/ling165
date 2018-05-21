# Ngram sentence generator

This is lab one for Ling 165, working with Ngrams. In this assignmet, you are asked to create a sentence generator that takes a source text, divides it accoridng to the ngram of the user's choice. 

The source material was provided with this assigment as "bullshit.txt." I have supplemented that with an archive of Donald Trump's tweets in addition.


## Getting Started

Just copy to your desktop and give it a whirl

### Prerequisites

What things you need to install the software and how to install them

```
python 2.7
```
Explaining how to install python is slightly beyond the scope of this assignment. 

## Running the tests

In order to run the program, run the following command
```
python ngramGen.py \path\to\source\file ngramSize DesiredSentences
```


You can specify what file to draw as a source, what size nGram to use, and how many sentence you would like, in that order. An example would look like:

```
pythong ngramGen.py bullshit.txt 3 4
```

Output will be printed to the console and a  text file named "sentenceOutput.txt"

## Notes regarding source material

If you would like to add your own source material, have each sentence on its own line and each word/punctuation piece separated by spaces.

## Authors

* **Robert Trout** - *Initial work* - (https://github.com/rjtrout)

## Acknowledgments

* Lots of help from Professor Koo, with some code from his previous work and instruction

