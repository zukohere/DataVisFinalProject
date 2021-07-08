def stock_list():    
    import requests
    import urllib.request
    from bs4 import BeautifulSoup
    import pandas as pd

    table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    SP_list = table[0]
    SP_list=[{"symbol": row["Symbol"], "name": row["Security"]+" ("+row["Symbol"]+")"} for index, row in SP_list.iterrows()]
    return SP_list