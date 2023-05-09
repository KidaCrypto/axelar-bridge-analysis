#packages
from flask import Blueprint, render_template

#plots 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#data 
import pandas as pd
import numpy as np

#utils
from .utils import get_unioned_data_from

api = Blueprint("api", __name__)

# stargate

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

    fig2 = px.line(
                monthly_median, 
                y='TOKEN_AMOUNT_USD',
                title="Median USD Value Bridged Per Month",
                labels={
                    "YearMonth": "Month",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig2.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Month")

    fig2_user = px.line(
                monthly_median, 
                y='USER_COUNT',
                title="Median Bridgers Per Day By Month",
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
    fig3.update_layout(yaxis_title="Amount USD", xaxis_title="Date", hovermode='x unified')

    fig3_user = px.bar(
        by_date_df,
        y="USER_COUNT",
        color="SOURCE_CHAIN",
        title="Bridgers Per Day By Chain",
        labels={
            "SOURCE_CHAIN": "Source Chain",
            "USER_COUNT": "User Count"
        }
    )
    fig3_user.update_layout(yaxis_title="User Count", xaxis_title="Date", hovermode='x unified')

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
                title="Average Amount USD Bridged Per User",
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
    total_tx_df = total_df.groupby('DATE').sum(numeric_only=True)
    fig2 = px.bar(
                total_tx_df, 
                y=['DEPOSIT_TX_COUNT', 'WITHDRAW_TX_COUNT'],
                title="Deposit and Withdraw Tx Count by Date",
                labels={
                    "DATE": "Date",
                    "TX_COUNT": "Amount USD"
                }
            )
    fig2.update_layout(yaxis_title="Tx Count", xaxis_title="Date")
    fig3 = px.line(
                total_tx_df, 
                y=['TOTAL_DEPOSIT', 'TOTAL_WITHDRAW'],
                title="Deposit and Withdraw Amount USD by Date",
                labels={
                    "DATE": "Date",
                    "TOTAL_DEPOSIT": "Deposit Amount USD",
                    "TOTAL_WITHDRAW": "Withdraw Amount USD",
                }
            )
    fig3.update_layout(yaxis_title="Amount USD", xaxis_title="Date", hovermode="x unified")

    return {
        "total_amount_usd": fig.to_html(),
        "total_tx_count": fig2.to_html(),
        "total_deposit_withdraw": fig3.to_html(),
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
                title="Top Bridgers Amount USD Bridged by Source Chain",
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
                title="Top Bridgers Tx Count by Source Chain",
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


@api.route('/stargate_top_user_profits')
async def stargate_top_user_profits():
    queryIds = [
        'd3250383-82f1-415f-9771-4051da89fdb1',
        'f27a788d-811b-4646-88a5-1072d28023a4',
        '0cf839d7-5d98-4477-b551-7e0fcea8095b',
        'ea88760e-67e5-4660-8c34-6b0619772295',
        'f1b8a2ef-a140-4e78-8d72-4e17d2b9bb3e',
        '29c0b7a4-235d-40d8-af2e-2b0f972554e4',
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    #total amounts
    total_df = df.groupby('ADDRESS').sum(numeric_only=True).sort_values('AMOUNT_USD_RECEIVED', ascending=False).reset_index()
    total_df['address_trunc'] = total_df['ADDRESS'].str.slice(0, 8) + ".."
    
    # get data by total volume for source chain
    fig = px.bar(
                total_df, 
                y=['AMOUNT_USD_RECEIVED', 'AMOUNT_USD_SENT'],
                x="address_trunc",
                title="Top Bridgers Sent Vs Received",
                labels={
                    "address_trunc": "Address",
                    "AMOUNT_USD_RECEIVED": "Amount USD Received",
                    "AMOUNT_USD_SENT": "Amount USD Sent"
                },
                barmode='group'
            )
    
    fig.update_layout(yaxis_title="Amount USD", xaxis_title="Address", hovermode="x")

    #diff
    total_df['slippage'] = (total_df['PROFIT'] / total_df['AMOUNT_USD_SENT']) * 100
    total_df['in_profit'] = total_df['PROFIT'].apply(lambda x: "Profit" if x >= 0 else "Loss" )
    total_df = total_df.sort_values('slippage', ascending=False)

    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Scatter(x=total_df['address_trunc'], y=total_df['slippage'], name="Slippage (%)", mode="lines"),
        secondary_y=True
    )

    fig2.add_trace(
        go.Bar(x=total_df['address_trunc'], y=total_df['PROFIT'], name="Profit (USD)"),
        secondary_y=False
    )

    fig2.update_xaxes(title_text="Address")
    # Set y-axes titles
    fig2.update_yaxes(title_text="Profit (USD)", secondary_y=False)
    fig2.update_yaxes(title_text="Slippage (%)", secondary_y=True)
    fig2.update_layout(hovermode="x")

    #get if address is in profit
    count_df = total_df.groupby('in_profit').count().reset_index()
    fig4 = px.pie(
                count_df, 
                names="in_profit",
                values="slippage", # any column cause the numbers are all the same
                title="Number of Top Bridgers In Profit",
                labels={
                    'slippage': "Count",
                    'in_profit': 'Type'
                }
            )

    fig5 = go.Figure(
            data=[go.Table(
                    header=dict(
                                values=list(["Address", "Amount USD Received", "Amount USD Sent", "Profit", "Slippage"]),
                                fill_color='paleturquoise',
                                align='left'),
                                cells=dict(values=[total_df.ADDRESS, total_df.AMOUNT_USD_RECEIVED, total_df.AMOUNT_USD_SENT, total_df.PROFIT, total_df.slippage],
                                fill_color='lavender',
                                align='left'
                            )
                )
            ]
        )

    return {
        "sent_vs_received": fig.to_html(),
        "slippage": fig2.to_html(),
        # "profit": fig3.to_html(),
        "profit_pie": fig4.to_html(),
        "totals_table": fig5.to_html(),
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
                title="Top Bridgers Amount USD Bridged Per Source Chain By Date",
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
                title="Top Bridgers Tx Count Per Source Chain By Date",
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


@api.route('/stargate_user_trading_activities')
async def stargate_user_trading_activities():
    queryIds = [
        'bafd3be4-c1bd-485d-bf60-dbbe9ac41c99',
    ]
    data = await get_unioned_data_from(queryIds)

    df = pd.DataFrame(data)

    #total amounts
    chain_total_df = df.groupby(['BLOCKCHAIN']).sum(numeric_only=True).sort_values('TOTAL_AMOUNT_USD', ascending=False)
    chain_date_total_df = df.groupby(['BLOCKCHAIN', 'DATE']).sum(numeric_only=True).reset_index().set_index('DATE')
    chain_average_df = chain_date_total_df.groupby(['BLOCKCHAIN']).mean(numeric_only=True).sort_values('AVERAGE_AMOUNT_USD', ascending=False)
    platform_total_df = df.groupby(['PLATFORM']).sum(numeric_only=True).sort_values('TOTAL_AMOUNT_USD', ascending=False)
    
    # get data by total volume for source chain
    fig = px.bar(
                chain_total_df, 
                y='TOTAL_AMOUNT_USD',
                title="Total Swap Amount USD by Blockchain",
                labels={
                    "BLOCKCHAIN": "Chain",
                    "TOTAL_AMOUNT_USD": "Total Amount USD"
                }
            )
    fig.update_layout(yaxis_title="Amount USD", xaxis_title="Chain")
    
    # get data by total swap tx for source chain
    fig2 = px.bar(
                chain_total_df, 
                y='TX_COUNT',
                title="Total Swap Tx by Blockchain",
                labels={
                    "BLOCKCHAIN": "Chain",
                    "TX_COUNT": "Tx Count"
                }
            )
    fig2.update_layout(yaxis_title="Tx Count", xaxis_title="Chain")
    
    # get data by average volume for source chain
    fig3 = px.bar(
                chain_average_df, 
                y='AVERAGE_AMOUNT_USD',
                title="Average Swap Amount USD Per Blockchain",
                labels={
                    "BLOCKCHAIN": "Chain",
                    "AVERAGE_AMOUNT_USD": "Average Amount USD"
                }
            )
    fig3.update_layout(yaxis_title="Amount USD", xaxis_title="Chain")
    
    # get data by total volume for source chain
    fig4 = px.bar(
                chain_date_total_df, 
                y='TOTAL_AMOUNT_USD',
                color="BLOCKCHAIN",
                title="Total Swap Amount USD Per Day Per Blockchain",
                labels={
                    "DATE": "Date",
                    "TOTAL_AMOUNT_USD": "Amount USD"
                }
            )
    fig4.update_layout(yaxis_title="Amount USD", xaxis_title="Date")
    
    # get data by total volume for source chain
    fig5 = px.bar(
                platform_total_df, 
                y='TOTAL_AMOUNT_USD',
                title="Total Swap Amount USD Per Platform",
                labels={
                    "PLATFORM": "Platform",
                    "TOTAL_AMOUNT_USD": "Total Amount USD"
                }
            )
    fig5.update_layout(yaxis_title="Amount USD", xaxis_title="Platform")

    return {
        "total_amount_usd": fig.to_html(),
        "total_tx_count": fig2.to_html(),
        "average_amount_usd": fig3.to_html(),
        "total_amount_usd_date": fig4.to_html(),
        "total_amount_usd_platform": fig5.to_html(),
    }

# squid
@api.route('/squid_volume')
async def squid_volume():
    queryIds = [
        '8b11eb1e-94cc-46a2-8960-e070c5b94347',
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
    fig.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Source Chain", hovermode="x")

    # get data by month's median
    df2 = pd.DataFrame(data)

    # sum all data first
    df2 = df2.groupby('DATE').sum(numeric_only=True).reset_index()
    df2['YearMonth'] = pd.to_datetime(df2['DATE'],format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
    monthly_median = df2.groupby('YearMonth').median(numeric_only=True)

    fig2 = px.line(
                monthly_median, 
                y='TOKEN_AMOUNT_USD',
                title="Median USD Value Bridged Per Month",
                labels={
                    "YearMonth": "Month",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig2.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Month", hovermode="x")

    fig2_user = px.line(
                monthly_median, 
                y='USER_COUNT',
                title="Median Bridgers Per Day By Month",
                labels={
                    "YearMonth": "Month",
                    "USER_COUNT": "User Count"
                }
            )
    fig2_user.update_layout(showlegend=False, yaxis_title="User Count", xaxis_title="Month", hovermode="x")

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
    fig3.update_layout(yaxis_title="Amount USD", xaxis_title="Date", hovermode='x unified')

    fig3_user = px.bar(
        by_date_df,
        y="USER_COUNT",
        color="SOURCE_CHAIN",
        title="Bridgers Per Day By Chain",
        labels={
            "SOURCE_CHAIN": "Source Chain",
            "USER_COUNT": "User Count"
        }
    )
    fig3_user.update_layout(yaxis_title="User Count", xaxis_title="Date", hovermode='x unified')

    #token amounts
    token_total_df = df.groupby("SYMBOL").sum(numeric_only=True).sort_values("TOKEN_AMOUNT_USD", ascending=False)

    fig4 = px.bar(
                token_total_df, 
                y='TOKEN_AMOUNT_USD',
                title="USD Value Bridged by Token",
                labels={
                    "SYMBOL": "Symbol",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig4.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Symbol", hovermode="x")

    return {
        "total_volume_by_source": fig.to_html(),
        "monthly_median_usd": fig2.to_html(),
        "by_date_usd": fig3.to_html(),

        "monthly_median_user": fig2_user.to_html(),
        "by_date_user": fig3_user.to_html(),

        "by_token": fig4.to_html(),
    }


# axelar
@api.route('/axelar_volume')
async def axelar_volume():
    queryIds = [
        '3e4cb76d-f7a8-4b42-b542-4d6a423ebff1',
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
    fig.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Source Chain", hovermode="x")

    # get data by month's median
    df2 = pd.DataFrame(data)

    # sum all data first
    df2 = df2.groupby('DATE').sum(numeric_only=True).reset_index()
    df2['YearMonth'] = pd.to_datetime(df2['DATE'],format='%Y-%m-%d').apply(lambda x: x.strftime('%Y-%m'))
    monthly_median = df2.groupby('YearMonth').median(numeric_only=True)

    fig2 = px.line(
                monthly_median, 
                y='TOKEN_AMOUNT_USD',
                title="Median USD Value Bridged Per Month",
                labels={
                    "YearMonth": "Month",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig2.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Month", hovermode="x")

    fig2_user = px.line(
                monthly_median, 
                y='USER_COUNT',
                title="Median Bridgers Per Day By Month",
                labels={
                    "YearMonth": "Month",
                    "USER_COUNT": "User Count"
                }
            )
    fig2_user.update_layout(showlegend=False, yaxis_title="User Count", xaxis_title="Month", hovermode="x")

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
        title="Bridgers Per Day By Chain",
        labels={
            "SOURCE_CHAIN": "Source Chain",
            "USER_COUNT": "User Count"
        }
    )
    fig3_user.update_layout(yaxis_title="User Count", xaxis_title="Date")

    #token amounts
    token_total_df = df.groupby("SYMBOL").sum(numeric_only=True).sort_values("TOKEN_AMOUNT_USD", ascending=False)

    fig4 = px.bar(
                token_total_df, 
                y='TOKEN_AMOUNT_USD',
                title="USD Value Bridged by Token",
                labels={
                    "SYMBOL": "Symbol",
                    "TOKEN_AMOUNT_USD": "Amount USD"
                }
            )
    fig4.update_layout(showlegend=False, yaxis_title="Amount USD", xaxis_title="Symbol", hovermode="x")

    return {
        "total_volume_by_source": fig.to_html(),
        "monthly_median_usd": fig2.to_html(),
        "by_date_usd": fig3.to_html(),

        "monthly_median_user": fig2_user.to_html(),
        "by_date_user": fig3_user.to_html(),

        "by_token": fig4.to_html(),
    }
