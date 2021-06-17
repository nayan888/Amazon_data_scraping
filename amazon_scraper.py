from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random

def get_data(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
    'Referer': 'https://www.amazon.com/'
    }
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.text, 'lxml')
    return soup


def parse_data(soup):
    tabs_list = []
    items = soup.select('.s-border-bottom .a-spacing-medium')

    for item in items:
        tab_dict = {}  
        tab_dict['name'] = item.select_one('.a-color-base.a-text-normal').text
        try:
            tab_dict['ratings'] = item.select_one('.aok-align-bottom').text
            tab_dict['number of ratings'] = item.select_one('.a-size-small .a-size-base').text
        except:
            tab_dict['ratings'] = 0
            tab_dict['number of ratings'] = 0

        try: 
            tab_dict['price'] = float(item.select_one('.a-price-whole').text) + float(item.select_one('.a-price-fraction').text)/100
        except:
            tab_dict['price'] = 'Price not found'
        tabs_list.append(tab_dict)
    
    return tabs_list

base_url = 'https://www.amazon.com'
query_s = '/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011%2Cn%3A13896617011%2Cn%3A1232597011&dc&qid=1622960357&rnid=13896617011&ref=sr_nr_n_3'
page = 1
tabs = []

if __name__ == '__main__':
    while(query_s is not None):
        url = base_url + query_s
        print(f'Scraping page: {page}..')
        soup = get_data(url)
        tabs_list = parse_data(soup)
        # print(tabs_list)
        tabs.extend(tabs_list)
        try:
            query_s = soup.find('li', {'class': 'a-last'}).a['href']
        except:
            query_s = None
        wait = random.randint(5, 10)
        print(f'Waiting for {wait}s..')
        time.sleep(wait)
        if page == 20:
            break
        page += 1

    tabs_df = pd.DataFrame(tabs)
    print('Saving data..')
    tabs_df.to_csv('tabs_data.csv', index=False)