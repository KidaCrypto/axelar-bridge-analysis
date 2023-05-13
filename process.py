import os
import sys

import pandas as pd
import numpy as np

# ML / Predictive Analytics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree

# to save trained data later
import joblib

def raw():
    directory = 'raw'
    concatted_df = pd.DataFrame()
    for filename in os.listdir(directory):
        exts = filename.split(".")
        ext = exts[len(exts) - 1]

        #only get csv files
        if(ext != 'csv'):
            continue

        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            df = pd.read_csv(f).set_index('ADDRESS')

            if concatted_df.empty:
                concatted_df = df
                continue
            
            concatted_df = pd.concat([concatted_df, df]).fillna(0)
            
            should_use_max = False
            for column in df.columns:
                if "AGE_DAY" in column or "SWAP_AMOUNT_USD" in column:
                    should_use_max = True
                    break

            # in case where we're checking median / average / total swap etc
            # the numbers should always be the same, hence we use max to get the value
            if should_use_max:
                print(f'{f}: using max')
                concatted_df = concatted_df.groupby('ADDRESS').max()
                continue
                
            print(f'{f}: using sum')
            concatted_df = concatted_df.groupby('ADDRESS').sum()

    concatted_df.to_csv('processed/base.csv')
    return

def get_non_zero_count(x, columns):
    count = 0

    for column in columns:
        if(x[column] > 0):
            count+= 1

    return count

