from flask import Flask, render_template, jsonify
from wordcloud import stock_wordcloud
from stock_list import stock_list
# Flask Setup
app = Flask(__name__, static_url_path='/static')

# app routes
@app.route('/')
def home():

    return render_template("index.html", list = stock_list())

@app.route("/stock-page/")
@app.route("/stock-page/<stock_name>")
def stock_page(stock_name=None):
    
    # If there is no selection, 
    if not stock_name:
        stock_name = "AMZN"
        # Webcrape for artricles and Jasonify results
        return jsonify(stock_wordcloud(stock_name))
    
    else:
        # Webcrape for artricles and Jasonify results
        return jsonify(stock_wordcloud(stock_name))
        

if __name__ == "__main__":
    app.run(debug=True)
