import pandas as pd

def create_df(file):
    df = pd.read_csv(file)
    return df

def subset(df, lane):
    '''This function will create a subset of the original dataframe containing only 
    columns related to the specified lane'''
    
    # bot lane consists of both the adc and the support
    if lane.lower() == 'bot':
        new_df = df[['Ad1', 'Ad1Summ1', 'Ad1Summ2', 'Ad1Keystone', 'Ad1Xp', 'Ad1Gold',
                     'Ad2', 'Ad2Summ1', 'Ad2Summ2', 'Ad2Keystone', 'Ad2Xp', 'Ad2Gold',
                     'Supp1', 'Supp1Summ1', 'Supp1Summ2', 'Supp1Keystone', 'Supp1Xp', 'Supp1Gold',
                     'Supp2', 'Supp2Summ1', 'Supp2Summ2', 'Supp2Keystone', 'Supp2Xp', 'Supp2Gold']]
    
    else:
        if lane == 'jg': # jg is a common abbreviation of jungle
            l = 'Jungle'
        else:
            l = lane[0].upper() + lane[1: ].lower()
        new_df = df[[f'{l}1', f'{l}1Summ1', f'{l}1Summ2', f'{l}1Keystone', f'{l}1Xp', f'{l}1Gold',
                     f'{l}2', f'{l}2Summ1', f'{l}2Summ2', f'{l}2Keystone', f'{l}2Xp', f'{l}2Gold']]
         
    return new_df

def make_new_col(sub_df, lane):
    if lane.lower() == 'bot':
        sub_df['AdXpDiff'] = (sub_df['Ad1Xp'] * 10) - (sub_df['Ad2Xp'] * 10)
        sub_df['AdGoldDiff'] = (sub_df['Ad1Gold'] * 10) - (sub_df['Ad2Gold'] * 10)
        sub_df['SuppXpDiff'] = (sub_df['Supp1Xp'] * 10) - (sub_df['Supp2Xp'] * 10)
        sub_df['SuppGoldDiff'] = (sub_df['Supp1Gold'] * 10) - (sub_df['Supp2Gold'] * 10)
    
    else:
        if lane == 'jg': # jg is a common abbreviation of jungle
            l = 'Jungle'
        else:
            l = lane[0].upper() + lane[1: ].lower()
            
        sub_df['XpDiff'] = (sub_df[f'{l}1Xp'] * 10) - (sub_df[f'{l}2Xp'] * 10)
        sub_df['GoldDiff'] = (sub_df[f'{l}1Gold'] * 10) - (sub_df[f'{l}2Gold'] * 10)

if __name__ == '__main__':
    
    pd.set_option('chained_assignment',None)
    
    # look at column names
    # print(df.columns)

    # check number of rows and columns
    #print(df.shape)

    # check if there are any null values
    # print(df.isnull().values.any())
    
    file = 'data.csv'
    dataframe = create_df(file)
    
    subset_df = subset(dataframe, 'top')
    make_new_col(subset_df, 'top')
    print(subset_df.columns)
    print(subset_df.shape)
    print(subset_df)
    
    