def advanced():
    df = pd.read_csv('processed/base.csv').set_index('ADDRESS')
    plucked_df = df[[
        'CONNEXT_TOTAL_AMOUNT_USD_BRIDGED',
        'HOP_TOTAL_AMOUNT_USD_BRIDGED',
        'ACROSS_TOTAL_AMOUNT_USD_BRIDGED',
        'WORMHOLE_TOTAL_AMOUNT_USD_BRIDGED',
        'CELER_TOTAL_AMOUNT_USD_BRIDGED',
        'SYNAPSE_TOTAL_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_TOTAL_AMOUNT_USD_BRIDGED',
        'SATELLITE_TOTAL_AMOUNT_USD_BRIDGED',
        'SQUID_TOTAL_AMOUNT_USD_BRIDGED',
        'STARGATE_TOTAL_AMOUNT_USD_BRIDGED',
    ]]
    df['TOTAL_AMOUNT_USD_BRIDGED'] = plucked_df.sum(axis=1)
    df['PREFERRED'] = plucked_df.idxmax(axis=1)
    df['PREFERRED'] = df['PREFERRED'].apply(lambda x: x.split("_")[0])

    # chain level
    plucked_chain_df = df[[
        'CONNEXT_ETH_AMOUNT_USD_BRIDGED',
        'HOP_ETH_AMOUNT_USD_BRIDGED',
        'ACROSS_ETH_AMOUNT_USD_BRIDGED',
        'WORMHOLE_ETH_AMOUNT_USD_BRIDGED',
        'CELER_ETH_AMOUNT_USD_BRIDGED',
        'SYNAPSE_ETH_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_ETH_AMOUNT_USD_BRIDGED',
        'SATELLITE_ETH_AMOUNT_USD_BRIDGED',
        'SQUID_ETH_AMOUNT_USD_BRIDGED',
        'STARGATE_ETH_AMOUNT_USD_BRIDGED',
    ]]
    df['ETH_AMOUNT_USD_BRIDGED'] = plucked_chain_df.sum(axis=1)

    plucked_chain_df = df[[
        'CONNEXT_OPTIMISM_AMOUNT_USD_BRIDGED',
        'HOP_OPTIMISM_AMOUNT_USD_BRIDGED',
        'ACROSS_OPTIMISM_AMOUNT_USD_BRIDGED',
        'WORMHOLE_OPTIMISM_AMOUNT_USD_BRIDGED',
        'CELER_OPTIMISM_AMOUNT_USD_BRIDGED',
        'SYNAPSE_OPTIMISM_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_OPTIMISM_AMOUNT_USD_BRIDGED',
        'SATELLITE_OPTIMISM_AMOUNT_USD_BRIDGED',
        'SQUID_OPTIMISM_AMOUNT_USD_BRIDGED',
        'STARGATE_OPTIMISM_AMOUNT_USD_BRIDGED',
    ]]
    df['OPTIMISM_AMOUNT_USD_BRIDGED'] = plucked_chain_df.sum(axis=1)

    plucked_chain_df = df[[
        'CONNEXT_ARBITRUM_AMOUNT_USD_BRIDGED',
        'HOP_ARBITRUM_AMOUNT_USD_BRIDGED',
        'ACROSS_ARBITRUM_AMOUNT_USD_BRIDGED',
        'WORMHOLE_ARBITRUM_AMOUNT_USD_BRIDGED',
        'CELER_ARBITRUM_AMOUNT_USD_BRIDGED',
        'SYNAPSE_ARBITRUM_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_ARBITRUM_AMOUNT_USD_BRIDGED',
        'SATELLITE_ARBITRUM_AMOUNT_USD_BRIDGED',
        'SQUID_ARBITRUM_AMOUNT_USD_BRIDGED',
        'STARGATE_ARBITRUM_AMOUNT_USD_BRIDGED',
    ]]
    df['ARBITRUM_AMOUNT_USD_BRIDGED'] = plucked_chain_df.sum(axis=1)

    plucked_chain_df = df[[
        'CONNEXT_AVALANCHE_AMOUNT_USD_BRIDGED',
        'HOP_AVALANCHE_AMOUNT_USD_BRIDGED',
        'ACROSS_AVALANCHE_AMOUNT_USD_BRIDGED',
        'WORMHOLE_AVALANCHE_AMOUNT_USD_BRIDGED',
        'CELER_AVALANCHE_AMOUNT_USD_BRIDGED',
        'SYNAPSE_AVALANCHE_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_AVALANCHE_AMOUNT_USD_BRIDGED',
        'SATELLITE_AVALANCHE_AMOUNT_USD_BRIDGED',
        'SQUID_AVALANCHE_AMOUNT_USD_BRIDGED',
        'STARGATE_AVALANCHE_AMOUNT_USD_BRIDGED',
    ]]
    df['AVALANCHE_AMOUNT_USD_BRIDGED'] = plucked_chain_df.sum(axis=1)

    plucked_chain_df = df[[
        'CONNEXT_BSC_AMOUNT_USD_BRIDGED',
        'HOP_BSC_AMOUNT_USD_BRIDGED',
        'ACROSS_BSC_AMOUNT_USD_BRIDGED',
        'WORMHOLE_BSC_AMOUNT_USD_BRIDGED',
        'CELER_BSC_AMOUNT_USD_BRIDGED',
        'SYNAPSE_BSC_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_BSC_AMOUNT_USD_BRIDGED',
        'SATELLITE_BSC_AMOUNT_USD_BRIDGED',
        'SQUID_BSC_AMOUNT_USD_BRIDGED',
        'STARGATE_BSC_AMOUNT_USD_BRIDGED',
    ]]
    df['BSC_AMOUNT_USD_BRIDGED'] = plucked_chain_df.sum(axis=1)

    plucked_chain_df = df[[
        'CONNEXT_POLYGON_AMOUNT_USD_BRIDGED',
        'HOP_POLYGON_AMOUNT_USD_BRIDGED',
        'ACROSS_POLYGON_AMOUNT_USD_BRIDGED',
        'WORMHOLE_POLYGON_AMOUNT_USD_BRIDGED',
        'CELER_POLYGON_AMOUNT_USD_BRIDGED',
        'SYNAPSE_POLYGON_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_POLYGON_AMOUNT_USD_BRIDGED',
        'SATELLITE_POLYGON_AMOUNT_USD_BRIDGED',
        'SQUID_POLYGON_AMOUNT_USD_BRIDGED',
        'STARGATE_POLYGON_AMOUNT_USD_BRIDGED',
    ]]
    df['POLYGON_AMOUNT_USD_BRIDGED'] = plucked_chain_df.sum(axis=1)

    #count_nonzero function sometimes return 0?
    df['BRIDGES_USED'] = np.count_nonzero(plucked_df, axis=1)
    #df['BRIDGES_USED'] = plucked_df.apply(lambda x: get_non_zero_count(x, plucked_df.columns), axis=1)
    
    #remove bad data
    df = df[df['BRIDGES_USED'] > 0]
    
    df.to_csv('processed/adv_processed.csv')

