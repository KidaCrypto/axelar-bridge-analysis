import os

import pandas as pd

def run():
    directory = 'address_stats'
    concatted_df = pd.DataFrame()
    for filename in os.listdir(directory):
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

if __name__ == '__main__':
    run()