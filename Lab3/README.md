# Vector Space Models and SVD (Single Value Decomposition)

This is lab three for Ling 165, working with Vector Space Models. Given a set of vocab and data from the WSJ, we are asked to do the following: 

1) Find the top ten words in WSJ_0725 with the highest tf-idf scores.
2) Use SVD to get a lower-rank approx of the matrix to:
	i) Find top ten words similar to oil
	ii) Find top ten documents most relevant to a query consisting of the two words *oil* and *price*

## Getting Started

Just copy to your desktop and run. The WSJ samples and vocab has been provided, but you can designate which sample to analyze, how many top words to return, the k value of the lower-rank, and what query you would like. Please be advised, the sample you would like to return the top words from must be contained in the same folder as the rest of your corpus.

### Prerequisites

What things you need to install the software and how to install them

```
python 2.7
```
Explaining how to install python is slightly beyond the scope of this assignment. 

Make sure that you have numpy installed before running
```
pip install numpy
```

## Running the tests

In order to run the program, run the following command.
```
python vsm20180314.py --sample /PATH/TO/FILE/TO/ANALYZE --top NUM_TOP_WORDS --k K_VALUE --queryWord QUERY -vocab /PATH/TO/VOCAB/FILE --query QUERY TO MATCH DOCUMENTS
```
A sample command is provided below.
```
python vsm20180314.py --sample ./wsj/WSJ_0725 --top 10 --k 100 --queryWord oil --vocab vocab.select --query oil price  
```
Output will be text file named "testOutput.txt".

## Authors

* **Robert Trout** - *Initial work* - (https://github.com/rjtrout)

## Acknowledgments

* Lots of help from Professor Koo, with some code from his previous work and instruction

