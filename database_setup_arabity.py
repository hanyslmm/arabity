# used to manipulate diff parts of py run-time env.
import sys
import datetime
import os
# import all modules needed for configuration
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
# base instance inherit all features of SQLAlchemy
Base = declarative_base()


# add usertype class definition code for usertype table
class UserType(Base):
    __tablename__ = 'usertype'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


# add class definition code and mapper for user table
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    user_type = Column(Integer, ForeignKey('usertype.id'), nullable=False)
    usertype = relationship(UserType)


# Provider class definition code
class Provider(Base):
    __tablename__ = 'provider'

# provider table mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    logo = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship(User)


# Address class definition code
class Address(Base):
    __tablename__ = 'address'

# address table mapper
    id = Column(Integer, primary_key=True)
    address = Column(String(80), nullable=False)
    parent_id = Column(Integer, nullable=False)


# ProviderAdd class definition code
class ProviderAdd(Base):
    __tablename__ = 'provider_add'

# provider_add table mapper
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)
    address_id = Column(Integer, ForeignKey('address.id'), nullable=False)
    address = relationship(Address)


# Telephone class definition code
class Telephone(Base):
    __tablename__ = 'telephone'

# telephone table mapper
    id = Column(Integer, primary_key=True)
    tel = Column(String(20), nullable=False)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)


# Mobile class definition code
class Mobile(Base):
    __tablename__ = 'mobile'

# mobile table mapper
    id = Column(Integer, primary_key=True)
    mob = Column(String(20), nullable=False)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)


# Location class definition code
class Location(Base):
    __tablename__ = 'location'

# location table mapper
    id = Column(Integer, primary_key=True)
    loc = Column(String(250), nullable=False)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)


# Brand class definition code
class Brand(Base):
    __tablename__ = 'brand'

# brand table mapper
    id = Column(Integer, primary_key=True)
    brand = Column(String(20), nullable=False)
    parent_id = Column(Integer, nullable=False)


# ProviderBrand class definition code
class ProviderBrand(Base):
    __tablename__ = 'provider_brand'

# provider_brand table mapper
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)
    brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False)
    brand = relationship(Brand)


# Service class definition code
class Service(Base):
    __tablename__ = 'service'

# service table mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


# ProviderService class definition code
class ProviderService(Base):
    __tablename__ = 'provider_service'

# provider_service table mapper
    id = Column(Integer, primary_key = True)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    service = relationship(Service)


# Verification class definition code
class Verification(Base):
    __tablename__ = 'verification'

# verification table mapper
    id = Column(Integer, primary_key=True)
    verify = Column(String(20), nullable=False)


# ProviderVerification class definition code
class ProviderVerification(Base):
    __tablename__ = 'provider_verification'

# provider_verification table mapper
    id = Column(Integer, primary_key = True)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)
    verification_id = Column(Integer, ForeignKey('verification.id'),
                             nullable=False)
    verification = relationship(Verification)


# Story class definition code
class Story(Base):
    __tablename__ = 'story'

# story table mapper
    id = Column(Integer, primary_key = True)
    storyby = Column(String(250), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)


# SocialType class definition code
class SocialType(Base):
    __tablename__ = 'socialtype'

# socialtype table mapper
    id = Column(Integer, primary_key=True)
    type = Column(String(20), nullable=False)
    logo = Column(String(250), nullable=False)


# SocialLink class definition code
class SocialLink(Base):
    __tablename__ = 'social_link'

# social_link table mapper
    id = Column(Integer, primary_key = True)
    link = Column(String(250), nullable=False)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)
    socialtype_id = Column(Integer, ForeignKey('socialtype.id'), nullable=False)
    socialtype = relationship(SocialType)


# Tag class definition code
class Tag(Base):
    __tablename__ = 'tag'

# tag table mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


# ProviderTag class definition code
class ProviderTag(Base):
    __tablename__ = 'provider_tag'

# provider_teg table mapper
    id = Column(Integer, primary_key = True)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)
    tag = relationship(Tag)


# Extra class definition code
class Extra(Base):
    __tablename__ = 'extra'

# extra table mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)


# ProviderExtra class definition code
class ProviderExtra(Base):
    __tablename__ = 'provider_extra'

# provider_extra table mapper
    id = Column(Integer, primary_key = True)
    provider_id = Column(Integer, ForeignKey('provider.id'), nullable=False)
    provider = relationship(Provider)
    extra_id = Column(Integer, ForeignKey('extra.id'), nullable=False)
    extra = relationship(Extra)


# === to connect to an existing db or create a new one ===
engine = create_engine('sqlite:///arabity.db')
Base.metadata.create_all(engine)
print("connected to arabity database")

if __name__ == '__main__':
    # fill usertype table with Admin and Normal
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    normal = UserType(name='Normal')
    session.add(normal)
    admin = UserType(name='Admin')
    session.add(admin)
    session.commit()
