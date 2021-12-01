# https://stackoverflow.com/questions/46271528/counting-words-inside-a-webpage

from collections import Counter
from string import punctuation
import re

import requests
from bs4 import BeautifulSoup
from googlesearch import search


# loop news function to display latest news
# check if article already displayed
def symbol_search(w):
    # Look for Stock Symbol Strings and other relevant strings ( Upper or lowercase)

    # pre-processing then print
    r = re.findall('([A-Z][a-z]+)', w)
    t = re.match('[A-Z]+$', w)
    string_check = re.compile('[1234567890.@_!#$%^&*()<>?/\|}{~:''"]')

    exclude = ["TV", "U.S", "I", "A", "CA", "HBO", "'I", "II'", "U.K", "FACTSET", "AZ", "‘I"]
    if w in exclude or string_check.search(w) or w.__len__() > 6:
        return None

    if w.isupper():
        w = w.replace('(', '').replace(')', '')
        w = w.replace('NASDAQ:', '')
        w = w.replace(":", " ")
        w = w.replace('NYSE', '')
        w = w.replace("'", " ")
        w = w.replace("[", " ").replace("]", " ")
        w = w.replace("’", "").replace("‘", "")
        print(" Symbol:", w)


def news():
    num_websites = 5
    amount_of_words = 1000
    query = "latest stock news"
    
    # search google query
    # older python version use (tld="co.in", num=num_websites, stop=num_websites,) as parameters + more
    # self.search_ = search(query, num_results=num_websites, lang="en")
    search_ = search(query, tld="co.in", num=num_websites, stop=num_websites)
    # print(self.search_)

    for s in search_:
        # start = timeit.timeit()
        print("\n", s)
        try:
            r = requests.get(s, timeout=3)
            #print(r)
            if r.status_code != requests.codes.ok:
                print(" Page request not OK ", r)
            # r = urlopen(path)

            # website soup
            soup = BeautifulSoup(r.text, features="html.parser")

            # retrieve links from site and create list of url's
            links = soup.find_all('a')
            print(" Total Links Found:", links.__len__())
            # print(links)

            link_list = []
            for link in links:
                link_ = link.get('href')
                if link_:
                    # print(link_)
                    link_list.append(link_)

            print(link_list)

            # We get the words within paragraphs
            text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
            c_p = Counter((x.rstrip(punctuation) for y in text_p for x in y.split()))

            # We get the words within divs
            text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
            c_div = Counter((x.rstrip(punctuation) for y in text_div for x in y.split()))

            # We sum the two counters and get a list with words count from most to less common
            words = c_div + c_p
            #print("Words:", words)
            # list_most_common_words = words.most_common(amount_of_words)
            # print(list_most_common_words)

            # look for stock symbols
            for w in c_p:
                symbol_search(w)

            for w in c_div:
                symbol_search(w)

        except Exception as e:
            print(e)


news()
