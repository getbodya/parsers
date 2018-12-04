import codecs
import time
import requests
from bs4 import BeautifulSoup as bs

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
query = 'Программист' # запрос поиска по сайту
jobs = []
page_urls = []

base_url = 'https://praca.by/search/vacancies/?search[query]='+query

def parser(query = 'Программист'):
    jobs = []
    page_urls = []
    base_url = 'https://praca.by/search/vacancies/?search[query]='+query
    req = session.get(base_url, headers=headers)
    page_urls.append(base_url)
    if req.status_code == 200:
        bs_obj = bs(req.content, 'html.parser')
        pagination = bs_obj.find('ul', attrs={'class': 'pagination__list'})
        pages = bs_obj.find_all('li', attrs={'class':'pagination__item'})
        if pages:
            for page in pages:
                url_2 = page.find('a')
                if url_2:
                    page_urls.append('https://praca.by/search/vacancies/' + page.a['href'])
        page_urls = set(page_urls)

    for url in page_urls:
        time.sleep(2)
        req = session.get(url, headers=headers)
        if req.status_code == 200:
            bs_obj = bs(req.content, 'html.parser')
            vac_list = bs_obj.find_all('li', attrs={'class':'vac-small'})
            for vac in vac_list:
                title = vac.find('a', attrs={'class':'vac-small__title'}).text
                href = vac.find('a', attrs={'class':'vac-small__title'})['href']
                organization = vac.find('a', attrs={'class': 'vac-small__organization'}).text
                salary = '---'
                if vac.find('span', attrs={'class': 'salary-dotted'}):
                    salary = vac.find('span', attrs={'class': 'salary-dotted'}).text
                jobs.append({
                    'href': href,
                    'title': title,
                    'salary': salary,
                    'organization': organization,
                })
    return jobs

if __name__ == "__main__":
    import pprint
    pprint.pprint(parser(''))