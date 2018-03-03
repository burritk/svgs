from random import randint
import traceback
import requests
import time
from lxml import etree
import urllib2
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from files.downloader import Downloader

downloader = Downloader()
def get_headless_driver(no_sandbox=False):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    if no_sandbox:
        chrome_options.add_argument('--no-sandbox')
    current_path = os.path.dirname(__file__)
    filename = os.path.join(current_path, 'chromedriver')
    driver = webdriver.Chrome(filename, chrome_options=chrome_options)
    # driver.fram
    return driver

def get_tree(url):
    # url = 'http://freedesignfile.com/category/free-vector/'
    request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib2.urlopen(request)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    return tree

history = [line.split('"')[0] for line in open('output.txt', 'r').readlines()]

hrefs = []
for i in range(1, 4093):
    not_passed = True
    # time.sleep(2)
    while not_passed:
        # print i
        url = 'http://freedesignfile.com/category/free-vector/page/{}/'.format(i)
        print url
        tree = get_tree(url)
        links = tree.xpath('//a')
        if links == 0:
            not_passed = True
            print 'uuh huh', i
            time.sleep(randint(1, 4))
        else:
            not_passed = False
        for element in links[1:]:
            for child in element.getchildren():
                if 'img' in child.tag:
                    hrefs.append(element.get('href'))
                    break
                # print child.get('src')


with open('output.txt', 'a+') as output:
    driver = get_headless_driver(no_sandbox=True)
    usedrefs = []
    counter = 0
    for href in hrefs:
        not_passed = True
        cycles = 0
        while not_passed:
            try:
                cycles += 1
                id = href.split('.com/')[1].split('-')[0]
                name = href.split(id)[1][1:-1]

                print counter

                if href in usedrefs:
                    print 'USED'
                    break
                if name in history:
                    print 'ALREADY DOWNLOADED'
                    break
                driver.get(href)
                tree = get_tree(href)
                tag_links = driver.find_elements_by_xpath('//*[@rel="tag"]')
                tags = []
                for tag in tag_links:
                    tags.append(tag.text)

                driver.get('http://freedesignfile.com/download.php?id=' + id)
                file_url = driver.find_element_by_xpath('//*[@id="downloadUrl"]/a').get_attribute('href')
                print file_url
                downloader.download_file(file_url, name)
                output_string = name
                for tag in tags:
                    output_string += '"' + tag
                output.write(output_string + '\n')
                usedrefs.append(href)
                not_passed = False

            except:
                traceback.print_exc()
                secs = cycles+1
                print 'Error. waiting {} seconds'.format(secs)
                if cycles == 5:
                    break
                time.sleep(secs)
        counter += 1

print 'chtm'


# for children in [element.getchildren() for element in links]:
#     for child in children:
#         if 'img' in child.tag:
#             print child.get('src')
#  url = "http://download.thinkbroadband.com/10MB.zip"

