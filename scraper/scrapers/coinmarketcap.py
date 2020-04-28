from bs4 import BeautifulSoup as bs
import requests


def fetch(url):
	r = requests.get(url)
	#soup = bs(r.text, 'lxml')
	soup = bs(r.text)
	value = soup.find('span', class_ = 'cmc-details-panel-price__price').text.replace("$", "")
	data = {
	#'url' : url,
	'value' : value,
	}

	return data

