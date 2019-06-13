import pandas as pd
import pymongo
import get_csv
import re

def to_mongo(options, download_dir):

    PRICING_COLUMNS = ['FixedPrice', 'VariablePrice', 'CustomPrice',
            'AdditionalFees'] 
    pd.options.mode.chained_assignment = None

    for option in options:
        supplier = options[option] 
        supplier = supplier.replace(' ', '_')
        fp = download_dir + f'/{supplier}_data.csv'
        df = pd.read_csv(fp)
        df = df.sort_values('Supplier')
        df = df.reset_index()
        df = df.drop('index', axis=1)
        df = df.astype(str)
        for col in df.columns:
            df[col] = df[col].str.replace('$', '', regex=True)
            #try converting column to float
            try:
                df[col] = df[col].astype(float)
            #if we can't, loop through series and find the problem cell(s) 
            except:
                for i, element in enumerate(df[col]):
                    #cast each individual one as a float 
                    try: 
                        element = float(element) 
                        df[col][i] = element 
                    #if we can't, just move on and leave as a string 
                    except:
                        continue
            #df[col] = df[col].astype(float)
        df = df.fillna(0)
        #print(df)

        #df.to_csv('data/test_data.csv') 

        mongo_uri = 'mongodb://heroku_cg8r2zh6:m3nbgu01cbq6tavgq57ot5seh9@ds237267.mlab.com:37267/heroku_cg8r2zh6'

        client = pymongo.MongoClient(mongo_uri)
        db = client['heroku_vkr5b9ph']
       
        coll = db[options[option]]
       
        for index, row in df.iterrows():
            plan_dict = {}
            pricing_dict = {}
            terms_dict = {}
            
            pricing_dict['fixed_price'] = row['FixedPrice']
            pricing_dict['variable_price'] = row['VariablePrice']
            pricing_dict['custom_price'] = row['CustomPrice']
            pricing_dict['additional_fees'] = row['AdditionalFees']

            terms_dict['number_of_months'] = row['TermInMonths']
            terms_dict['termination_fee'] = row['TerminationFee']

            plan_dict['plan_description'] = row['ProductDescription']
            plan_dict['supplier'] = row['Supplier']
            plan_dict['pricing'] = pricing_dict
            plan_dict['terms'] = terms_dict
            
            coll.insert_one(plan_dict)




