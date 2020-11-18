from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import random
from itertools import islice

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    # Quotes site
    url_quotes = "https://wisdomquotes.com/life-quotes/"
    source_quote = requests.get(url_quotes).text
    soup_quote = BeautifulSoup(source_quote, 'lxml')
    quotes = soup_quote.find_all('blockquote')
    quote = random.choice(quotes)

    # World news from bbc
    url_world = "https://www.bbc.com/news/world"
    source_world = requests.get(url_world).text
    soup_world = BeautifulSoup(source_world, 'lxml')
    bbc = "https://bbc.com"

    five_img = []
    five_headlines = []
    five_links = []

    s = soup_world.find('ol', class_="gs-u-m0 gs-u-p0 lx-stream__feed qa-stream")
    li = s.find_all('article')
    iter = islice(s, 20)
    for i in iter:
        try:
            if i.img['src'] and not i.figure and i.img['src'].startswith('https:') and not i.img['sizes'] == '(min-width: 600px) 56px, 48px':
                five_headlines.append(i.h3.text)
                five_links.append(bbc + i.h3.a['href'])
                five_img.append(i.img['src'])
        except (AttributeError, TypeError):
            pass

    # Local news from dutchnews

    url_local =  "https://nltimes.nl"
    source_local = requests.get(url_local).text
    soup_local = BeautifulSoup(source_local, 'lxml')
    link_beginning = "https://nltimes.nl"
    img_local = []
    headlines_local = []
    links_local = []

    only_ten = soup_local.find('section', class_='col-sm-9 sidebar-visible')

    local = only_ten.find_all('div', class_="news-card")
    iter = islice(local, 12)
    for i in iter:
    	img_local.append(link_beginning+i.img['src'])
    	links_local.append(link_beginning+i.img.parent['href'])


    title_tags = only_ten.find_all('div', class_='news-card__title')
    iter1 = islice(title_tags, 12)
    for title in iter1:
    	headlines_local.append(title.a.text)

#  ------ENTERNTAINMENT NEWS

    url = "https://collider.com/all-news/#page/1"

    source_ent = requests.get(url).text
    soup_ent = BeautifulSoup(source_ent, 'lxml')


    img_ent=[]
    headlines_ent = []
    links_ent = []
    e = soup_ent.find('div', id="content")
    enter_news = e.find_all("article")
    iter3 = islice(enter_news, 12)
    for l in iter3:
        try:
            headlines_ent.append(l.h2.text)
            links_ent.append(l.a['href'])
            img_ent.append(l.img['src'])

        except (AttributeError, TypeError):
            pass

# ------------TECHNOLOGY NEWS--------------------

    url = "https://www.wired.co.uk/topic/technology"
    source_tech = requests.get(url).text
    soup_tech = BeautifulSoup(source_tech, 'lxml')
    link_tech = "https://www.wired.co.uk"
    img_tech=[]
    headlines_tech = []
    links_tech = []
    t = soup_tech.find('ul', class_="c-card-section__card-list js-c-card-section__card-list")
    tech_news = t.find_all("article")
    iter3 = islice(tech_news, 12)
    for x in iter3:
        try:

            headlines_tech.append(x.a.text)
            links_tech.append(link_tech + x.a['href'])
            img_tech.append(x.picture.img['data-src'])

        except (AttributeError, TypeError):
            pass

    return render_template('index.html', quote=quote, five_headlines=five_headlines, five_img=five_img, five_links=five_links, img_local=img_local, headlines_local=headlines_local, links_local=links_local, img_ent=img_ent, headlines_ent=headlines_ent, links_ent=links_ent, img_tech=img_tech, headlines_tech=headlines_tech, links_tech=links_tech)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
