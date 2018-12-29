#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import pandas
import numpy as np
import pandas as pd

# import all modules needed for configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from database_setup_arabity import Base, Provider, User, UserType, Story
from database_setup_arabity import Address, ProviderAdd, Telephone
from database_setup_arabity import Mobile, AddType



# === let program know which database engine we want to communicate===
engine = create_engine('sqlite:///arabity.db')

# bind the engine to the Base class corresponding tables
Base.metadata.bind = engine

# create session maker object
DBSession = sessionmaker(bind = engine)
session = DBSession()


# READ csv file create DataFrame df
df = pd.read_csv('/Users/macbookpro/projects/arabity/addtype.csv')
# CREATE variable counter count all rows in the csv
row_counter = df.shape[0]
row_counter = int(row_counter)

print (df)

i_row = 0
while i_row < row_counter:
    # GIT type for address add_type
    add_type = df.loc[df.index[i_row], 'Type']
    type = session.query(AddType).\
              filter(AddType.name==add_type).scalar()
    if type is None:
        # ADD type to add_type table
        newtype = AddType(name=add_type)
        session.add(newtype)
        session.commit()
    else:
        # type already exist so do nothing
        print ("type already exist")
    i_row += 1
