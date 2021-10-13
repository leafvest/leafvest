import requests as rq
from bs4 import BeautifulSoup
from typing import Any

from html.parser import HTMLParser


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# r0bn4c rQMQod


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        f = open("result.txt", "a")
        
        f.write(f"Encountered a start tag: {tag}, {attrs} \n")
                
        f.close()

    def handle_endtag(self, tag):
        pass
        #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        f = open("result.txt", "a")
        f.write(f"Encountered some data : {data}\n")
        f.close()

def google(q: str) -> str:
    q = '+'.join(q.split())
    q = f'{q}+stock'
    url = "https://www.google.com/search?q=" + q
    html = rq.get(url, headers=HEADERS).text
    return html


def bing(q: str) -> str:
    q = '+'.join(q.split())
    q = f'{q}+ticker'
    url = "https://www.bing.com/search?q=" + q
    html = rq.get(url, headers=HEADERS).text
    return html


def yahoo(q: str) -> str:
    q = '+'.join(q.split())
    q = f'{q}+ticker'
    url = "https://www.yahoo.com/search?q=" + q
    html = rq.get(url, headers=HEADERS).text
    return html


def get_knowledge_panel(html: str) -> Any:
    soup = BeautifulSoup(html, 'lxml')
    print(soup.select('div[data-md="1007"]'))
    for subsoup in soup.find_all('span', class_='fin_sitext b_focusTextMedium'):
        print(subsoup)
    # parser = MyHTMLParser()
    # parser.feed(html)
    

def main() -> None:
    q = 'EXELON CORP'
    # html = google(q)
    html = bing(q)
    knowledge_panel = get_knowledge_panel(html)
    print(knowledge_panel)



if __name__ == "__main__":
    main()
