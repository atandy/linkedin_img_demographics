from clarifai.rest import ClarifaiApp
import os
import pandas as pd 
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename='face_demographics.log', 
    filemode='w', 
    format='%(asctime)s:%(levelname)s:%(message)s', 
    level=logging.DEBUG)

#https://fle.github.io/reset-a-postgresql-sequence-and-recompute-column-values.html

# create clarifai app and get models.
CLARIFAIAPI_KEY = os.getenv('CLARIFAIAPI_KEY')
app = ClarifaiApp(api_key=CLARIFAIAPI_KEY)
model = app.models.get('demographics')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
engine = create_engine(SQLALCHEMY_DATABASE_URI)

def get_image(image_url):
    try:
        print("Making request for {}".format(image_url))
        prediction = model.predict_by_url(image_url)
    except:
        return None
    '''
    try:
        face_data = prediction['outputs'][0]['data']['regions'][0]['data']['face']
    except:
        return None
    '''
    return prediction

# get data from db. 
df = pd.read_sql("SELECT * from linkedin_people;", con=engine, index_col='id')

df['clarifai_data'] = None
counter = 0
for idx, row in df.iterrows():

    counter +=1
    if counter > 500:
        try:
            image_url = row['image'].replace('"', '') # RIP
        except AttributeError as e:
            print(e)
            df.at[idx, 'clarifai_data'] = None
            continue
        logging.info("Handling index: {} with URL: {}".format(idx, image_url))
        prediction = get_image(image_url)
        df.at[idx, 'clarifai_data'] = prediction

# store data in a single csv
df.to_csv('main_data.csv')