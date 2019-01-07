#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

# import pandas
import numpy as np
import pandas as pd

# import all modules needed for configuration
# IMPORT flask and sqlalchemy
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from database_setup_arabity import *

# initializes an app variable, using the __name__ attribute
app = Flask(__name__)

# === let program know which database engine we want to communicate===
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arabity.db'
db = SQLAlchemy(app)


# read csv file create DataFrame sheet
sheet = pd.read_csv('/Users/macbookpro/projects/arabity/5krecord.csv')
# create variable counter count all rows in the csv
row_counter = sheet.shape[0]
row_counter = int(row_counter)
# col_counter = sheet.shape[1]
# col_counter = int(col_counter)
print (sheet)
i_row = 0
prov_name = sheet.loc[sheet.index[i_row], 'Name']
print(prov_name)
i_row = 0
while i_row < row_counter:
    prov_name = sheet.loc[sheet.index[i_row], 'Name']
    prov_gov = sheet.loc[sheet.index[i_row], 'Gov']
    prov_logo = sheet.loc[sheet.index[i_row], 'Logo']
    prov_mob = sheet.loc[sheet.index[i_row], 'Mobile']
    prov_tel = sheet.loc[sheet.index[i_row], 'Telephone']
    prov_user = sheet.loc[sheet.index[i_row], 'User']
    prov_mob = int(prov_mob)
    prov_tel = int(prov_tel)
    prov_user = int(prov_user)
    prov_username = prov_name + str(random.randint(1,1000))
    print (prov_mob)
    print (prov_tel)
    prov_exist = Provider.query.filter_by(username=prov_username).scalar()
    if prov_exist is None:
        # ADD new provider with name and logo
        newprovider = Provider(name=prov_name, username=prov_username\
                                ,logo=prov_logo, user_id=3)
        db.session.add(newprovider)
        db.session.commit()

        # ADD provider mobile
        mobile = Mobile(mob=prov_mob, provider_id=newprovider.id)
        db.session.add(mobile)
        db.session.commit()

        # ADD provider telephone
        telephone = Telephone(tel=prov_tel, provider_id=newprovider.id)
        db.session.add(telephone)
        db.session.commit()
    else:
        print ("provider name {} already exist".format(prov_exist))
    i_row += 1







"""booleans = []
for length in sheet.Gov:
    if length == "Alexandria":
        booleans.append(True)
    else:
        booleans.append(False)"""




# Interact with my database and see what's inside of it
