# used to manipulate diff parts of py run-time env.
import sys
import datetime
import os
# IMPORT flask and sqlalchemy
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# initializes an app variable, using the __name__ attribute
app = Flask(__name__)

# let program know which database db.Model engine we want to communicate
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arabity.db'
db = SQLAlchemy(app)


# ADD user_type class definition code for user_type table
class UserType(db.Model): #change user_type table to user_table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    users = db.relationship('User', backref='type')


# ADD class definition code and mapper for user table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    picture = db.Column(db.String(250))
    providers = db.relationship('Provider', backref='user')
    stories = db.relationship('Story', backref='user')
    user_type = db.Column(db.Integer, db.ForeignKey('user_type.id'),\
                            nullable=False)

# PROVIDER service table mapper
prov_service = db.Table('prov_service',
            db.Column('provider_id',db.Integer, db.ForeignKey('provider.id')),
            db.Column('service_id',db.Integer, db.ForeignKey('service.id')))


# PROVIDER Brand table mapper
prov_brand = db.Table('prov_brand',
            db.Column('provider_id',db.Integer, db.ForeignKey('provider.id')),
            db.Column('brand_id',db.Integer, db.ForeignKey('brand.id')))


# PROVIDER daysOff table mapper
prov_dayOff = db.Table('prov_dayOff',
            db.Column('provider_id',db.Integer, db.ForeignKey('provider.id')),
            db.Column('dayOff_id',db.Integer, db.ForeignKey('day.id')))

# PROVIDER openH table mapper
prov_openH = db.Table('prov_openH',
            db.Column('provider_id',db.Integer, db.ForeignKey('provider.id')),
            db.Column('hour_id',db.Integer, db.ForeignKey('hour.id')))

# PROVIDER closeH table mapper
prov_closeH = db.Table('prov_closeH',
            db.Column('provider_id',db.Integer, db.ForeignKey('provider.id')),
            db.Column('hour_id',db.Integer, db.ForeignKey('hour.id')))


# PROVIDER table mapper
class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    logo = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # DEFINE relationship with mobile table
    mobiles = db.relationship('Mobile', cascade="all,delete",\
                                                            backref='provider')
    # DEFINE relationship with telephone table
    telephones = db.relationship('Telephone', cascade="all,delete",\
                                                            backref='provider')
    # DEFINE relationship with story table
    stories = db.relationship('Story', cascade="all,delete", backref='provider')
    # DEFINE relationship with provider_add table
    address = db.relationship('ProviderAdd', cascade="all,delete",\
                                                            backref='provider')
    # DEFINE relationship with provider_brand table many to many
    brands = db.relationship('Brand', secondary="prov_brand", \
                                backref=db.backref('provider', lazy='dynamic'))
    # DELETE all orphans incase deleting any provider
    # DEFINE relationship with provider_service table many to many
    services = db.relationship('Service', secondary="prov_service", \
                                backref=db.backref('provider', lazy='dynamic'))
    # DEFINE relationship with provider_daysOff table many to many
    daysOff = db.relationship('Day', secondary="prov_dayOff", \
                                backref=db.backref('provider', lazy='dynamic'))
    # DEFINE relationship with provider_openH table many to many
    openH = db.relationship('Hour', secondary="prov_openH", \
                                backref=db.backref('providerOpen', lazy='dynamic'))
    closeH = db.relationship('Hour', secondary="prov_closeH", \
                                backref=db.backref('providerClose', lazy='dynamic'))





# Mobile class definition code one to many
class Mobile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mob = db.Column(db.String(20), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)


# Telephone class definition code telephone one to many
class Telephone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tel = db.Column(db.String(20), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)


# PROVIDERADD class definition code provider_add
class ProviderAdd(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    address_id = db.Column(db.Integer, nullable=False)
    gov_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    providers = db.relationship('Provider', backref='providerAdd')


# ADDREESS class definition code
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(80), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('add_type.id'), nullable=False)
    # DEFINE relationship with provider_add table
    provAdd = db.relationship('ProviderAdd', backref='address')

