# flask-app
This app is a compilation of learning Flask and SQL Alchemy here https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
The end result of this application was based off a problem I saw with the Mecklenburg County ABC Store.  I wanted to determine what rare bottles of bourbon were at my local ABC store but the website only allowed me to search by bottle and then it would tell me which stores had it, if any.  

This app screen scrapes the ABC store website, stores this data, and then pivots it to be available online using a Flask web app.  http://abcstore.eastus.cloudapp.azure.com:8000/ - create an account to check it out! 


## Installation
First, load virutal environment:
```bash
source venv/Scripts/activate
```
if source doesn't work
```bash
venv/Scripts/activate
```

Load dependencies:
```bash
pip install -r requirements.txt
```
```bash
pip install -r requirements.txt -t lib/
```d

## Execute
```bash
python main.py
```
or
```
flask run
``` 

## Set up for packaging
```bash
pip freeze > requirements.txt
```

## Gcloud
To load on gcloud dev server run:
```bash
dev_appserver.py app.yaml
```

To deploy:
```bash
gcloud app deploy
gcloud app browse
```




