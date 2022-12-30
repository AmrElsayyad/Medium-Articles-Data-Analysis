# Medium Articles Data Analysis

## Table of Contents

0. [Status](#status)
1. [Installation](#installation)
2. [Project Motivation](#motivation)

## Status <a id="status"></a>

Project is not yet deployed.

## Installation <a id="installation"></a>

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

## Project Motivation<a id="motivation"></a>

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

