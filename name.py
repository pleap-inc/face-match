import time
import re
import os
import pprint
import time
import urllib.error
import urllib.request
import requests
import joblib
from pathlib import Path
from bs4 import BeautifulSoup

url = 'https://www.tokyo-hot.com/cast/all/japanese?page='
linklist = []

def make_file(input_to_write):
    file_location = "names.txt"
    file = open(file_location, "a")
    file.write(input_to_write)
    file.close()
    
for page_num in range(75):
	url_with_page = url + str(page_num + 1)
	html = requests.get(url_with_page).text
	soup = BeautifulSoup(html, 'lxml')
	span_list =soup.select('div.grid > ul > li > a')
	
	for span in span_list:
		name_span = span.find('span')
		name= name_span.get_text(strip=True)
		linklist.append(name)
		
print(linklist[73])

'''
for index in range(2965):
	file_path = "tokyo_hot/" + str(index).zfill(3) + ".jpg"
	rename = "tokyo_hot/" + linklist[index] + ".jpg"
	os.rename(file_path, rename)
'''