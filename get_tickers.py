from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen

class Get_Tickers:

    def __init__(self):
        pass
    
    # returns a list of penny stock tickers that are top gainers
    def penny_stocks(self):
        # url = 'https://swing-trading.org/penny-stocks/'
        url = 'https://penny-stocks.co/gainers/'

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        soup = bs(webpage, "html.parser")
        table = soup.find('table', attrs = {'class','styled'})


        # slicing array starting at 0 ending at the end of the array, go by every 7th step
        rows = table.find_all('td')
        # tickers = rows[:len(rows):7]
        tickers = rows[:len(rows):8]
        for i, ticker in enumerate(tickers):
            tickers[i] = ticker.get_text()

        return tickers

