#packages
from flask import Blueprint, render_template

#plots 
import plotly.express as px

#data 
import pandas as pd
import numpy as np

#utils
from .utils import get_unioned_data_from

views = Blueprint("views", __name__)

@views.route('/')
async def home():
    return render_template("tab-stargate.html", page="home")

@views.route('/squid')
async def squid():
    return render_template("tab-squid.html", page="squid")

@views.route('/satellite')
async def satellite():
    return render_template("tab-satellite.html", page="satellite")

@views.route('/comparison')
async def comparison():
    return render_template("tab-key-differences.html", page="differences")

@views.route('/overview')
async def overview():
    return render_template("tab-overview.html", page="overview")