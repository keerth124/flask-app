# flask-app

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

## Execute
```bash
python main.py
```
or
'''
flask run
''' 

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




