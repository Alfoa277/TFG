import os.path
from flask import Flask, render_template, request, redirect, Response, url_for, flash
import pandas as pd
import numpy as np
import pickle
import tensorflow
from tensorflow import keras
from keras.models import load_model
import torch

app = Flask(__name__)


@app.route("/")
def home():
    options_df = pd.read_csv("selectedRent_web.csv",sep=";")
    town_data = options_df.groupby('PROVINCE')['TOWN'].unique().apply(list).to_dict()
    return render_template('main.html', type_options=options_df['TYPE'].unique(), province_options=options_df['PROVINCE'].unique(),town_options = town_data, flag="false")


@app.route("/query", methods=["POST"])
def submit():
  options_df = pd.read_csv("selectedRent_web.csv",sep=";")
  variables = request.form
  print(variables)
  data = []
  responses = []
  for i in variables:
    data.append(variables[i])
    responses.append(variables[i])
  if len(data)!=10:
    town_data = options_df.groupby('PROVINCE')['TOWN'].unique().apply(list).to_dict()
    return render_template('main.html', type_options=options_df['TYPE'].unique(), province_options=options_df['PROVINCE'].unique(),town_options = town_data, flag="true")

  data[0] = 'TYPE'+data[0].replace(' ','.')
  data[1] = 'PROVINCE'+data[1].replace(' ','.')
  data[2] = 'TOWN'+data[2].replace(' ','.')
  data[6] = 'LOCATION'+data[6]
  data[7] = 'ELEVATOR'+data[7]
  data[8] = 'GARAGE'+data[8].upper()
  print(data)

  rent = pd.read_csv("rentSelected_plus.csv",sep=";")
  rent.loc[len(rent)] = 0
  if data[0] in list(rent):
    rent.loc[len(rent)-1,data[0]] = 1
  if data[1] in list(rent):
    rent.loc[len(rent)-1,data[1]] = 1
  if data[2] in list(rent):
    rent.loc[len(rent)-1,data[2]] = 1
  if data[6] in list(rent):
    rent.loc[len(rent)-1,data[6]] = 1
  if data[7] in list(rent):
    rent.loc[len(rent)-1,data[7]] = 1
  if data[8] in list(rent):
    rent.loc[len(rent)-1,data[8]] = 1
  temp = options_df[options_df['TOWN']==responses[2]]
  num_houses = temp['NUM_HOUSES'].to_list()[0]
  population = temp['POPULATION'].to_list()[0]

  rent.loc[len(rent)-1,'ROOMS'] = data[3]
  rent.loc[len(rent)-1,'AREA'] = data[4]
  rent.loc[len(rent)-1,'FLOOR'] = data[5]


  rent.loc[len(rent)-1,'NUM_HOUSES']=num_houses
  rent.loc[len(rent)-1,'POPULATION']=population

  temp_ = rent.drop(['PRICE'],axis=1)
  temp_['AREA'] = temp_['AREA'].astype(int)
  temp_['AREA'] = (temp_['AREA'] - np.mean(temp_['AREA']))/np.std(temp_['AREA'])
  temp_['ROOMS'] = temp_['ROOMS'].astype(int)
  temp_['ROOMS'] = (temp_['ROOMS'] - np.mean(temp_['ROOMS']))/np.std(temp_['ROOMS'])
  temp_['FLOOR'] = temp_['FLOOR'].astype(int)
  temp_['FLOOR'] = (temp_['FLOOR'] - np.mean(temp_['FLOOR']))/np.std(temp_['FLOOR'])
  temp_['POPULATION'] = temp_['POPULATION'].astype(int)
  temp_['POPULATION'] = (temp_['POPULATION'] - np.mean(temp_['POPULATION']))/np.std(temp_['POPULATION'])
  temp_['NUM_HOUSES'] = temp_['NUM_HOUSES'].astype(int)
  temp_['NUM_HOUSES'] = (temp_['NUM_HOUSES'] - np.mean(temp_['NUM_HOUSES']))/np.std(temp_['NUM_HOUSES'])

  target = temp_.loc[len(rent)-1]
  target = target.astype(int)

  mean_price = 0
  sd_price = 0
  
  with open('normalization.pkl', 'rb') as inp:
    mean_price = pickle.load(inp)
    sd_price = pickle.load(inp)

  
  model = load_model('Model')

  target_numpy = target.to_numpy()
  print(target_numpy.shape)
  target_numpy = target_numpy.reshape(1, -1)
  print(target_numpy.shape)
  prediction=model.predict(target_numpy)
  pred = prediction[0][0]
  print((pred*sd_price)+mean_price)

  responses[2] = responses[2].title()
  price = (pred*sd_price)+mean_price
  purchase_price = responses.pop()
  responses.append(round(price,2))

  if purchase_price!='0':
    responses.append(round(round(price,2)*12/int(purchase_price),4))
  else:
    responses.append('-')
  
  return render_template('result.html', results = responses)