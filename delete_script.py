#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import all modules needed for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from database_setup_arabity import Base, Provider, User, UserType, Story
from database_setup_arabity import Address, ProviderAdd, Telephone, Mobile


# === let program know which database engine we want to communicate===
engine = create_engine('sqlite:///arabity.db')

# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine

# create session maker object
DBSession = sessionmaker(bind = engine)
session = DBSession()

deletedProvider = session.query(Provider).filter(Provider.id > 4).all()
for i in deletedProvider:
    print (i.name)


deletedmobile = session.query(Mobile).filter(Mobile.provider_id > 4)
for i in deletedmobile:
    print (i.mob)
for i in deletedProvider:
    session.delete(i)
session.commit()

# Interact with my database and see what's inside of it

"""vaggis = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for vaggi in vaggis:
    print(vaggi.id)
    print(vaggi.price)
    print(vaggi.restaurant.name)
    print("\n")
BurgerFuther = session.query(MenuItem).filter_by(id = 8).one()
print(BurgerFuther.price)
print("\n")

BurgerFuther.price = '$2.99'
session.add(BurgerFuther)
session.commit()"""
