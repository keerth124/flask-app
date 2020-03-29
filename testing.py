from urllib.request import urlopen
from bs4 import BeautifulSoup
#import time
from app import db
from app.models import Inventory, LastUpdate, DataHistory
from datetime import datetime

rows = Inventory.query.all()
for row in rows:
	searchResults = db.session.query(DataHistory).filter(DataHistory.sku==row.sku).filter(DataHistory.store==row.store).filter(DataHistory.size ==row.size).filter(DataHistory.datadatetime==row.insertTime)
	if searchResults is None:
		print(searchResults.fetchall())
	

