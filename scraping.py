import time
import re
import os
import pprint
import time
import urllib.error
import urllib.request
import requests
from pathlib import Path
from bs4 import BeautifulSoup

output_folder = Path('tokyo_hot')
output_folder.mkdir(exist_ok=True)

url = 'https://www.tokyo-hot.com/cast/all/japanese?page='
linklist = []

i = 0

for page_num in range(75):
	url_with_page = url + str(page_num + 1)
	html = requests.get(url_with_page).text
	soup = BeautifulSoup(html, 'lxml')
	a_list =soup.select('div.grid > ul > li > a > img')
	for a in a_list:
  		link_url = a.attrs['src']
  		response = requests.get(link_url)
  		image = response.content
  		file_name = "tokyo_hot/{}.jpg".format(str(i).zfill(3))
  		with open(file_name, "wb") as f:
  			f.write(image)
  		linklist.append(link_url)
  		i = i + 1
  		