# ADD AddType class definition code for add_type table
class AddType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    addresses = db.relationship('Address', backref='add')


# Brand class definition code many to many with provider table
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('brand_type.id'), nullable=False)
    # DEFINE relationship with provider table many to many
    providers = db.relationship('Provider', secondary="prov_brand", \
                                backref=db.backref('providerBrand', lazy='dynamic'))


# Service class definition code
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serviceType = db.Column(db.String(20), nullable=False)
    # DEFINE relationship with provider table many to many
    providers = db.relationship('Provider', secondary="prov_service", \
                                backref=db.backref('providerService', lazy='dynamic'))


# Service class definition code
class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    days = db.Column(db.String(20), nullable=False)
    # DEFINE relationship with provider table many to many
    providers = db.relationship('Provider', secondary="prov_dayOff", \
                                backref=db.backref('providerDay', lazy='dynamic'))

# Service class definition code
class Hour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.String(20), nullable=False)
    # DEFINE relationship with provider table many to many
    providersOpen = db.relationship('Provider', secondary="prov_openH", \
                            backref=db.backref('providerOpen', lazy='dynamic'))
    providersClose = db.relationship('Provider', secondary="prov_closeH", \
                            backref=db.backref('providerClose', lazy='dynamic'))

# ADD BrandType class definition code for brand_type table
class BrandType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    brands = db.relationship('Brand', backref='brandType')


# Story class definition code
class Story(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    post = db.Column(db.String(250), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


"""    location = db.relationship("Location", cascade="all, delete-orphan")
    provider_service = db.relationship("ProviderService", cascade="all, delete-orphan")
    provider_verification = db.relationship("ProviderVerification", cascade="all, delete-orphan")
    social_link = db.relationship("SocialLink", cascade="all, delete-orphan")
    provider_tag = db.relationship("ProviderTag", cascade="all, delete-orphan")
    provider_extra = db.relationship("ProviderExtra", cascade="all, delete-orphan")"""



"""# Location class definition code
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.String(250), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    provider = db.relationship(Provider)"""


"""# Service class definition code
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


# ProviderService class definition code
class ProviderService(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    provider = db.relationship(Provider)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    service = db.relationship(Service)"""


"""# Verification class definition code
class Verification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    verify = db.Column(db.String(20), nullable=False)


# ProviderVerification class definition code
class ProviderVerification(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    provider = db.relationship(Provider)
    verification_id = db.Column(db.Integer, db.ForeignKey('verification.id'),
                             nullable=False)
    verification = db.relationship(Verification)"""


"""# SocialType class definition code
class SocialType(db.Model): #change socialtable to social_table
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    logo = db.Column(db.String(250), nullable=False)


# SocialLink class definition code
class SocialLink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(250), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    provider = db.relationship(Provider)
    social_id = db.Column(db.Integer, db.ForeignKey('social_type.id'), nullable=False)
    social_type = db.relationship(SocialType)"""


"""# Tag class definition code
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


# ProviderTag class definition code
class ProviderTag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    provider = db.relationship(Provider)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), nullable=False)
    tag = db.relationship(Tag)"""


"""# Extra class definition code
class Extra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


# ProviderExtra class definition code
class ProviderExtra(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    provider_id = db.Column(db.Integer, db.ForeignKey('provider.id'), nullable=False)
    provider = db.relationship(Provider)
    extra_id = db.Column(db.Integer, db.ForeignKey('extra.id'), nullable=False)
    extra = db.relationship(Extra)"""



# === to connect to an existing db or create a new one ===
db.create_all()
print("connected to arabity database")

if __name__ == '__main__':
    # fill user_type table with Admin and Normal
    type = UserType.query.filter_by(name='normal').scalar()
    if type is None:
        normal = UserType(name='normal')
        db.session.add(normal)
    else:
        print ("type normal already exist")
    type = UserType.query.filter_by(name='admin').first()
    if type is None:
        admin = UserType(name='admin')
        db.session.add(admin)
    else:
        print ("type admin already exist")
    db.session.commit()
