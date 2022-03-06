from bs4 import BeautifulSoup
import requests
import requests.exceptions
import urllib.parse
from collections import deque
from datetime import timedelta
import re
import os
import sys
import getpass
import time

R = '\n\033[31m' # redError
red = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white
Y = '\033[33m' # yellow

def banner():
	banner = """ 
		       (                           )
		  ) )( (                           ( ) )( (
	       ( ( ( )  ) )                     ( (   (  ) )(
	      ) )     ,,''\                     ///,,       ) (
	   (  ((    (;;;;//                     ;;////)      )
	    ) )    (-(__//                       ;;__)-)     (
	   (((   ((-(__||                         ||__)-))    ) )
	  ) )   ((-(-(_||           ```\__        ||_)-)-))   ((
	  ((   ((-(-(/(/;;        ''; 9.- `      //\)\)-)-))    )
	   )   (-(-(/(/(/;;      '';;;;-\~      //\)\)\)-)-)   (   )
	(  (   ((-(-(/(/(/\======,:;:;:;:,======/\)\)\)-)-))   )
	    )  '(((-(/(/(/(//////:%%%%%%%:;;;;;;)\)\)\)-)))`  ( (
	   ((   '((-(/(/(/('uuuu:WWWWWWWWW:uuuu`)\)\)\)-))`    )
	     ))  '((-(/(/(/('|||:wwwwwwwww:|||')\)\)\)-))`    ((
	  (   ((   '((((/(/('uuu:WWWWWWWWW:uuu`)\)\))))`     ))
		))   '':::UUUUUU:wwwwwwwww:UUUUUU:::``     ((   )
		  ((      '''''''-uuuuuuuu/``````         ))
		   ))            `JJJJJJJJJ`            ((
		     ((            LLLLLLLLLLL         ))
		       ))         ///|||||||;;\       ((
		         ))      (/(/(/(^)\)\)\)       ((
		          ((                           ))
		            ((                       ((
		              ( )( ))( ( ( ) )( ) (()
		              """

	project = "Email Gathering Tool"
	version = "1.0.3"
	author = "MarySue"
	os.system('clear')
	print(f'{red + banner}')
	print(f"	     {C}{project} v{version} by {red + author}")
	print(f"      {C}Tool to gather emails from websites! Choose the right option and then URL to scan")
	global nickname
	nickname = getpass.getuser().capitalize()
	main()
	
def lol():
	global amount, nickname
	print(f"{G}If you want to change it, you can type in '{Y}back{G}'")
	print(f"{G}Put in the URL (https://example.com) that you want to scan:")
	user_url = str(input(f"{Y}User {nickname}: {red}eG/URLs > {W}"))
	if user_url == "back":
		print(f"{C}Proceeding back...")
		banner()
	if user_url == "exit" or user_url == "quit":
		sys.exit(f"{R}Quitting...{W}")
	print(f"{G}	[***] Starting the scan of {Y + user_url + G} [***]")
	start_time = time.monotonic()
	urls = deque([user_url])

	scraped_urls = set()
	emails = set()

	count = 0
	try:
		while len(urls):
			count += 1
			if count == amount: break
			url = urls.popleft()
			scraped_urls.add(url)

			parts = urllib.parse.urlsplit(url)
			base_url = '{0.scheme}://{0.netloc}'.format(parts)

			path = url[:url.rfind('/')+1] if '/' in parts.path else url

			print(f"{Y}[%d]{G} Processing %s" % (count, url))
			try:
				response = requests.get(url)
			except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
				continue

			new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
			emails.update(new_emails)

			soup = BeautifulSoup(response.text, features="lxml")

			for anchor in soup.find_all("a"):
				link = anchor.attrs['href'] if 'href' in anchor.attrs else ''
				if link.startswith('/'):
					link = base_url + link
				elif not link.startswith('http'):
					link = path + link
				if not link in urls and not link in scraped_urls:
					urls.append(link)
	except KeyboardInterrupt:
		print(f'\n{R}[-]{G} Closing!\n')
	print(f"{G}	[***] The program found {Y + str(len(emails)) + G} email-adresses. [***]")
	end_time = time.monotonic()
	print(f"{G}	[***] Duration: {Y}{timedelta(seconds=end_time - start_time)}s{G} [***]")

	for mail in emails:
		print(f"{G + mail}")
	filename = user_url[8:].replace('.', '_') + '_' + str(amount) + '_urls.txt'
	with open(filename, 'w') as f:
		for mail in emails:
			f.write(mail + '\n')
	sys.exit(f"{Y}\nThank you for using the program.\nAll the info is written in the file named {red}{filename} {W}")
		
def main():
	global amount, nickname
	print(f"{G}      [***] Choose the model of gathering [***]")
	print(f"	   {Y}[1]{G} Small (30 urls)")
	print(f"	   {Y}[2]{G} Medium (100 urls)")
	print(f"	   {Y}[3]{G} Big (200 urls)")
	print(f"	   {Y}[4]{G} Huge (500 urls)")
	print(f"	   {Y}[5]{G} Mega Huge (1000 urls)")
	print(f"	   {Y}[6]{G} Unreal (5000 urls)")
	print("")
	print(f"	   {Y}[exit]{G} To quit the program")
	while True:
		amount = input(f"\n{Y}User {nickname}: {red}eG > {W}")
		if amount == "1":
			amount = 30
			print(f"{G}You have chosen: {Y}30{G} URLs")
			lol()
		elif amount == "2":
			amount = 100
			print(f"{G}You have chosen: {Y}100{G} URLs")
			lol()
		elif amount == "3":
			amount = 200
			print(f"{G}You have chosen: {Y}200{G} URLs")
			lol()
		elif amount == "4":
			amount = 500
			print(f"{G}You have chosen: {Y}500{G} URLs")
			lol()
		elif amount == "5":
			amount = 1000
			print(f"{G}You have chosen: {Y}1000{G} URLs")
			lol()
		elif amount == "6":
			amount = 5000
			print(f"{G}You have chosen: {Y}5000{G} URLs")
			lol()
		elif amount == "exit" or amount == "quit":
			sys.exit(f"{R}Quitting...{W}")
		else:
			print(f"{R}[-]{G} Invalid input...{W}")
			continue
	
banner()
