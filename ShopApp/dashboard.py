#!/usr/bin/env python3

from flask import Blueprint, render_template, request, flash, session, redirect, url_for, jsonify
import MySQLdb
import gc
from .dbconnect import connection
from .routes import *
import itertools
    



@mod.route( '/dashboard/', methods = ['GET', 'POST'] )
def dashboard():
    
    try:
        arg = []
        arglist = [] 
        where = ""
        filtre = "" 
        newargs = ""
        results = ""
        products = ""
        argstring = ""
        final_item = ""
        categ_filtre = ""
    
        cursor, connect = connection()
        categ_filtre = cursor.execute( """ SELECT name, idCategoriFilters FROM categori_filters """ )
        categ_filtre = cursor.fetchall()

        """             FOR EACH NAME IN "CATEG_FILTRE" UPDATES ARGS FOR "REQUEST.ARGS" """
        for i in range( len( categ_filtre ) ):
            arg.append( categ_filtre[i][0] )  

        """             FOR EACH VALUE IN "GET" DICTIONARY IT FORMATS MySQL.QUERY TO FILTER THE PRODUCTS """
        get = dict( request.args )
        for i in get:
            if i in arg:
                arglist.append( get[i][0] )
                x = ", "
                argstring = x.join( repr( i ) for i in arglist )
        for i in argstring:
            newargs += i
        
        if request.args:
            results = ", GROUP_CONCAT( product_filters.idFilters SEPARATOR ',' ) AS results "
            where = " WHERE filters.name IN ({0}) ".format( newargs )
        
        products = cursor.execute(""" SELECT products.idProduct, products.name, products.description, products.amount, products.price
                                    {0}
                                    FROM products
                                    LEFT JOIN product_filters ON product_filters.idProduct=products.idProduct
                                    LEFT JOIN filters ON filters.idFilters=product_filters.idFilters
                                    {1}
                                    GROUP BY products.idProduct """.format( results, where ))
        products = cursor.fetchall()
        
        for i in range(len(products)):
            item = products[i]
            

                
        filtre = cursor.execute( """ SELECT DISTINCT filters.name, filters.idCategoriFilters FROM filters ORDER BY filters.name DESC """ )
        filtre = cursor.fetchall()  

        connect.close()
        cursor.close()
    except Exception as e:
        flash(e)
    return render_template( 'dashboard.html', products = products, categ_filtre = categ_filtre, filtre = filtre, final_item=item )

