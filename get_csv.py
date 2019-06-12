from bs4 import BeautifulSoup
from selenium import webdriver 
from splinter import Browser
from selenium.webdriver.support.ui import Select
import re
import pprint
import os
import time
import pandas as pd
import tempfile 
import csv_to_mongo

def get_browser():
    GOOGLE_CHROME_BIN = "/app/.apt/usr/bin/google-chrome"
    CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"

    chrome_options = webdriver.ChromeOptions()

    chrome_options.binary_location = GOOGLE_CHROME_BIN
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('headless')

    browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    return browser

def get_csv(get_options=False):
    browser = get_browser()  
   
    download_dir = tempfile.TemporaryDirectory().name
    os.mkdir(download_dir)
    print('created temporary directory')
    print(download_dir)
    #send a command to tell chrome to download files in the download_dir
    #without asking
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}} 
    browser.execute("send_command", params)

    browser.get("https://www.pluginillinois.org/OffersBegin.aspx")
    results = browser.page_source
    soup = BeautifulSoup(results, 'html.parser')
   
    name = 'ctl00$ctl00$ctl00$ctl00$MasterContent$MasterContent$RightColumn$RightColumn$UtilityServiceTerritoryList'
    dropdown = soup.find('select', attrs={'name': name})
    options_full = dropdown.findAll('option') 

    options= {}
    for option in options_full:
        options[option['value']] = option.get_text()

    if get_options:
        return options, download_dir
        exit()

    all_suppliers = [] 
    for option in options: 
        print('in the loop') 
        print(options[option])
        browser.implicitly_wait(10)
        #this is all just opening the browser, choosing the option from the
        #list of rate zones and clicking the submit button then getting the
        #html. 
        select = Select(browser.find_element_by_id('MasterContent_MasterContent_RightColumn_RightColumn_UtilityServiceTerritoryList'))
        select.select_by_visible_text(options[option])
        button = browser.find_element_by_xpath('//*[@id="MasterContent_MasterContent_RightColumn_RightColumn_SubmitButton" and not(@disabled)]')
        button.click()
        results = browser.page_source

        #click the csv download button
        time.sleep(3) 
        link = browser.find_element_by_link_text("Export to CSV (Excel)")

        link.click() 
        time.sleep(15)

        old_filename = 'PlugInIllinoisExport.csv'
        new_filename = options[option].replace(' ', '_') + '_data.csv' 
        print(new_filename) 
        old_exists = os.path.isfile(download_dir + '/{}'.format(old_filename))
        #first while loop to check if file has been downloaded 
        while not old_exists:
            print('in first while') 
            time.sleep(1)
            old_exists = os.path.isfile(download_dir + '/{}'.format(old_filename))
        
        new_exists = os.path.isfile(download_dir + '/{}'.format(old_filename))
        #second while loop to check if file name has been changed
        while not new_exists:
            print('in second while')
            if old_exists:
                os.rename(download_dir + '/{}'.format(old_filename),
                        download_dir + '/{}'.format(old_filename))
                time.sleep(1) 
                break
            else:
                print('no file!')
            
        print('renamed')
        browser.back()
    csv_to_mongo.to_mongo(options, download_dir)




