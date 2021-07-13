
def stock_wordcloud(stock_name):
    # https://medium.com/illumination/scraping-news-and-creating-a-word-cloud-in-python-10ea312c49ba
    import requests
    import urllib.request
    import time
    import spacy
    from bs4 import BeautifulSoup
    import pandas as pd
    from joblib import dump, load
    clf = load('sentiment.joblib')
    
    #To translate sentiments as 0,1 into English
    sentdict = {0: "Negative", 1: "Positive"}

    # Create a dictionary of stock symbols and company names

    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    SP_dict = table[0].set_index('Symbol')
    SP_dict=SP_dict['Security'].to_dict()

    # Set up webscrape of google artciles. 
    numResults = 100
    url = f'https://www.google.com/search?q=stock+symbol+{stock_name}&tbm=nws&hl=en&num={str(numResults)}'
    # https://www.google.com/search?q=stock+symbol+AMZN&tbm=nws&hl=en&num=50

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Get the links, headline and description text
    results = soup.find_all("div", attrs={"class": "ZINbbc"})
    headlines = []
    descriptions = []
    links = []
    combined = []
    for result in results:
        try:
            headline = result.find("div", attrs={"class": "vvjwJb"}).get_text()
            if headline != "":
                headlines.append(headline)
                links.append("google.com"+result.a["href"])
            description = result.find(
                "div", attrs={"class": "s3v9rd"}).get_text()
            if description != "":
                # remove the "1 day ago" etc.
                description = description[description.find("·")+1:]
                descriptions.append(description)
            combined.append(headline+" "+description)
        except:
            continue
    # Add sentiments using the stored model.
    sentiments = [sentdict[clf.predict([text])[0]] for text in combined]
    # flattens string
    text_h = " ".join(headlines)
    text_p = " ".join(descriptions)
    text = text_h + text_p

    sp = spacy.load('en_core_web_sm')
    doc = sp(text)

    #Only allow valid tokens which are not stop words
    # and punctuation symbols.https://realpython.com/natural-language-processing-spacy-python/#word-frequency
    def is_token_allowed(token):
        if (not token or token.is_stop or token.is_punct or not token.pos_ in ["ADJ"]
            or token.lemma_.strip().lower() in ["inc", "stock", "stocks", "price", "market", stock_name.lower()]+
            [word.lower() for word in SP_dict[stock_name].lower().replace(".com","").split()]):
            return False
        else:
            return True

    def preprocess_token(token):
            # Reduce token to its lowercase lemma form
        return token.lemma_.strip().lower()

    pos_dict={}
    for token in doc:
        if is_token_allowed(token):
            pos_dict[preprocess_token(token)]=token.pos_

    # Set up list of dictionaries with words, pos, counts
    from collections import Counter
    word_freq = Counter([token.lemma_.strip().lower()
                         for token in doc if not token.is_stop and not token.is_punct])
    words = [{"Words": key, "POS": pos_dict[key], "Counts": word_freq[key]}
             for key in pos_dict.keys()]


    # Add headlines, links, and sentiment
    for item in words:
        headline_dict = {}
        sentcount_pos = 0
        sentcount_neg = 0
        for i in range(len(headlines)-1):
            if item["Words"] in descriptions[i].lower() or item["Words"] in headlines[i].lower():
                headline_dict[headlines[i]] = [links[i], sentiments[i]]
                if sentiments[i] == "Negative":
                    sentcount_neg+=1
                else:
                    sentcount_pos+=1
                word_score = sentcount_pos/(sentcount_pos+sentcount_neg)
        item.update({"links": headline_dict, "WordScore": word_score})
    
    # Add overall positivity rating for stock
    words = [{"Pos_Neg":sum([clf.predict([text])[0] for text in combined])/len(combined),"cloudData": words}]
    # Send list to be jsonified
    return(words)
