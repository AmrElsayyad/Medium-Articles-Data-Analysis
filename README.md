# Medium Articles Data Analysis

## Table of Contents

0. [Status](#status)
1. [Installation](#installation)
2. [Project Motivation](#motivation)
3. [File Descriptions](#files)
4. [How to Use Jupyter Notebooks](#HowToUse)
5. [Results](#results)
6. [Licensing, Authors, and Acknowledgements](#licensing)

## Status <a name="status"></a>

Project is not yet deployed.

## Installation <a name="installation"></a>

You need to have [Python](https://www.python.org/downloads/) (>= 3.9) installed.
Then make sure to install the following libraries:
* NumPy
* Pandas
* SciKit-learn
* Matplotlib
* Seaborn
* JupyterLab

Additionally, if you want to use the webscraping library you will need the following:
* [Firefox](https://www.mozilla.org/en-US/firefox/new/)
* VPN (Here is what I used: [ProtonVPN](https://protonvpn.com/download))
* Selenium (Python Package)
* [Geckodriver](https://github.com/mozilla/geckodriver/releases) extracted in [Python directory](file://%userprofile%\AppData\Local\Programs\Python\Python39).

## Project Motivation<a name="motivation"></a>

I was thinking to start writing on [Medium](https://medium.com/), but as I always have been, I was afraid of failure. So, I started doing what I always do in this situation, make a plan.

So, I started following [CRISP-SM](https://www.datascience-pm.com/crisp-dm-2/):

1. Business Understanding
	* My main question is **What are the factors that make an article more clappable?**
	* Does the word choice for the title have an impact on the article clappability?
	* Can I predict the number of claps and responses based on the other factors?


2. Data Understanding
	
	I collected some data from the most clapped medium articles, according to this website [Top Medium Stories](https://topmediumstories.com/). I know the data might not be updated, but it was the best choice I have. I haven't found a link on medium that shows the most clapped articles of all time, only currently trending. 
	
	The features I collected:
	* Article link
	* Title
	* Header image link
	* Number of images in the article
	* Number of h1 and h2 headers
	* Number of paragraphs
	* Average word count per paragraph
	* Number of quotes
	* Publication name
	* Writer name
	* Date of the article
	* Read time in minutes
	* Number of claps
	* Number of responses


3. Data Preparation
4. Modeling
5. Evaluation
6. Deployment

## File Descriptions <a name="files"></a>



## How to Use Jupyter Notebooks <a name="HowToUse"></a>

1. Clone the project to your local machine.
2. Open the project folder.
3. In the address bar, type `cmd` then press Enter.
4. In the Command window type `jupyter notebook` then press enter.

Now you should have jupyter running in your default browser, you can now explore the notebooks.

**Note:**	You have to keep the cmd window open, in order to keep the jupyter session running.

## Results<a name="results"></a>

The main findings of the code can be found at the post available [here]().

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

LICENSE file is included in the main files.

