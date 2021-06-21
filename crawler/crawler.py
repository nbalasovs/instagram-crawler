import requests as req
import json, re, time

class Crawler:
    def __init__(self, url: str):
        self.url = url
        self.headers = {'User-Agent': 'PostmanRuntime/7.28.0'}

    def fetch(self):
        response = req.get(self.url, headers = self.headers)
        urls_re = re.compile('window.\_sharedData\s?=\s?(\{.+\});')
        name_re = re.compile('https://www.instagram.com/([^/]+)/$')
        name = name_re.search(self.url).group(1)
        output = []
        if (response.status_code == 200):
            urls = urls_re.search(response.text)
            if urls:
                urls = json.loads(urls.group(1))
                urls = urls['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']
                for url in urls['edges']:
                    time.sleep(1)
                    output.append(req.get(url['node']['display_url']).content)
                return [(name, out) for out in output]
        raise Exception("Error occurred during fetch")
