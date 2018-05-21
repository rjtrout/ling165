# Edit distance and string alignment, EM algo

This is lab four for Ling 165, which is a mix of two different subjects. The first is Edit distance and the second string alignment/EM algo. 

For the first task:
Write a program that calculates the minimal edit distance between two strings of letters.

For the second task:
Write a program that runs the EM algorithm to estimate Spanish-to-English word translation probabilities.
Stop the EM algo with the first the following stopping criteria:
	1) 100 iterations
	2) log-likelihood of the training data increases by less than 0.01

## Getting Started

Just copy to your desktop and run. All needed files are included except for mathplotlib. Please see below for how to install that.

### Prerequisites

What things you need to install the software and how to install them

```
python 2.7
```
Explaining how to install python is slightly beyond the scope of this assignment. 

Make sure that you have mathplotlib installed before running
```
pip install mathplotlib
```

## Running the tests

In order to run the first program, run the following command.
```
python lab4_task1.py <firstWord> <secondWord>
```
A sample command is provided below.
```
python lab4_task1.py bus bums 
```
Output will be the terminal

In order to run the second program, run the following command.
```
python lab4_task2.py
```

This will work through the iterations and save a png file with a plot with how the word probabilities change for the Spanish word "resto" over time. 

## Authors

* **Robert Trout** - *Initial work* - (https://github.com/rjtrout)

## Acknowledgments

* Lots of help from Professor Koo, with some code from his previous work and instruction

