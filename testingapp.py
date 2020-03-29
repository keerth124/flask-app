from urllib.request import urlopen
from bs4 import BeautifulSoup
from app import db
from app.models import Inventory, LastUpdate, DataHistory
from datetime import datetime


def printOut():
    print('Im in testing.py now!!')