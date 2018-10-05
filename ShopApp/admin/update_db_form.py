#!/usr/bin/env python3
from wtforms import Form, BooleanField, TextField, PasswordField, validators, IntegerField, DecimalField
from .validator import *

length = Length
class RegistrationProducts( Form ):
    product_name = TextField("Product Name", [validators.length( min = 1, max = 70 )])
    procesor = TextField('Procesor Type',    [validators.length( min = 1, max = 20 )])
    brand = TextField('Brand',               [validators.length( min = 1, max = 50 )])
    os = TextField('Operation System',       [validators.length( min = 1, max = 20 )])
    display = TextField('Display Size',      [validators.length( min = 1, max = 50 )])
    description = TextField('Description',   [validators.length( min = 1, max = 250 )])
    price = DecimalField('Price',            [validators.InputRequired( message=None )])
    amount = IntegerField('Amount',          [validators.InputRequired( message=None )])