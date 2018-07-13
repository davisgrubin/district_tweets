import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import psycopg2
import pandas as pd
import json
import datetime as dt


app = dash.Dash(__name__)

#get global data
conn = psycopg2.connect('dbname=davis user=davis host=/var/run/postgresql')


state_codes = {'53': 'WA', '10': 'DE', '11': 'DC', '55': 'WI', '54': 'WV',
    '15': 'HI', '12': 'FL', '56': 'WY', '72': 'PR', '34': 'NJ', '35': 'NM',
    '48': 'TX', '22': 'LA', '37': 'NC', '38': 'ND', '31': 'NE', '47': 'TN',
    '36': 'NY', '42': 'PA', '2': 'AK', '32': 'NV', '33': 'NH', '51': 'VA',
    '8': 'CO', '6': 'CA', '1': 'AL', '5': 'AR', '50': 'VT', '17': 'IL','13':'GA',
    '18': 'IN','19': 'IA', '25': 'MA', '4': 'AZ', '16': 'ID', '9': 'CT','23':'ME',
    '24': 'MD', '40': 'OK', '39': 'OH', '49': 'UT', '29': 'MO', '27': 'MN',
    '26': 'MI', '44': 'RI', '20': 'KS', '30': 'MT', '28': 'MS', '45': 'SC',
    '21': 'KY', '41': 'OR', '46': 'SD'}





app.css.append_css({
    "external_url": "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css"
})

app.layout =html.Div([
 html.Div([
    html.Label(children='Search Term Sentiment'),
    dcc.Input(id='search-term',type='text', value=''),
    html.Button(id='submit-button', children='Submit'),
    html.Label('Date Range (UTC)'),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        initial_visible_month=dt.datetime.now()),
    dcc.RadioItems(
        id = 'hourly-or-daily',
        options=[
        {'label': 'Hourly Avg','value': 'H'},
        {'label': 'Daily Avg', 'value': 'D'},],
        value='H',
        labelStyle={'display': 'inline-block'}),
    dcc.Checklist(
        id = 'all-parties',
        options = [
            {'label':'All Democratic Districts', 'value': 'D'},
            {'label':'All Republican Districts', 'value': 'R'}
        ],
        values = [],
        labelStyle={'display': 'inline-block'}
    ),
    ]),
html.Div([html.Label('Multi-Select Districts for Comparison'),
    dcc.Dropdown(
        id = 'district-selection',
        options=[],
        value = [],
        multi=True)]),
html.Div(id='time-series'),

html.Div(id='intermediate-value', style={'display': 'none'})])


#Helper/Cleaning Functions
def state_from_num(i,dictionary=None):
    a = i.split('-')
    a[0] = dictionary[a[0]]
    return '-'.join(a)

def num_state_format():
    dem_dists, rep_dists = get_parties()
    codes = {v:k for k,v in state_codes.items()}
    dem_dists = {state_from_num(i,codes) for i in dem_dists}
    rep_dists = {state_from_num(i,codes) for i in rep_dists}
    return dem_dists, rep_dists




def get_unique_dists(dists):
    return [{'label': i , 'value': i} for i in dists]


def get_parties(stream=False):
    df = pd.read_csv('legislators-current.csv')
    df = df[df['type'] != 'sen']
    df = df[df['state'] != 'GU']
    df = df[df['state'] != 'MP']
    df = df[df['state'] != 'PR']
    df = df[df['state'] != 'AS']
    df = df[df['state'] != 'VI']
    df['district'] = [str(int(i)) for i in df['district']]
    df['district'] = ['0'+i if len(i) < 2 else i for i in df['district']]
    df['state_dist'] = df['state'] + '-' + df['district']
    dem_dists = df.loc[df['party'] == 'Democrat']
    rep_dists = df.loc[df['party'] == 'Republican']
    dem_dists = set(dem_dists['state_dist'])
    rep_dists = set(rep_dists['state_dist'])
    return dem_dists, rep_dists

def downsample(filter_df,freq,name):
    downsamp = filter_df.polarity.resample(freq).mean()
    n_tweets = filter_df.polarity.resample(freq).count()
    n_tweets = ['n_tweets: ' + str(i) for i in n_tweets.values]
    return {'x':downsamp.index,'y':downsamp.values,'name':name,'text':n_tweets}


def filter_by_dists(dists,df,freq):
    data = []
    for i in dists:
        filter_df = df[df.district.str.match(i)==True]
        data.append(downsamp(filter_df,freq,i))
    return data



def filter_by_party(parties,df,freq):
    dem_dists, rep_dists = get_parties()
    data = []
    for i in parties:
        if i == 'D':
            filter_df = df[df['district'].isin(dem_dists)]
            name = 'All ' + i + ' avg'
            dems = downsample(filter_df,freq,name)
            dems['line'] = {'color':'rgb(22, 96, 167)'}
            data.append(dems)
        else:
            filter_df = df[df['district'].isin(rep_dists)]
            name = 'All ' + i + ' avg'
            reps = downsample(filter_df,freq,name)
            reps['line'] = {'color':'rgb(205, 12, 24)'}
            data.append(reps)

    return data


#Search and store resulting df in client Browser
@app.callback(
    Output('intermediate-value', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('search-term', 'value'),
    State('my-date-picker-range','start_date'),
    State('my-date-picker-range','end_date')]
    )
def search_data(n_clicks,input1,min_date,max_date):
    query = """
    SELECT polarity, date_time, district
    FROM tweetstest
    WHERE content LIKE %(input1)s
    AND date_time BETWEEN %(min_date)s AND %(max_date)s
    ORDER BY date_time DESC;
    """
    params = {'input1':'%' +input1+ '%','min_date':min_date,'max_date':max_date}
    cur = conn.cursor()
    cur.execute(query,params)
    df = pd.DataFrame(cur.fetchall(),columns=['polarity','date_time','district'])

    # df_search = df[df.content.str.contains('{}'.format(str(input1)),case=False,
    #  regex=False) == True]
    df.district = df.district.apply(state_from_num,dictionary=state_codes)
    # more generally, this line would be
    # json.dumps(cleaned_df)
    return df.to_json(date_format='iso', orient='split')


@app.callback(
    Output('time-series', 'children'),
    [Input('intermediate-value','children'),
    Input('district-selection','value'),
    Input('hourly-or-daily','value'),
    Input('all-parties','values')]
    )
def update_time_series(jsonified_cleaned_data,dist,freq,parties):
    # return("You've clicked {0} times and entered {1}".format(n_clicks,input1))
    df = pd.read_json(jsonified_cleaned_data, orient='split')
    # df.date_time = df.date_time.values.astype('datetime64[h]')
    df.set_index('date_time',inplace=True)
    downsamp = df.polarity.resample(freq).mean()
    n_tweets = df.polarity.resample(freq).count()
    n_tweets = ['n_tweets: ' + str(i) for i in n_tweets.values]
    data = []
    data.append({'x':downsamp.index,'y':downsamp.values,'name':"Nat'l Avg",
    'text':n_tweets,'line':{'color':'rgb(115,54,97)'}})
    data_districts = filter_by_dists(dist,df,freq)
    data_parties = filter_by_party(parties,df,freq)
    all_data  = data + data_districts + data_parties
    return dcc.Graph(id='output-graph',figure = {'data':all_data})



@app.callback(
    Output('district-selection','options'),
    [Input('intermediate-value','children')]
    )
def update_dists(jsonified_cleaned_data):
    df_search = pd.read_json(jsonified_cleaned_data, orient='split')
    return(get_unique_dists(df_search.district.unique()))







if __name__ == '__main__':
    app.run_server(host='0.0.0.0')
