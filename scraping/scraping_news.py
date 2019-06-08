#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 26 23:35:22 2019

@author: sethurishabh

Scrapes comments from links in directories given.
Used as:
    python scraper.py news
"""

from selenium import webdriver
import os
import time
import sys

SRC_DIR = os.path.join('..','source_links')
DATA_DIR = os.path.join('..','data')

def scrape(folder, file):
    """
    Scrapes comments from all links in the folder/file path.

    Parameters
    ----------
    folder : str
        folder of file with links
    file : str
        file containing links

    Output
    -------
    Writes comments into file of given filename in data/folder/file/

    """
    assert isinstance(folder, str)
    assert isinstance(file, str)
    in_path = os.path.join(SRC_DIR, folder, file)
    assert os.path.exists(in_path)
    driver=webdriver.Chrome()

    fd = open(SRC_DIR + folder + file)
    data = fd.read().splitlines()
    fd.close()
    
    c = 0
    for d in data:
        if c >= 20 :
            break
        c += 1
        
        fname, link = d.split(' - ')
        out_path = os.path.join(DATA_DIR, folder, file)
        if not os.path.exists(out_path):
            os.makedirs(out_path)
        fd = open(os.path.join(out_path, fname), "w+")

        print("Getting link :", link)
        driver.get(link)
        driver.maximize_window()
        time.sleep(7)

        count = 0

        driver.execute_script('window.scrollTo(0, 500);')
        SCROLL_PAUSE_TIME = 5


        # Get scroll height
        last_height = driver.execute_script("return document.documentElement.scrollHeight")

        while count < 200:
            #now wait let load the comments
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
            count+=1
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if last_height == new_height:
                break
            last_height = new_height    

        count = 0
        print('Outputted to :', path+file)
        comment_div=driver.find_element_by_xpath('//*[@id="contents"]')
        comments=comment_div.find_elements_by_xpath('//*[@id="content-text"]')
        for comment in comments:
            fd.write(comment.text + "\n")
            count += 1
        time.sleep(5)
        print('Comments scraped :', count)
    fd.close()


if __name__ == '__main__':
    """
    Automatically gets all comments from link in directories given in source_links/
    """
    for i in range(1, len(sys.argv)):
        folder = sys.argv[i]
        path = os.path.join(SRC_DIR, folder)
        filelist = os.listdir(path)
        try :
            print('Removing .DS_Store')
            filelist.remove('.DS_Store')
        except ValueError:
            print('No .DS_Store...\nContinuing...')
        else :
            print('.DS_Store removed...\nContinuing...')
        print("In folder :", folder)
        print(filelist)
        for file in filelist:
            print("In file :", file)
            scrape(folder, file)
    print("Exiting...")

