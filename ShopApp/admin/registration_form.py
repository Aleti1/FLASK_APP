#!/usr/bin/env python3
from wtforms import Form, BooleanField, TextField, PasswordField, validators, IntegerField
from .validator import *

length = Length
class Registration(Form):
    username = TextField("Username",      [validators.length( min = 4, max = 20 )])
    email =     TextField('Email Adress', [validators.length( min = 4, max = 50 )])
    password =  PasswordField('Password', [validators.Required(),
                                           validators.EqualTo('confirm', message = 'Password must be equal!')])
    confirm =   PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the <a href= "/tos/">  Terms of Service</a> & The  <a href= "/pn/">  Privacy Notice  </a> (Last updated 15.02.2018)', 
                                          [validators.DataRequired()])
