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

# Create Admin user
adminUser = User(name="Arabity", email="arabity4@gmail.com",
             picture='https://secure.gravatar.com/avatar/22ccd1d726®91c9ed4f6d235863713c45', user_type=2)
session.add(adminUser)
session.commit()





"""# adding governorate address
govadd1 = ["Alexandria", 'Aswan', 'Asyut', 'Beheira', 'Beni Suef', 'Cairo', 'Dakahlia', 'Damietta', 'Faiyum']
govadd2 = ['Gharbia', 'Giza', 'Ismailia', 'Kafr el-Sheikh', 'Matruh', 'Minya', 'Monufia']
govadd3 = ['New Valley', 'North Sinai', 'Port Said', 'Qalyubia', 'Qena', 'Red Sea']
govadd4 = ['Al Sharqia', 'Sohag', 'South Sinai', 'Suez', 'Luxor']
govadd = govadd1 + govadd2 + govadd3 + govadd4
print(govadd)

for gov in govadd:
    add = Address(address=gov, parent_id=0)
    session.add(add)
    session.commit()"""

"""# Interact with my database and see what's inside address
govs = session.query(Address).all()
for gov in govs:
    print(gov.id)
    print(gov.address)
    print("\n")

provider_id = 5
provadd = session.query(ProviderAdd).filter_by(provider_id=provider_id).one()
if provadd != None:
    add = session.query(Address).filter_by(id=provadd.address_id).one()
    print (add.address)"""
# adding new entry to arabity database
"""newEntry = ClassName(property = "value", )
session.add(newEntry)
session.commit()"""
"""myFirstProvider = Provider(name = "Pizza Father")
session.add(myFirstProvider)
session.commit()"""
# end of adding Provider Pizza Station

# hablo = session.query(Provider).filter_by(id=1).one()

"""# adding new ServiceItem entry to Pizza Station
provider1 = Telephone(tel="02334987", provider=hablo)
session.add(provider1)
session.commit()# all items created in menu_items.py

provider1 = Mobile(mob="01222345349", provider=hablo)
session.add(provider1)
session.commit()
"""
# provider1 = Story(post="a7la markz syana fe el 3alm احلى مركز صيانة ",
#                  provider=hablo, user_id=2)
# session.add(provider1)
# session.commit()

# Interact with my database and see what's inside of it
"""vaggis = session.query(ServiceItem).filter_by(name = 'Veggie Burger')
for vaggi in vaggis:
    print(vaggi.id)
    print(vaggi.price)
    print(vaggi.provider.name)
    print("\n")
BurgerFuther = session.query(ServiceItem).filter_by(id = 8).one()
print(BurgerFuther.price)
print("\n")

BurgerFuther.price = '$2.99'
session.add(BurgerFuther)
session.commit()

vaggis = session.query(ServiceItem).filter_by(name = 'Veggie Burger')
for vaggi in vaggis:
    print(vaggi.id)
    print(vaggi.price)
    print(vaggi.provider.name)
    print("\n")"""
