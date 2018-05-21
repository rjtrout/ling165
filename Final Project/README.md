# Final Project, utilizing SVD for Movie Recommendations

This is final Project for Ling 165. I have elected to create a movie recommendations engine with tf-idf, truncated SVD, and LDA. 

Please refer to the paper for the details of how the truncated SVD and LDA work.

## Getting Started

Just copy to your desktop and run. All needed files are included, including pickles. If you would like to re-run the program to recreate the matricies, just delete the pickles from their folder.

Test plots have already been provided under the /plotTest, however if you would like to test your own, paste the plot, the name of the movie/book, and then the year of publication into a .txt file. All fields should be seperated by a newline character. 

### Prerequisites

What things you need to install the software and how to install them

```
python 2.7
```
Explaining how to install python is slightly beyond the scope of this assignment. 

## Running the tests

In order to run the first program, run the following command.
```
python plotCompare.py <location of all plots> <location of Test Plots>
```
A sample command is provided below.
```
python plotCompare.py ./plots/ ./plotTest/
```
Output will be the terminal and text output

## Authors

* **Robert Trout** - *Initial work* - (https://github.com/rjtrout)

## Acknowledgments

* Lots of help from Professor Koo, with some code from his previous work and instruction

