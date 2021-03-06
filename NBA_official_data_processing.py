import pandas as pd
import numpy as np
import pickle

import pycountry
from pycountry_convert import country_alpha3_to_country_alpha2, country_alpha2_to_country_name


COUNTRIES = ['Nigéria', 'Nouvelle_Zélande', 'États-Unis', 'Espagne', 'Canada',
             'Grèce', 'United_Kingdom', 'Israël', 'France', 'Bahamas',
             'Lettonie', 'Géorgie', 'Serbie', 'Croatie', 'Soudan', 'Argentine',
             'Allemagne', 'Saint_Lucia', 'Slovénie', 'Suisse', 'Sénégal',
             'République_dominicaine', 'Cameroun', 'Angola', 'Turquie', 'Italie',
             'Australie', 'Japan', 'Republic_of_the_Congo', 'République_tchèque',
             'Lituanie','République_Démocratique_du_Congo', 'Ukraine',
             'Brésil', 'Finland', 'Egypt', 'Bosnia_and_Herzegovina',
             'Austria', 'Portugal', 'Jamaïque', 'Monténégro']
CODES = ['NGA','NZL','USA','ESP','CAN','GRC','GBR','ISR','FRA','BHS','LVA','GEO',
         'SRB','HRV','SDN','ARG','DEU','LCA','SVN','CHE','SEN','DOM','CMR','AGO',
         'TUR','ITA','AUS','JPN','COD','CZE','LTU','COD','UKR','BRA','FIN','EGY',
         'BIH','AUT','PRT','JAM','MNE']
DICT_ALPHA3 = {COUNTRIES[i] : CODES[i] for i in range(len(COUNTRIES))}



#################################################################################################################################
#                                                                                                                               #
#                                                           PROCESSING                                                          #
#                                                                                                                               #
#################################################################################################################################
def remove_nan_lines(df):
    '''Retire les lignes dans lesquelles il y a une valeur Nan'''
    return df.dropna()


def remove_nan_columns(df):
    '''Retire les colonnes dans lesquelles il y a une valeur Nan'''
    return df.dropna(axis=1)


def alpha3code(column):
    CODE=[]
    for country in column:
        try:
            code=DICT_ALPHA3[country]
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE


def process_data_players(df):
    '''Processing du dataset des stats de joueurs'''
    # Remove Nan
    print(df.shape)
    df = remove_nan_lines(df)
    print(df.shape)

    # Set POSS to float type
    df['POSS'] = df['POSS'].map(lambda x:x.replace(",","."))
    df['POSS'] = df['POSS'].astype('float64')

    # Get alpha3 country codes
    df['iso_alpha'] = alpha3code(df['Pays'])
    df['country'] = df['iso_alpha'].apply(lambda x: country_alpha2_to_country_name(country_alpha3_to_country_alpha2(x)))
    df['PDV'] = df['PDV'].replace('C-F','F-C').replace('F-G','G-F')
    df['PDV'] = df['PDV'].replace('F-C','F').replace('G-F','F')
    
    return df


def process_data_teams(df):
    '''Pour l'instant on met juste les colonnes au bon format'''
    df['POSS'] = df['POSS'].map(lambda x:x.replace(",","."))
    df['POSS'] = df['POSS'].astype('float64')
    return df



#################################################################################################################################
#                                                                                                                               #
#                                                               MERGING                                                         #
#                                                                                                                               #
#################################################################################################################################
def get_common_columns(list_of_df):
    d = [df.columns for df in list_of_df]
    return set(d[0]).intersection(*d[1:])


def merge_all_datasets(list_of_df, key='PLAYER', name='df_players_merged'):
    
    common_cols = [i for i in get_common_columns([list_of_df[0], list_of_df[1]]) if i != key]
    list_of_df[1] = list_of_df[1].drop(list(common_cols), axis=1)
    df_new = list_of_df[0].merge(list_of_df[1], how='left', on=key)
    
    for df in list_of_df[2:]:
        common_cols = [ i for i in get_common_columns([df_new, df]) if i != key]
        df = df.drop(list(common_cols), axis=1)
        df_new = df_new.merge(df, how='left', on=key)
    
        
    # On sauve le dataframe créé
    df_new.to_excel('datasets/'+name+'.xlsx')   # Pour un meilleur apperçu des données
    df_new.to_csv('datasets/'+name+'.csv')
    
    return df_new



#################################################################################################################################
#                                                                                                                               #
#                                                               MAIN                                                            #
#                                                                                                                               #
#################################################################################################################################
if __name__ == '__main__':
    
    ### Merging players datasets ###
    dfp1 = pd.read_csv("datasets/stats_players_trad.csv").drop(["Unnamed: 0"], axis=1)
    dfp2 = pd.read_csv("datasets/stats_players_advanced.csv").drop(["Unnamed: 0"], axis=1)
    dfp3 = pd.read_csv("datasets/stats_players_scoring.csv").drop(["Unnamed: 0"], axis=1)
    dfp4 = pd.read_csv("datasets/stats_players_usage.csv").drop(["Unnamed: 0"], axis=1)

    dfp_a = pd.read_csv("datasets/players.csv").rename({"Unnamed: 0":"PLAYER", "Equipe":"TEAM"}, axis=1).drop(['Unit'], axis=1)
    dfp_a['PLAYER'] = dfp_a['PLAYER'].map(lambda x:x.replace('III',' III').replace('II',' II').replace('IV',' IV').replace('  ',' '))
    dfp_a['PLAYER'] = dfp_a['PLAYER'].map(lambda x:x.replace('Jr.',' Jr.').replace('Sr.',' Sr.').replace('  ',' '))
    dfp_a['PLAYER'] = dfp_a['PLAYER'].map(lambda x:x.replace(" '","'"))

    list_of_df = [dfp1, dfp2, dfp3, dfp4, dfp_a]
    df_to_rule_them_all = merge_all_datasets(list_of_df, key='PLAYER', name='df_players_merged')

    ### Merging teams datasets ###
    dft1 = pd.read_csv("datasets/stats_teams_trad.csv").drop(["Unnamed: 0"], axis=1)
    dft2 = pd.read_csv("datasets/stats_teams_advanced.csv").drop(["Unnamed: 0"], axis=1)

    list_of_df = [dft1, dft2]
    df_to_rule_them_all = merge_all_datasets(list_of_df, key='TEAM', name='df_teams_merged')



    ### Processing data ###
    df = pd.read_csv('datasets/df_players_merged.csv').drop(["Unnamed: 0"], axis=1)
    df = process_data_players(df)
    df.to_excel('datasets/df_players_merged.xlsx')
    df.to_csv('datasets/df_players_merged.csv')

    df = pd.read_csv('datasets/df_teams_merged.csv').drop(["Unnamed: 0"], axis=1)
    df = process_data_teams(df)







