#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify, json
from passlib.hash import sha256_crypt
from functools import wraps
import datetime
import MySQLdb
import gc
from .dbconnect import connection
from .registration_form import *
from .checkout import *
import json

mod = Blueprint( 'site', __name__ )
messages  = open( 'ShopApp/static/messages.json' ).read()
messages  = json.loads( messages ) if messages else False

products = ""

def get_message( ms, field = None, lang = 'RO' ):
    if lang in messages and  ms in messages[lang]:
        if field:
            return messages[lang][ms].replace( '{field}', field )
        else:
            return messages[lang][ms]
    return False

def login_required(f):
    @wraps(f)
    def wrap( *args, **kwargs ):
        if 'logged_in' in session:
            return f( *args, **kwargs )
        else:
            flash( "You need to be logged first!" )
            return redirect( url_for( '.login' ) )
    return wrap


@mod.route( '/' )
def homepage():
    return render_template( 'homepage.html' )

@mod.route( '/final-step/' )
def final_step():
    return render_template( 'final_step.html' )


@mod.route( '/products/' )
def products():
    return render_template( 'product_list.html' )

@mod.route( '/nextstep/', methods=['GET', 'POST'] )  # get email and check if user exists
def next_step():
    email_addr = ""
    cursor, connect = connection()
    try:
        if request.method == "POST":
            cursor = connect.cursor( MySQLdb.cursors.DictCursor )
            data = cursor.execute(""" SELECT * FROM users WHERE email = '{}' """
                                    .format( request.form["email"] ))
            data = cursor.fetchone()
            if data:
                email_addr = data['email']
                return redirect(url_for(".passwordstep", email_addr=email_addr))
            else:
                return redirect(url_for(".signup"))
    except Exception as e:
        # flash(e)
        pass
    cursor.close()
    gc.collect()
    return render_template( 'nextstep.html' )

@mod.route( '/passwordstep/<email_addr>', methods=['GET', 'POST'] )   # if user exists verify password and complete loggin 
def passwordstep(email_addr):
    error = ""
    cursor, connect = connection()
    try:
        if request.method == "POST":

            cursor = connect.cursor( MySQLdb.cursors.DictCursor )
            data = cursor.execute(""" SELECT * FROM users WHERE email = '{}' """
                                    .format( email_addr ))
            data = cursor.fetchone()
            if data:
                if sha256_crypt.verify( request.form["password"], data["password"] ):
                    session['logged_in'] = True
                    session['username'] = data["username"]
                    return redirect(url_for( ".checkout" ))
                else:
                    error = "Invalid credentials, try again!"
    except Exception as e:
        # flash(e)
        pass
    cursor.close()
    gc.collect()
    return render_template( 'passwordstep.html', error = error )

@mod.route( '/checkout/', methods=['GET', 'POST'] )  # order details
@login_required
def checkout():
    form = Checkout(request.form)
    username = session['username']
    cursor, connect = connection()
    personal_data = cursor.execute(""" SELECT user_personal_data.fullName, user_personal_data.fullAddress, user_personal_data.phone, user_personal_data.city
                             FROM user_personal_data 
                             LEFT JOIN users 
                             ON users.idUsers=user_personal_data.idUsers 
                             WHERE users.username = '{}' """.format( username ))
    personal_data = cursor.fetchall()
    if personal_data:
       form.fullname.data = personal_data[0][0] 
       form.fulladdress.data = personal_data[0][1]
       form.phone.data = personal_data[0][2]
       form.city.data = personal_data[0][3]
    else:
        try:
            if request.method == "POST" and form.validate():
                fullname = form.fullname.data
                fulladdress = form.fulladdress.data
                phone = form.phone.data  # must be number!!!!!!!!!! form.validate()
                city = form.city.data
                cursor, connect = connection()           
                data = cursor.execute("""SELECT * FROM users WHERE username = '{}'""".format( username )) 
                data = cursor.fetchone()       
                cursor.execute(""" INSERT INTO user_personal_data ( idUsers, fullName, fullAddress, phone, city ) 
                                VALUES ('{0}', '{1}', '{2}', '{3}', '{4}') """
                                .format( data[0], fullname, fulladdress, phone, city ))              
                connect.commit()
                cursor.close()
                connect.close()
                gc.collect()
        except Exception as e:
            # flash(e)
            pass
    return render_template( 'checkout.html', username = username, form = form, personal_data = personal_data )

