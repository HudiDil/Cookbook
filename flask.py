from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHMEY_DATABASE_URL'] =\
'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
