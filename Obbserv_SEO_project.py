from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import scrapy
import logging
import scrapy_proxies

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
store = file.Storage('credentials.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret_1.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('sheets', 'v4', http=creds.authorize(Http()))

		
SPREADSHEET_ID = '1zXLFsLIdMEOsgy4fPK4kL9_4cOjGL1Y3s3Sfuz7EwyA'

class firstscrapy(scrapy.Spider):
	name = "spider"
	allowed_domains = ["google.com"]
	index = 2
	#indicator in case of an error
	flag = 1
	def start_requests(self):
		SS_RANGE = 'AppTestingSheet!F2:F'
		result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range=SS_RANGE).execute()
		values = result.get('values',[])
		#The cell value from which the current execution of the script would run
		start_value = 0
		i = 2
		for row in values:
			i+=1;	
		start_value = i

		#While loop is used to incorporate delay while making requests (time delay in introduced through time.sleep(t(secs)))

		while True:
			# Break the loop in case of failure
			if firstscrapy.flag==0:
				break				
			RANGE_NAME = 'AppTestingSheet!A'+str(start_value)+':A'+str(start_value)
			start_value+=1
			#Parsing the keywords		
			result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range=RANGE_NAME).execute()
			values = result.get('values', [])
			index = start_value
			#a dictionery to store urls and their particular indexes
			urls = []	
			if not values:
			    print("No values")
			else:
			    for row in values:
			    	url = 'https://www.google.co.in/search?q=allintitle:"{}"'.format(str(row[0])) 
			        urls.append({
			        	'url':url,
			        	'index':index
			        })
			        index +=1   

			#Parsing URL among the list of URLs and subsequently parsing the required page
			for item in urls:
				# logging.info("parse_request")				
				request = scrapy.Request(item['url'],callback=self.parse,errback=self.error)
				request.meta['index'] = item['index']
				yield request
				# logging.info(firstscrapy.flag)

			#FOR THE RANDOM PROXY METHOD
			#First make a list/array of the valid 'private' proxies, say proxies_['proxy_address1','proxy_address2'...]
			#List of proxies(private) probably from Hidemyass.com
			#In the "for item in urls" loop
			#set request.meta['proxy'] = random.choice(proxies_)	

	#Function to scrape the results from a particular google search page
	def parse(self,response):		
		RANGE_NAME1 = 'AppTestingSheet!F'+ str(response.meta['index'])+':F'
		values = [
				[str(response.css('div#resultStats::text').re(r'[0-9,]+')[0])]
			]
		body = {
			'values':values
		}
		#Making the request to the sheetsAPI to write
		request = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME1, valueInputOption="RAW", body=body)
		response = request.execute()
	
	#callable function in case of an error
	def error(self,response):
		# logging.info("failure")	
		firstscrapy.flag = 0

	
