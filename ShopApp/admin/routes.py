#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify
from passlib.hash import sha256_crypt
from functools import wraps
import datetime
import MySQLdb
import gc
from .dbconnect import connection
from .registration_form import *
from .update_db_form import *
from .delete_db_form import *
from .deals_db_form import *
mod = Blueprint( 'admin_area', __name__ )



def login_required_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['username'] == 'admin':
            return f(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for('site.login'))
    return wrap


@mod.route( '/admin_dashboard/' )
@login_required_admin
def admin_dashboard():
    return render_template( '/admin/admin_dashboard.html' )


@mod.route( '/delete_db/' )
@login_required_admin
def delete_db():
    return render_template( '/admin/delete_db.html' )


@mod.route( '/deals_db/' )
@login_required_admin
def deals_db():
    return render_template( '/admin/deals_db.html' )


@mod.route( '/update_db/', methods = ['POST', 'GET'] )
@login_required_admin
def update_dp():
    form = RegistrationProducts(request.form)
    try:
        if request.method == "POST" and form.validate():
            createdDate = datetime.datetime.now()
            product_name = form.product_name.data
            description = form.description.data
            os = form.os.data
            brand = form.brand.data
            amount = form.amount.data
            procesor = form.procesor.data
            display = form.display.data
            price = form.price.data 
            product_name = str(brand) + " " + str(description) + " " + str(display) + " " + str(procesor) + " " + str(os)
            cursor, connect = connection()
            cursor = connect.cursor( MySQLdb.cursors.DictCursor )
            i = cursor.execute( """ SELECT * FROM products WHERE name = '{0}' """.format( product_name ))
            if i != 0:
                flash( " This product name allready exists! Try Another. " )
                return(render_template( '/admin/update_db.html', form = form ))
            else:
                
                
                cursor.execute(""" INSERT INTO products ( name, description, createdDate, amount, price ) 
                                VALUES ( '{0}', '{1}', '{2}', '{3}', '{4}' ) """.format( product_name, description, createdDate, amount, price ))
                product_id = cursor.lastrowid 
                
    
                cursor.execute(""" SELECT * FROM categori_filters WHERE name = 'BRAND' """)
                brandid = cursor.fetchone()['idCategoriFilters']
                cursor.execute(""" INSERT INTO filters ( idCategoriFilters, name ) VALUES ( '{0}', '{1}' ) """.format( brandid, brand ))
                brand_filter_id = cursor.lastrowid
                
                
                cursor.execute(""" SELECT * FROM categori_filters WHERE name = 'OS' """)
                osid = cursor.fetchone()['idCategoriFilters']
                cursor.execute(""" INSERT INTO filters ( idCategoriFilters, name ) VALUES ( '{0}', '{1}' ) """.format( osid, os ))
                os_filter_id = cursor.lastrowid
                
                
                cursor.execute(""" SELECT * FROM categori_filters WHERE name = 'DISPLAY' """)
                displayid = cursor.fetchone()['idCategoriFilters']
                cursor.execute(""" INSERT INTO filters ( idCategoriFilters, name ) VALUES ( '{0}', '{1}' ) """.format( displayid, display ))
                display_filter_id = cursor.lastrowid

                cursor.execute(""" SELECT * FROM categori_filters WHERE name = 'PROCESOR' """)
                procesorid = cursor.fetchone()['idCategoriFilters']
                cursor.execute(""" INSERT INTO filters ( idCategoriFilters, name ) VALUES ( '{0}', '{1}' ) """.format( procesorid, procesor ))
                procesor_filter_id = cursor.lastrowid

                filter_list = [ (product_id, brand_filter_id), (product_id, os_filter_id), (product_id, display_filter_id), (product_id, procesor_filter_id) ]
                query = """ INSERT INTO product_filters ( idProduct, idFilters ) VALUES ( %s, %s ) """
                cursor.executemany( query, filter_list )                                                                                                  
                connect.commit()
                flash("Product " + product_name + " added to db.")
                cursor.close()
                gc.collect()
    except Exception as e:
        flash(e)
    return render_template( '/admin/update_db.html', form = form )


@mod.route('/log_out/')
@login_required_admin
def log_out():
    session.pop('username', None)
    session.pop('logged_in', None)
    flash("You logged out!")
    gc.collect()
    return redirect(url_for("site.homepage"))





