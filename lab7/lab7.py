# -*- coding: UTF-8 -*-

import sys
import os
import requests
import Queue
import csv
from BeautifulSoup import BeautifulSoup
from lepl.apps.rfc3696 import HttpUrl #валидатор url
from urlparse import urlparse, urljoin, urlsplit, urlunsplit
import urlnorm

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class CFinder_broken_links():
    path = './result/' 

    def __init__(self):
        self.PATH_TO = self.file_init()

    def run(self, url):
        
        url = urlnorm(url)
        host = url;
        host_name = urlparse(url).hostname
        
        check_queue = Queue.Queue()#Очередь к просмотру
        check_queue.put(url)#Кладем первый url
        
        all_urls = set()
        good_urls = set()
        bad_urls = set()
        
        while not check_queue.empty():
            current_url = check_queue.get()#Выбор следующей страницы для проверки
        
            result = self.read_link(current_url, all_urls)
            urls = result['links']#Выбираем новые ссылки .difference(all_urls)
            all_urls.update(urls)
        
            for url in urls:            
                if (host_name == urlparse(url).hostname ):#Проверка чужой сайт это или нет
                    url = urlnorm(url)
                    link_connection_result = self.check_connection(url)#Проверка доступности url
                    
                    if(link_connection_result['code'] != 0):#Если url валидный, то записываем его
                        if(url not in good_urls and url not in bad_urls):
                            if(not link_connection_result['result']):
                                self.write_url_to_file(url, link_connection_result['code'], self.PATH_TO['CORRECT_URLS'])
                                check_queue.put(url)
                                good_urls.add(url)
                            else:
                                self.write_url_to_file(url, link_connection_result['code'], self.PATH_TO['BAD_URLS'])
                                bad_urls.add(url)
                else:
                    link_connection_result = self.check_connection(url)
                    if(not link_connection_result['result']):
                        self.write_url_to_file(url, link_connection_result['code'], self.PATH_TO['CORRECT_URLS'])
                    else:
                        self.write_url_to_file(url, link_connection_result['code'], self.PATH_TO['BAD_URLS'])
        self.bad_urls = bad_urls
        self.good_urls = good_urls  
    
    def file_init(self):
        #Создаем папку, куда скачиваем сайты
        
        if not os.path.exists(self.path):
            os.mkdir(self.path)
    
        PATH_CORRECT_URLS = self.path + 'correct_urls.csv'
        PATH_BAD_URLS = self.path + 'incorrect_urls.csv'
    
        #создаем таблицы CSV
        with open(PATH_BAD_URLS, 'w') as csvfile:
            fieldnames = ['status', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    
        with open(PATH_CORRECT_URLS, 'w') as csvfile:
            fieldnames = ['status', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    
        return {'CORRECT_URLS':PATH_CORRECT_URLS, 'BAD_URLS':PATH_BAD_URLS}
    
    def write_url_to_file(self,url, return_code, path):
        #Заполняем таблицы SCV
        with open(path, 'a') as csvfile:
            fieldnames = ['status', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'status': return_code, 'url': url})
    
    def check_connection(self, url):
        #Проверяем статус соединения
        s = requests.session()
        try:
            url = s.get(url)
        except Exception:
            return {'result':False, 'code':0}
        return {'result':(url.status_code >= 400 and url.status_code < 500), 'code':url.status_code}
    
    
    def read_link(self, url, all_links):
        #считываем ссылки со страницы
        s = requests.session()
        page = s.get(url)
    
        if(page.status_code >= 400 and page.status_code < 500):
            bad_url_list = url
            return {'links':set(), 'result':False, 'code':page.status_code}
    
        soup = BeautifulSoup(page.content)
        links = soup.findAll("a", href=True)
    
        urls = set()
        for flink in links:
            link = flink['href']
            if(link not in all_links):
                if(not bool(urlparse(link).netloc)):
                    link = urljoin(url, link)
            
                urls.add(link)
    
        return {'links':urls, 'result':True, 'code':page.status_code}    
    
    def get_result(self):
        return {'bad_links':len(self.bad_urls), 'good_links':len(self.good_urls)}


def urlnorm( base, url=''):#Вспомогательная функция, для нормализации url
      '''Normalizes an URL or a link relative to a base url. URLs that point to the same resource will return the same string.'''
      new = urlparse(urljoin(base, url).lower())
      return urlunsplit((
        new.scheme,
        (new.port == None) and (new.hostname) or new.netloc,
        new.path,
        new.query,
        ''))


if (len(sys.argv) != 2):
    print u"Укажите адрес страницы в качестве параметра. Формат ввода pars_links.py http://test.com"
else:
    validator = HttpUrl()
    if(validator(sys.argv[1])):
        finder = CFinder_broken_links()
        finder.run(sys.argv[1])
        result = finder.get_result()
        print 'Complete result:\n\tBad links {}\n\tGood links{}'.format(result['bad_links'], result['good_links'])
    else:
        print u"Введенный адрес не является корректным URL. Пожалуйста, введите адрес в формате http://test.com"
