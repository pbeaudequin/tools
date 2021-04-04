import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator



class litteratureaudioScrapper(object):

    def __init__(self):
        self.bootstrap_url = 'http://www.litteratureaudio.com/classement-de-nos-livres-audio-gratuits-les-plus-vus'

        
    def getTopBooks(self):
        html_doc=requests.get(self.bootstrap_url).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        links_div = soup.find_all("div", {"class": "entrybody2"})[0]
        return [(i.string,i['href']) for i in links_div.find_all("a")]

    def parseBook(self,title,url):
        html_doc=requests.get(url).content
        soup = BeautifulSoup(html_doc, 'html.parser')
        links = [a for a in soup.find_all("a") if a.get("href") and \
                 a["href"].endswith(".mp3") and \
                 a.string and \
                 a.string.endswith(".mp3")]
        if not links:
            links = [a for a in soup.find_all("a") if a.get("href") and \
                     a["href"].endswith(".mp3") and \
                     a.string ]
            
        return [(i.string[:-4],i['href']) for i in links]
    
    def generateRSS(self,topx=10):
        fg = FeedGenerator()
        fg.id(self.bootstrap_url)
        fg.title('Litterature Audio - Top Books Podcast')
        fg.description('Litterature Audio - Top Books Podcast')
        fg.author( {'name':'Philippe Beaudequin','email':'tyboon@gmail.com'} )
        fg.link( href=self.bootstrap_url, rel='self' )
        fg.language('fr')

        for title,book_url in self.getTopBooks()[:topx]:
            print(title)
            for chapter_name,mp3 in self.parseBook(title,book_url):
                fe = fg.add_entry()
                fe.id(mp3)
                fe.title(f'{title} - {chapter_name}')
                fe.link(href=mp3)
                fe.enclosure(mp3, 0, 'audio/mpeg')

        fg.rss_file(f'la.xml')
        return f'la.xml'
    
 if __name__ == '__main__':
     litteratureaudioScrapper().generateRSS(1000)
