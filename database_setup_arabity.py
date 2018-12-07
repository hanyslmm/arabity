# used to manipulate diff parts of py run-time env.
import sys
import os

# import all modules needed for configuration
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

 # base instance inherit all features of SQLAlchemy
 Base = declarative_base()



# === to connect to an existing db or create a new one ===
engine = create_engine('sqlite:///arabity.db')
Base.metadata.create_all(engine)
print("connected to arabity database")
