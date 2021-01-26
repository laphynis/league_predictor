import dataframe
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor

def tree(df, lane, x):
    if lane.lower() == 'bot':
        x_ad_train = df[['Ad1', 'Ad1Summ1', 'Ad1Summ2', 'Ad1Keystone',
                         'Ad2', 'Ad2Summ1', 'Ad2Summ2', 'Ad2Keystone']]

        x_supp_train = df[['Supp1', 'Supp1Summ1', 'Supp1Summ2', 'Supp1Keystone',
                           'Supp2', 'Supp2Summ1', 'Supp2Summ2', 'Supp2Keystone']]

        ad_xp_diff = df['AdXpDiff']
        ad_g_diff = df['AdGoldDiff']
        supp_xp_diff = df['SuppXpDiff']
        supp_g_diff = df['SuppGoldDiff']

        ad_xp_model = DecisionTreeRegressor()
        ad_xp_model.fit(x_ad_train, ad_xp_diff)

        ad_gold_model = DecisionTreeRegressor()
        ad_gold_model.fit(x_ad_train, ad_g_diff)

        supp_xp_model = DecisionTreeRegressor()
        supp_xp_model.fit(x_supp_train, supp_xp_diff)

        supp_gold_model = DecisionTreeRegressor()
        supp_gold_model.fit(x_supp_train, supp_g_diff)

        x_ad_test = x[['Ad1', 'Ad1Summ1', 'Ad1Summ2', 'Ad1Keystone',
                     'Ad2', 'Ad2Summ1', 'Ad2Summ2', 'Ad2Keystone']]

        x_supp_test = x[['Supp1', 'Supp1Summ1', 'Supp1Summ2', 'Supp1Keystone',
                     'Supp2', 'Supp2Summ1', 'Supp2Summ2', 'Supp2Keystone']]

        ad_xp_pred = ad_xp_model.predict(x_ad_test)
        ad_g_pred = ad_gold_model.predict(x_ad_test)

        supp_xp_pred = supp_xp_model.predict(x_supp_test)
        supp_g_pred = supp_gold_model.predict(x_supp_test)

        return ad_xp_pred, ad_g_pred, supp_xp_pred, supp_g_pred

    else:
        if lane == 'jg':  # jg is a common abbreviation for jungle
            l = 'Jungle'
        else:
            l = lane[0].upper() + lane[1:].lower()
        x_train = df[[f'{l}1', f'{l}1Summ1', f'{l}1Summ2', f'{l}1Keystone',
                     f'{l}2', f'{l}2Summ1', f'{l}2Summ2', f'{l}2Keystone']]

        x_test = x[[f'{l}1', f'{l}1Summ1', f'{l}1Summ2', f'{l}1Keystone',
                     f'{l}2', f'{l}2Summ1', f'{l}2Summ2', f'{l}2Keystone']]

        xp_diff = df['XpDiff']
        gold_diff = df['GoldDiff']

        xp_model = RandomForestRegressor(max_depth=4, n_estimators=500)
        xp_model.fit(x_train, xp_diff)

        gold_model = RandomForestRegressor(max_depth=4, n_estimators=500)
        gold_model.fit(x_train, gold_diff)

        xp = xp_model.predict(x_test)
        gold = gold_model.predict(x_test)

        return xp, gold

if __name__ == '__main__':
    # testing the model

    df = dataframe.create_df('data.csv')
    training_data_top = dataframe.subset(df, 'top')
    dataframe.make_new_col(training_data_top, 'top')

    training_data_jg = dataframe.subset(df, 'jg')
    dataframe.make_new_col(training_data_jg, 'jg')

    training_data_mid = dataframe.subset(df, 'mid')
    dataframe.make_new_col(training_data_mid, 'mid')

    training_data_ad = dataframe.subset(df, 'ad')
    dataframe.make_new_col(training_data_ad, 'ad')

    training_data_supp = dataframe.subset(df, 'supp')
    dataframe.make_new_col(training_data_supp, 'supp')

    test_df = dataframe.create_df('test.csv')

    print(test_df[['Top1', 'Top2']])
    xp, gold = tree(training_data_top, 'top', test_df)
    print(xp, gold)

    print('\n')

    print(test_df[['Jungle1', 'Jungle2']])
    xp, gold = tree(training_data_jg, 'jg', test_df)
    print(xp, gold)

    print('\n')

    print(test_df[['Mid1', 'Mid2']])
    xp, gold = tree(training_data_mid, 'mid', test_df)
    print(xp, gold)

    print('\n')

    print(test_df[['Ad1', 'Ad2']])
    xp, gold = tree(training_data_ad, 'ad', test_df)
    print(xp, gold)

    print('\n')

    print(test_df[['Supp1', 'Supp2']])
    xp, gold = tree(training_data_supp, 'supp', test_df)
    print(xp, gold)


