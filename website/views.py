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
    return render_template("home.html", page="home")