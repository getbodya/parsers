import codecs
import time
import requests
from bs4 import BeautifulSoup as bs

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}
query = 'Программист' # запрос поиска по сайту

def parser(query=''):
    page = 1
    jobs = []
    is_next_page = True

    while is_next_page:
        time.sleep(2)
        base_url = 'https://praca.by/search/vacancies/?page={}&search[query]={}&search[query-text-params][headline]=0'.format(page,query)
        req = session.get(base_url, headers=headers)
        bs_obj = bs(req.content, 'html.parser')
        vac_list = bs_obj.find_all('li', attrs={'class':'vac-small'})
        pagination = bs_obj.find('ul', attrs={'class': 'pagination__list'})
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
        if pagination:
            page +=1
        else:
            is_next_page = False
    print('==============================================================')
    
    print('==============================================================')
    
    print('==============================================================')
    
    print('==============================================================')
    print(len(jobs))
    return jobs

if __name__ == "__main__":
    import pprint
    pprint.pprint(parser('мастер'))