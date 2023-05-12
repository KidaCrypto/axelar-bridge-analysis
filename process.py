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

def data():
    directory = 'address_stats'
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

    concatted_df.to_csv('processed.csv')
    return

def get_non_zero_count(x, columns):
    count = 0

    for column in columns:
        if(x[column] > 0):
            count+= 1

    return count

def advanced():
    df = pd.read_csv('processed.csv').set_index('ADDRESS')
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
    
    df.to_csv('adv_processed.csv')

def correlation():
    df = pd.read_csv('processed.csv')
    total_swap_df = df[[
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
    return

if __name__ == '__main__':
    if len(sys.argv) > 1:
        # use this code in command line
        # example python3 process.py data
        globals()[sys.argv[1]]()