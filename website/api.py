#packages
from flask import Blueprint, render_template

#plots 
import plotly.express as px

#data 
import pandas as pd
import numpy as np

#utils
from .utils import get_unioned_data_from

api = Blueprint("api", __name__)

@api.route('/median')
async def median():
    #@title Get Latency (Seconds)
    urls = [
        'https://node-api.flipsidecrypto.com/api/v2/queries/3d6d6474-3f45-4f68-8705-dcce7423244d/data/latest',
        'https://node-api.flipsidecrypto.com/api/v2/queries/71d93269-9dbe-4d58-b94a-8b7af4b1a708/data/latest',
        'https://node-api.flipsidecrypto.com/api/v2/queries/499733fd-d51a-4043-866d-5e345d1011e8/data/latest',
        'https://node-api.flipsidecrypto.com/api/v2/queries/814664ea-eb0b-4a8b-b49d-9e2f7952d21a/data/latest',
    ]
    latencies = await get_unioned_data_from(urls)

    df6 = pd.DataFrame(latencies).sort_values("MEDIAN_LATENCY")
    avg_median_latency_df = df6.groupby('FROM_CHAIN').mean(numeric_only=True).sort_values("MEDIAN_LATENCY")
    fig = px.bar(avg_median_latency_df, y=['MEDIAN_LATENCY'],
                title="Average Median Latency by From Source Chain (s)")
    fig.update_layout(showlegend=False)
    return fig.to_html()