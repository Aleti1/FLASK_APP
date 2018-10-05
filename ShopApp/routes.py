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
mod = Blueprint( 'site', __name__ )

products = ""
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
            print(data)
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
     
    try:
        if request.method == "POST" and form.validate():
            fullname = form.fullname.data
            fulladdress = form.fulladdress.data
            phone = form.phone.data
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
    return render_template( 'checkout.html', username = username, form = form )

@mod.route( '/add-cart/', methods= ['POST'] )
def add_cart():
    return json.dumps( { 'error':0, 'post':request.form['post'] } )
    

@mod.route( '/cart/' )
def cart():
    return render_template( 'shoping_cart.html' )


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
    return render_template("login.html", error = error)


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
                return redirect(url_for(".homepage"))
    except Exception as e:
        # flash(e)
        pass
    return render_template("signup.html", form = form) 


@mod.route('/logout/')
@login_required
def logout():
    session.clear()
    #session.pop('logged_in', None)
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for("site.homepage"))