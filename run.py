#!/usr/bin/env python3

from ShopApp import app
from flask_mail import Message, Mail


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/312321'
app.config['SESSION_TYPE'] = 'filesystem'
app.config.update(  #EMAIL SETTINGS
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'alexeluca2017@gmail.com',
	MAIL_PASSWORD = ''
	)
mail = Mail(app)

app.run(debug=True)