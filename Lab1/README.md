# Spam detection using a naive Bayes classifier

This is lab one for Ling 165, working with Naive Bayes classifiers. This is an example of a very simple classifier, used to distinguish between spam and ham. It works off of subject lines only and applies add-one smoothing. 

Spam/ham data was provided to the class, presumably from the "spam_assassin" open source project.


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
python spamFinder.py --train \path\to\train\file --test \path\to\test\file
```

Output will be text file named "testOutput.txt" and will list precision and recall of tests

## Notes regarding smoothing

In the assignment details, Add-one smoothing is requested.

## Authors

* **Robert Trout** - *Initial work* - (https://github.com/rjtrout)

## Acknowledgments

* Lots of help from Professor Koo, with some code from his previous work and instruction

