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

# READ csv file create DataFrame df
df = pd.read_csv('/Users/macbookpro/projects/arabity/sheets/brandtype.csv')
# CREATE variable counter count all rows in the csv
row_counter = df.shape[0]
row_counter = int(row_counter)

print (df)

i_row = 0
while i_row < row_counter:
    # GIT type for address add_type
    brand_type = df.loc[df.index[i_row], 'Type']
    type = BrandType.query.filter_by(name=brand_type).scalar()
    if type is None:
        # ADD type to add_type table
        newtype = BrandType(name=brand_type)
        db.session.add(newtype)
    else:
        # type already exist so do nothing
        print ("{} type already exist".format(type.name))
    i_row += 1
db.session.commit()
print ("brand types added Successfully")
