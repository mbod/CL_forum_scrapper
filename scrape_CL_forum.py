
#######################################
#  Scrape Craigslist forums for posts #
#  containing a specified set of      #
#  keywords                           #
#######################################

'''
mbod 0.1 - 2/16/17 - initial setup in notebook and pull for 'scamming' kws
mbod 0.2 - 4/17/17 - create script from notebook code test on second set
'''

import requests
from bs4 import BeautifulSoup, Tag, BeautifulStoneSoup
import random
import time
import re
import os

import pickle

# ------------- FUNCTIONS -------------------

def do_search(url):
    '''
      take search url (including params) and submit
      request to Craigslist and retrieve a result set
      follow 'next' pagination until there are no more pages
    '''

    next=None
    # add in exception handling
    resp = requests.get(url)
    doc = BeautifulSoup(resp.text)

    results = doc.body.find('section', {'class': 'searchresults'})

    #pagination
    try:
        paging = results.find('div', {'class':'paginator'})
    except:
        return [],None

    has_next = paging.find('div',{'class': 'next'}).findAll('a')
    if len(has_next)>0:
        print('next page of results is:', has_next[0])
        next = has_next[0].attrs['href']

    result_list=results.findAll('article',{'class':'searchresult'})
    print('current page has {} results for search term'.format(len(result_list)))

    return result_list, next




# ------------------------

kws = '''Scam, scams, scammed, scamming, scammer, scammers;
        fraud, frauds, defrauded, fraudster, fraudsters;
        con, cons, conned, conning, con artist, con artists;
        trick, tricks, tricked, tricking, trickster, tricksters;
        swindle, swindles, swindled, swindler, swindlers'''


kw_list=[i.lower() for k in kws.strip().split(';') for i in k.strip().split(', ')]


post2thread = {}
thread2posts = {}

search_URL = 'https://forums.craigslist.org/?act=RSR&forumID={}&SQ={}&resultsPerPage=100'
