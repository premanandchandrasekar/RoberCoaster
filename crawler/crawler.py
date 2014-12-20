import os
import json
import sys
import httplib
import urllib2
from urlparse import urlparse
import BeautifulSoup


def crawler():
	urls = []
	crawled_data = []
	for url in urls:
		to_crawle_url = url
		pagesource = urllib2.urlopen(to_crawle_url)
        source = pagesource.read()
        soup = BeautifulSoup.BeautifulSoup(source)
        review_data = soup.findAll("div", { "class" : "fclear fk-review fk-position-relative line " })
        product_name = 'puma'
        for data in review_data:
        	prossed_data = {}
        	prossed_data['star'] = ((data.findAll("div", { "class" : "fk-stars" }))[0]['title']).strip()[0]
        	prossed_data['date'] = ((data.findAll("div", { "class" : "date line fk-font-small" })[0]).contents[0]).strip()
        	prossed_data['description'] = (data.findAll("span", { "class" : "review-text" }))[0].text
        	crawled_data.append(prossed_data)

	f = open('/home/bharan/DataHackthon/PaypalDataHack/reviews/shoes/'+product_name+'.json', 'w')
	if crawled_data:
	    f.write(json.dumps(crawled_data, indent=4))
	    f.close()


if __name__ == "__main__":
	crawler()


