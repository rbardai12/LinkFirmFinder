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


#Paste Infortmation in "input.txt" file and Get Companies
paste()
removal()

#Rename .txt file 
os.rename('Companies.txt', f'{SearchTerm}.txt')