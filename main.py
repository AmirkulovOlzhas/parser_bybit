import pandas as pd
from bs4 import BeautifulSoup as bs
from config import cookies, headers

import requests
from time import sleep

from selenium import webdriver

params = {
    'page': '1',
}

root = "https://announcements.bybit.com"
url = "https://announcements.bybit.com/en-US/"

def get_html_selenium(page):
      browser = webdriver.Chrome()
      browser.get(url+'?page='+page)
      sleep(2)
      html = browser.page_source
      html = bs(html, 'html.parser')
      return html

def get_html(page):
      params['page'] = page
      response = requests.get(url, params=params, cookies=cookies, headers=headers)
      
      html = bs(response.content, 'html.parser')
      return html


def to_datetime(date, page):
      try:
            date = pd.to_datetime(date, errors='coerce').strftime('%Y-%m-%d')
            return True, date
      except:
            html = get_html_selenium(str(page))
            page_data = pd.DataFrame(columns=['date', 'title', 'link', 'page'])
            for el in html.select('.article-list')[0].find_all('a', href=True):
                  title = el.find('span').text
                  date = el.find('div', 'article-item-date').text
                  date = pd.to_datetime(date, errors='coerce').strftime('%Y-%m-%d')
                  link = root + el['href']
                  dict = {'date': date, 'title': title, 'link': link, 'page': page}
                  page_data.loc[len(page_data)] = dict
            return False, page_data


def scarp_page(page):
      html = get_html(str(page))

      
      page_data = pd.DataFrame(columns=['date', 'title', 'link', 'page'])
      for el in html.select('.article-list')[0].find_all('a', href=True):
            title = el.find('span').text
            date = el.find('div', 'article-item-date').text
            link = root + el['href']

            condition, retr = to_datetime(date, page)
            if condition:
                  dict = {'date': retr, 'title': title, 'link': link, 'page': page}
                  page_data.loc[len(page_data)] = dict
            else:
                  page_data = retr
                  break
      return page_data


def scarp_all():
      html = get_html('1')
      pages = int(html.select('.ant-pagination-item')[-1].text)

      page = 1

      data = pd.DataFrame(columns=['date', 'title', 'link', 'page'])

      while page-1 != pages:
            page_data = scarp_page(page)
            data = pd.concat([data, page_data])
            print(f'page = {page} of {pages}')
            if page == 126:
                  break
            page += 1
      return data


def check_first_page():
      # page_data = scarp_page(1)
      page_data = pd.DataFrame(columns=['date', 'title', 'link', 'page'])
      page_data.loc[0] = ['2023-10-20', 'test', 'test', '1']
      # print(type(page_data))
      older_data = pd.read_csv('csv/data.csv')
      for i, row in page_data.iterrows():
            # print(row)
            old_elements = older_data[older_data['date'] == row['date']]
            if (old_elements.empty) or (row['title'] not in old_elements['title'].values):
                  print(row)
                  older_data.loc[len(older_data)] = row
                  older_data = older_data.sort_values(by=['date'], ascending=False)
                  older_data.to_csv('csv/updated.csv', index=False)
            


def data_to_csv():
      data = scarp_all()
      data = data.sort_values(by=['date'], ascending=False)
      data.to_csv('csv/data.csv', index=False)


# while True:
# sleep(0.1)
check_first_page()



