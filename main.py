from crawler.crawler import Crawler
from model import Image
import re, os

if __name__ == '__main__':
    Image.create_database()
    URL = input('Enter Instagram URL: ')
    url_re = re.compile('https://www.instagram.com/[^/]+/$')
    name_re = re.compile('https://www.instagram.com/([^/]+)/$')
    matches = url_re.match(URL)
    if matches:
        name = name_re.search(URL).group(1)
        urls = Crawler(URL).fetch()
        for url in urls:
            Image(url[0], url[1]).commit()
        OUTPUT_PATH = os.getcwd() + '/output'
        if (not os.path.exists(OUTPUT_PATH)):
            os.makedirs(OUTPUT_PATH)
        Image.output(name, OUTPUT_PATH)
    else:
        raise Exception("Please enter URL in correct format https://www.instagram.com/\{account_name\}/")
        