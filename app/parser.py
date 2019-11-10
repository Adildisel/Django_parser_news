from bs4 import BeautifulSoup
import requests

from random import choice


class Helper:
    def __init__(self):
        self.r = ''
        self.ip = ''
        self.user_a = ''
        self.proxies = []
        self.useragents = []

    def get_html(self, url):
        proxy = {
            'http': 'http://{}'.format(choice(self.proxies)),
            }
        useragent = {
            'User-Agent': choice(self.useragents)
        }
        self.r = requests.get(url, headers=useragent, proxies=proxy).text
        
    def get_ip(self):
        soup = BeautifulSoup(self.r, features='html.parser')
        self.ip = soup.find('span', class_='ip').text.strip()
        self.user_a = soup.find('span', class_='ip').find_next_sibling('span').text.strip()

    def get_proxy_list(self):
        self.proxies = open('txt_file/proxies.txt').read().split('\n')

    def get_user_a_list(self):
        self.useragents = open('txt_file/useragents.txt').read().split('\n')


def main():
    helper = Helper()

    url = 'http://sitespy.ru/my-ip'

    helper.get_proxy_list()
    helper.get_user_a_list()

    helper.get_html(url)
    

    # helper.get_html(url)
    helper.get_ip()

    print(helper.ip)
    print(helper.user_a)
    # print(helper.proxies[-1])

    pass




if __name__ == "__main__":
    main()