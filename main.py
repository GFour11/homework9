import requests
import json
from bs4 import BeautifulSoup



url = 'http://quotes.toscrape.com'


def parse_authors():
    json_ = []
    new_url = url
    while True:
        connect = requests.get(new_url)
        soup = BeautifulSoup(connect.content, 'html.parser')
        links = soup.select("div[class = quote] span a")
        urls = []
        for link in links:
            urls.append(link['href'])
        for ur in urls:
            conn = requests.get(url+ur)
            soup = BeautifulSoup(conn.content, 'html.parser')
            div_tags = soup.select("div.author-details")
            for div_tag in div_tags:
                author= list(div_tag.select_one('h3.author-title'))[0]
                born = div_tag.select_one('span.author-born-date').text
                born_location = div_tag.select_one('span.author-born-location').text
                description = div_tag.select_one('div.author-description').text.replace('\n', '').strip()
                result = {'fullname':author, 'born_date': born, 'born_location': born_location,'description': description}
                if len(json_)==0:
                    json_.append(result)
                flag = True
                for i in json_:
                    if result['fullname'] == i['fullname']:
                       flag = False
                if flag:
                    json_.append(result)
        try:
            connect = requests.get(new_url)
            soup = BeautifulSoup(connect.content, 'html.parser')
            next_url = soup.select('nav li[class=next] a')[0]['href']
            new_url= url + next_url
        except IndexError:
            break
    with open('authors.json', 'w') as fd:
        json.dump(json_, fd)


def parse_quotes():
    json_ = []
    new_url = url
    while True:
        connect = requests.get(new_url)
        soup = BeautifulSoup(connect.content, 'html.parser')
        selection = soup.select('div[class = quote]')
        for object in selection:
            quote = object.select('span[class=text]')[0].text.strip()
            author = object.select('span small[class=author]')[0].text
            tags = object.select('div[class=tags] a[class=tag]')
            tag = ''
            for i in tags:
                tag+=f'{i.text} '
            tag = tag.split(' ')
            tag.pop(-1)
            json_.append({'quote': quote, 'author': author, 'tags':tag})
        try:
            next_url = soup.select('nav li[class=next] a')[0]['href']
            new_url= url + next_url
        except IndexError:
            break
    with open('quotes.json', 'w', encoding='utf-8') as fd:
        json.dump(json_, fd, ensure_ascii= False)




if __name__ == '__main__':
    parse_authors()
    parse_quotes()