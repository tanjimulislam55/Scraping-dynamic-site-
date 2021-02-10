import bs4
from bs4 import BeautifulSoup
import json
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException


class All_Baby_Names():
    
    def __init__(self, alphabet, gender):
        self.alphabet = alphabet
        self.gender = gender 
        self.names = dict()

    def getUrl(self):
        return f'https://www.onlymyhealth.com/baby-names/{self.gender}-muslim-baby-names-starting-with-{self.alphabet}'

    def getParsedContent(self, html):
        return BeautifulSoup(html, 'lxml')

    def runSelenium(self):
        path_to_chrome_driver = '/home/king/Desktop/Scraping/chromedriver'
        browser = webdriver.Chrome(executable_path = path_to_chrome_driver)
        # getting site url
        browser.get(self.getUrl())
        # loading duration
        self.waitForLoad(browser)
        # sending selenium based 'page content' to deal with 'beautifulsoup'
        self.getInformations(browser.page_source)

    def getInformations(self, response):
        bs = self.getParsedContent(response)
        # getting all 'tr' tags inside table>tbody
        trs = bs.find('div', {'class': 'babytable searchresultspage'}).tbody
        # each tr holds separate tds of name and meanings
        for tr in trs:
            # skipping NavigableString
            if type(tr) == bs4.element.NavigableString:
                continue
            elif type(tr) == bs4.element.Tag:
                self.getData(tr)
        del self.names['Name']
        return self.makeJson(self.names)
        
    def makeJson(self, names):
        with open(f"babyNames_from_onlymyhealth_{self.gender}_{self.alphabet}.json", "w") as outfile:
            json.dump(names, outfile)

    def getData(self, tr):
        # name
        td_first = tr.find('td')
        # meanings
        td_second = tr.find('td').next_sibling
        # storing data to a dictaionary
        return self.makeDictionary(td_first.text.strip(), td_second.text.strip())

    def makeDictionary(self, key, value):
        self.names[key] = value

    def waitForLoad(self, browser):
        elem = browser.find_element_by_tag_name("html")
        count = 0
        while True:
            count += 1
            if count > 20:
                print('Timing out after 10 seconds and returning')
                return
            time.sleep(.5)
            try:
                elem == browser.find_element_by_tag_name('html')
            except StaleElementReferenceException:
                return


if __name__ == "__main__":
    gender = input('Gender: ').lower()
    alphabet = input('Alphabet: ').upper()
    scrapper = All_Baby_Names(alphabet, gender)
    scrapper.runSelenium()

