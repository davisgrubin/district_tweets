import pandas as pd
from collections import deque
import os
state_codes = {
'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
'PA': '42', 'AK': '2', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '8',
'CA': '6', 'AL': '1', 'AR': '5', 'VT': '50', 'IL': '17', 'GA': '13',
'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '4', 'ID': '16', 'CT': '9',
'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}
state_codes  = {v:k for k,v in state_codes.items()}
def place_by_dist(cd_file,cdp_file,incp_file):

    df_cd = pd.read_csv(cd_file)
    df_cdp = pd.read_csv(cdp_file,sep="|")
    df_incp = pd.read_csv(incp_file,sep="|")
    df_cd = df_cd.reset_index()
    tab_name = df_cd.columns[3]
    df_cd = df_cd.rename(columns={'level_0':'State','level_1':'PLACEFP','level_2':'County',
                         '{0}'.format(tab_name):'CongressionalDistrict'})
    df_cd = df_cd.drop(index=0)
    df_cd['PLACEFP'] = [str(i).lstrip('0') for i in df_cd['PLACEFP']]
    df_cd['PLACEFP'] = df_cd['PLACEFP'].astype(int)
    df_place_names = pd.concat([df_cdp,df_incp])
    df_place_names['PLACEFP'] = df_place_names['PLACEFP'].astype(int)
    master_df = pd.merge(df_place_names,df_cd,how='inner',on='PLACEFP')
    master_df['State_Abrv'] = [state_codes[str(i)] for i in master_df['STATEFP']]
    master_df['NAME']= master_df['NAME'] +', '+ master_df['State_Abrv']
    return master_df


def make_dict(df):
    dist_dict = dict()
    for dist in df.CongressionalDistrict.unique():
        statefp = df['STATEFP'][0]
        dist_dict["{0}-{1}".format(statefp,dist)] = set(df[df.CongressionalDistrict == dist]['NAME'].values)
    return dist_dict

def get_files():
    files = os.listdir('place_names/')
    files.sort()
    one_dist = ['AK','WY','DE','MT','ND','SD','VT','DC']
    for i in one_dist:
        files = [j for j in files if i not in j]
    files = deque(files)
    listofdict = []
    for i in range(int(len(files)/3)):
        state_dict = make_dict(place_by_dist('place_names/{0}'.format(files[0]),
                                            'place_names/{0}'.format(files[1]),
                                            'place_names/{0}'.format(files[2])))
        listofdict.append(state_dict)
        files.rotate(-3)
    one_dist_files = []
    for i in one_dist:
        for j in os.listdir('place_names/'):
            if i in j:
                one_dist_files.append(j)
    one_dist_files = deque(one_dist_files)
    one_dist_dfs = []
    for j in range(len(one_dist_files)//2):
        df = pd.read_csv('place_names/{0}'.format(one_dist_files[0]),sep = '|')
        df2 = pd.read_csv('place_names/{0}'.format(one_dist_files[1]),sep = '|')
        df = pd.concat([df,df2])
        df = df.reset_index()
        df['CongressionalDistrict'] = '00'
        df['State_Abrv'] = [state_codes[str(i)] for i in df['STATEFP']]
        df['NAME']= df['NAME'] +', '+ df['State_Abrv']
        one_dist_dfs.append(make_dict(df))
        one_dist_files.rotate(-2)

    listofdict = listofdict + one_dist_dfs
    main_dict = { k: v for d in listofdict for k, v in d.items() }
    return main_dict

if __name__ == '__main__':
    DistDict = get_files()
