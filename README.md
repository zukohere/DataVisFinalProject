# DataVisFinalProject
Final Project for Rutgers Data Visualization Bootcamp.
https://stocks-sentiment-wordcloud.herokuapp.com/


Purpose: To use sentiment analysis to create an informative visualization regarding the positive vs. negative news buzz around any stock in the S&P 500.

This project entails the following phases.
1. Data ETL/Cleanup and Sentiment Analysis Model Creation. (Jupyter Notebook DataCleanAndModel.ipynb)
2. Data Validation and Exploration. (Jupyter Notebook DataExploration.ipynb)
3. Development of a JSON File for Visualization Development. (Jupyter Notebook jsonFileDevelopment.ipynb)
4. Flask App Creation and Deployment. (wordcloud.js, wordcloud.py, app.py and others)


## 1. Data ETL/Cleanup and Sentiment Analysis Model Creation. (Jupyter Notebook DataCleanAndModel.ipynb)
The dataset used to create the model was obtained from http://help.sentiment140.com/for-students/ and cleaned using a method similar to the one used in https://towardsdatascience.com/another-twitter-sentiment-analysis-bb5b01ebad90. The dataset entails 1.6 Million tweets with sentiment marked as 0 for negative, 4 for positive (later translated to 0 and 1). 

Tweets from the dataset are expected to be 140 characters long, but using a box plot to visualize character lengths demonstrates this is not the case.

![Box-pre-clean](static\Resources\Box_pre-clean.png)

Cleaning functions were used to handle HTML decoding, mentions with @, URL links, UTF-8 BOM (Byte Order Mark), and hastags/numbers. The post-clean visualization appears as expected.

![Box-post-clean](static\Resources\Box_post-clean.png)

The sentiment analysis model creation was performed using the sklearn and textblob libraries. The logistical regression model recommended by the literature was not able to achieve convergence. A Multinomial Naive Bayes model was chosen instead, as it may be a good fit for the application (https://scikit-learn.org/stable/modules/naive_bayes.html). The confusion matrix is listed below. And the model is stored as sentiment.joblib to be called later.

![Conf-Matrix](static\Resources\Confusion-Matrix.png)

## 2. Data Validation and Exploration. (Jupyter Notebook DataExploration.ipynb)
Next, a notebook was created to explore the how the model would interpret headlines and blurbs from a google search for a stock symbol. The notebook randomly samples from the would-be complete headline/blurb dataset and writes the sample and sentiments to csv. After all, news articles about stock are not tweets. However, the model was sufficient to partition the headlines/blurbs into positive or negative with some utility.

![Sample-sentiment](static\Resources\Sample-Sentiment.png)

## 3. Development of a JSON File for Visualization Development. (Jupyter Notebook jsonFileDevelopment.ipynb)
To build the visualizaiton, a JSON file was created so that the datasource was static until it was time to build the app framework. The JSON file structure needed the following elements:
* An overall assessment of positivity of all headline/blurbs related to the stock
* A list of records of only relevant words, counts, articles where they appear and the sentiments of those articles.

The data was pre-processed using spacy to remove stop words and drill down to only relevant items. The JSON file structure (ex: jsonsample.txt) was created with the javascript wordcloud layout in mind.

## 4. Flask App Creation and Deployment. (wordcloud.js, wordcloud.py, app.py and others)
The D3 word cloud is modified from the layout found at https://www.d3-graph-gallery.com/graph/wordcloud_size.html. The app is deployed on heroku. The user can select any stock form the S&P 500 dropdown menu to display a word cloud. Words are sized based on frequency of use and colored based on the how often the sentiment of the articles that they appear in is positive or negative. Clicking any word will list the article links and their respective sentiments to allow the user to continue their research. An overall positivity rating for the stock (ie. how many of its articles are positive out of total) appears above the cloud.

![Screenshot](static\Resources\Screenshot.png)