#!/usr/bin/env python3
from wtforms import Form, BooleanField, TextField, PasswordField, validators, IntegerField, StringField, FormField
from .validator import *

class TelephoneForm(Form):
    number       = StringField('Number')

length = Length
class Checkout(Form):
    fullname = TextField("Full Name",      [validators.length( min = 4, max = 85 )])
    fulladdress = TextField('Full Adress', [validators.length( min = 4, max = 155 )])
    phone = StringField('Phone Number',    [validators.required()])
    city = TextField('City',               [validators.length( min = 4, max = 75 )])
    