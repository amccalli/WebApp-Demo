from flask import Blueprint, render_template

from .extensions import db
from .models import Stock


main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index_new.html')
