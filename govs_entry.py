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


# adding governorate address
govadd1 = ["Alexandria", 'Aswan', 'Asyut', 'Beheira', 'Beni Suef', 'Cairo', 'Dakahlia', 'Damietta', 'Faiyum']
govadd2 = ['Gharbia', 'Giza', 'Ismailia', 'Kafr el-Sheikh', 'Matruh', 'Minya', 'Monufia']
govadd3 = ['New Valley', 'North Sinai', 'Port Said', 'Qalyubia', 'Qena', 'Red Sea']
govadd4 = ['Al Sharqia', 'Sohag', 'South Sinai', 'Suez', 'Luxor']
govadd = govadd1 + govadd2 + govadd3 + govadd4
print(govadd)

for gov in govadd:
    add = Address(address=gov, parent_id=0)
    session.add(add)
    session.commit()
