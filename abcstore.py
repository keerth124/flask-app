from urllib.request import urlopen
from bs4 import BeautifulSoup
#import time
from app import db
from app.models import Inventory, LastUpdate, DataHistory
from datetime import datetime

def runScreenScrape(url):
	html = urlopen(url)
	soup = BeautifulSoup(html, 'lxml')
	type(soup)	
	title = soup.title

	text = soup.get_text()

	data_table = soup.find('table',id="dnn_ctr543_View_GridViewSearchResults")
	rows = data_table.findAll('tr')

	return rows

# Uses URLs with an existing search criteria, see above
def updateInventory(urls, executionTime):

	for url in urls:
		print('URL Starting: ' + str(datetime.utcnow()))
		numBottles = 0
		numStores = 0
		error = 0
		rows = runScreenScrape(url)


		for row in rows:
			#time.sleep(5)
			counter = 1
			row_td = row.find_all('td')
			sku = None
			brand = None
			wtype = None
			desc = None
			size = None
			price = None
			link = None
			for rowtd in row_td:
				if counter == 1:
					sku = BeautifulSoup(str(rowtd), 'lxml').get_text()
				if counter == 2:
					brand = BeautifulSoup(str(rowtd), 'lxml').get_text()
				if counter == 3:
					wtype = BeautifulSoup(str(rowtd), 'lxml').get_text()
				if counter == 4: 
					desc = BeautifulSoup(str(rowtd), 'lxml').get_text()
				if counter == 5:
					size = BeautifulSoup(str(rowtd), 'lxml').get_text()
				if counter == 6:
					price = BeautifulSoup(str(rowtd), 'lxml').get_text()
				if counter == 7:
					link = rowtd.find('a').get('href')
					#print(brand,price)
					if link is not None:
						
						url = "https://www.meckabc.com/" + link
						html = urlopen(url)
						soup = BeautifulSoup(html, 'lxml')
						type(soup)
						data_table = soup.findAll('div', {'class':"store"})

						for divs in data_table:
							store = BeautifulSoup(str(divs.find('h3')), 'lxml').get_text()
							qty = BeautifulSoup(str(divs.find('div', {'class':"qty"})), 'lxml').get_text()
							addr = BeautifulSoup(str(divs.find('div', {'class':"addr"})), 'lxml').get_text()
							phone = BeautifulSoup(str(divs.find('div', {'class':"phone"})), 'lxml').get_text()
							
							numStores = numStores + 1
							#stores.append({'store':store.strip(),"quantity":qty.strip(),"address":addr.strip(),"phone": phone.strip()})

							# Clean up the data
							# Wasted space for quantity, removing "Bottles" or "Bottle" in count
							if ' Bottles' in qty:
								qty = qty.replace(' Bottles', '')
							else:
								qty = qty.replace(' Bottle', '')
							
							# Removing "/r/n" from data
							store = store.strip()
							qty = qty.strip()
							addr = addr.strip()
							phone = phone.strip()
							
							inventory = Inventory(sku=sku, brand=brand, wtype=wtype, description=desc, size=size, price=price, link=url, store=store.replace('Store ', ''), quantity=qty, address=addr, phone=phone.replace('Phone: ', ''), insertTime=executionTime)
							db.session.add(inventory)
							#print(store, qty, addr)
						#print(stores)
				counter = counter + 1
			# Commit to database
			db.session.commit()

def transferData():
	inventoryData = Inventory.query.all()

	if inventoryData:
		for data in inventoryData:
			db.session.query(DataHistory).delete()
			historyData = DataHistory(datadatetime=data.insertTime, sku=data.sku, wtype=data.wtype, description=data.description, size=data.size, price=data.price, store=data.store, quantity=data.quantity,address=data.address)
			db.session.add(historyData)
		db.session.commit()
		db.session.query(Inventory).delete()
		db.session.commit()

def updateLastUpdate(executionTime):
	lastUpdate = LastUpdate(recordcount=Inventory.query.count(), datestamp=executionTime)
	db.session.add(lastUpdate)
	db.session.commit()




