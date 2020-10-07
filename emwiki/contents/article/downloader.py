from tqdm import tqdm
import requests
from bs4 import BeautifulSoup


class Downloader:
    def __init__(self, url, extension):
        self.url = url
        self.extension = extension
        self.urls = []

    def read_index(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, 'lxml')
        links = soup.findAll('a')

        for link in links:
            href = link.get('href')
            if href and self.extension in href:
                self.urls.append(href)

    def download(self, to_dir):
        for url in tqdm(self.urls):
            filename = url.split('/')[-1]
            to_path = to_dir + '/' + filename

            if self.url in url:
                r = requests.get(url)
            else:
                r = requests.get(self.url + '/' + url)

            if r.status_code == 200:
                f = open(to_path, 'bw')
                f.write(r.content)
                f.close()
            else:
                raise Exception
