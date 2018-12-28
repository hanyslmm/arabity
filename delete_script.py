#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# used to manipulate diff parts of py run-time env.
import sys
import datetime
import os
import numpy as np
import pandas as pd

# import all modules needed for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from database_setup_arabity import Base, Provider, User, UserType, Story
from database_setup_arabity import Address, ProviderAdd, Telephone, Mobile
from flask import jsonify
import json


# === let program know which database engine we want to communicate===
engine = create_engine('sqlite:///arabity.db')

# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine

# create session maker object
DBSession = sessionmaker(bind = engine)
session = DBSession()

# read csv file create DataFrame sheet
sheet = pd.read_csv('/Users/macbookpro/projects/arabity/testo.csv')
# create variable counter count all rows and columns in the csv
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
    prov_user - int(prov_user)


    # ADD new provider with name and logo
    newprovider = Provider(name=prov_name, logo=prov_logo, user_id=3)
    session.add(newprovider)
    session.commit()

    # ADD provider address id
    address = session.query(Address).filter_by(address=prov_gov).one()
    prov_add = ProviderAdd(provider_id=newprovider.id, address_id=address.id)
    session.add(prov_add)
    session.commit()

    # ADD provider mobile
    mobile = Mobile(mob=prov_mob, provider_id=newprovider.id)
    session.add(mobile)
    session.commit()

    # ADD provider telephone
    telephone = Telephone(tel=prov_tel, provider_id=newprovider.id)
    session.add(telephone)
    session.commit()

    i_row += 1












"""booleans = []
for length in sheet.Gov:
    if length == "Alexandria":
        booleans.append(True)
    else:
        booleans.append(False)"""




# Interact with my database and see what's inside of it
