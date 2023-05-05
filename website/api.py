#packages
from flask import Blueprint, render_template

#plots 
import plotly.express as px
import plotly.graph_objects as go

#data 
import pandas as pd
import numpy as np

#utils
from .utils import get_unioned_data_from

api = Blueprint("api", __name__)

@api.route('/stargate_volume')
async def stargate_volume():
    queryIds = [
        '5ca98cb1-ed7a-43eb-9b37-8f61dd8ee3fd',
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    source_chain_df = df.groupby("SOURCE_CHAIN").sum(numeric_only=True).sort_values("TOKEN_AMOUNT_USD", ascending=False)

    # get data by total volume for source chain
    fig = px.bar(
                source_chain_df, 
                y='TOKEN_AMOUNT_USD',
                title="USD Value Bridged by Source Chain",
                labels={
                    "SOURCE_CHAIN": "Source Chain",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Source Chain")

    # get data by month's median
    df2 = pd.DataFrame(data)

    # sum all data first
    df2 = df2.groupby('DATE').sum(numeric_only=True).reset_index()
    df2['YearMonth'] = pd.to_datetime(df2['DATE'],format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
    monthly_median = df2.groupby('YearMonth').median(numeric_only=True)

    fig2 = px.bar(
                monthly_median, 
                y='TOKEN_AMOUNT_USD',
                title="Median USD Value Bridged Per Month",
                labels={
                    "YearMonth": "Month",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig2.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Month")

    fig2_user = px.bar(
                monthly_median, 
                y='USER_COUNT',
                title="Median Users Per Day By Month",
                labels={
                    "YearMonth": "Month",
                    "USER_COUNT": "User Count"
                }
            )
    fig2_user.update_layout(showlegend=False, yaxis_title="User Count", xaxis_title="Month")

    #get data by date and source chain
    by_date_df = df.groupby(['DATE', 'SOURCE_CHAIN']).sum(numeric_only=True).reset_index().set_index('DATE')
    fig3 = px.bar(
        by_date_df,
        y="TOKEN_AMOUNT_USD",
        color="SOURCE_CHAIN",
        title="USD Value Bridged Per Day by Chain",
        labels={
            "SOURCE_CHAIN": "Source Chain",
            "TOKEN_AMOUNT_USD": "Amount USD"
        }
    )
    fig3.update_layout(yaxis_title="Amount USD", xaxis_title="Date")

    fig3_user = px.bar(
        by_date_df,
        y="USER_COUNT",
        color="SOURCE_CHAIN",
        title="Users Per Day By Chain",
        labels={
            "SOURCE_CHAIN": "Source Chain",
            "USER_COUNT": "User Count"
        }
    )
    fig3_user.update_layout(yaxis_title="User Count", xaxis_title="Date")

    return {
        "total_volume_by_source": fig.to_html(),
        "monthly_median_usd": fig2.to_html(),
        "by_date_usd": fig3.to_html(),

        "monthly_median_user": fig2_user.to_html(),
        "by_date_user": fig3_user.to_html(),
    }

@api.route('/stargate_token_stats')
async def stargate_token_stats():
    queryIds = [
        'cb8807b2-d514-46e7-ba97-8afe7e488355', #bsc
        'b508a928-eb49-4307-abe3-1c856dc21cba', #arb
        '45cd1428-f6ef-4159-a2b3-e100f3db7beb', #polygon
        'ab212eb2-3aea-4929-857e-00d2db4a36c8', #eth
        'f2700ac0-e91d-40ca-b55f-56e1ae5a2596', #op
        '76bec6cc-9fda-4f3f-ab68-d4ed05388ad1', #avax
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    #total amounts
    total_amount_usd_df = df.groupby(['SYMBOL']).sum(numeric_only=True).reset_index().set_index('SYMBOL')
    filter = total_amount_usd_df["TOKEN_AMOUNT_USD"] > 1e6
    total_amount_usd_df = total_amount_usd_df.where(filter).dropna().sort_values("TOKEN_AMOUNT_USD", ascending=False)
    
    # get data by total volume for source chain
    fig = px.bar(
                total_amount_usd_df, 
                y='TOKEN_AMOUNT_USD',
                title="USD Value Bridged by Token",
                labels={
                    "SOURCE_CHAIN": "Source Chain",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Token")

    #total amounts by chain
    total_amount_usd_chain_df = df.groupby(['SOURCE_CHAIN']).sum(numeric_only=True)
    filter = total_amount_usd_chain_df["TOKEN_AMOUNT_USD"] > 1e6
    total_amount_usd_chain_df = total_amount_usd_chain_df.where(filter).dropna().sort_values("TOKEN_AMOUNT_USD", ascending=False)
    
    total_amount_usd_chain_df["AVERAGE_AMOUNT_USD_PER_TX"] = total_amount_usd_chain_df["TOKEN_AMOUNT_USD"] / total_amount_usd_chain_df["TX_COUNT"]

    total_amount_usd_chain_df["AVERAGE_AMOUNT_USD_PER_USER"] = total_amount_usd_chain_df["TOKEN_AMOUNT_USD"] / total_amount_usd_chain_df["USER_COUNT"]


    # get data by total volume for source chain
    fig2 = px.bar(
                total_amount_usd_chain_df, 
                y='TOKEN_AMOUNT_USD',
                title="USD Value Bridged by Chain",
                labels={
                    "SOURCE_CHAIN": "Source Chain",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig2.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Source Chain")

    fig2_avg_tx = px.bar(
                total_amount_usd_chain_df, 
                y='AVERAGE_AMOUNT_USD_PER_TX',
                title="Average Amount USD Bridged Per Tx",
                labels={
                    "SOURCE_CHAIN": "Source Chain",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig2_avg_tx.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Source Chain")

    fig2_avg_user = px.bar(
                total_amount_usd_chain_df, 
                y='AVERAGE_AMOUNT_USD_PER_USER',
                title="Average Amount USD Bridged Per Tx",
                labels={
                    "SOURCE_CHAIN": "Source Chain",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig2_avg_user.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Source Chain")

    return {
        "total_amount_usd": fig.to_html(),
        "total_amount_usd_chain": fig2.to_html(),
        "avg_amount_usd_chain_tx": fig2_avg_tx.to_html(),
        "avg_amount_usd_chain_user": fig2_avg_user.to_html(),
    }

@api.route('/stargate_bucketed_user_stats')
async def stargate_bucketed_user_stats():
    queryIds = [
        '0c0803f3-7bfc-4a4e-802a-73569687ea3d', #
    ]
    data = await get_unioned_data_from(queryIds)
    df = pd.DataFrame(data)

    df.set_index("BUCKET", inplace=True)

    #get averages
    df["AVERAGE_AMOUNT_USD_PER_TX"] = df["GRAND_TOTAL_AMOUNT_USD_BRIDGED"] / df["TX_COUNT"]
    df["AVERAGE_AMOUNT_USD_PER_USER"] = df["GRAND_TOTAL_AMOUNT_USD_BRIDGED"] / df["ADDRESS_COUNT"]

    # get data by total volume for source chain
    fig = px.bar(
                df, 
                y='GRAND_TOTAL_AMOUNT_USD_BRIDGED',
                title="USD Bridged by Bucket",
                labels={
                    "BUCKET": "Bucket",
                    "GRAND_TOTAL_AMOUNT_USD_BRIDGED": "Amount USD"
                }
            )
    fig.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Bucket")


    # get data by total volume for source chain
    fig2_avg_tx = px.bar(
                df, 
                y='AVERAGE_AMOUNT_USD_PER_TX',
                title="Average USD Bridged Per Tx by Bucket",
                labels={
                    "BUCKET": "Bucket",
                    "AVERAGE_AMOUNT_USD_PER_TX": "Amount USD"
                }
            )
    fig2_avg_tx.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Bucket")

    fig2_avg_user = px.bar(
                df, 
                y='AVERAGE_AMOUNT_USD_PER_USER',
                title="Average USD Bridged Per User by Bucket",
                labels={
                    "BUCKET": "Bucket",
                    "AVERAGE_AMOUNT_USD_PER_User": "Amount USD"
                }
            )
    fig2_avg_user.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Bucket")

    fig2_median_tx_count = px.bar(
                df, 
                y='MEDIAN_TX_COUNT',
                title="Median Tx Count",
                labels={
                    "BUCKET": "Bucket",
                    "MEDIAN_TX_COUNT": "Tx Count"
                }
            )
    fig2_median_tx_count.update_layout(showlegend=False, yaxis_title="Tx Count", xaxis_title="Bucket")

    fig2_median_days_active = px.bar(
                df, 
                y='MEDIAN_DAYS_ACTIVE',
                title="Median Days Active",
                labels={
                    "BUCKET": "Bucket",
                    "MEDIAN_DAYS_ACTIVE": "Days Active"
                }
            )
    fig2_median_days_active.update_layout(showlegend=False, yaxis_title="Days Active", xaxis_title="Bucket")

    return {
        "total_amount_usd": fig.to_html(),
        "median_tx_count": fig2_median_tx_count.to_html(),
        "median_days_active": fig2_median_days_active.to_html(),
        "avg_amount_usd_chain_tx": fig2_avg_tx.to_html(),
        "avg_amount_usd_chain_user": fig2_avg_user.to_html(),
    }

@api.route('/stargate_liquidity_changes')
async def stargate_liquidity_changes():
    queryIds = [
        '611598fb-70a5-4bf6-aabf-a4b0077a2647', #bsc
        '4410249a-e364-48ca-8df9-87bd7e593e13', #arb
        'df09ab03-ed21-4a19-a875-a9fd6dc32776', #polygon
        'a599cd0b-497c-41c1-9f97-a4452dc08d27', #eth
        '44b9eee7-30e2-4b37-892c-0dd98b85bada', #op
        'e3e5bc21-2bfb-4267-8914-38f64510dbef', #avax
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    #total amounts
    total_df = df.groupby(['DATE', 'SOURCE_CHAIN']).sum(numeric_only=True).reset_index().set_index('DATE')
    
    # get data by total volume for source chain
    fig = px.bar(
                total_df, 
                y='NET_DEPOSIT',
                color='SOURCE_CHAIN',
                title="Net USD Value Deposited by Date",
                labels={
                    "DATE": "Date",
                    "NET_DEPOSIT": "Amount USD"
                }
            )
    fig.update_layout(yaxis_title="Amount USD", xaxis_title="Date")
    
    # get data by total volume for source chain
    fig2 = px.bar(
                total_df, 
                y='TX_COUNT',
                color='SOURCE_CHAIN',
                title="Deposit Tx Count by Date",
                labels={
                    "DATE": "Date",
                    "TX_COUNT": "Amount USD"
                }
            )
    fig2.update_layout(yaxis_title="Tx Count", xaxis_title="Date")

    return {
        "total_amount_usd": fig.to_html(),
        "total_tx_count": fig2.to_html(),
    }


@api.route('/stargate_bridge_initiator')
async def stargate_bridge_initiator():
    queryIds = [
        'd7376011-882a-4905-811d-007aa232ceb1', #bsc
        '1e8544f4-50de-4b89-ae98-d3e49064179c', #arb
        'ec3263a5-5c9a-4fa8-9c14-74611e7e1f98', #polygon
        'a49377ed-c877-4850-b77c-1daa6e626334', #eth
        'a54efdbf-d37a-4199-a32c-19e411bca99f', #op
        'f9994302-3437-4823-bc0d-418706aca64c', #avax
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    #total amounts
    total_df = df.groupby(['DATE', 'PROJECT']).sum(numeric_only=True).reset_index().set_index('DATE')
    
    # get data by total volume for source chain
    fig = px.bar(
                total_df, 
                y='TOKEN_AMOUNT_USD',
                color='PROJECT',
                title="Amount USD Initiated Per Project by Date",
                labels={
                    "DATE": "Date",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig.update_layout(yaxis_title="Amount USD", xaxis_title="Date")
    
    # get data by total volume for source chain
    fig2 = px.bar(
                total_df, 
                y='TX_COUNT',
                color='PROJECT',
                title="Tx Count Per Project by Date",
                labels={
                    "DATE": "Date",
                    "TX_COUNT": "Tx Count"
                }
            )
    fig2.update_layout(yaxis_title="Tx Count", xaxis_title="Date")
    
    # get data by total volume for source chain
    fig3 = px.bar(
                total_df, 
                y='USER_COUNT',
                color='PROJECT',
                title="User Count Per Project by Date",
                labels={
                    "DATE": "Date",
                    "USER_COUNT": "User Count"
                }
            )
    fig3.update_layout(yaxis_title="User Count", xaxis_title="Date")

    return {
        "total_amount_usd": fig.to_html(),
        "total_tx_count": fig2.to_html(),
        "total_user_count": fig3.to_html(),
    }


@api.route('/stargate_top_user_bridge_stats')
async def stargate_top_user_bridge_stats():
    queryIds = [
        '1965d97f-5d9f-447d-b8ee-cf02a87b693a',
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    #total amounts
    total_df = df.groupby(['SOURCE_CHAIN', 'SYMBOL']).sum(numeric_only=True).reset_index().set_index('SOURCE_CHAIN')
    
    # get data by total volume for source chain
    fig = px.bar(
                total_df, 
                y='TOKEN_AMOUNT_USD',
                color='SYMBOL',
                title="Top Users Amount USD Bridged by Source Chain",
                labels={
                    "SOURCE_CHAIN": "Source Chain",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig.update_layout(yaxis_title="Amount USD", xaxis_title="Source Chain")
    
    # get data by total volume for source chain
    fig2 = px.bar(
                total_df, 
                y='TX_COUNT',
                color='SYMBOL',
                title="Top Users Tx Count by Source Chain",
                labels={
                    "DATE": "Date",
                    "TX_COUNT": "Tx Count"
                }
            )
    fig2.update_layout(yaxis_title="Tx Count", xaxis_title="Source Chain")

    fig3 = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.ORIGIN_FROM_ADDRESS, df.SYMBOL, df.SOURCE_CHAIN, df.DESTINATION_CHAIN, df.TOKEN_AMOUNT_USD, df.TX_COUNT],
                fill_color='lavender',
                align='left'))
    ])

    return {
        "total_amount_usd": fig.to_html(),
        "total_tx_count": fig2.to_html(),
        "table": fig3.to_html(),
    }

@api.route('/stargate_top_user_bridge_stats_by_date')
async def stargate_top_user_bridge_stats_by_date():
    queryIds = [
        '8eb03dbb-5abc-4861-b164-79a0df17be7c',
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    #total amounts
    total_df = df.groupby(['SOURCE_CHAIN', 'DATE']).sum(numeric_only=True).reset_index().set_index('DATE')
    
    # get data by total volume for source chain
    fig = px.bar(
                total_df, 
                y='TOKEN_AMOUNT_USD',
                color='SOURCE_CHAIN',
                title="Top Users Amount USD Bridged Per Source Chain By Date",
                labels={
                    "DATE": "Date",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig.update_layout(yaxis_title="Amount USD", xaxis_title="Date")
    
    # get data by total volume for source chain
    fig2 = px.bar(
                total_df, 
                y='TX_COUNT',
                color='SOURCE_CHAIN',
                title="Top Users Tx Count Per Source Chain By Date",
                labels={
                    "DATE": "Date",
                    "TX_COUNT": "Tx Count"
                }
            )
    fig2.update_layout(yaxis_title="Tx Count", xaxis_title="Date")

    return {
        "total_amount_usd": fig.to_html(),
        "total_tx_count": fig2.to_html(),
    }

