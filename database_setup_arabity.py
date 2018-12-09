# used to manipulate diff parts of py run-time env.
import sys
import os
# import all modules needed for configuration
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
# base instance inherit all features of SQLAlchemy
Base = declarative_base()


# add class definition code
class CenterReg(Base):
    __tablename__ = 'center_reg'

# center_reg table mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    logo = Column(String(250), nullable=False)


# Addresses class definition code
class Addresses(Base):
    __tablename__ = 'addresses'

# addresses table mapper
    id = Column(Integer, primary_key=True)
    address = Column(String(250), nullable=False)
    parent_id = Column(Integer, nullable=False)


# CenterAdd class definition code
class CenterAdd(Base):
    __tablename__ = 'center_add'

# center_add table mapper
    id = Column(Integer, primary_key=True)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)
    address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
    addresses = relationship(Addresses)


# Telephones class definition code
class Telephones(Base):
    __tablename__ = 'telephones'

# telephones table mapper
    id = Column(Integer, primary_key=True)
    tel = Column(String(250), nullable=False)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)


# Mobiles class definition code
class Mobiles(Base):
    __tablename__ = 'telephones'

# mobiles table mapper
    id = Column(Integer, primary_key=True)
    mob = Column(String(250), nullable=False)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)


# Locations class definition code
class Locations(Base):
    __tablename__ = 'locations'

# locations table mapper
    id = Column(Integer, primary_key=True)
    loc = Column(String(250), nullable=False)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)


# Brands class definition code
class Brands(Base):
    __tablename__ = 'brands'

# brands table mapper
    id = Column(Integer, primary_key=True)
    brands = Column(String(20), nullable=False)
    parent_id = Column(Integer, nullable=False)


# ProviderBrand class definition code
class ProviderBrand(Base):
    __tablename__ = 'provider_brand'

# provider_brand table mapper
    id = Column(Integer, primary_key=True)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)
    brands_id = Column(Integer, ForeignKey('brands.id'), nullable=False)
    brands = relationship(Brands)


# Services class definition code
class Services(Base):
    __tablename__ = 'services'

# services table mapper
    id = Column(Integer, primary_key=True)
    services = Column(String(20), nullable=False)


# ProviderService class definition code
class ProviderService(Base):
    __tablename__ = 'provider_service'

# provider_service table mapper
    id = Column(Integer, primary_key = True)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)
    services_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    services = relationship(Services)

# Verification class definition code
class Verification(Base):
    __tablename__ = 'verification'

# verification table mapper
    id = Column(Integer, primary_key=True)
    services = Column(String(20), nullable=False)


# ProviderVerification class definition code
class ProviderVerification(Base):
    __tablename__ = 'provider_verification'

# provider_verification table mapper
    id = Column(Integer, primary_key = True)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)
    verification_id = Column(Integer, ForeignKey('verification.id'),
                             nullable=False)
    verification = relationship(Verification)


# Story class definition code
class Story(Base):
    __tablename__ = 'story'

# story table mapper
    id = Column(Integer, primary_key = True)
    storyby = Column(String(250), nullable=False)
    center_id = Column(Integer, ForeignKey('center_reg.id'), nullable=False)
    center_reg = relationship(CenterReg)

# === to connect to an existing db or create a new one ===
engine = create_engine('sqlite:///arabity.db')
Base.metadata.create_all(engine)
print("connected to arabity database")
