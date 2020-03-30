# flask-app

# run using dev_appserver.py app.yaml on gcloud
# gcloud app deploy for execution to prod server

# run virtual environment:
#   source venv/Scripts/activate

## Installation
First, load virutal environment:
'''
source venv/Scripts/activate
'''
if source doesn't work
'''
venv/Scripts/activate
'''

Load dependencies:
'''
pip install -r requirements.txt
'''

## Set up for packaging
'''
pip freeze > requirements.txt
'''

## Gcloud
To load on gcloud dev server run:
'''
dev_appserver.py app.yaml
'''

To deploy:
'''
gcloud app deploy
gcloud app browse
'''



