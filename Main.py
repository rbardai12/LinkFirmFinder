import code
from dataclasses import replace
import time
from turtle import down, left
from numpy import full, half
from pandas import interval_range
from pyrsistent import v
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import hashlib
import os
import multiprocessing
from pynput.keyboard import Key, Controller
from pyautogui import*
from pynput import keyboard
import pyperclip as pc

SearchTerm = 'Master Anaplanner'

#URl + Chrome Path
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
URL = f'https://www.linkedin.com/jobs/search/?geoId=103644278&keywords={SearchTerm}'
PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(executable_path=PATH, options=options)
session = HTMLSession()
driver.get(URL)
time.sleep(5)
x = driver.page_source


#Define the Scoll and Click Command
def csinitial():
    num = 30
    for _ in range(num):
        keyDown("pagedown")
        time.sleep(0.5)
        keyDown('up')
        time.sleep(0.5)
        keyDown('down')

    time.sleep(2.5)

    leftClick(x=500, y=1300)

    time.sleep(2)

def cspost():
    num = 10
    for _ in range(num):
        keyDown("pagedown")
        time.sleep(0.5)
        keyDown('up')
        time.sleep(0.5)
        keyDown('down')

    time.sleep(2.5)

    leftClick(x=500, y=1300)

    time.sleep(2)

def openinspec():
    key = Controller()
    with key.pressed(Key.ctrl):
        key.press(Key.shift)
        key.press('i')
        key.release(Key.shift)
        key.release('i')
        time.sleep(1)
    with key.pressed(Key.ctrl):
        key.press('f')
        key.release('f')
        time.sleep(0.5)
    codecontent = 'jobs-search__results-list'
    pc.copy(codecontent)
    with key.pressed(Key.ctrl):
        key.press('v')
        key.release('v')

def copy():
     leftClick(x=800, y=478)
     time.sleep(1)
     rightClick(x=800, y=478)
     time.sleep(1)
     leftClick(x=900, y=620)
     time.sleep(1)
     leftClick(x=990, y=630)

def paste():
    info = pc.paste()
    file = 'input.txt'
    with open(file, 'w', encoding="utf-8") as f:
        f.write(info)

def removal():
    #Get Companies
    file = 'input.txt'
    with open(file, 'r')as inputfile, open('Post.txt', 'w')as outfile:
        for line in inputfile:
            if '            ' in line:
                outfile.write(line)
        inputfile.close()
        outfile.close()

    #Remove Spaces
    file = 'Post.txt'
    output=""
    with open(file) as f:
        for line in f:
            if not line.isspace():
                output+=line            
    f= open(file,"w")
    f.write(output)
    f.close()

    #Remove Unwanted Lines
    file = 'Post.txt'
    file2 = 'Companiesout.txt'
    bad_words = ['Apply Now','/h4','base-search-card__metadata', 'base-search-card__subtitle','li', 'div','States', 'Area', ', AK', ', AL', ', AR', ', AZ', ', CA', ', CO', ', CT', ', DC', ', DE', ', FL', ', GA', ', HI', ', IA', ', ID', ', IL', ', IN', ', KS', ', KY', ', LA', ', MA', ', MD', ', ME', ', MI', ', MN', ', MO', ', MS', ', MT', ', NC', ', ND', ', NE', ', NH', ', NJ', ', NM', ', NV', ', NY', ', OH', ', OK', ', OR', ', PA', ', RI', ', SC', ', SD', ', TN', ', TX', ', UT', ', VA', ', VT', ', WA', ', WI', ', WV', ',WY']
    with open(file) as oldfile, open(file2, 'w') as newfile:
        for line in oldfile:
            if not any(bad_word in line for bad_word in bad_words):
                newfile.write(line)
        newfile.close()
        oldfile.close()
    os.remove('Post.txt')

    #Remove Duplicates
    infilename = 'Companiesout.txt'
    outfilename = 'FinalCompanies.txt'
    lines_seen = set() 
    outfile = open(outfilename, "w")
    for line in open(infilename, "r"):
        if line not in lines_seen: 
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
    os.remove('Companiesout.txt')

    #Sort Alphabetically 
    with open('FinalCompanies.txt', 'r') as r, open('Final.txt', 'w') as outfile:
        for line in sorted(r):
            outfile.write(line)
        outfile.close()
    os.remove('FinalCompanies.txt')

    #Remove Leading White Space
    file1 = 'Final.txt'
    file2 = 'Companies.txt'
    with open(file1, 'r') as infile, open(file2, 'w') as outfile:
        for line in infile:
            eachline = line.lstrip()
            outfile.write(eachline)
        infile.close()
        outfile.close()
    os.remove('Final.txt')

#Run the Scroll and Click Command
csinitial()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()
cspost()



#Get comapnies from Inspect Element
openinspec()
copy()


#Close Chrome Window
driver.quit()


#Paste Infortmation in "input.txt" file and Get Companies
paste()
removal()

#Rename .txt file 
os.rename('Companies.txt', f'{SearchTerm}.txt')