# @mod.route( '/validation', methods=['POST'] )
# def validation():
#     errors, values = {}, {}
#     if 'Full Name' in request.form and len( request.form['Full Name'] ) > 0:
#         values['Full Name'] = request.form['Full Name']
#     else:
#         errors['Full Name'] = get_message( 'dn', 'Full Name' )
#     if 'Full Adress' in request.form and len( request.form['Full Adress'] ) > 0:
#         values['Full Adress'] = request.form['Full Adress']
#     else:
#         errors['Full Adress'] = get_message( 'dn', 'Full Adress' )
#     if 'Phone Number' in request.form and len( request.form['Phone Number'] ) > 0:
#         values['Phone Number'] = request.form['Phone Number']
#     else:
#         errors['Phone Number'] = get_message( 'dn', 'Phone Number' )
#     if 'City' in request.form and len( request.form['City'] ) > 0:
#         values['City'] = request.form['City']
#     else:
#         errors['City'] = get_message( 'dn', 'City' )
#     if errors:
#         return json.dumps( { 'error':2, 'errors':errors } )
#     else:
#         return json.dumps( { 'error':0, 'message':'Datele sunt corecte' } )

@mod.route('/processs', methods=['POST'])
def processs():
    username = request.form['username']
    email = request.form['email']
    password = request.form['Password']
    confirm = request.form['Repeat Password']
    if username and email:
        newName = username[::-1]
        return jsonify({'username' : newName})
    return jsonify({'error' : 'Missing Data!'})
    

@mod.route( '/cart/', methods=['GET', 'POST'] )
def cart():
    username = ""
    if 'logged_in' in session:
        username = session['username']
    return render_template( 'shoping_cart.html', username = username )


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    error = ''
    cursor, connect = connection()
    try:
        if request.method == "POST":
            cursor = connect.cursor( MySQLdb.cursors.DictCursor )
            data = cursor.execute(""" SELECT * FROM users WHERE username = '{}' """
                                    .format(request.form["username"]))
            data = cursor.fetchone()
            if data:
                if sha256_crypt.verify(request.form["password"], data['password']):
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    if session['username'] == 'admin':
                        return redirect(url_for("admin_area.admin_dashboard"))
                    else:
                        return redirect(url_for(".homepage"))
                else:
                    error = "Invalid credentials, try again!"
            else:
                error = "Invalid credentials, try again!"
    except Exception as e:
        # flash(e)
        pass
    cursor.close()
    gc.collect()
    return render_template( "login.html", error = error )


@mod.route( '/signup/', methods=['POST', 'GET'] )
def signup():
    form = Registration(request.form)
    try:
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            cursor, connect = connection()           
            x = cursor.execute("""SELECT * FROM users WHERE username = '{}'""".format( username ))           
            if x != 0:
                flash("That username is allready taken, please choose another!")
                return render_template('signup.html', form = form)
            else:
                createdDate = datetime.datetime.now()
                cursor.execute(""" INSERT INTO users (username, password, email, createdDate) 
                                VALUES ('{0}', '{1}', '{2}', '{3}') """
                                .format( username, password, email, createdDate ))                
                connect.commit()
                flash("Thanks for register!")
                cursor.close()
                connect.close()
                gc.collect()
                session["logged_in"] = True
                session["username"] = username
                return redirect( url_for(".homepage") )
    except Exception as e:
        # flash(e)
        pass
    return render_template( "signup.html", form = form ) 


@mod.route('/logout/')
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for("site.homepage"))


