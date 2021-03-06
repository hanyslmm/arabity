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
db.init_app(app)


# read csv file create DataFrame sheet
sheet = pd.read_csv('/Users/macbookpro/projects/arabity/sheets/5krecord.csv')
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
    #prov_gov = sheet.loc[sheet.index[i_row], 'Gov']
    #prov_logo = sheet.loc[sheet.index[i_row], 'Logo']
    #prov_mob = sheet.loc[sheet.index[i_row], 'Mobile']
    #prov_tel = sheet.loc[sheet.index[i_row], 'Telephone']
    #prov_user = sheet.loc[sheet.index[i_row], 'User']
    #prov_area = sheet.loc[sheet.index[i_row], 'Area']
    #prov_brand = sheet.loc[sheet.index[i_row], 'Brand']
    #prov_service = sheet.loc[sheet.index[i_row], 'Service']
    #prov_dayOff = sheet.loc[sheet.index[i_row], 'DayOff']
    #prov_OpenH = sheet.loc[sheet.index[i_row], 'OpenH']
    prov_CloseH = sheet.loc[sheet.index[i_row], 'CloseH']
    #prov_mob = int(prov_mob)
    #prov_tel = int(prov_tel)
    #prov_user = int(prov_user)
    #prov_username = prov_name + str(random.randint(1,10000))
    # REMOVE last . in gov name and add to database
    #prov_gov = str(prov_gov)
    #prov_gov = list(prov_gov)
    #prov_gov = prov_gov[:-1]
    #prov_gov = "".join(prov_gov)
    #print (prov_gov)
    #print (prov_dayOff)
    prov_exist = Provider.query.filter_by(username=prov_username).scalar()
    if prov_exist is None:
        # ADD new provider with name and logo
        newprovider = Provider(name=prov_name, username=prov_username\
                                ,logo=prov_logo, user_id=3)
        db.session.add(newprovider)
        db.session.commit()

        # ADD provider mobile
        mobile = Mobile(mob=prov_mob, provider=newprovider)
        db.session.add(mobile)
        db.session.commit()

        # ADD provider telephone
        telephone = Telephone(tel=prov_tel, provider=newprovider)
        db.session.add(telephone)
        db.session.commit()
        # SEARCH for gov address in address table
        gov_address = Address.query.filter_by(parent_id=0,\
                                            address=prov_gov).scalar()
        if gov_address is None:
            # ADD new governorate name to address table
            gov_address = Address(address=prov_gov, parent_id=0, type_id=2)
            db.session.add(gov_address)
            db.session.commit()

        # SEARCH for area address in address table
        area_address = Address.query.filter_by(address=prov_area).scalar()
        if area_address is None:
            # GIT governorate id which is parent id for area
            gov_id = gov_address.id
            # ADD area to address table
            area_address = Address(address=prov_area, parent_id=gov_id,\
                                        type_id=3)
            db.session.add(area_address)
            db.session.commit()

        # SEARCH for brand name in brand table
        prov_brand_list = prov_brand.split()
        for i in prov_brand_list:
            brandName = Brand.query.filter_by(parent_id=0,\
                                                brand=i).scalar()
            if brandName is None:
                brandName = Brand(parent_id=0, brand=i, type_id=2)
                db.session.add(brandName)
                db.session.commit()
            # ADD new relation between brand and provider
            brandName.providers.append(newprovider)
            db.session.commit()


        # SEARCH for dayOff name in day table
        prov_dayOff_list = prov_dayOff.split()
        print (prov_dayOff_list)
        for i in prov_dayOff_list:
            dayOff = Day.query.filter_by(days=i).scalar()
            if dayOff is None:
                dayOff = Day(days=i)
                db.session.add(dayOff)
                db.session.commit()
            # ADD new relation between brand and provider
            dayOff.providers.append(newprovider)
            db.session.commit()

        # SEARCH for open Hour in Hour table
        openH = Hour.query.filter_by(hours=prov_OpenH).scalar()
        if openH is None:
            openH = Hour(hours=prov_OpenH)
            db.session.add(openH)
            db.session.commit()
        # ADD new relation in provider open hour
        openH.providersOpen.append(newprovider)
        db.session.commit()


        # SEARCH for close Hour in Hour table
        closeH = Hour.query.filter_by(hours=prov_CloseH).scalar()
        if closeH is None:
            closeH = Hour(hours=prov_CloseH)
            db.session.add(closeH)
            db.session.commit()
        # ADD new relation in provider open hour
        closeH.providersClose.append(newprovider)
        db.session.commit()


        # SEARCH for service name in service table
        prov_service_list = prov_service.split()
        for i in prov_service_list:
            serviceName = Service.query.filter_by(serviceType=i).scalar()
            if serviceName is None:
                serviceName = Service(serviceType=i)
                db.session.add(serviceName)
                db.session.commit()
            # ADD new relation between servicetype and provider
            serviceName.providers.append(newprovider)
            db.session.commit()


        # GIT id number of provider, gov, area
        print ("getting id numbers of {}".format(newprovider.name))
        prov_id = newprovider.id
        area_id = area_address.id
        gov_id = gov_address.id



        prov_address = ProviderAdd.query.filter_by(provider_id=prov_id).scalar()
        if prov_address is None:
            prov_address = ProviderAdd(provider=newprovider,\
                            address_id=area_id, gov_id=gov_id)
            db.session.add(prov_address)
            db.session.commit()
        else:
            # address already exist so update with new value
            prov_address.address_id = area_id
            prov_address.gov_id = gov_id
            db.session.add(prov_address)
            db.session.commit()


    else:
        print ("provider name {} already exist".format(prov_exist.name))
    i_row += 1

print ("done!!!!")






"""booleans = []
for length in sheet.Gov:
    if length == "Alexandria":
        booleans.append(True)
    else:
        booleans.append(False)"""




# Interact with my database and see what's inside of it