def train():
    df = pd.read_csv('processed/adv_processed.csv')
    train_age_day(df)
    train_all_params(df)
    train_general_swap(df)
    train_bridged_volume(df)
    train_day_and_tx(df)
    train_protocol_swap_activity(df)
    train_swap_and_bridge(df)
    train_tx_count(df)

    return


def train_bridged_volume(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
    ]], df['PREFERRED'])

    #get decision tree
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print(x_test)
    print("Bridged Volume Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))
    filename = 'tree_models/bridged_volume.sav'
    joblib.dump(model, filename)

def train_age_day(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'ETH_AGE_DAY',
        'OPTIMISM_AGE_DAY',
        'ARBITRUM_AGE_DAY',
        'BSC_AGE_DAY',
        'POLYGON_AGE_DAY',
        'AVALANCHE_AGE_DAY',
    ]], df['PREFERRED'])

    #get decision tree
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Address Age Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))
    filename = 'tree_models/age_day.sav'
    joblib.dump(model, filename)

def train_tx_count(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'ETH_TX_COUNT',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_TX_COUNT',
        'BSC_TX_COUNT',
        'POLYGON_TX_COUNT',
        'AVALANCHE_TX_COUNT',
    ]], df['PREFERRED'])

    #get decision tree
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Tx Count Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))
    filename = 'tree_models/tx_count.sav'
    joblib.dump(model, filename)

def train_protocol_swap_activity(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
    ]], df['PREFERRED'])

    #get decision tree
    #model = DecisionTreeClassifier(criterion='entropy')
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Protocol Swap Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))
    filename = 'tree_models/protocol_swap_activity.sav'
    joblib.dump(model, filename)

def train_general_swap(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
    ]], df['PREFERRED'])

    #get decision tree
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("General Swap Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))
    filename = 'tree_models/general_swap.sav'
    joblib.dump(model, filename)

def train_swap_and_bridge(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'TOTAL_SWAP_AMOUNT_USD',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]], df['PREFERRED'])

    #get decision tree
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Swap and Bridge Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))
    filename = 'tree_models/swap_and_bridge.sav'
    joblib.dump(model, filename)

