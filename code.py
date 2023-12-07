import urllib.request
from bs4 import BeautifulSoup
import os
import requests
from urllib.request import Request, urlopen
import certifi


filePath1 = 'output/found.txt'
filePath2 = 'output/notfound.txt'
filePath3 = 'output/redirect_list.txt'


if os.path.exists(filePath1):
    os.remove(filePath1)
if os.path.exists(filePath2):
    os.remove(filePath2)
if os.path.exists(filePath3):
    os.remove(filePath3)


#Alizaib Backlink Checker
cnt=1
check_cnt=0
found_total=0;
redirect_links=0;
not_found_total=0;

f5= open("output/redirect_list.txt","a")
f3= open("output/found.txt","a")
f4= open("output/notfound.txt","a")
f2 = open('input/yoursiteurl.txt')
yoursite = f2.readline()
print("Started Checking Please Wait ... ")
f = open('input/backlinks-list.txt')
line = f.readline()



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

while line:
	try:
		response = requests.get(line,headers=headers,allow_redirects=True)
	except requests.exceptions.SSLError as err:
	    #print('SSL Error. Adding custom certs to Certifi store...')
	    cafile = certifi.where()
	    with open('cacert.pem', 'rb') as infile:
	        customca = infile.read()
	    with open(cafile, 'ab') as outfile:
	        outfile.write(customca)
	    #print('That might have worked.')	

	if response.status_code == 200:

		url = line
		try:
			# Perform the request

			request = urllib.request.Request(url)
			# Set a normal User Agent header, otherwise Google will block the AZ request.
			request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
			raw_response = urllib.request.urlopen(request).read()
		except urllib.error.HTTPError as e:
			if e.code == 404:
				check_cnt+=1
				pass

		#except http.client.IncompleteRead as e: ResponseData = ''

		# Read the repsonse as a utf-8 string
		#html = raw_response.decode("utf-8")
		html = str(raw_response)
		# The code to get the html contents here.

		#soup = BeautifulSoup(html, 'html.parser')


		# Find all the search result divs
		site_src = html.find(yoursite)
		
		if site_src == -1 or check_cnt==1:
			not_found_total+=1;
			check_cnt=0
			f4.write(url)
			print("Checking URL # "+str(cnt)+ " Not Found")
		else:
			found_total+=1;
			print("Checking URL # "+str(cnt)+ " Found")
			f3.write(url)
			

		line = f.readline()
		cnt=cnt+1
	else:
		print("Checking URL # "+str(cnt)+ " Redirect")
		redirect_links+=1
		cnt=cnt+1
		not_found_total+=1
		f5.write(url)
		line = f.readline()

print("Done! Check Output Folder For List")
print(str(found_total)+" "+"Links Found")
print(str(not_found_total)+" "+"Links Not Found")
print(str(redirect_links)+" "+"Redirect Links")
f.close()
f2.close() 
f3.close() 
f4.close() 