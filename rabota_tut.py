import codecs
import time
import requests
from bs4 import BeautifulSoup as BS

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'}

def parser(query=''):
    page = 0
    jobs = []
    is_next_page = True
    while is_next_page:
        time.sleep(2)
        base_url = 'https://jobs.tut.by/search/vacancy?area=1002&search_period=3&order_by=publication_time&clusters=true&currency_code=BYR&search_field=name&text={}&page={}'.format(query, page)
        req = session.get(base_url, headers=headers)
        bs_obj = BS(req.content, 'html.parser')
        vac_list = bs_obj.find_all('div', attrs={'class':'vacancy-serp-item'})
        pagination = bs_obj.find('a', attrs={'class': 'HH-Pager-Controls-Next'})
        for vac in vac_list:
            title = vac.find('a', attrs={'class':'bloko-link'}).text
            href = vac.find('a', attrs={'class':'bloko-link'})['href']
            organization = vac.find('a', attrs={'class': 'bloko-link', 'data-qa':'vacancy-serp__vacancy-employer'}).text
            salary = '---'
            salary_text = vac.find('div', attrs={'class': 'vacancy-serp-item__compensation'})
            if salary_text:
                salary = salary_text.text
            jobs.append({
                'href': href,
                'title': title,
                'salary': salary,
                'organization': organization,
            })
        if pagination:
            page+=1
        else:
            is_next_page = False
    return jobs

if __name__ == "__main__":
    import pprint
    pprint.pprint(parser('js'))
