# POS tagger utilizing the Viterbi algorithm

This is lab two for Ling 165, working with the Viterbi algorithm. This uses a bigram classifier to label POS for tokens. Markov assumptions have been made. The dictionaries containing word emission probabilities and tag transition probabilities have been provided to the class to use. A test set of words plus answers have been provided as well.  

## Getting Started

Just copy to your desktop and run. Make sure brown.test and brown.test.answers or equivalent files are specified in your command. Test files should be one sentence per line, each token separated by whitespace. Answer documents should have each token labeled with a POS, delimited by "_#_". The tags should come from those that appear in A.pickle. Make sure that A.pickle and B.pickle are present in the folder, as those locations are hard-coded in.

### Prerequisites

What things you need to install the software and how to install them

```
python 2.7
```
Explaining how to install python is slightly beyond the scope of this assignment. 

## Running the tests

In order to run the program, run the following command
```
python posClassifer.py --test \path\to\test\file --answer \path\to\answer\file
```

Output will be text file named "testOutput.txt" and will list tag accuracy.

## Authors

* **Robert Trout** - *Initial work* - (https://github.com/rjtrout)

## Acknowledgments

* Lots of help from Professor Koo, with some code from his previous work and instruction

