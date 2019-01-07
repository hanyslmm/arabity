#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from flask import session as login_session  # dictionary store values in it
import random  # to create a pseudo-random string identify each login session
import string
# import all modules needed for configuration
# IMPORT flask and sqlalchemy
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from database_setup_arabity import *
# google OAuth
from oauth2client.client import flow_from_clientsecrets  # creates flow object
from oauth2client.client import FlowExchangeError
# occured during exchange an authorization code for an access token

import httplib2
import json
from flask import make_response
import requests  # to use args.get function

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "arabity"

# initializes an app variable, using the __name__ attribute
app = Flask(__name__)

# === let program know which database engine we want to communicate===
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///arabity.db'
db = SQLAlchemy(app)

# User helper functions
def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'],
                   user_type=1)
    session.add(newUser)
    session.commit()
    user = User.query.filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = User.query.filter_by(id=user_id).one()
    return user  # user object associated with his ID number


def getUserID(email):
    try:
        user = User.query.filter_by(email=email).one()
        return user.id
    except:
        return None


# 1 login: Create anti-forgery state token
@app.route('/login')
def showLogin():
    choices = string.ascii_uppercase + string.digits
    state = ""
    for i in range(32):
        state += random.choice(choices)
    print(state)
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/callback', methods=['POST'])
def callback():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        # creates an OAuth flow object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        # specigy with post message one time flow
        oauth_flow.redirect_uri = 'postmessage'
        # initiate the exchange passing one time code as input
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        # send response as JSON object
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    # json GET request containing the URL and access token
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info,
    # abort and send internal server error to the client
    if result.get('error') is not None:  # result contains any error
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    google_id = credentials.id_token['sub']  # gplus_id
    if result['user_id'] != google_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check if user is already logged in
    stored_access_token = login_session.get('access_token')
    stored_google_id = login_session.get('google_id')
    if stored_access_token is not None and google_id == stored_google_id:
        response = make_response(
                       json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['google_id'] = google_id

    # Use google plus API to get more user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    print (data)
    # Store data that we are intersted in
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't create new owner
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    # to make interaction with user
    flash("you are now logged in as {}".format(login_session['username']))
    print ("done!")
    return output


# Revoke current user and reset their login_session.
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print (access_token)
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # use acces token and pass it into Google's url
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    print ('shaghaaaaaal')
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200' or result['status'] == '400':  # review
        username = login_session['username']
        del login_session['access_token']
        del login_session['google_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
    # response = make_response(json.dumps('Successfully disconnected.'), 200)
    # response.headers['Content-Type'] = 'application/json'
        # using flash to make interaction with user
        flash("{} logged out!".format(username))
        return redirect(url_for('providerName'))
    else:
        response = make_response(
                    json.dumps('Failed to revoke token for given user.', 401))
        response.headers['Content-Type'] = 'application/json'
        return response


# 1 list all service provider name
@app.route('/')
@app.route('/provider')
def providerName():
    provider = Provider.query.all()
    governorate = Address.query.filter_by(parent_id=0).all()
    #governorate = session.query(Address).filter_by(parent_id=0).all()
    if 'username' not in login_session:
        return render_template('publicmain.html', provider=provider,\
                                governorate=governorate)
    else:
        return render_template('main.html', provider=provider,\
                                governorate=governorate)


# FILTER provider
@app.route('/provider/<string:filterGov>', methods=['GET', 'POST'])
def providerFilter(filterGov):
    provider = Provider.query.all()
    governorate = Address.query.filter_by(parent_id=0).all()
    provider = []
    # create array of objects for all records in provider_add table
    allAdd_id = ProviderAdd.query.all()
    # FOR loop till parent_id = 0

    for addId in allAdd_id:
        childAdd = Address.query.filter_by(id=addId.address_id).one()

        # WHILE loop till parent_id = 0
        while True:
            # IF parent id = 0 check if governorate name = filterGov
            if childAdd.parent_id == 0:
                if childAdd.address == filterGov:
                #    filterAdd = session.query(ProviderAdd).\
                #                filter_by(address_id=addId.id).one()
                    filterProv = Provider.query.filter_by(id=addId.provider_id)\
                                                            .one()
                    # ADD result to provider list
                    provider.append(filterProv)
                break
            else:
            # GET the next address object add from address table using parent_id
                childAdd = Address.query.filter_by(id=childAdd.parent_id).one()


    if 'username' not in login_session:
        return render_template('publicmain.html', provider=provider,\
                                governorate=governorate)
    else:
        return render_template('main.html', provider=provider,\
                                governorate=governorate)


# 2 delete provider
@app.route('/provider/<int:provider_id>/delete', methods=['GET', 'POST'])
def providerDelete(provider_id):
    deletedProvider = Provider.query.filter_by(id=provider_id).one()
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    if deletedProvider.user_id != login_session['user_id']:
        output = "<script>{alert('You are not authorized"
        output += " to delete this Provider.');}</script>"
        return output
    if request.method == 'POST':
        db.session.delete(deletedProvider)
        db.session.commit()
        # using flash to make interaction with user
        flash("{} Provider Deleted!".format(deletedProvider.name))
        return redirect(url_for('providerName'))
    else:
        return render_template('deleteprovider.html',
                               provider_id=provider_id,
                               provider=deletedProvider)


# 3: create new provider
@app.route('/provider/new/', methods=['GET', 'POST'])
def newProvider():
    # verify that a user is logged in
    if 'username' not in login_session:
        return redirect('/login')
    governorate = Address.query.filter_by(parent_id).all()
    if request.method == 'POST':
        newprovider = Provider(name=request.form['name'], logo=request.form['logo'],
                                   user_id=login_session['user_id'])
        db.session.add(newprovider)
        db.session.commit()
        newmobile = Mobile(mob=request.form['mobile'], provider_id=newprovider.id)
        newtelephone = Telephone(tel=request.form['telephone'],\
                                    provider_id=newprovider.id)
        db.session.add(newmobile)
        db.session.add(newtelephone)
        db.session.commit()
        gov = session.query(Address).filter_by(address=request.form['gov']).one()
        newadd = ProviderAdd(provider_id=newprovider.id, address_id=gov.id)
        db.session.add(newadd)
        db.session.commit()
        return redirect(url_for('providerName'))
    else:
        return render_template('newprovider.html', governorate=governorate)


# 4: list service items in provider using its id
@app.route('/provider/<int:provider_id>/service')
@app.route('/provider/<int:provider_id>/')
def providerService(provider_id):
    provider = Provider.query.filter_by(id=provider_id).one()
    mobile = Mobile.query.filter_by(provider_id=provider.id)
    telephone = Telephone.query.filter_by(provider_id=provider.id)
    story = Story.query.filter_by(provider_id=provider.id)
    creator = getUserInfo(provider.user_id)
    # GET provider add from provider_add table
    provadd = provider_add.query.filter_by(provider_id=provider.id)

    # GET end of tree address object add from address table
    add = Address.query.filter_by(id=provadd.address_id).one()
    addDic = {}
    # WHILE loop till parent_id = 0
    while True:
        # GET add type from add_type table
        addtype = AddType.query.filter_by(id=add.type_id).one()
        # SAVE address in dictionary
        addDic[addtype.name]=add.address
        if add.parent_id == 0:
            break
        # GET the next address object add from address table using parent_id
        add = Address.query.filter_by(id=add.parent_id).one()


    # ANOTHER method addDict.__setitem__(addtype, add)

    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicservice.html', provider=provider,
                                mobile=mobile,telephone=telephone,
                                story=story, creator=creator, addDic=addDic)
    else:
        return render_template('service.html', provider=provider,
                                mobile=mobile,telephone=telephone,
                                story=story, creator=creator, addDic=addDic)


# 5: Create route for newServiceItem Function
@app.route('/provider/<int:provider_id>/newStory/', methods=['GET', 'POST'])
def newStory(provider_id):
    # verify that a user is logged in
    provider = session.query(Provider).filter_by(id=provider_id).one()
    # creator = getUserInfo(provider.user_id)
    if 'username' not in login_session:
        return redirect('/login')
    user_id = login_session['user_id']
    if request.method == 'POST':
        newStory = Story(provider_id=provider_id, user_id=user_id)
        if request.form['post']:
            newStory.post = request.form['post']
        session.add(newStory)
        session.commit()
        flash("service story Created!")
        return redirect(url_for('providerService',
                        provider_id=provider_id, provider=provider))
    else:
        return render_template('newStory.html', provider_id=provider_id,
                               provider=provider)


# 5: Create route for newServiceItem Function
@app.route('/provider/<int:provider_id>/new/', methods=['GET', 'POST'])
def newService(provider_id):
    # verify that a user is logged in
    provider = session.query(Provider).filter_by(id=provider_id).one()
    creator = getUserInfo(provider.user_id)
    governorate = session.query(Address).filter_by(parent_id=0).all()
    if 'username' not in login_session:
        return redirect('/login')
    if creator.id != login_session['user_id']:
        return
        "<script>{alert('You are not authorized to edit this');}</script>"
    if request.method == 'POST':
        newMob = Mobile(provider_id=provider_id)
        newTel = Telephone(provider_id=provider_id)
        if request.form['mobile']:
            newMob.mob = request.form['mobile']
        if request.form['telephone']:
            newTel.tel = request.form['telephone']
        session.add(newMob)
        session.add(newTel)
        session.commit()
        flash("service items Created!")
        return redirect(url_for('providerService',
                        provider_id=provider_id, provider=provider))
    else:
        return render_template('newserviceitem.html', provider_id=provider_id,
                               provider=provider)


# 6: Create route for editServiceItem function
@app.route('/provider/<int:provider_id>/<int:service_id>/<int:idItem>/edit',
           methods=['GET', 'POST'])
def editService(provider_id, service_id, idItem):
    # verify that a user is logged in
    provider = session.query(Provider).filter_by(id=provider_id).one()
    creator = getUserInfo(provider.user_id)
    governorate = session.query(Address).filter_by(parent_id=0).all()
    if 'username' not in login_session:
        return redirect('/login')
    if creator.id != login_session['user_id']:
        return
        "<script>{alert('You are not authorized to edit this');}</script>"
    if service_id == 1:
        editedItem = session.query(Mobile).filter_by(id=idItem).one()
    if service_id == 2:
        editedItem = session.query(Telephone).filter_by(id=idItem).one()
    if service_id == 3:
        editedItem = session.query(ProviderAdd).filter_by(provider_id=provider.id).one()
    if request.method == 'POST':
        if service_id == 1:
            editedItem = session.query(Mobile).filter_by(id=idItem).one()
            editedItem.mob = request.form['number']
            # to make interaction with user
            flash("{} number Added!".format(editedItem.mob))
            return redirect(url_for('providerService', provider_id=provider_id))
        #if service_id == 2:
            #editedItem = session.query(Telephone).filter_by(provider_id=provider_id)
                #return redirect(url_for('providerService', provider_id=provider_id))
        if service_id == 2:
            editedItem = session.query(Telephone).filter_by(id=idItem).one()
            editedItem.tel = request.form['number']
            # to make interaction with user
            flash("{} number Added!".format(editedItem.tel))
            return redirect(url_for('providerService', provider_id=provider_id))
        if service_id == 3:
            addItem = session.query(Address).filter_by\
                        (address=request.form['governorate']).one()
            editedItem = session.query(ProviderAdd).filter_by\
                        (provider_id=provider.id).one()
            editedItem.address_id = addItem.id
            # to make interaction with user
            flash("{} address updated!".format(addItem.address))
            return redirect(url_for('providerService', provider_id=provider_id))
        session.add(editedItem)
        session.commit()


    else:
        return render_template(
            'editserviceitem.html', provider_id=provider_id,
             service_id=service_id, governorate=governorate, item=editedItem)


# 7: Create a route for deleteServiceItem function
@app.route('/provider/<int:provider_id>/<int:service_id>/<int:idItem>/delete/',
           methods=['GET', 'POST'])
def deleteService(provider_id, service_id, idItem):
    # verify that a user is logged in
    provider = session.query(Provider).filter_by(id=provider_id).one()
    creator = getUserInfo(provider.user_id)
    if 'username' not in login_session:
        return redirect('/login')
    if creator.id != login_session['user_id']:
        return
        "<script>{alert('You are not authorized to delete this');}</script>"
    if service_id == 1:
        deletedItem = session.query(Mobile).filter_by(id=idItem).one()
    if service_id == 2:
        deletedItem = session.query(Telephone).filter_by(id=idItem).one()
    if request.method == 'POST':
        if service_id == 1:
            deletedItem = session.query(Mobile).filter_by(id=idItem).one()
            session.delete(deletedItem)
            session.commit()
            # to make interaction with user
            flash("{} provider number Deleted!".format(deletedItem.mob))
            return redirect(url_for('providerService', provider_id=provider_id))
        if service_id == 2:
            deletedItem = session.query(Telephone).filter_by(id=idItem).one()
            session.delete(deletedItem)
            session.commit()
            # to make interaction with user
            flash("{} provider number Deleted!".format(deletedItem.tel))
            return redirect(url_for('providerService', provider_id=provider_id))
    else:
        return render_template('deleteservice.html',
                                   provider_id=provider_id,
                                   service_id=service_id, item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
