import scrapy
import re

class PlantSpider(scrapy.Spider):
    name = "plant" #spider name
    allowed_domains = ['esveld.nl']
    start_urls = [
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=a',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=b',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=c',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=d',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=e',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=f',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=g',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=h',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=i',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=j',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=k',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=l',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=m',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=n',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=o',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=p',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=q',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=r',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=s',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=t',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=u',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=v',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=w',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=x',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=y',
            'http://www.esveld.nl/nederlandse-namen.php?pagina=w&letter=z',
            ]
    
    def request(self, url, callback):
        """
        wrapper for scrapy.request
        """
        request = scrapy.Request(url=url, callback=callback)
        # attach cookies and headers to the request to be able to get a translated version of the text
        request.cookies['taal'] = 'en'
        request.headers['User-Agent'] = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0')
        return request

    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield self.request(url, self.parse)
    
    def parse(self, response):
        for plant in response.css('table#namen tr'):
            botanical_name = plant.css('td.plant_td::text').get()
            common_name = plant.css('td.naam_td a::text').get()
            item = {}
            item['common']=re.sub(r'[^a-zA-Z0-9\- ]', '', common_name) # removes any character that is not alfanum, '-', or  ' ' in the string.
            item['botanical']=re.sub(r'[^a-zA-Z0-9\- ]', '', botanical_name) # remove any character that is not alfanum, '-'. or ' ' in the string.
            item['word_count']=len(botanical_name.split(' ') + common_name.split(' ')) # counts words in common_name and botanical_name
            yield item
            

