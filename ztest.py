#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import pandas
import numpy as np
import pandas as pd

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


# READ csv file create DataFrame sheet
sheet = pd.read_csv('/Users/macbookpro/projects/arabity/5krecord.csv')
# CREATE variable counter count all rows in the csv
row_counter = sheet.shape[0]
row_counter = int(row_counter)
# area = sheet['Area']
# area_len = len(area)

i_row = 0
while i_row < row_counter:
    prov_area = sheet.loc[sheet.index[i_row], 'Gov']
    prov_area = list(prov_area)
    prov_area = prov_area[:-1]
    prov_area = "".join(prov_area)
    print (prov_area)
    i_row += 1
