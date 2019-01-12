#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
db.init_app(app)

# === let program know which database engine we want to communicate===
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arabity.db'



# READ csv file create DataFrame sheet
sheet = pd.read_csv('/Users/macbookpro/projects/arabity/areasheet.csv')
# CREATE variable counter count all rows in the csv
row_counter = sheet.shape[0]
row_counter = int(row_counter)
# area = sheet['Area']
# area_len = len(area)

i_row = 0
while i_row < row_counter:
    prov_area = sheet.loc[sheet.index[i_row], 'Area']
    prov_name = sheet.loc[sheet.index[i_row], 'Name']
    area_address = Address.query.filter_by()
    session.query(Address).\
              filter(Address.address == prov_area).scalar()
    if area_address is None:
        # GIT governorate id which is parent id for area
        prov_gov = sheet.loc[sheet.index[i_row], 'Gov']
        gov_id = Address.query.filter_by(parent_id=0, address=prov_gov).one()
        # ADD area to address table
        area_address = Address(address=prov_area, parent_id=gov_id, type_id=3)
        session.add(area_address)
        session.commit()
    # ASSIGN address to provider_id in provider_add table
    print ("hablooooooooooooooooooooooo")
    print (prov_name)
    prov_id = session.query(Provider.id).\
                  filter(Provider.name == prov_name).scalar()
    print (prov_id)
    area_id = session.query(Address.id).\
              filter(Address.address == prov_area).scalar()
    prov_address = session.query(ProviderAdd).\
                    filter(ProviderAdd.provider_id == prov_id).scalar()
    if prov_address is None:
        prov_address = ProviderAdd(provider_id=prov_id,\
                        address_id=area_id)
        session.add(prov_address)
        session.commit()
    else:
        # address already exist so update with new value
        prov_address = session.query(ProviderAdd).\
                        filter_by(provider_id=prov_id).one()
        prov_address.address_id = area_id
        session.add(prov_address)
        session.commit()


    i_row += 1


"""# col_counter = sheet.shape[1]
# col_counter = int(col_counter)
print (sheet)
i_row = 0
prov_name = sheet.loc[sheet.index[i_row], 'Name']
print(prov_name)
i_row = 0
while i_row < row_counter:
    prov_name = sheet.loc[sheet.index[i_row], 'Name']
    prov_gov = sheet.loc[sheet.index[i_row], 'Gov']
    prov_area = sheet.loc[sheet.index[i_row], 'Area']
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

    # ADD provider Area to databsase
    area = session.query(Address).filter_by(address=prov_area).one()
    if area not
    prov_add = ProviderAdd(provider_id=newprovider.id, address_id=address.id)
    session.add(prov_add)
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

for gov in govadd:
    add = Address(address=gov, parent_id=0)
    session.add(add)
    session.commit()
"""