def train_day_and_tx(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'ETH_AGE_DAY',
        'OPTIMISM_AGE_DAY',
        'ARBITRUM_AGE_DAY',
        'BSC_AGE_DAY',
        'POLYGON_AGE_DAY',
        'AVALANCHE_AGE_DAY',
        'ETH_TX_COUNT',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_TX_COUNT',
        'BSC_TX_COUNT',
        'POLYGON_TX_COUNT',
        'AVALANCHE_TX_COUNT',
    ]], df['PREFERRED'])

    #get decision tree
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    print("Age and Tx Count Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))
    filename = 'tree_models/day_and_tx.sav'
    joblib.dump(model, filename)

def train_all_params(df: pd.DataFrame):
    #train the model
    x_train, x_test, y_train, y_test = train_test_split(df[[
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]], df['PREFERRED'])

    #get decision tree
    model = DecisionTreeClassifier(
        criterion='entropy', 
        min_samples_leaf=20, 
    )
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    print("All Params Tree Accuracy: {accuracy:.2f}%".format(accuracy=accuracy_score(y_test, y_pred) * 100))

    filename = 'tree_models/all_params.sav'
    joblib.dump(model, filename)


def correlation():
    folder = 'correlations'
    df = pd.read_csv('processed/adv_processed.csv')
    bridge_df = df[[
        'TOTAL_AMOUNT_USD_BRIDGED',
        'CONNEXT_TOTAL_AMOUNT_USD_BRIDGED',
        'HOP_TOTAL_AMOUNT_USD_BRIDGED',
        'ACROSS_TOTAL_AMOUNT_USD_BRIDGED',
        'WORMHOLE_TOTAL_AMOUNT_USD_BRIDGED',
        'CELER_TOTAL_AMOUNT_USD_BRIDGED',
        'SYNAPSE_TOTAL_AMOUNT_USD_BRIDGED',
        'MULTICHAIN_TOTAL_AMOUNT_USD_BRIDGED',
        'SATELLITE_TOTAL_AMOUNT_USD_BRIDGED',
        'SQUID_TOTAL_AMOUNT_USD_BRIDGED',
        'STARGATE_TOTAL_AMOUNT_USD_BRIDGED',
    ]]
    corr_df = bridge_df.corr()
    corr_df.to_csv(f'{folder}/bridge_corr.csv')

    all_params_df = df[[
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = all_params_df.corr()
    corr_df.to_csv(f'{folder}/all_params_corr.csv')

    protocol_df = df[[
        'CONNEXT_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/connext_corr.csv')

    protocol_df = df[[
        'HOP_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/hop_corr.csv')

    protocol_df = df[[
        'ACROSS_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/across_corr.csv')

    protocol_df = df[[
        'WORMHOLE_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/wormhole_corr.csv')

    protocol_df = df[[
        'CELER_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/celer_corr.csv')

    protocol_df = df[[
        'SYNAPSE_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/synapse_corr.csv')

    protocol_df = df[[
        'MULTICHAIN_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/multichain_corr.csv')

    protocol_df = df[[
        'SATELLITE_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/satellite_corr.csv')

    protocol_df = df[[
        'SQUID_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/squid_corr.csv')

    protocol_df = df[[
        'STARGATE_TOTAL_AMOUNT_USD_BRIDGED',
        'BSC_AGE_DAY',
        'BSC_TX_COUNT',
        'TOTAL_SWAP_AMOUNT_USD',
        'AVERAGE_SWAP_AMOUNT_USD_PER_TX',
        'MEDIAN_SWAP_AMOUNT_USD_PER_TX',
        'UNISWAP_SWAP_VOLUME',
        'CURVE_SWAP_VOLUME',
        'OTHER_SWAP_VOLUME',
        'SWAP_DAYS_ACTIVE',
        'SWAP_TX_COUNT',
        'ETH_AGE_DAY',
        'ETH_TX_COUNT',
        'AVALANCHE_AGE_DAY',
        'AVALANCHE_TX_COUNT',
        'OPTIMISM_AGE_DAY',
        'OPTIMISM_TX_COUNT',
        'ARBITRUM_AGE_DAY',
        'ARBITRUM_TX_COUNT',
        'POLYGON_AGE_DAY',
        'POLYGON_TX_COUNT',
        'TOTAL_AMOUNT_USD_BRIDGED',
        'ETH_AMOUNT_USD_BRIDGED',
        'OPTIMISM_AMOUNT_USD_BRIDGED',
        'ARBITRUM_AMOUNT_USD_BRIDGED',
        'AVALANCHE_AMOUNT_USD_BRIDGED',
        'BSC_AMOUNT_USD_BRIDGED',
        'POLYGON_AMOUNT_USD_BRIDGED',
        'BRIDGES_USED',
    ]]
    corr_df = protocol_df.corr()
    corr_df.to_csv(f'{folder}/stargate_corr.csv')
    return

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # use this code in command line
        # example python3 process.py data
        globals()[sys.argv[1]]()