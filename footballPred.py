import pandas as pd
from math import pi
import numpy as np
from numpy import average
import itertools
import copy 
import ipywidgets as widgets
from ipywidgets import interact, interactive, Dropdown
from IPython.display import display, clear_output

from datetime import datetime
from bokeh.models import ColumnDataSource, Select, HoverTool,CategoricalColorMapper, Spacer, FactorRange, Panel,Tabs, LabelSet, Label, StringFormatter, NumeralTickFormatter
from bokeh.layouts import column, row, gridplot 
from bokeh.transform import dodge, cumsum
from bokeh.models.widgets import DataTable, TableColumn, HTMLTemplateFormatter, Div, Dropdown
from bokeh.palettes import PuBu, PuRd, Pastel1, PiYG, YlGnBu, RdYlGn, viridis, YlGn, GnBu, YlOrRd, YlOrBr

from bokeh.plotting import figure, save
import matplotlib.pyplot as plt
from bokeh.io import output_notebook, show, output_file, export_png
import seaborn as sns
from scipy.stats import poisson,skellam
import statsmodels.formula.api as smf
import statsmodels.api as sm
sns.set_style('white')
from sklearn.preprocessing import Normalizer, MinMaxScaler, LabelEncoder, scale

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn import svm

from sklearn.datasets import load_linnerud
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from statsmodels.formula.api import ols
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from scipy import stats
from bokeh.resources import CDN
from bokeh.embed import file_html


#%matplotlib inline
#output_notebook()


#Italy df build
def DFmerged(lg):
    #firstdf, lg, a,b,c,d,e,f = str(firstdf), str(lg), str(a),str(b),str(c),str(d), str(e), str(f)
    firstdf = pd.read_csv('spi_matches.csv', delimiter=',', index_col=0)
    a,b,c,d,e,f = 'I1(1).csv','I1(2).csv','I1(3).csv','I1(4).csv','I1(5).csv','I1(6).csv'
    
    
    #firstdf = pd.read_csv(firstdf, delimiter=',', index_col=0)
    

    colIT = ['date','league','team1','team2','score1','score2', 'spi1' ,'spi2' , 'importance1','importance2']
    df = firstdf[colIT]
    df = df.reset_index()
    df.columns = ['season','Date','league','HomeTeam','AwayTeam','GoalsHome','GoalsAway', 'spi1' ,'spi2' , 'importance1','importance2']

    
    #league
    df =  df[(df['league'] == lg) & (df['GoalsHome'] >= 0)]
    #df = df.dropna()
    df[['GoalsHome','GoalsAway']] = df[['GoalsHome','GoalsAway']].astype(int)
    #coldf = ['season', 'Date', 'league', 'HomeTeam', 'AwayTeam', 'GoalsHome', 'GoalsAway', 'spi1', 'spi2']
    #df = df[coldf]
    
    dfa = pd.read_csv(a, delimiter=',', index_col=0)
    dfb = pd.read_csv(b, delimiter=',', index_col=0)
    dfc = pd.read_csv(c, delimiter=',', index_col=0)
    dfd = pd.read_csv(d, delimiter=',', index_col=0)
    dfe = pd.read_csv(e, delimiter=',', index_col=0)
    dff = pd.read_csv(f, delimiter=',', index_col=0)

    df1 = pd.DataFrame(dfa.assign(Season=15).merge(dfb.assign(Season=16), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfc.assign(Season=17), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfd.assign(Season=18), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfe.assign(Season=19), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dff.assign(Season=20), 'outer').fillna(0))
    
    
    colS = ['Season','Date','HomeTeam','AwayTeam','FTHG','FTAG', 'FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    colSc = ['FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    df2 = df1[colS]

    #create conditions to compare the scores
    #cond1 = [ (df2['FTHG'] > df2['FTAG']), (df2['FTHG'] < df2['FTAG']), (df2['FTHG'] == df2['FTAG'])]
    #cond2 = [ (df2['FTAG'] > df2['FTHG']), (df2['FTAG'] < df2['FTHG']), (df2['FTAG'] == df2['FTHG'])]

    #choices result and points
    #cc = ['W','L','D']
    #ccp = [3,0,1]

    #adding new columns for results
    #df2['HRes'] = np.select(cond1, ccp, default=0 )
    #df2['ARes'] = np.select(cond2, ccp, default=0 )
    #df2['resultH'] = np.select(cond1, cc, default=0)
    #df2['resultA'] = np.select(cond2, cc,default=0)
    #df2['resultT'] = df2['resultH']

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))
    
    t1 = df2.set_index('Date')
    t2 = df.set_index('Date')
    
    df16_set2 = t1[t1['Season'] == 16].reset_index()
    df17_set2 = t1[t1['Season'] == 17].reset_index()
    df18_set2 = t1[t1['Season'] == 18].reset_index()
    df19_set2 = t1[t1['Season'] == 19].reset_index()
    df20_set2 = t1[t1['Season'] == 20].reset_index()
    
    df16_set1 = t2[t2['season'] == 2016].reset_index()
    df17_set1 = t2[t2['season'] == 2017].reset_index()
    df18_set1 = t2[t2['season'] == 2018].reset_index()
    df19_set1 = t2[t2['season'] == 2019].reset_index()
    df20_set1 = t2[t2['season'] == 2020].reset_index()
    
    
    
    df16_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df16_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df17_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df17_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df18_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df18_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df19_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df19_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df20_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df20_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]


    dfT = df16_set1.append(df17_set1)
    dfT = dfT.append(df18_set1)
    dfT = dfT.append(df19_set1)
    dfT = dfT.append(df20_set1)
    dfT.dropna()
    
        
    return dfT


#England df build
def DFmergedEngland(lg):
    #firstdf, lg, a,b,c,d,e,f = str(firstdf), str(lg), str(a),str(b),str(c),str(d), str(e), str(f)
    firstdf = pd.read_csv('spi_matches.csv', delimiter=',', index_col=0)
    a,b,c,d,e,f = 'E0.csv','E0(0).csv','E0(1).csv','E0(2).csv','E0(3).csv','E0(4).csv'
    
    
    #firstdf = pd.read_csv(firstdf, delimiter=',', index_col=0)
    

    colIT = ['date','league','team1','team2','score1','score2', 'spi1' ,'spi2' , 'importance1','importance2']
    df = firstdf[colIT]
    df = df.reset_index()
    df.columns = ['season','Date','league','HomeTeam','AwayTeam','GoalsHome','GoalsAway', 'spi1' ,'spi2' , 'importance1','importance2']

    
    #league
    df =  df[(df['league'] == lg) & (df['GoalsHome'] >= 0)]
    #df = df.dropna()
    df[['GoalsHome','GoalsAway']] = df[['GoalsHome','GoalsAway']].astype(int)
    #coldf = ['season', 'Date', 'league', 'HomeTeam', 'AwayTeam', 'GoalsHome', 'GoalsAway', 'spi1', 'spi2']
    #df = df[coldf]
    
    dfa = pd.read_csv(a, delimiter=',', index_col=0)
    dfb = pd.read_csv(b, delimiter=',', index_col=0)
    dfc = pd.read_csv(c, delimiter=',', index_col=0)
    dfd = pd.read_csv(d, delimiter=',', index_col=0)
    dfe = pd.read_csv(e, delimiter=',', index_col=0)
    dff = pd.read_csv(f, delimiter=',', index_col=0)

    df1 = pd.DataFrame(dfa.assign(Season=15).merge(dfb.assign(Season=16), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfc.assign(Season=17), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfd.assign(Season=18), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfe.assign(Season=19), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dff.assign(Season=20), 'outer').fillna(0))
    
    
    colS = ['Season','Date','HomeTeam','AwayTeam','FTHG','FTAG', 'FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    colSc = ['FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    df2 = df1[colS]

    #create conditions to compare the scores
    #cond1 = [ (df2['FTHG'] > df2['FTAG']), (df2['FTHG'] < df2['FTAG']), (df2['FTHG'] == df2['FTAG'])]
    #cond2 = [ (df2['FTAG'] > df2['FTHG']), (df2['FTAG'] < df2['FTHG']), (df2['FTAG'] == df2['FTHG'])]

    #choices result and points
    #cc = ['W','L','D']
    #ccp = [3,0,1]

    #adding new columns for results
    #df2['HRes'] = np.select(cond1, ccp, default=0 )
    #df2['ARes'] = np.select(cond2, ccp, default=0 )
    #df2['resultH'] = np.select(cond1, cc, default=0)
    #df2['resultA'] = np.select(cond2, cc,default=0)
    #df2['resultT'] = df2['resultH']

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))
    
    t1 = df2.set_index('Date')
    t2 = df.set_index('Date')
    
    df16_set2 = t1[t1['Season'] == 16].reset_index()
    df17_set2 = t1[t1['Season'] == 17].reset_index()
    df18_set2 = t1[t1['Season'] == 18].reset_index()
    df19_set2 = t1[t1['Season'] == 19].reset_index()
    df20_set2 = t1[t1['Season'] == 20].reset_index()
    
    df16_set1 = t2[t2['season'] == 2016].reset_index()
    df17_set1 = t2[t2['season'] == 2017].reset_index()
    df18_set1 = t2[t2['season'] == 2018].reset_index()
    df19_set1 = t2[t2['season'] == 2019].reset_index()
    df20_set1 = t2[t2['season'] == 2020].reset_index()
    
    
    
    df16_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df16_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df17_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df17_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df18_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df18_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df19_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df19_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df20_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df20_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]


    dfT = df16_set1.append(df17_set1)
    dfT = dfT.append(df18_set1)
    dfT = dfT.append(df19_set1)
    dfT = dfT.append(df20_set1)
    dfT.dropna()
    dfT.replace('West Bromwich Albion', 'West Brom', inplace=True)
    dfT.replace('Brighton and Hove Albion', 'Brighton', inplace=True)
    dfT.replace('Tottenham Hotspur', 'Tottenham', inplace=True)
    dfT.replace('Manchester United', 'Man United', inplace=True)
    dfT.replace('Manchester City','Man City', inplace=True)
    dfT.replace('Leicester City', 'Leicester', inplace=True)
    dfT.replace('West Ham United', 'West Ham', inplace=True)
    dfT.replace('Sheffield United', 'Sheffield', inplace=True)  
        
    return dfT

def DFmergedFrance(lg):
    
    firstdf = pd.read_csv('spi_matches.csv', delimiter=',', index_col=0)
    a,b,c,d,e,f = 'F1.csv','F1(1).csv','F1(2).csv','F1(3).csv','F1(4).csv','F1(5).csv'
    
    
    #firstdf = pd.read_csv(firstdf, delimiter=',', index_col=0)
    

    colIT = ['date','league','team1','team2','score1','score2', 'spi1' ,'spi2' , 'importance1','importance2']
    df = firstdf[colIT]
    df = df.reset_index()
    df.columns = ['season','Date','league','HomeTeam','AwayTeam','GoalsHome','GoalsAway', 'spi1' ,'spi2' , 'importance1','importance2']

    
    #league
    df =  df[(df['league'] == lg) & (df['GoalsHome'] >= 0)]
    df[['GoalsHome','GoalsAway']] = df[['GoalsHome','GoalsAway']].astype(int)
   
    
    dfa = pd.read_csv(a, delimiter=',', index_col=0)
    dfb = pd.read_csv(b, delimiter=',', index_col=0)
    dfc = pd.read_csv(c, delimiter=',', index_col=0)
    dfd = pd.read_csv(d, delimiter=',', index_col=0)
    dfe = pd.read_csv(e, delimiter=',', index_col=0)
    dff = pd.read_csv(f, delimiter=',', index_col=0)

    df1 = pd.DataFrame(dfa.assign(Season=15).merge(dfb.assign(Season=16), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfc.assign(Season=17), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfd.assign(Season=18), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfe.assign(Season=19), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dff.assign(Season=20), 'outer').fillna(0))
    
    
    colS = ['Season','Date','HomeTeam','AwayTeam','FTHG','FTAG', 'FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    colSc = ['FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    df2 = df1[colS]

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))
    
    t1 = df2.set_index('Date')
    t2 = df.set_index('Date')
    
    df16_set2 = t1[t1['Season'] == 16].reset_index()
    df17_set2 = t1[t1['Season'] == 17].reset_index()
    df18_set2 = t1[t1['Season'] == 18].reset_index()
    df19_set2 = t1[t1['Season'] == 19].reset_index()
    df20_set2 = t1[t1['Season'] == 20].reset_index()
    
    df16_set1 = t2[t2['season'] == 2016].reset_index()
    df17_set1 = t2[t2['season'] == 2017].reset_index()
    df18_set1 = t2[t2['season'] == 2018].reset_index()
    df19_set1 = t2[t2['season'] == 2019].reset_index()
    df20_set1 = t2[t2['season'] == 2020].reset_index()
    
    
    
    df16_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df16_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df17_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df17_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df18_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df18_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df19_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df19_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df20_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df20_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]


    dfT = df16_set1.append(df17_set1)
    dfT = dfT.append(df18_set1)
    dfT = dfT.append(df19_set1)
    dfT = dfT.append(df20_set1)
    dfT.dropna()
    dfT.replace('West Bromwich Albion', 'West Brom', inplace=True)
    dfT.replace('Brighton and Hove Albion', 'Brighton', inplace=True)
    dfT.replace('Tottenham Hotspur', 'Tottenham', inplace=True)
    dfT.replace('Manchester United', 'Man United', inplace=True)
    dfT.replace('Manchester City','Man City', inplace=True)
    dfT.replace('Leicester City', 'Leicester', inplace=True)
    dfT.replace('West Ham United', 'West Ham', inplace=True)
    dfT.replace('Sheffield United', 'Sheffield', inplace=True)  
        
    return dfT



#Germany df build
def DFmergedGermany(lg):
    #firstdf, lg, a,b,c,d,e,f = str(firstdf), str(lg), str(a),str(b),str(c),str(d), str(e), str(f)
    firstdf = pd.read_csv('spi_matches.csv', delimiter=',', index_col=0)
    a,b,c,d,e,f = 'D1.csv','D2.csv','D2(1).csv','D2(2).csv','D2(3).csv','D2(4).csv'
    
    
    #firstdf = pd.read_csv(firstdf, delimiter=',', index_col=0)
    

    colIT = ['date','league','team1','team2','score1','score2', 'spi1' ,'spi2' , 'importance1','importance2']
    df = firstdf[colIT]
    df = df.reset_index()
    df.columns = ['season','Date','league','HomeTeam','AwayTeam','GoalsHome','GoalsAway', 'spi1' ,'spi2' , 'importance1','importance2']

    
    #league
    df =  df[(df['league'] == lg) & (df['GoalsHome'] >= 0)]
    #df = df.dropna()
    df[['GoalsHome','GoalsAway']] = df[['GoalsHome','GoalsAway']].astype(int)
    #coldf = ['season', 'Date', 'league', 'HomeTeam', 'AwayTeam', 'GoalsHome', 'GoalsAway', 'spi1', 'spi2']
    #df = df[coldf]
    
    dfa = pd.read_csv(a, delimiter=',', index_col=0)
    dfb = pd.read_csv(b, delimiter=',', index_col=0)
    dfc = pd.read_csv(c, delimiter=',', index_col=0)
    dfd = pd.read_csv(d, delimiter=',', index_col=0)
    dfe = pd.read_csv(e, delimiter=',', index_col=0)
    dff = pd.read_csv(f, delimiter=',', index_col=0)

    df1 = pd.DataFrame(dfa.assign(Season=15).merge(dfb.assign(Season=16), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfc.assign(Season=17), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfd.assign(Season=18), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dfe.assign(Season=19), 'outer').fillna(0))
    df1 = pd.DataFrame(df1.merge(dff.assign(Season=20), 'outer').fillna(0))
    
    
    colS = ['Season','Date','HomeTeam','AwayTeam','FTHG','FTAG', 'FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    colSc = ['FTHG','FTAG','FTR','HTHG','HTAG','HTR','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A']
    df2 = df1[colS]

    #create conditions to compare the scores
    #cond1 = [ (df2['FTHG'] > df2['FTAG']), (df2['FTHG'] < df2['FTAG']), (df2['FTHG'] == df2['FTAG'])]
    #cond2 = [ (df2['FTAG'] > df2['FTHG']), (df2['FTAG'] < df2['FTHG']), (df2['FTAG'] == df2['FTHG'])]

    #choices result and points
    #cc = ['W','L','D']
    #ccp = [3,0,1]

    #adding new columns for results
    #df2['HRes'] = np.select(cond1, ccp, default=0 )
    #df2['ARes'] = np.select(cond2, ccp, default=0 )
    #df2['resultH'] = np.select(cond1, cc, default=0)
    #df2['resultA'] = np.select(cond2, cc,default=0)
    #df2['resultT'] = df2['resultH']

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))

    
    df2['Date'] = pd.to_datetime(df2['Date'], infer_datetime_format=True)
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True)
    df2['Date'] = pd.to_datetime(df2['Date'], format=('%Y/%m/%d'))
    df['Date'] = pd.to_datetime(df['Date'], format=('%Y/%m/%d'))
    
    t1 = df2.set_index('Date')
    t2 = df.set_index('Date')
    
    df16_set2 = t1[t1['Season'] == 16].reset_index()
    df17_set2 = t1[t1['Season'] == 17].reset_index()
    df18_set2 = t1[t1['Season'] == 18].reset_index()
    df19_set2 = t1[t1['Season'] == 19].reset_index()
    df20_set2 = t1[t1['Season'] == 20].reset_index()
    
    df16_set1 = t2[t2['season'] == 2016].reset_index()
    df17_set1 = t2[t2['season'] == 2017].reset_index()
    df18_set1 = t2[t2['season'] == 2018].reset_index()
    df19_set1 = t2[t2['season'] == 2019].reset_index()
    df20_set1 = t2[t2['season'] == 2020].reset_index()
    
    
    
    df16_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df16_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df17_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df17_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df18_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df18_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df19_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df19_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]
    df20_set1[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']] = df20_set2[['HS', 'AS', 'HST', 'AST', 'HF', 'AF', 'HC', 'AC', 'HY', 'AY', 'HR', 'AR', 'B365H', 'B365D', 'B365A']]


    dfT = df16_set1.append(df17_set1)
    dfT = dfT.append(df18_set1)
    dfT = dfT.append(df19_set1)
    dfT = dfT.append(df20_set1)
    dfT.dropna()
    dfT.replace('West Bromwich Albion', 'West Brom', inplace=True)
    dfT.replace('Brighton and Hove Albion', 'Brighton', inplace=True)
    dfT.replace('Tottenham Hotspur', 'Tottenham', inplace=True)
    dfT.replace('Manchester United', 'Man United', inplace=True)
    dfT.replace('Manchester City','Man City', inplace=True)
    dfT.replace('Leicester City', 'Leicester', inplace=True)
    dfT.replace('West Ham United', 'West Ham', inplace=True)
    dfT.replace('Sheffield United', 'Sheffield', inplace=True)
    dfT.dropna(inplace=True)   
        
    return dfT



def dfWLD(df):
    home = df
    home['opponent'] = home['HomeTeam']
    home = home[['Date','season','HomeTeam','AwayTeam','GoalsHome','GoalsAway', 'opponent']]
    home['dateHT'] = home['Date'].dt.strftime('%d-%m-%y').astype(str)
    home['ResultHT'] = home['HomeTeam'] + ' '+ home['GoalsHome'].astype(str) + ':'  + home['GoalsAway'].astype(str) + ' ' + home['AwayTeam']
    home['dateHT'] = home['Date'].dt.strftime('%d-%m-%y').astype(str)
    
    #create conditions to compare the scores
    cond1 = [ (home['GoalsHome'] > home['GoalsAway']), (home['GoalsHome'] < home['GoalsAway']), (home['GoalsHome'] == home['GoalsAway'])]
    cond2 = [ (home['GoalsAway'] > home['GoalsHome']), (home['GoalsAway'] < home['GoalsHome']), (home['GoalsAway'] == home['GoalsHome'])]

    #choices result and points
    cc = ['W','L','D']
    ccp = [3,0,1]
    #team = home.team.values[0]

    #adding new columns for results
    home['HRes'] = np.select(cond1, ccp, default=0 )
    home['ARes'] = np.select(cond2, ccp, default=0 )
    home['resultH'] = np.select(cond1, cc, default=0)
    home['resultA'] = np.select(cond2, cc,default=0)
    home['resultT'] = home['resultH']
    home.resultT[home['AwayTeam'] == team] = home.resultA
    home['TeamRes'] = home['HRes']
    home.TeamRes[home['AwayTeam'] == team ] = home.ARes
    home['team'] = team

    home = home[['Date', 'opponent','ResultHT', 'dateHT','TeamRes', 'resultT','team']]


    return home

def dfWLD1(df):
    home = df
    home['opponent'] = home['HomeTeam']
    home = home[['Date','season','HomeTeam','AwayTeam','GoalsHome','GoalsAway', 'opponent']]
    home['dateHT'] = home['Date'].dt.strftime('%d-%m-%y').astype(str)
    home['ResultHT'] = home['HomeTeam'] + ' '+ home['GoalsHome'].astype(str) + ':'  + home['GoalsAway'].astype(str) + ' ' + home['AwayTeam']
    home['dateHT'] = home['Date'].dt.strftime('%d-%m-%y').astype(str)
    
    #create conditions to compare the scores
    cond1 = [ (home['GoalsHome'] > home['GoalsAway']), (home['GoalsHome'] < home['GoalsAway']), (home['GoalsHome'] == home['GoalsAway'])]
    cond2 = [ (home['GoalsAway'] > home['GoalsHome']), (home['GoalsAway'] < home['GoalsHome']), (home['GoalsAway'] == home['GoalsHome'])]

    #choices result and points
    cc = ['W','L','D']
    ccp = [3,0,1]
    #team = home.team.values[0]

    #adding new columns for results
    home['HRes'] = np.select(cond1, ccp, default=0 )
    home['ARes'] = np.select(cond2, ccp, default=0 )
    home['resultH'] = np.select(cond1, cc, default=0)
    home['resultA'] = np.select(cond2, cc,default=0)
    
    return home


def tableDF(df, season):
    df = dfWLD1(df[df['season'] == season])
    df.dropna()
    #df = df[df['season'] == season]
    df1 = pd.DataFrame()
    #df1 = df
    df1['Home'] = df.groupby('HomeTeam')['HRes'].sum()
    df1['HW'] = df[df['HRes']== 3].groupby('HomeTeam')['HRes'].count()
    df1['HD'] = df[df['HRes']== 1].groupby('HomeTeam')['HRes'].count()
    df1['HL'] = df[df['HRes']== 0].groupby('HomeTeam')['HRes'].count()
    df1['HGames'] = df1['HW'] + df1['HD'] + df1['HL']
    df1['HGF'] = df.groupby('HomeTeam')['GoalsHome'].sum()
    df1['HGA'] = df.groupby('HomeTeam')['GoalsAway'].sum()
    df1['HGD'] = df1['HGF'] - df1['HGA']



    df1['Away'] = df.groupby('AwayTeam')['ARes'].sum()
    df1['AW'] = df[df['ARes']== 3].groupby('AwayTeam')['ARes'].count()
    df1['AD'] = df[df['ARes']== 1].groupby('AwayTeam')['ARes'].count()
    df1['AL'] = df[df['ARes']== 0].groupby('AwayTeam')['ARes'].count()
    df1['AGames'] = df1['AW'] + df1['AD'] + df1['AL']

    df1['AGF'] = df.groupby('AwayTeam')['GoalsAway'].sum()
    df1['AGA'] = df.groupby('AwayTeam')['GoalsHome'].sum()
    df1['AGD'] = df1['AGF'] - df1['AGA']


    df1['W'] = df1['HW'] + df1['AW'] 
    df1['D'] = df1['HD'] + df1['AD'] 
    df1['L'] = df1['HL'] + df1['AL']
    df1['Games'] = df1['W'] + df1['D'] + df1['L']
    df1['GF'] = df1['HGF'] + df1['AGF']
    df1['GA'] = df1['HGA'] + df1['AGA']
    df1['GD'] = df1['GF'] - df1['GA']
    #df1['nGames'] = df1[['W','D','L']].count()


    df1['Points'] = df1['Home'] + df1['Away']
    df1 = df1.sort_values(['Points', 'GD','W'], ascending=[False, False, False])
    df1 = df1.reset_index()
    #dfT19 = dfT19.index =+1
    #df1.columns[1] = ['Rank']


    df1.index = range(1,len(df1.index)+1)
    df1 = df1.reset_index()
    #df1.dropna(inplace=True)
    df1.fillna(method='ffill', inplace=True)
    #df1.dropna(inplace=True)
    df1.iloc[:,2:] = df1.iloc[:,2:].astype(int)

    #df1.asof(df1.isnull()[-1], subset=['HW','W'])
    dfO = df1[['HomeTeam','Games','W','D','L','GF','GA','GD','Points']]
    dfO.sort_values(by=['Points','GD'], inplace=True, ascending=False)
    dfO.reset_index(inplace=True)
    dfO['n'] = range(1, len(dfO.index) + 1)
    srcO = ColumnDataSource(dfO)
    
    
    
    dfH = df1[['HomeTeam','HGames','HW','HD','HL','HGF','HGA','HGD','Home']]
    dfH.sort_values(by=['Home','HGD'], inplace=True, ascending=False)
    dfH.reset_index(inplace=True)
    dfH['n'] = range(1, len(dfH.index) + 1)
    srcCS = ColumnDataSource(dfH)
    
    dfA = df1[['HomeTeam','AGames','AW','AD','AL','AGF','AGA','AGD','Away']]
    dfA.sort_values(by=['Away','AGD'], inplace=True, ascending=False)
    dfA.reset_index(inplace=True)
    dfA['n'] = range(1, len(dfA.index) + 1)
    srcCA = ColumnDataSource(dfA)
    
    cCO = [
        TableColumn(field='n', title='#', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HomeTeam', title='team', formatter=StringFormatter(text_align='center')),
        TableColumn(field='Games', title='MP', formatter=StringFormatter(text_align='center')),
        TableColumn(field='W', title='W', formatter=StringFormatter(text_align='center')),
        TableColumn(field='D', title='D', formatter=StringFormatter(text_align='center')),
        TableColumn(field='L', title='L', formatter=StringFormatter(text_align='center')),
        TableColumn(field='GF', title='GF', formatter=StringFormatter(text_align='center')),  
        TableColumn(field='GA', title='GA', formatter=StringFormatter(text_align='center')),
        TableColumn(field='GD', title='GD', formatter=StringFormatter(text_align='center')),
        TableColumn(field='Points', title='Pts', formatter=StringFormatter(text_align='center'))
    ]
    tableCO = DataTable(source=srcO, columns=cCO, index_position=None, width=400, height=550, autosize_mode='fit_columns', align='center')

    
    
    cCS = [
        TableColumn(field='n', title='#', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HomeTeam', title='team', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HGames', title='MP', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HW', title='W', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HD', title='D', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HL', title='L', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HGF', title='GF', formatter=StringFormatter(text_align='center')),  
        TableColumn(field='HGA', title='GA', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HGD', title='GD', formatter=StringFormatter(text_align='center')),
        TableColumn(field='Home', title='Pts', formatter=StringFormatter(text_align='center'))
    ]
    tableCS = DataTable(source=srcCS, columns=cCS, index_position=None, width=400, height=550, autosize_mode='fit_columns', align='center')

    cCA = [
        TableColumn(field='n', title='#', formatter=StringFormatter(text_align='center')),
        TableColumn(field='HomeTeam', title='team', formatter=StringFormatter(text_align='center')),
        TableColumn(field='AGames', title='MP', formatter=StringFormatter(text_align='center')),
        TableColumn(field='AW', title='W', formatter=StringFormatter(text_align='center')),
        TableColumn(field='AD', title='D', formatter=StringFormatter(text_align='center')),
        TableColumn(field='AL', title='L', formatter=StringFormatter(text_align='center')),
        TableColumn(field='AGF', title='GF', formatter=StringFormatter(text_align='center')),  
        TableColumn(field='AGA', title='GA', formatter=StringFormatter(text_align='center')),
        TableColumn(field='AGD', title='GD', formatter=StringFormatter(text_align='center')),
        TableColumn(field='Away', title='Pts', formatter=StringFormatter(text_align='center'))
    ]
    tableCA = DataTable(source=srcCA, columns=cCA, index_position=None, width=400, height=550, autosize_mode='fit_columns', align='center')

    cOverall = Panel(child=tableCO, title='Overall')
    cHome = Panel(child=tableCS, title='Home')
    cAway = Panel(child=tableCA, title='Away')
    
    tabs = Tabs(tabs=[cOverall, cHome, cAway])
    
    return tabs


  

def tableTeamAbySeason(df, team, season):
    team , season = str(team), int(season)
    home = df[(df['HomeTeam']== team ) & (df['season']==season) | (df['AwayTeam']== team ) & (df['season']==season)]
    #away = df[(df['AwayTeam']== team ) & (df['season']==season) | (df['AwayTeam']== team ) & (df['season']==season)]
    cond1 = [ (home['GoalsHome'] > home['GoalsAway']), (home['GoalsHome'] < home['GoalsAway']), (home['GoalsHome'] == home['GoalsAway'])]
    cond2 = [ (home['GoalsAway'] > home['GoalsHome']), (home['GoalsAway'] < home['GoalsHome']), (home['GoalsAway'] == home['GoalsHome'])]

    #choices result and points   
    ccp = [3,0,1]

    #adding new columns for results
    home['HRes'] = np.select(cond1, ccp, default=0)
    home['ARes'] = np.select(cond2, ccp, default=0)

    
    condT = [(home['HomeTeam'] == team ), (home['HomeTeam'] != team)]
    ccT = [home['HRes'], home['ARes']]

    home['teamPoints'] = np.select(condT, ccT)
    home['totalPoints'] = home['teamPoints'].cumsum()
    home['opponent'] = home['HomeTeam']
    home.opponent[home['opponent'] == team ] = home.AwayTeam + '*'
    home['team'] = team
    home = home[['Date','season','HomeTeam','AwayTeam','GoalsHome','GoalsAway','teamPoints','totalPoints','opponent', 'team']]
    home['ResultHT'] = home['HomeTeam'] + ' '+ home['GoalsHome'].astype(str) + ':'  + home['GoalsAway'].astype(str) + ' ' + home['AwayTeam']
    home['dateHT'] = home['Date'].dt.strftime('%d-%m-%y').astype(str)
    return home



def tableTeamA(df, team):
    #df = df[df['season'] == season]
    team = str(team)
    home = df[(df['HomeTeam']== team ) | (df['AwayTeam']== team )]
    #away = df[(df['AwayTeam']== team ) & (df['season']==season) | (df['AwayTeam']== team ) & (df['season']==season)]
    cond1 = [ (home['GoalsHome'] > home['GoalsAway']), (home['GoalsHome'] < home['GoalsAway']), (home['GoalsHome'] == home['GoalsAway'])]
    cond2 = [ (home['GoalsAway'] > home['GoalsHome']), (home['GoalsAway'] < home['GoalsHome']), (home['GoalsAway'] == home['GoalsHome'])]

    #choices result and points   
    ccp = [3,0,1]
    cc = ['W','L','D']

    #adding new columns for results
    home['HRes'] = np.select(cond1, ccp, default=0)
    home['ARes'] = np.select(cond2, ccp, default=0)
    home['resultH'] = np.select(cond1, cc, default=0)
    home['resultA'] = np.select(cond2, cc,default=0)
    home['resultT'] = home['resultH']
    home.resultT[home['AwayTeam'] == team] = home.resultA
    home['TeamRes'] = home['HRes']
    home.TeamRes[home['AwayTeam'] == team ] = home.ARes

    
    condT = [(home['HomeTeam'] == team ), (home['HomeTeam'] != team)]
    ccT = [home['HRes'], home['ARes']]
    
    

    home['teamPoints'] = np.select(condT, ccT)
    home['totalPoints'] = home.groupby('season')['teamPoints'].transform(pd.Series.cumsum)
    home['team'] = team
    home['opponent'] = home['HomeTeam']
    home.opponent[home['opponent'] == team ] = home.AwayTeam + '*'
    home = home[['Date','season','HomeTeam','AwayTeam','GoalsHome','GoalsAway','teamPoints', 'resultT','TeamRes', 'totalPoints','opponent','team','HS', 'AS', 'HST', 'AST','HF', 'AF', 'HY', 'AY', 'HR', 'AR', 'HC', 'AC']]
    home['ResultHT'] = home['HomeTeam'] + ' '+ home['GoalsHome'].astype(str) + ':'  + home['GoalsAway'].astype(str) + ' ' + home['AwayTeam']
    home['dateHT'] = home['Date'].dt.strftime('%d-%m-%y').astype(str)
    
    return home



def teamWLD(df, team, season):
    team , season = str(team), int(season)
    home = df[(df['HomeTeam']== team ) & (df['season']==season) | (df['AwayTeam']== team ) & (df['season']==season)]
    #away = df[(df['AwayTeam']== team ) & (df['season']==season) | (df['AwayTeam']== team ) & (df['season']==season)]
    
    home['opponent'] = home['HomeTeam']
    home.opponent[home['opponent'] == team ] = home.AwayTeam + '*'
    #home = home[['season','HomeTeam','AwayTeam','GoalsHome','GoalsAway','teamPoints','totalPoints','opponent']]
    home = home[['Date','season','HomeTeam','AwayTeam','GoalsHome','GoalsAway', 'opponent']]
    home['ResultHT'] = home['HomeTeam'] + ' '+ home['GoalsHome'].astype(str) + ':'  + home['GoalsAway'].astype(str) + ' ' + home['AwayTeam']
    home['dateHT'] = home['Date'].dt.strftime('%d-%m-%y').astype(str)
    
    #create conditions to compare the scores
    cond1 = [ (home['GoalsHome'] > home['GoalsAway']), (home['GoalsHome'] < home['GoalsAway']), (home['GoalsHome'] == home['GoalsAway'])]
    cond2 = [ (home['GoalsAway'] > home['GoalsHome']), (home['GoalsAway'] < home['GoalsHome']), (home['GoalsAway'] == home['GoalsHome'])]

    #choices result and points
    cc = ['W','L','D']
    ccp = [3,0,1]

    #adding new columns for results
    home['HRes'] = np.select(cond1, ccp, default=0 )
    home['ARes'] = np.select(cond2, ccp, default=0 )
    home['resultH'] = np.select(cond1, cc, default=0)
    home['resultA'] = np.select(cond2, cc,default=0)
    home['resultT'] = home['resultH']
    home.resultT[home['AwayTeam'] == team] = home.resultA
    home['TeamRes'] = home['HRes']
    home.TeamRes[home['AwayTeam'] == team ] = home.ARes

    home = home[['HomeTeam','AwayTeam','Date', 'opponent','ResultHT', 'dateHT','TeamRes', 'resultT','season','GoalsAway','GoalsHome']]


    return home


   
league1 = ['Barclays Premier League', 'English League Championship', 'French Ligue 1', 'French Ligue 2','Spanish Primera Division', 'Spanish Segunda Division','Italy Serie A',  'Italy Serie B','German Bundesliga', 'German 2. Bundesliga','UEFA Champions League',  'UEFA Europa League','Brasileiro Série A', 'Russian Premier Liga', 'Austrian T-Mobile Bundesliga', 'Swiss Raiffeisen Super League', 'Danish SAS-Ligaen','Belgian Jupiler League' ]



def dfWinS(df):
    df['streak2'] = (df['TeamRes'] == 3).cumsum()
    df['cumsum'] = np.nan
    df.loc[df['TeamRes'] != 3, 'cumsum'] = df['streak2']
    df['cumsum'] = df['cumsum'].fillna(method='ffill')
    df['cumsum'] = df['cumsum'].fillna(0)
    df['streak'] = df['streak2'] - df['cumsum']
    #df['streak'] = df['streak2'].astype(int)
    df.drop(['streak2', 'cumsum'], axis=1, inplace=True)
    maxS = int(df['streak'].nlargest(1))
    maxIdx = df['streak'].idxmax() +1
    df = df.iloc[maxIdx-maxS:maxIdx,:]
    df['n'] = range(1, maxS + 1)
    
    srcCS = ColumnDataSource(df)
    cCS = [
    TableColumn(field='n', title='#', formatter=StringFormatter(text_align='center')),
    TableColumn(field='ResultHT', title='Longest win streak', formatter=StringFormatter(text_align='center')),
    TableColumn(field='dateHT', title='date', formatter=StringFormatter(text_align='center'))
        
    ]
    tableCS = DataTable(source=srcCS, columns=cCS, index_position=None, width=355, height=135, autosize_mode='fit_columns', align='center')
    return tableCS

def dfLS(df):
    df['streak2'] = (df['TeamRes'] == 0).cumsum()
    df['cumsum'] = np.nan
    df.loc[df['TeamRes'] != 0, 'cumsum'] = df['streak2']
    df['cumsum'] = df['cumsum'].fillna(method='ffill')
    df['cumsum'] = df['cumsum'].fillna(0)
    df['streak'] = df['streak2'] - df['cumsum']
    df.reset_index(inplace=True)

    #df['streak'] = df['streak2'].astype(int)
    df.drop(['streak2', 'cumsum'], axis=1, inplace=True)
    maxS = int(df['streak'].nlargest(1))
    maxIdx = df['streak'].idxmax() +1
    df = df.iloc[maxIdx-maxS:maxIdx,:]
    df['n'] = range(1, maxS + 1)
    
    srcCS = ColumnDataSource(df)
    cCS = [
    TableColumn(field='n', title='#', formatter=StringFormatter(text_align='center')),
    TableColumn(field='ResultHT', title='Longest loss streak', formatter=StringFormatter(text_align='center')),
    TableColumn(field='dateHT', title='date', formatter=StringFormatter(text_align='center'))]
    tableCS = DataTable(source=srcCS, columns=cCS, index_position=None, width=355, height=135, autosize_mode='fit_columns', align='center')
    
    return tableCS


def dfDS(df):
    #df = df[['Date','opponent','ResultHT','dateHT','TeamRes','resultT']]
    df['streak2'] = (df['TeamRes'] == 1).cumsum()
    df['cumsum'] = np.nan
    df.loc[df['TeamRes'] != 1, 'cumsum'] = df['streak2']
    df['cumsum'] = df['cumsum'].fillna(method='ffill')
    df['cumsum'] = df['cumsum'].fillna(0)
    df['streak'] = df['streak2'] - df['cumsum']
    #df['streak'] = df['streak2'].astype(int)
    df.reset_index(drop=True, inplace=True)

    df.drop(['streak2', 'cumsum'], axis=1, inplace=True)
    maxS = int(df['streak'].nlargest(1))
    maxIdx = df['streak'].idxmax() +1
    #df = df[['ResultHT', 'dateHT']]

    df = df.iloc[maxIdx-maxS:maxIdx,:]
    df['n'] = range(1, maxS + 1)
    
    srcCS = ColumnDataSource(df)
    cCS = [
    TableColumn(field='n', title='#', formatter=StringFormatter(text_align='center')),
    TableColumn(field='ResultHT', title='Longest draw streak', formatter=StringFormatter(text_align='center')),
    TableColumn(field='dateHT', title='date', formatter=StringFormatter(text_align='center'))
        
    ]
    tableCS = DataTable(source=srcCS, columns=cCS, index_position=None, width=355, height=135, autosize_mode='fit_columns', align='center')
    return tableCS

def CleanSheet(df, team, season):
    df = df[(df['HomeTeam'] == team) & (df['season'] == season)]
    df1 = df[(df['AwayTeam'] == team) & (df['season'] == season)]
    csH = df[df['GoalsAway'] == 0]
    csA = df1[df1['GoalsHome'] == 0]
    cs = csH.append(csA)
    cs = cs.sort_values('Date')
    cs = cs[['ResultHT', 'dateHT']]
    #cs.reset_index(inplace=True)
    cs['n'] = range(1, len(cs.index) + 1)
    srcCS = ColumnDataSource(cs)
    cCS = [
        TableColumn(field='n', title='#', formatter=StringFormatter(text_align='center')),
        TableColumn(field='ResultHT', title='Clean sheets', formatter=StringFormatter(text_align='center')),
    TableColumn(field='dateHT', title='date', formatter=StringFormatter(text_align='center'))
        
    ]
    tableCS = DataTable(source=srcCS, columns=cCS, index_position=None, width=355, height=135, autosize_mode='fit_columns', align='center')
    return tableCS

def sheets(df, team, season):
    teamA = teamWLD(df, team, season)
    lst = dfLS(teamA)
    wst = dfWinS(teamA)
    dst = dfDS(teamA)
    cst = CleanSheet(teamA, team, season)
    st =  row([wst, cst])
    st1 = row([dst, lst])
    st2 = column([st, st1])
    return st2

#

def AxBsumm(df, teamA, teamB):
    df = df[(df['HomeTeam'] == teamA) & (df['AwayTeam'] == teamB) | (df['HomeTeam'] == teamB) & (df['AwayTeam'] == teamA) ]
    df['ResultHT'] = df['HomeTeam'] + ' '+ df['GoalsHome'].astype(str) + ':'  + df['GoalsAway'].astype(str) + ' ' + df['AwayTeam']
    df['dateHT'] = df['Date'].dt.strftime('%d-%m-%y').astype(str)
    #create conditions to compare the scores
    cond1 = [ (df['GoalsHome'] > df['GoalsAway']), (df['GoalsHome'] < df['GoalsAway']), (df['GoalsHome'] == df['GoalsAway'])]
    cond2 = [ (df['GoalsAway'] > df['GoalsHome']), (df['GoalsAway'] < df['GoalsHome']), (df['GoalsAway'] == df['GoalsHome'])]

    #choices result and points
    cc = ['W','L','D']
    ccp = [3,0,1]

    #adding new columns for results
    df['HRes'] = np.select(cond1, ccp, default=0 )
    df['ARes'] = np.select(cond2, ccp, default=0 )
    df['resultH'] = np.select(cond1, cc, default=0)
    df['resultA'] = np.select(cond2, cc,default=0)
    
    
    df['team'] = teamA
    df['teamA_res'] = None
    #df.teamA_res = df[(df['HomeTeam'] == teamA) | (df['AwayTeam'] == teamA)][['resultH','resultA']]
    df.teamA_res[df['HomeTeam'] == teamA] = df.resultH
    df.teamA_res[df['AwayTeam'] == teamA] = df.resultA
    
    df['teamB_res'] = None
    df.teamB_res[df['HomeTeam'] == teamB] = df.resultH
    df.teamB_res[df['AwayTeam'] == teamB] = df.resultA
    
    df['teamA_SO'] = None
    df.teamA_SO[df['HomeTeam'] == teamA] = df['HS']
    df.teamA_SO[df['AwayTeam'] == teamA] = df['AS']
    df['teamA_SO'] = df['teamA_SO'].astype(int)
    
    df['teamB_SO'] = None
    df.teamB_SO[df['HomeTeam'] == teamB] = df['HS']
    df.teamB_SO[df['AwayTeam'] == teamB] = df['AS']
    
    df['teamA_ST'] = None
    df.teamA_ST[df['HomeTeam'] == teamA] = df['HST']
    df.teamA_ST[df['AwayTeam'] == teamA] = df['AST']
    
    df['teamB_ST'] = None
    df.teamB_ST[df['HomeTeam'] == teamB] = df['HST']
    df.teamB_ST[df['AwayTeam'] == teamB] = df['AST']
    
    df['teamA_G'] = None
    df.teamA_G[df['HomeTeam'] == teamA] = df['GoalsHome']
    df.teamA_G[df['AwayTeam'] == teamA] = df['GoalsAway']
    
    df['teamB_G'] = None
    df.teamB_G[df['HomeTeam'] == teamB] = df['GoalsHome']
    df.teamB_G[df['AwayTeam'] == teamB] = df['GoalsAway']
    
    df['teamA_F'] = None
    df.teamA_F[df['HomeTeam'] == teamA] = df['HF']
    df.teamA_F[df['AwayTeam'] == teamA] = df['AF']
    
    df['teamB_F'] = None
    df.teamB_F[df['HomeTeam'] == teamB] = df['HF']
    df.teamB_F[df['AwayTeam'] == teamB] = df['AF']
    
    df['teamA_Y'] = None
    df.teamA_Y[df['HomeTeam'] == teamA] = df['HY']
    df.teamA_Y[df['AwayTeam'] == teamA] = df['AY']
    
    df['teamB_Y'] = None
    df.teamB_Y[df['HomeTeam'] == teamB] = df['HY']
    df.teamB_Y[df['AwayTeam'] == teamB] = df['AY']
    
    df['teamA_R'] = None
    df.teamA_R[df['HomeTeam'] == teamA] = df['HR']
    df.teamA_R[df['AwayTeam'] == teamA] = df['AR']
    
    df['teamB_R'] = None
    df.teamB_R[df['HomeTeam'] == teamB] = df['HR']
    df.teamB_R[df['AwayTeam'] == teamB] = df['AR']
    
    df['teamA_C'] = None
    df.teamA_C[df['HomeTeam'] == teamA] = df['HC']
    df.teamA_C[df['AwayTeam'] == teamA] = df['AC']
    
    df['teamB_C'] = None
    df.teamB_C[df['HomeTeam'] == teamB] = df['HC']
    df.teamB_C[df['AwayTeam'] == teamB] = df['AC']

    
    
    df.drop(['resultH','resultA', 'HRes','ARes','HS','AS','HST','AST', 'HF', 'AF', 'HC','AC','HY','AY','HR','AR'],1, inplace=True)
    df.iloc[: ,19:] = df.iloc[: ,19:].astype(int)

    

    return df

def AxBfigures(df, teamA, teamB):
    
    dictMF = {'shotOff*': [df['teamA_SO'].median(), df['teamB_SO'].median()],
         'shotTarget*': [df['teamA_ST'].median(), df['teamB_ST'].median()],
         'goals':[df['teamA_G'].sum(), df['teamB_G'].sum()],
         'fouls*' : [df['teamA_F'].median(), df['teamB_F'].median()],
         'yellowC': [df['teamA_Y'].sum(), df['teamB_Y'].sum()],
         'redC': [df['teamA_R'].sum(), df['teamB_R'].sum()],
         'corners*': [df['teamA_C'].median(), df['teamB_C'].median()]}

    dfMF = pd.DataFrame(dictMF, index=[teamA,teamB])
    dfMF.iloc[:,:] = dfMF.iloc[:,:].astype(int)
    #dfMF.reset_index(inplace=True)

    
    return dfMF.T


def figAxB_plot(df, teamA, teamB):
    df = AxBfigures(df, teamA, teamB)
    
    #df.reset_index(inplace=True)
    #df.columns = ['x',teamA, teamB]

    xrange = 'shots off*', 'shots target*', 'goals', 'fouls*', 'yellow cards', 'red cards', 'corners'
    srcTF = ColumnDataSource(data=dict(x=xrange, y=df[teamA], y1=df[teamB]))

    pTF = figure(x_range=FactorRange(*xrange), plot_height=350, plot_width=540, tools='pan, wheel_zoom, box_zoom, reset',
                 title= teamA + ' vs ' + teamB)

    pTF.vbar(x=dodge( 'x', -.25, range=pTF.x_range), top='y', width=.2, color= '#2c7fb8', source=srcTF, legend_label=teamA)
    pTF.vbar(x=dodge('x', .0, range=pTF.x_range), top='y1', width=.2, color='#fee08b', source=srcTF, legend_label=teamB)


    pTF.y_range.start = 0
    pTF.grid.grid_line_alpha = 0.8
    pTF.grid.grid_line_dash = 'dotted'
    pTF.grid.grid_line_dash_offset = 5
    pTF.grid.grid_line_width = 2
    pTF.axis.major_label_text_font_style = 'bold'
    pTF.title.text_font_size = '17px'
    pTF.outline_line_color=None
    pTF.toolbar.autohide = True

    hTF= HoverTool()
    hTF.tooltips=[('type', '@x'),(teamA,'@y'), (teamB,'@y1')]
    pTF.add_tools(hTF)

    pTF.legend.location= 'top_right'#(370,180)
    pTF.legend.background_fill_alpha=None
    pTF.legend.border_line_color = None

    pTF.legend.click_policy="hide"
    pTF.legend.orientation = 'horizontal'
    pTF.legend.title = '↓ Disable/Enable'

    pTF.legend.border_line_color = None
    pTF.y_range.end = df.max(axis=1).max() *1.35

    lTF = Label(x=10, y=260, x_units='screen', y_units='screen', 
                            text='*', render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='left', angle=0, text_alpha=1, text_font_style='bold')
    pTF.add_layout(lTF)

    lTF1 = Label(x=20, y=268, x_units='screen', y_units='screen', 
                            text='median figures', render_mode='css', text_font_size='7.5pt', text_color='#2c7fb8',
                            text_align='left', angle=0, text_alpha=1, text_font_style='bold')
    pTF.add_layout(lTF1)
    
    return pTF
    

def xPlus1(df):
    l = [[1]* 1] * len(df.index)
    newL = []
    newL.insert(0,1)
    cumsum = 1
    for x in l:
        cumsum += 2
        newL.append(cumsum)
    return newL



def rectPlot1(df, teamA, teamB):

    lr = df['teamA_res'].values[-5:]
    #lr = ['L', 'L', 'W', 'W', 'W', 'D', 'W', 'W', 'W',teamA_res 'W']
    x = xPlus1(df[-5:])
    mapper = CategoricalColorMapper(palette=['#7fcdbb', '#feb24c','#ffeda0'], factors=['W','L','D'])


    # instantiating the figure object 
    pR = figure(match_aspect = True, y_range=[0,2], x_range=(0,(x[-1]+1)), plot_height=180, plot_width=250) 

    # the points to be plotted 
    y = [1] * len(x)
    w = [1.9] * len(x)
    h = [.5] * len(x)



    pR.x_range.start=0
    # plotting the graph 

    srcR = ColumnDataSource(data=dict(x=x, y=y, w=w, h=h, l=lr, r=df['ResultHT'][-5:], d=df['dateHT'][-5:]))
    pR.rect(x='x', y='y', width='w', height='h',
               line_color='white', line_width=.7,
              color={'field':'l','transform':mapper}, source=srcR,
              hover_fill_alpha=0.7, hover_fill_color='#2c7fb8')
              #hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='lightblue')#, legend_field='l') 

    lRec = LabelSet(x='x', y='y',text='l', level='overlay', text_font_size='11pt', text_font_style='bold',
                x_offset=-8, y_offset=-10, source=srcR, render_mode='canvas', text_alpha=.5)
    pR.add_layout(lRec)

    gH= HoverTool()
    gH.tooltips=[('outcome', '@l'),('score','@r'),('date','@d')]
    pR.add_tools(gH)

    gL = Label(x=15, y=125, x_units='screen', y_units='screen', 
                            text=teamA, render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='left', angle=0, text_alpha=1, text_font_style='bold')
    pR.add_layout(gL)
    


    #remove grid lines
    pR.axis.axis_label=None
    pR.axis.visible=False
    pR.grid.grid_line_color = None
    pR.outline_line_color=None
    pR.toolbar.autohide = True
    
    lr1 = df['teamB_res'].values[-5:]
    x1 = xPlus1(df[-5:])
    mapper1 = CategoricalColorMapper(palette=['#7fcdbb', '#feb24c','#ffeda0'], factors=['W','L','D'])


    # instantiating the figure object 
    pR1 = figure(match_aspect = True, y_range=[0,2], x_range=(0,(x[-1]+1)), plot_height=180, plot_width=250) 

    # the points to be plotted 
    y1 = [1] * len(x)
    w1 = [1.9] * len(x)
    h1 = [.5] * len(x)



    pR1.x_range.start=0
    # plotting the graph 

    srcR1 = ColumnDataSource(data=dict(x=x1, y=y1, w=w1, h=h, l=lr1, r=df['ResultHT'][-5:], d=df['dateHT'][-5:]))
    pR1.rect(x='x', y='y', width='w', height='h',
               line_color='white', line_width=.7,
              color={'field':'l','transform':mapper1}, source=srcR1,
              hover_fill_alpha=0.7, hover_fill_color='#2c7fb8')
              #hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='lightblue')#, legend_field='l')
    #pR1.line(x=50, y=100, line_width=2.5, line_color='black', source=srcR1)

    lRec1 = LabelSet(x='x', y='y',text='l', level='overlay', text_font_size='11pt', text_font_style='bold',
                x_offset=-8, y_offset=-10, source=srcR1, render_mode='canvas', text_alpha=.5)
    pR1.add_layout(lRec1)

    gH1= HoverTool()
    gH1.tooltips=[('outcome', '@l'),('score','@r'),('date','@d')]
    pR1.add_tools(gH1)

    gL1 = Label(x=180, y=125, x_units='screen', y_units='screen', 
                            text=teamB, render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='right', angle=0, text_alpha=1, text_font_style='bold')
    pR1.add_layout(gL1)
    
    gL2 = Label(x=-2, y=50, x_units='screen', y_units='screen', 
                            text='|', render_mode='css', text_font_size='50pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=.7)
    pR1.add_layout(gL2)
    


    #remove grid lines
    pR1.axis.axis_label=None
    pR1.axis.visible=False
    pR1.grid.grid_line_color = None
    pR1.outline_line_color=None
    pR1.toolbar.autohide = True
    #pR1.toolbar_location = 'above'
    
    rT = row([pR, pR1], spacing=-75)



    return rT


def countWLD(df, teamA, teamB):
    
    totalg = {'teams': [teamA, teamB],
          'W': [len(df[df['teamA_res'] == 'W']['teamA_res']), len(df[df['teamB_res'] == 'W']['teamB_res'])],
          'L': [len(df[df['teamA_res'] == 'L']['teamA_res']), len(df[df['teamB_res'] == 'L']['teamB_res'])],
          'D': [len(df[df['teamA_res'] == 'D']['teamA_res']), len(df[df['teamB_res'] == 'D']['teamB_res'])]}

    dftg = pd.DataFrame(totalg, index=range(0,2))
    dftg

    srcStack = ColumnDataSource(dftg)
    pStack = figure(x_range=list(dftg.teams.values), plot_height=350, plot_width=350, title='Past ' + str(dftg.iloc[1,1:].sum()) + ' matches', tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')


    pStack.vbar_stack(['W', 'L','D'], 
                    x='teams', 
                    width=0.35, 
                    color=['#7fcdbb', '#feb24c','#ffeda0'],
                    line_color='white',
                    legend_label=['Win', 'Loss','Draw'],
                    #legend=[x for x in dftg.columns[1:]],
                    source=srcStack)

    pStack.grid.grid_line_alpha = 0.8
    pStack.grid.grid_line_dash = 'dotted'
    pStack.grid.grid_line_dash_offset = 5
    pStack.grid.grid_line_width = 2
    pStack.axis.major_label_text_font_style = 'bold'
    pStack.title.text_font_size = '20px'
    #pR19.xaxis.major_label_orientation = 45
    pStack.outline_line_color=None
    pStack.legend.location= 'top_left'#(370,180)
    pStack.legend.background_fill_alpha=None
    pStack.legend.border_line_color = None
    pStack.legend.orientation = 'horizontal'

    pStack.legend.click_policy="hide"
    pStack.legend.title='↓ Disable/Enable'

    pStack.legend.border_line_color = None
    pStack.legend.background_fill_color=None
    pStack.y_range.start= 0
    pStack.y_range.end = int(dftg.iloc[1,1:].sum() * 1.4) # if int(dftg.iloc[1,1:].sum()) < 4 int(dftg.iloc[1,1:].sum() * 2)]
    pStack.yaxis.ticker.desired_num_ticks = int(dftg.iloc[1,1:].sum())
    pStack.toolbar.autohide = True

    pStack_h= HoverTool()
    pStack_h.tooltips=[('Win', '@W'), ('Loss', '@L'), ('Draw', '@D')]
    pStack.add_tools(pStack_h)
    pStack.y_range.start = 0
    
    return pStack


def mathcStory(df, teamA, teamB):
    df['n'] = range(1, len(df.index)+1)
    srcCS = ColumnDataSource(df)
    cCS = [
        TableColumn(field='n',  title='#', formatter=StringFormatter(text_align='center')),
        TableColumn(field='ResultHT', title= teamA + ' x ' + teamB, formatter=StringFormatter(text_align='center')),
        TableColumn(field='dateHT', title='date', formatter=StringFormatter(text_align='center'))

    ]
    tableCS = DataTable(source=srcCS, columns=cCS, index_position=None, width=350, height=150, autosize_mode='fit_columns')
    return tableCS

def AxBteams(df, teamA, teamB, season):
    dfA, dfB = tableTeamA(df, teamA), tableTeamA(df, teamB)
    dfA, dfB = dfA[dfA['season'] == season], dfB[dfB['season'] == season]
    
    dfA.reset_index(inplace=True)
    dfA.drop('index', 1, inplace=True)
    dfB.reset_index(inplace=True)
    dfB.drop('index', 1, inplace=True)
    
    
    #AxB overall plot
    blues = PuBu
    blues1 = YlGnBu
    xlen = [dfA.index, dfB.index]
    xInt = max(map(len, xlen))
    xran = range(1, xInt+1)
    xm1 = list(map(str, xran))
    
    src = ColumnDataSource(data=dict(x=xm1, tA=dfA['totalPoints'], tB=dfB['totalPoints'], tAr=dfA['ResultHT'], tAd=dfA['dateHT'], tBr=dfB['ResultHT'], tBd=dfB['dateHT']))

    pAB = figure(x_range=xm1, plot_height=500, plot_width=800, title=teamA + ' x ' + teamB + ' '+ str(season), tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points', x_axis_label='matches')

    pAB.line(x='x',y='tA', line_width=2.5, line_color=blues[6][0], source=src, legend_label=teamA)
    pAB.circle(x='x',y='tA', line_color='black', color=blues1[6][2], size=5, source=src, legend_label=teamA)

    pAB.line(x='x',y='tB', line_width=2.5, line_color=blues[6][3], source=src, legend_label=teamB)
    pAB.circle(x='x',y='tB', line_color='black', color=blues1[6][3], size=5, source=src, legend_label=teamB)
    
    pAB.y_range.start = -1
    
    pAB.grid.grid_line_alpha = 0.8
    pAB.grid.grid_line_dash = 'dotted'
    pAB.grid.grid_line_dash_offset = 5
    pAB.grid.grid_line_width = 2
    pAB.axis.major_label_text_font_style = 'bold'
    pAB.title.text_font_size = '20px'
    #pR19.xaxis.major_label_orientation = 45
    pAB.outline_line_color=None
    pAB.legend.location= 'top_left'#(370,180)
    pAB.legend.background_fill_alpha=None
    pAB.legend.border_line_color = None

    pAB.legend.click_policy="hide"
    pAB.legend.title='↓ Disable/Enable'

    pAB.legend.border_line_color = None
    pAB.legend.background_fill_color=None
    
    pAB_h= HoverTool()
    pAB_h.tooltips=[(teamA, '@tA'), ('', '@tAr'), ('', '@tAd'),(teamB,'@tB'), ('', '@tBr'),('','@tBd')]
    pAB.add_tools(pAB_h)
    pAB.yaxis.ticker.desired_num_ticks = 18
    pAB.toolbar.autohide = True
    
    
    #AxB home plot
    dfAH, dfBH = dfA[dfA['HomeTeam'] == teamA], dfB[dfB['HomeTeam'] == teamB]
    
    xh = [dfAH.index, dfBH.index]
    xhI = max(map(len, xh))
    xhr = range(1, xhI+1)
    xrm = list(map(str, xhr))
    
    srcH = ColumnDataSource(data=dict(x=xrm, tAh=dfAH['TeamRes'].cumsum(), tBh=dfBH['TeamRes'].cumsum(), tArh=dfAH['ResultHT'], tAdh=dfAH['dateHT'], tBrh=dfBH['ResultHT'], tBdh=dfBH['dateHT']))

    pABH = figure(x_range=xrm, plot_height=500, plot_width=800, title=teamA + ' x ' + teamB + ' - home', tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points', x_axis_label='matches')

    pABH.line(x='x',y='tAh', line_width=2.5, line_color=blues[6][0], source=srcH, legend_label=teamA)
    pABH.circle(x='x',y='tAh', line_color='black', color=blues1[6][2], size=5, source=srcH, legend_label=teamA)

    pABH.line(x='x',y='tBh', line_width=2.5, line_color=blues[6][3], source=srcH, legend_label=teamB)
    pABH.circle(x='x',y='tBh', line_color='black', color=blues1[6][3], size=5, source=srcH, legend_label=teamB)
    
    pABH.y_range.start = -1
    pABH.grid.grid_line_alpha = 0.8
    pABH.grid.grid_line_dash = 'dotted'
    pABH.grid.grid_line_dash_offset = 5
    pABH.grid.grid_line_width = 2
    pABH.axis.major_label_text_font_style = 'bold'
    pABH.title.text_font_size = '20px'
    #pR19.xaxis.major_label_orientation = 45
    pABH.outline_line_color=None
    pABH.legend.location= 'top_left'#(370,180)
    pABH.legend.background_fill_alpha=None
    pABH.legend.border_line_color = None

    pABH.legend.click_policy="hide"
    pABH.legend.title='↓ Disable/Enable'

    pABH.legend.border_line_color = None
    pABH.legend.background_fill_color=None
    
    pht= HoverTool()
    pht.tooltips=[(teamA, '@tAh'), ('', '@tArh'), ('', '@tAdh'),(teamB,'@tBh'), ('', '@tBrh'),('','@tBdh')]
    pABH.add_tools(pht)
    pABH.yaxis.ticker.desired_num_ticks = 12
    pABH.toolbar.autohide = True
    
    #AxB away plot
    dfAA, dfBA = dfA[dfA['AwayTeam'] == teamA], dfB[dfB['AwayTeam'] == teamB]
    
    xa = [dfAA.index, dfBA.index]
    xaI = max(map(len, xa))
    xar = range(1, xaI+1)
    xam = list(map(str, xar))
    
    srcA = ColumnDataSource(data=dict(x=xam, tAh=dfAA['TeamRes'].cumsum(), tBh=dfBA['TeamRes'].cumsum(), tArh=dfAA['ResultHT'], tAdh=dfAA['dateHT'], tBrh=dfBA['ResultHT'], tBdh=dfBA['dateHT']))

    pABA = figure(x_range=xam, plot_height=500, plot_width=800, title=teamA + ' x ' + teamB + ' - away', tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points', x_axis_label='matches')

    pABA.line(x='x',y='tAh', line_width=2.5, line_color=blues[6][0], source=srcA, legend_label=teamA)
    pABA.circle(x='x',y='tAh', line_color='black', color=blues1[6][2], size=5, source=srcA, legend_label=teamA)

    pABA.line(x='x',y='tBh', line_width=2.5, line_color=blues[6][3], source=srcA, legend_label=teamB)
    pABA.circle(x='x',y='tBh', line_color='black', color=blues1[6][3], size=5, source=srcA, legend_label=teamB)
    
    pABA.y_range.start = -1
    pABA.grid.grid_line_alpha = 0.8
    pABA.grid.grid_line_dash = 'dotted'
    pABA.grid.grid_line_dash_offset = 5
    pABA.grid.grid_line_width = 2
    pABA.axis.major_label_text_font_style = 'bold'
    pABA.title.text_font_size = '20px'
    #pR19.xaxis.major_label_orientation = 45
    pABA.outline_line_color=None
    pABA.legend.location= 'top_left'#(370,180)
    pABA.legend.background_fill_alpha=None
    pABA.legend.border_line_color = None

    pABA.legend.click_policy="hide"
    pABA.legend.title='↓ Disable/Enable'

    pABA.legend.border_line_color = None
    pABA.legend.background_fill_color=None
    
    pha= HoverTool()
    pha.tooltips=[(teamA, '@tAh'), ('', '@tArh'), ('', '@tAdh'),(teamB,'@tBh'), ('', '@tBrh'),('','@tBdh')]
    pABA.add_tools(pha)
    pABA.yaxis.ticker.desired_num_ticks = 12
    pABA.toolbar.autohide = True
    
    #plot tabs
    pO = Panel(child=pAB, title='Overall')
    pH = Panel(child=pABH, title='Home')
    pA = Panel(child=pABA, title='Away')
    
    tabs = Tabs(tabs=[pO, pH, pA])
    
    #rect plot
    dfr = AxBsumm(df, teamA, teamB)
    rects = rectPlot1(dfr, teamA, teamB)
    vbarStack = countWLD(dfr, teamA, teamB)
    tableRes = mathcStory(dfr, teamA, teamB)
    figs = figAxB_plot(dfr, teamA, teamB)
    tableC = tableDF(df, season)
    pred = simMatch(df, teamA, teamB)

    c3 = column([rects, tableRes], spacing=-50)
    c3a = column([c3, pred], spacing=-10)
    #r2 = row([tableC, c3])
    r1 = row([vbarStack, figs], spacing=-30)
    c1 = row([c3a, tableC], spacing=-17)
    c2 = column([tabs, r1, c1], spacing=5)
    
    #dC = column([rects, vbarStack], spacing=-40)
    #c1 = column([tableC, tableRes, dC], margin=(0,10,0,10))
    #r1 = row([c1, tabs])#, spacing = 5)
    #c2 = column([r1, figs])

    return c2



def pct(part, whole):
    return round(100 * part/whole, 2)



def xPlus(df):
    l = [[1]* 1] * len(df.index)
    newL = []
    newL.insert(0,1)
    cumsum = 1
    for x in l:
        cumsum += 2
        newL.append(cumsum)
    return newL



def rectPlot(df):

    lr = df['resultT'][-15:].values
    #lr = ['L', 'L', 'W', 'W', 'W', 'D', 'W', 'W', 'W', 'W']
    x = xPlus(df[-15:])
    mapper = CategoricalColorMapper(palette=['#7fcdbb', '#feb24c','#ffeda0'], factors=['W','L','D'])


    # instantiating the figure object 
    pR = figure(match_aspect = True, y_range=[0,2], x_range=(0,(x[-1]+1)), plot_height=180, plot_width=700) 

    # the points to be plotted 
    y = [1] * len(x)
    w = [1.9] * len(x)
    h = [.5] * len(x)



    pR.x_range.start=0
    # plotting the graph 

    srcR = ColumnDataSource(data=dict(x=x, y=y, w=w, h=h, l=lr, r=df['ResultHT'][-15:], d=df['dateHT'][-15:]))
    pR.rect(x='x', y='y', width='w', height='h',
               line_color='white', line_width=.7,
              color={'field':'l','transform':mapper}, source=srcR,
              hover_fill_alpha=0.7, hover_fill_color='#2c7fb8')
              #hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='lightblue')#, legend_field='l') 

    lRec = LabelSet(x='x', y='y',text='l', level='overlay', text_font_size='11pt', text_font_style='bold',
                x_offset=-8, y_offset=-10, source=srcR, render_mode='canvas', text_alpha=.5)
    pR.add_layout(lRec)

    gH= HoverTool()
    gH.tooltips=[('outcome', '@l'),('score','@r'),('date','@d')]
    pR.add_tools(gH)

    gL = Label(x=85, y=125, x_units='screen', y_units='screen', 
                            text='Past 15 matches', render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pR.add_layout(gL)
    
    gL1 = Label(x=620, y=130, x_units='screen', y_units='screen', 
                            text='From 45pts/15pts', render_mode='css', text_font_size='10.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pR.add_layout(gL1)
    
    tpts = str(df['TeamRes'][-15:].sum()) + 'pts/' + str(df['TeamRes'][-5:].sum()) +'pts'
    
    gL2 = Label(x=635, y=110, x_units='screen', y_units='screen', 
                            text= tpts , render_mode='css', text_font_size='10.5pt', text_color='#253494',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pR.add_layout(gL2)



    #remove grid lines
    pR.axis.axis_label=None
    pR.axis.visible=False
    pR.grid.grid_line_color = None
    pR.outline_line_color=None
    pR.toolbar.autohide = True


    return pR


def teamOverall(df, season):
    
    
    team19 = df[df['season']==2019]
    team18 = df[df['season']==2018]
    team17 = df[df['season']==2017]
    teamS = df[df['season'] == season]
    
    xlist = teamS.opponent.tolist()
    b = PuBu
    b1 = YlGnBu
    src = ColumnDataSource(teamS)
    team = str(teamS.team.values[0])
    season1 =  str(teamS.season.values[0])
    
    p = figure(x_range=xlist, plot_height=500, plot_width=800, title=team + ' ' + season1, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points')#, x_axis_label='games')

    p.line(x='opponent',y='totalPoints', line_width=2.5, line_color=b[6][0], source=src)
    p.circle(x='opponent',y='totalPoints', line_color='black', color=b1[6][2], size=5, source=src)
    
    #label
    l1 = Label(x=615, y=-5, x_units='screen', y_units='screen', 
                            text='*', render_mode='css', text_font_size='17.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    l2 = Label(x=670, y=0, x_units='screen', y_units='screen', 
                            text='Home match', render_mode='css', text_font_size='11.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    
    l3 = Label(x=360, y=150, x_units='screen', y_units='screen', 
                            text=team, render_mode='css', text_font_size='74pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=.1, text_font_style='bold')
    
    p.add_layout(l1)
    p.add_layout(l2)
    p.add_layout(l3)
    
    p.grid.grid_line_alpha = 0.8
    p.grid.grid_line_dash = 'dotted'
    p.grid.grid_line_dash_offset = 5
    p.grid.grid_line_width = 2
    p.axis.major_label_text_font_style = 'bold'
    p.title.text_font_size = '25px'
    p.xaxis.major_label_orientation = 45
    p.xaxis.major_label_text_font_size = '10px'
    p.outline_line_color=None
    p.toolbar.autohide = True
    p_h1= HoverTool()
    p_h1.tooltips=[('match', '@ResultHT'),('date','@dateHT'), ('Pts','@totalPoints')]
    p.add_tools(p_h1)
    p.yaxis.ticker.desired_num_ticks = int(teamS['totalPoints'].max() / 3)
    p.y_range.start = -1    
    
    
    #xlist
    #list of opponents season selected
    
    
    blues = PuBu
    blues1 = YlGnBu
    xran = range(1,39)
    xm1 = list(map(str, xran))

    src3 = ColumnDataSource(data=dict(x=xm1, y19d=team19['dateHT'], y19=team19['totalPoints'], y19ht=team19['ResultHT'], y18=team18['totalPoints'], y18ht=team18['ResultHT'], y18d=team18['dateHT'], y17=team17['totalPoints'], y17ht=team17['ResultHT'], y17d=team17['dateHT']))

    p3 = figure(x_range=xm1, plot_height=500, plot_width=800, title=team, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points', x_axis_label='matches')

    p3.line(x='x',y='y19', line_width=2.5, line_color=blues[6][0], source=src3, legend_label='2019')
    p3.circle(x='x',y='y19', line_color='black', color=blues1[6][2], size=5, source=src3, legend_label='2019')

    p3.line(x='x',y='y18', line_width=2.5, line_color=blues[6][2], source=src3, legend_label='2018')
    p3.circle(x='x',y='y18', line_color='black', color=blues1[6][3], size=5, source=src3, legend_label='2018')

    p3.line(x='x',y='y17', line_width=2.5, line_color=blues[6][4], source=src3, legend_label='2017')
    p3.circle(x='x',y='y17', line_color='black', color=blues1[6][5], size=5, source=src3, legend_label='2017')

    p3.grid.grid_line_alpha = 0.8
    p3.grid.grid_line_dash = 'dotted'
    p3.grid.grid_line_dash_offset = 5
    p3.grid.grid_line_width = 2
    p3.axis.major_label_text_font_style = 'bold'
    p3.title.text_font_size = '25px'
    #pR19.xaxis.major_label_orientation = 45
    p3.outline_line_color=None
    p3.legend.location= 'top_left'#(370,180)
    p3.legend.background_fill_alpha=None
    p3.legend.border_line_color = None

    p3.legend.click_policy="hide"
    p3.legend.title='↓ Disable/Enable'

    p3.legend.border_line_color = None
    p3.legend.background_fill_color=None

    p_h3= HoverTool()
    p_h3.tooltips=[('2017', '@y17ht'),('date','@y17d'), ('Pts','@y17'), ('2018', '@y18ht'), ('date','@y18d'), ('Pts','@y18'), ('2019', '@y19ht'),('date','@y19d'), ('Pts','@y19'),]
    p3.add_tools(p_h3)
    p3.yaxis.ticker.desired_num_ticks = 25
    p3.y_range.start = -1
    
    teamHome = teamS[teamS['HomeTeam'] == team]
    teamAway = teamS[teamS['AwayTeam'] == team]
    teamHome['HPts'] = teamHome['teamPoints'].cumsum()
    teamAway['HPts'] = teamAway['teamPoints'].cumsum()

    xlH = teamHome.opponent.tolist()
    xlA = teamAway.opponent.tolist()
    bH = PuBu
    bH1 = YlGnBu
    xlenght = len(xlH) + len(xlA) +1
    xrHA = range(1, 20)
    xHA = list(map(str, xrHA))


    srcTH = ColumnDataSource(teamHome)
    srcTA = ColumnDataSource(teamAway)
    srcTHxA = ColumnDataSource(data=dict(x=xHA, y=teamHome['HPts'], ya=teamHome['ResultHT'], yd=teamHome['dateHT'],
                                         z=teamAway['HPts'], za=teamAway['ResultHT'], zd=teamAway['dateHT'], zp=teamAway['HPts']))

    pH = figure(x_range=xlH, plot_height=500, plot_width=800, title='home', tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points')#, x_axis_label='games')
    pA = figure(x_range=xlA, plot_height=500, plot_width=800, title='away', tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points')#, x_axis_label='games')
    pHxA = figure(x_range=xHA, plot_height=500, plot_width=800, title='home x away', tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', y_axis_label='points')#, x_axis_label='games')


    pH.line(x='opponent',y='HPts', line_width=2.5, line_color=b[6][0], source=srcTH)
    pH.circle(x='opponent',y='HPts', line_color='black', color=b1[6][2], size=5, source=srcTH)

    pA.line(x='opponent',y='HPts', line_width=2.5, line_color=b[6][2], source=srcTA)
    pA.circle(x='opponent',y='HPts', line_color='black', color=b1[6][4], size=5, source=srcTA)

    pHxA.line(x='x',y='y', line_width=2.5, line_color=b[6][0], source=srcTHxA, legend_label='home')
    pHxA.circle(x='x',y='y', line_color='black', color=b1[6][2], size=5, source=srcTHxA, legend_label='home')

    pHxA.line(x='x',y='z', line_width=2.5, line_color=b[6][2], source=srcTHxA, legend_label='away')
    pHxA.circle(x='x',y='z', line_color='black', color=b1[6][4], size=5, source=srcTHxA, legend_label='away')
    
    pH.y_range.start = -1
    pA.y_range.start = -1
    pHxA.y_range.start = -1

    pH.grid.grid_line_alpha = 0.8
    pH.grid.grid_line_dash = 'dotted'
    pH.grid.grid_line_dash_offset = 5
    pH.grid.grid_line_width = 2
    pH.axis.major_label_text_font_style = 'bold'
    pH.title.text_font_size = '20px'
    pH.xaxis.major_label_orientation = 45
    pH.outline_line_color=None
    pH.toolbar.autohide = True

    h_pH= HoverTool()
    h_pH.tooltips=[('match', '@ResultHT'),('date','@dateHT'), ('Pts','@HPts')]
    pH.add_tools(h_pH)
    
    pA.grid.grid_line_alpha = 0.8
    pA.grid.grid_line_dash = 'dotted'
    pA.grid.grid_line_dash_offset = 5
    pA.grid.grid_line_width = 2
    pA.axis.major_label_text_font_style = 'bold'
    pA.title.text_font_size = '20px'
    pA.xaxis.major_label_orientation = 45
    pA.outline_line_color=None
    pA.toolbar.autohide = True

    h_pA= HoverTool()
    h_pA.tooltips=[('match', '@ResultHT'),('date','@dateHT'), ('Pts','@HPts')]
    pA.add_tools(h_pA)
    
    pHxA.grid.grid_line_alpha = 0.8
    pHxA.grid.grid_line_dash = 'dotted'
    pHxA.grid.grid_line_dash_offset = 5
    pHxA.grid.grid_line_width = 2
    pHxA.axis.major_label_text_font_style = 'bold'
    pHxA.title.text_font_size = '20px'
    pHxA.outline_line_color=None
    pHxA.toolbar.autohide = True

    h_pHxA= HoverTool()
    h_pHxA.tooltips=[('home', '@ya'),('date','@yd'), ('Pts','@yp'), ('away', '@za'),('date','@zd'), ('Pts','@zp')]
    pHxA.add_tools(h_pHxA)

    pHxA.legend.location= 'top_left'#(370,180)
    pHxA.legend.background_fill_alpha=None
    pHxA.legend.border_line_color = None

    pHxA.legend.click_policy="hide"
    pHxA.legend.title='↓ Disable/Enable'

    pHxA.legend.border_line_color = None
    pHxA.legend.background_fill_color=None
    

    pH.yaxis.ticker.desired_num_ticks = int(teamHome['HPts'].max() / 3)
    pA.yaxis.ticker.desired_num_ticks = int(teamAway['HPts'].max() / 3)
    pHxA.yaxis.ticker.desired_num_ticks = 15

    
    t1 = Panel(child=p, title='overall')
    t2 = Panel(child=pH, title='home')
    t3 = Panel(child=pA, title='away')
    t4 = Panel(child=pHxA, title='home x away') 
    t5 = Panel(child=p3, title='Past years')
    
    
    dfR = tableTeamA(teamS, team)
    pRect = rectPlot(dfR)
    
    shotH, shotHT, goalsH, shotA, shotAT, goalsA = (teamHome['HS'].sum() - teamHome['HST'].sum()), (teamHome['HST'].sum() - teamHome['GoalsHome'].sum()), teamHome['GoalsHome'].sum(), (teamAway['AS'].sum() - teamAway['AST'].sum()), (teamAway['AST'].sum() - teamAway['GoalsAway'].sum()),  teamAway['GoalsAway'].sum()
    attack1 = [shotH, shotHT, goalsH, shotA, shotAT, goalsA]
    attack = [shotH, shotHT, goalsH, shotA, shotAT, goalsA, sum(attack1[:3]), sum(attack1[3:])]


    shotAb, shotATb, goalsAb, shotHb, shotHTb, goalsHb = (teamHome['AS'].sum() - teamHome['AST'].sum()), (teamHome['AST'].sum() - teamHome['GoalsAway'].sum()), teamHome['GoalsAway'].sum(), (teamAway['HS'].sum() - teamAway['HST'].sum()), (teamAway['HST'].sum() - teamAway['GoalsHome'].sum()),  teamAway['GoalsHome'].sum()
    defense1 = [shotAb, shotATb, goalsAb,shotHb, shotHTb, goalsHb ]
    defense = [shotAb, shotATb, goalsAb,shotHb, shotHTb, goalsHb, sum(defense1[:3]), sum(defense1[3:])]
    
    
    
    #values
    overall = {'attack': attack}
    index = ['off target','on target','goals','off target.','on target.','goals.','home','away']


    cYGB = YlGnBu
    cYG = YlGn
    colors =   '#253494',   '#1d91c0',   '#7fcdbb',  '#feb24c', '#fed976', '#ffeda0', 'green','yellow'


    #dataframe
    dfpie = pd.DataFrame(overall, index = index)
    dfpie['color'] = colors

    #df without overal which would be the first pie chart
    dfpie1 = dfpie.iloc[:-2]


    #df overall
    dfpie2 = pd.DataFrame(dfpie.iloc[-2:])
    dfpie2['color'] = ['#2c7fb8', '#fee08b']


    #angle for both df * pi instead *2*pi to keep it half circumference C=2πr
    dfpie1['angles'] = dfpie1['attack'] / dfpie1['attack'].sum() * pi
    dfpie2['angles'] = dfpie2['attack'] / dfpie2['attack'].sum() * pi

    dfpie1['pct'] = pctA = [round(attack[0] / attack[6] *100, 2), round(attack[1] / attack[6] *100, 2), round(attack[2] / attack[6] *100, 2), round(attack[3] / attack[7] *100, 2), round(attack[4] / attack[7] *100, 2), round(attack[5] / attack[7] *100, 2)]
    #pct(dfpie1['attack'], dfpie1['attack'].sum())
    dfpie1['pct'] = dfpie1['pct'].astype(str) + '%'

    dfpie2['pct'] = pct(dfpie2['attack'], dfpie2['attack'].sum())
    dfpie2['pct'] = dfpie2['pct'].astype(str) + '%'

    #sources
    sa1 = ColumnDataSource(data=dict(x=list(dfpie2.index.values), y=dfpie2['attack'], c=dfpie2['color'], a=dfpie2['angles'], l=dfpie2['pct']))
    sa2 = ColumnDataSource(data=dict(x=list(dfpie1.index.values), x1=list(dfpie1.index.values), y=dfpie1['attack'], c=dfpie1['color'], a=dfpie1['angles'], l=dfpie1['pct']))

    #figure instance
    piA = figure(plot_height=400, plot_width=500, toolbar_location='left', tools = 'pan, wheel_zoom, box_zoom, reset',  x_range=(-0.4, 0.9))

    #glyph
    piA.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('a', include_zero=True), end_angle=cumsum('a'),
             line_color='white', fill_color='c', source=sa1) #, legend_field='x'

    #overlay glyph
    piA.wedge(x=0, y=1, radius=0.3, start_angle=cumsum('a', include_zero=True), end_angle=cumsum('a'),
             line_color='white', fill_color='c', legend_field='x1', source=sa2)

    #hovertool
    ha1 = HoverTool()
    ha1.tooltips=[  ('type','@x'),('amount','@y'), ('pct','@l')]
    piA.add_tools(ha1)

    #hovertool 2
    ha2 = HoverTool()
    ha2.tooltips=[('type','@x'), ('amount','@y'), ('pct','@l')]
    piA.add_tools(ha2)

    #label
    hal = Label(x=255, y=330, x_units='screen', y_units='screen', 
                            text='Home', render_mode='css', text_font_size='17.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold') #Played at home
    hal1 = Label(x=45, y=330, x_units='screen', y_units='screen',
                            text='Away', render_mode='css', text_font_size='17.5pt', text_color='#fee08b',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    hal2 = Label(x=155, y=365, x_units='screen', y_units='screen',
                            text='Attack', render_mode='css', text_font_size='17.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')


    piA.add_layout(hal)
    piA.add_layout(hal1)
    piA.add_layout(hal2)



    #remove grid lines
    piA.axis.axis_label=None
    piA.axis.visible=False
    piA.grid.grid_line_color = None
    piA.outline_line_color=None


    piA.legend.background_fill_alpha=None
    piA.legend.border_line_alpha=0
    piA.legend.location= (320,185) #'center_right'
    piA.legend.label_text_font_size = "15px"
    piA.legend.title = 'shots'
    #piA.legend.orientation ='horizontal'
    piA.toolbar.autohide = True



    #defense
    overallD = {'defense': defense}
    indexD = ['shots off','shots on Target','goals','shots off away','shots on target away','goals aways','home','away']



    #dataframe
    dfpieD = pd.DataFrame(overallD, index = indexD)
    dfpieD['color'] = colors

    #df without overal which would be the first pie chart
    dfpie1D = dfpieD.iloc[:-2]


    #df overall
    dfpie2D = pd.DataFrame(dfpieD.iloc[-2:])
    dfpie2D['color'] = ['#2c7fb8', '#fee08b']


    #angle for both df * pi instead *2*pi to keep it half circumference C=2πr
    dfpie1D['angles'] = dfpie1D['defense'] / dfpie1D['defense'].sum() * pi
    dfpie2D['angles'] = dfpie2D['defense'] / dfpie2D['defense'].sum() * pi

    dfpie1D['pct'] =  [round(defense[0] / defense[6] *100, 2), round(defense[1] / defense[6] *100, 2), round(defense[2] / defense[6] *100, 2), round(defense[3] / defense[7] *100, 2), round(defense[4] / defense[7] *100, 2), round(defense[5] / defense[7] *100, 2)]
    #pct(dfpie1['attack'], dfpie1['attack'].sum())
    dfpie1D['pct'] = dfpie1D['pct'].astype(str) + '%'

    dfpie2D['pct'] = pct(dfpie2D['defense'], dfpie2D['defense'].sum())
    dfpie2D['pct'] = dfpie2D['pct'].astype(str) + '%'


    #sources
    sd1 = ColumnDataSource(data=dict(x=list(dfpie2D.index.values), y=dfpie2D['defense'], c=dfpie2D['color'], a=dfpie2D['angles'], l=dfpie2D['pct']))
    sd2 = ColumnDataSource(data=dict(x=list(dfpie1D.index.values), x1=list(dfpie1D.index.values), y=dfpie1D['defense'], c=dfpie1D['color'], a=dfpie1D['angles'], l=dfpie1D['pct']))

    #figure instance
    piD = figure(plot_height=400, plot_width=500,tools = 'pan, wheel_zoom, box_zoom, reset',  x_range=(-0.4, 0.9))

    #glyph
    piD.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('a', include_zero=True), end_angle=cumsum('a'),
             line_color='white', fill_color='c', source=sd1) #, legend_field='x'

    #overlay glyph
    piD.wedge(x=0, y=1, radius=0.3, start_angle=cumsum('a', include_zero=True), end_angle=cumsum('a'),
             line_color='white', fill_color='c', source=sd2) # legend_field='x1',

    #hovertool
    hd1 = HoverTool()
    hd1.tooltips=[  ('type','@x'),('amount','@y'), ('pct','@l')]
    piD.add_tools(hd1)

    #hovertool 2
    hd2 = HoverTool()
    hd2.tooltips=[('type','@x'), ('amount','@y'), ('pct','@l')]
    piD.add_tools(hd2)
    #piD.legend.title = 'opponent stats'

    #label
    hdl = Label(x=255, y=330, x_units='screen', y_units='screen', 
                            text='Home', render_mode='css', text_font_size='17.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold') #Played at home
    hdl1 = Label(x=45, y=330, x_units='screen', y_units='screen',
                            text='Away', render_mode='css', text_font_size='17.5pt', text_color='#fee08b',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    hdl2 = Label(x=155, y=360, x_units='screen', y_units='screen',
                            text='Defense', render_mode='css', text_font_size='17.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')


    piD.add_layout(hdl)
    piD.add_layout(hdl1)
    piD.add_layout(hdl2)

    #remove grid lines
    piD.axis.axis_label=None
    piD.axis.visible=False
    piD.grid.grid_line_color = None
    piD.outline_line_color=None
    #piD.toolbar.autohide = True
    piD.toolbar.logo = None
    piD.toolbar_location = None
    
    
    disH = [teamHome['HF'].median(), teamHome['HY'].sum(), teamHome['HR'].sum()]
    disA = [teamAway['AF'].median(), teamAway['AY'].sum(), teamAway['AR'].sum()]
    disInd = '*Fouls', 'Yellow Cards', 'Red Cards'
    dis = {'home':disH, 'away':disA }

    dfDis = pd.DataFrame(dis, index=disInd)
    dfDis[['home','away']] = dfDis[['home','away']].astype(int)
    dfDis


    xDis = disInd

    sourceDis = ColumnDataSource(data=dict(x=xDis, y=dfDis['home'], y1=dfDis['away']))

    pDis = figure(x_range=FactorRange(*xDis), plot_height=280, plot_width=350, tools='pan, wheel_zoom, box_zoom, reset', title='Discipline')
    #y_axis_label='quantity',

    pDis.vbar(x=dodge('x', -0.25, range=pDis.x_range), top='y', width=0.2, color= '#2c7fb8', source=sourceDis, legend_label='home')
    pDis.vbar(x=dodge('x', 0, range=pDis.x_range), top='y1', width=0.2, color= '#fee08b', source=sourceDis, legend_label='away')


    hDis1 = Label(x=260, y=150, x_units='screen', y_units='screen',
                            text='* median', render_mode='css', text_font_size='7.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')


    pDis.add_layout(hDis1)
    
    pDis.y_range.start = 0


    pDis.grid.grid_line_alpha = 0.8
    pDis.grid.grid_line_dash = 'dotted'
    pDis.grid.grid_line_dash_offset = 5
    pDis.grid.grid_line_width = 2
    pDis.axis.major_label_text_font_style = 'bold'
    pDis.title.text_font_size = '17px'
    pDis.outline_line_color=None
    pDis.toolbar.autohide = True

    hDis= HoverTool()
    hDis.tooltips=[('home', '@y'),('away','@y1')]
    pDis.add_tools(hDis)

    pDis.legend.location= 'top_right'#(370,180)
    pDis.legend.background_fill_alpha=None
    pDis.legend.border_line_color = None

    pDis.legend.click_policy="hide"
    #pDis.legend.title='↓ Disable/Enable'

    pDis.legend.border_line_color = None
    pDis.legend.background_fill_color=None

    
    figTeamAH = [int(teamHome['GoalsHome'].median()), int(teamHome['HS'].median()), int(teamHome['HST'].median()), int(teamHome['HC'].median())]
    figTeamAA = [int(teamAway['GoalsAway'].median()), int(teamAway['AS'].median()), int(teamAway['AST'].median()), int(teamAway['HC'].median())]
    indexfig = 'goals', 'shots off target','shots on target','corners'
    figDict = {'home':figTeamAH, 'away':figTeamAA}

    dfFig = pd.DataFrame(figDict, index=indexfig)
    srcM = ColumnDataSource(data=dict(x=indexfig, y=dfFig['home'], y1=dfFig['away']))

    pCnM = figure(x_range=FactorRange(*indexfig),plot_height=280, plot_width=400, tools='pan, wheel_zoom, box_zoom, reset', title='Median figures')

    pCnM.vbar(x=dodge('x', -0.25, range=pCnM.x_range), top='y', width=0.2, color= '#2c7fb8', source=srcM, legend_label='home')
    pCnM.vbar(x=dodge('x', 0, range=pCnM.x_range), top='y1', width=0.2, color= '#fee08b', source=srcM, legend_label='away')

    pCnM.y_range.start = 0
    
    pCnM.grid.grid_line_alpha = 0.8
    pCnM.grid.grid_line_dash = 'dotted'
    pCnM.grid.grid_line_dash_offset = 5
    pCnM.grid.grid_line_width = 2
    pCnM.axis.major_label_text_font_style = 'bold'
    pCnM.title.text_font_size = '17px'
    pCnM.outline_line_color=None
    pCnM.toolbar.autohide = True

    hcnM= HoverTool()
    hcnM.tooltips=[('type', '@x'),('home','@y'), ('away','@y1')]
    pCnM.add_tools(hcnM)

    pCnM.legend.location= 'top_right'#(370,180)
    pCnM.legend.background_fill_alpha=None
    pCnM.legend.border_line_color = None

    pCnM.legend.click_policy="hide"

    pCnM.legend.border_line_color = None
    pCnM.y_range.end = dfFig[['home','away']].max(axis=1).max() *1.3



    homeTeamF = teamHome[['Date','opponent','GoalsHome','GoalsAway','HS','AS','HST','AST','HC','AC', 'HF', 'AF', 'HY', 'AY', 'HR', 'AR']]
    homeTeamF.columns = ['Date','opponent','goals', 'goalsO', 'shots', 'shotsO','shots on target', 'shots on target O','corners','cornersO',
                        'fouls', 'foulsO', 'yellow card', 'yellow cardO','red card', 'red cardO']
    teamAwayF = teamAway[['Date','opponent','GoalsAway', 'GoalsHome','AS','HS','AST','HST','AC','HC','AF','HF','AY','HY','AR','HR']]
    teamAwayF.columns = ['Date','opponent','goals', 'goalsO', 'shots', 'shotsO','shots on target', 'shots on target O', 'corners','cornersO',
                        'fouls', 'foulsO', 'yellow card', 'yellow cardO','red card', 'red cardO']
    
    
    teamGoals = homeTeamF.append(teamAwayF)
    teamGoals = teamGoals.sort_values('Date')
    
    
    xGST = teamGoals['opponent'].values.tolist()

    sourceGST = ColumnDataSource(data=dict(x=xGST, g=teamGoals['goals'], go=teamGoals['goalsO'], s=teamGoals['shots'],
                                           so=teamGoals['shotsO'], st=teamGoals['shots on target'], sto=teamGoals['shots on target O'],h=teamGoals['corners'], a=teamGoals['cornersO']))

    pGST = figure(x_range=xGST, plot_height=500, plot_width=800, tools='pan, wheel_zoom, box_zoom, reset', title='Goals')

    pGST.diamond(x='x', y='g', source=sourceGST, size=13, color='#2c7fb8', line_color='black', legend_label='goals scored')
    pGST.circle(x='x', y='go', source=sourceGST, size=8, color='#fee08b', line_color='black', legend_label='goals conceded')

    #pGST.y_range.start = 0
    pGST.grid.grid_line_alpha = 0.8
    pGST.grid.grid_line_dash = 'dotted'
    pGST.grid.grid_line_dash_offset = 5
    pGST.grid.grid_line_width = 2
    pGST.axis.major_label_text_font_style = 'bold'
    pGST.title.text_font_size = '20px'
    pGST.outline_line_color=None
    pGST.toolbar.autohide = True
    pGST.axis.major_label_text_font_size = '13px'

    hgst= HoverTool()
    hgst.tooltips=[('opponet', '@x'),('scored','@g'), ('conceded','@go')]
    pGST.add_tools(hgst)

    pGST.legend.location= 'top_right'#(370,180)
    pGST.legend.background_fill_alpha=None
    pGST.legend.border_line_color = None

    pGST.legend.click_policy="hide"
    pGST.legend.title='↓ Disable/Enable'

    pGST.legend.border_line_color = None
    #pCn1.legend.background_fill_color=None
    pGST.legend.orientation = 'horizontal'
    pGST.xaxis.major_label_orientation = 45
    pGST.y_range.end = teamGoals[['goals','goalsO']].max(axis=1).max() *1.25
    pGST.yaxis.ticker.desired_num_ticks = 5#int(teamGoals[['goals','goalsO']].max(axis=1).max() / .5)


    gstl1 = Label(x=10, y=300, x_units='screen', y_units='screen', 
                            text='*', render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pGST.add_layout(gstl1)

    gstl2 = Label(x=47, y=310, x_units='screen', y_units='screen', 
                            text='Home match', render_mode='css', text_font_size='7.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pGST.add_layout(gstl2)

    
    

    pSO = figure(x_range=xGST, plot_height=500, plot_width=800, tools='pan, wheel_zoom, box_zoom, reset', title='Shots')

    pSO.diamond(x='x', y='s', source=sourceGST, size=14, color='#2c7fb8', line_color='black', legend_label='taken')
    pSO.circle(x='x', y='so', source=sourceGST, size=8, color='#fee08b', line_color='black', legend_label='conceded')

    pSO. diamond_cross(x='x', y='st', source=sourceGST, size=14, color='#7fcdbb', line_color='black', legend_label='on target taken')
    pSO.circle_cross(x='x', y='sto', source=sourceGST, size=8, color='#feb24c', line_color='black', legend_label='on target conceded')

    #pSO.y_range.start = 0
    pSO.grid.grid_line_alpha = 0.8
    pSO.grid.grid_line_dash = 'dotted'
    pSO.grid.grid_line_dash_offset = 5
    pSO.grid.grid_line_width = 2
    pSO.axis.major_label_text_font_style = 'bold'
    pSO.title.text_font_size = '20px'
    pSO.outline_line_color=None
    pSO.toolbar.autohide = True
    pSO.axis.major_label_text_font_size = '13px'

    hso= HoverTool()
    hso.tooltips=[('opponet', '@x'),('taken','@s'), ('conceded','@so'), ('taken on target','@st'), ('conceded on target','@sto')]
    pSO.add_tools(hso)

    pSO.legend.location= 'top_right'#(370,180)
    pSO.legend.background_fill_alpha=None
    pSO.legend.border_line_color = None

    pSO.legend.click_policy="hide"
    pSO.legend.title='↓ Disable/Enable'

    pSO.legend.border_line_color = None
    #pCn1.legend.background_fill_color=None
    pSO.legend.orientation = 'horizontal'
    pSO.xaxis.major_label_orientation = 45
    pSO.y_range.end = teamGoals[['shots','shotsO']].max(axis=1).max() *1.25
    pSO.yaxis.ticker.desired_num_ticks = int(teamGoals[['shots','shotsO']].max(axis=1).max() / 3)


    lso = Label(x=10, y=290, x_units='screen', y_units='screen', 
                            text='*', render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pSO.add_layout(lso)

    lso1 = Label(x=47, y=300, x_units='screen', y_units='screen', 
                            text='Home match', render_mode='css', text_font_size='7.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pSO.add_layout(lso1)
    
    pCn1 = figure(x_range=xGST, plot_height=500, plot_width=800, tools='pan, wheel_zoom, box_zoom, reset', title='Corners')

    pCn1.diamond(x='x', y='h', source=sourceGST, size=13, color='#2c7fb8', line_color='black', legend_label='taken')
    pCn1.circle(x='x', y='a', source=sourceGST, size=8, color='#fee08b', line_color='black', legend_label='conceded')


    #pCn1.y_range.start = 0
    pCn1.grid.grid_line_alpha = 0.8
    pCn1.grid.grid_line_dash = 'dotted'
    pCn1.grid.grid_line_dash_offset = 5
    pCn1.grid.grid_line_width = 2
    pCn1.axis.major_label_text_font_style = 'bold'
    pCn1.title.text_font_size = '20px'
    pCn1.outline_line_color=None
    pCn1.toolbar.autohide = True
    pCn1.axis.major_label_text_font_size = '13px'

    cnH= HoverTool()
    cnH.tooltips=[('opponet', '@x'),('taken','@h'), ('conceded','@a')]
    pCn1.add_tools(cnH)

    pCn1.legend.location= 'top_right'#(370,180)
    pCn1.legend.background_fill_alpha=None
    pCn1.legend.border_line_color = None

    pCn1.legend.click_policy="hide"
    pCn1.legend.title='↓ Disable/Enable'

    pCn1.legend.border_line_color = None
    #pCn1.legend.background_fill_color=None
    pCn1.legend.orientation = 'horizontal'
    pCn1.xaxis.major_label_orientation = 45
    pCn1.y_range.end = teamGoals[['corners','cornersO']].max(axis=1).max() *1.25
    pCn1.yaxis.ticker.desired_num_ticks = int(teamGoals[['corners','cornersO']].max(axis=1).max() / 2)


    lcnr = Label(x=10, y=290, x_units='screen', y_units='screen', 
                            text='*', render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pCn1.add_layout(lcnr)

    lcnr1 = Label(x=47, y=300, x_units='screen', y_units='screen', 
                            text='Home match', render_mode='css', text_font_size='7.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pCn1.add_layout(lcnr1)
    
   


    teamGoals['red card'].replace(0, np.nan, inplace=True)
    teamGoals['red cardO'].replace(0, np.nan, inplace=True)
    teamGoals = teamGoals.sort_values('Date')
    
    xFR = list(teamGoals['opponent'].values)


    srcF = ColumnDataSource(data=dict(x=xFR, f=teamGoals['fouls'], fo=teamGoals['foulsO'], yc=teamGoals['yellow card'], yco=teamGoals['yellow cardO'],
                                           rc=teamGoals['red card'], rco=teamGoals['red cardO']))


    pFR = figure(x_range=xFR, plot_height=500, plot_width=800, tools='pan, wheel_zoom, box_zoom, reset', title='Discipline overall')

    pFR.diamond(x='x', y='f', source=srcF, size=14, color='#fe9929', line_color='black', legend_label='fouls received')
    pFR.circle(x='x', y='fo', source=srcF, size=8, color='#fe9929', line_color='black', legend_label='fouls committed')

    pFR.diamond_cross(x='x', y='yc', source=srcF, size=14, color='#fff7bc', line_color='black', legend_label='yellow card')
    pFR.circle_cross(x='x', y='yco', source=srcF, size=8, color='#fff7bc', line_color='black', legend_label='yellow card opponent')

    pFR.square(x='x', y='rc', source=srcF, size=6.5, color='#993404', line_color='black', legend_label='red card')
    pFR.square_cross(x='x', y='rco', source=srcF, size=6.5, color='#993404', line_color='black', legend_label='red card opponent')


    #pFR.y_range.start = 0
    pFR.grid.grid_line_alpha = 0.8
    pFR.grid.grid_line_dash = 'dotted'
    pFR.grid.grid_line_dash_offset = 5
    pFR.grid.grid_line_width = 2
    pFR.axis.major_label_text_font_style = 'bold'
    pFR.title.text_font_size = '20px'
    pFR.outline_line_color=None
    pFR.toolbar.autohide = True
    pFR.axis.major_label_text_font_size = '13px'

    hfr= HoverTool()
    hfr.tooltips=[('opponent', '@x'),('committed','@f'), ('received','@fo'), ('yellow card','@yc'), ('yellow card opponent','@yco'),('red card','@rc'),('red card opponent','@rco')]
    pFR.add_tools(hfr)

    pFR.legend.location= 'top_right'#(370,180)
    pFR.legend.background_fill_alpha=None
    pFR.legend.border_line_color = None

    pFR.legend.click_policy="hide"
    pFR.legend.title='↓ Disable/Enable'

    pFR.legend.border_line_color = None
    #pCn1.legend.background_fill_color=None
    pFR.legend.orientation = 'horizontal'
    pFR.xaxis.major_label_orientation = 45
    pFR.y_range.end = teamGoals[['fouls','foulsO']].max(axis=1).max() *1.25
    pFR.yaxis.ticker.desired_num_ticks = int(teamGoals[['fouls','foulsO']].max(axis=1).max() / 2)


    lfr = Label(x=610, y=320, x_units='screen', y_units='screen', 
                            text='*', render_mode='css', text_font_size='15.5pt', text_color='black',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pFR.add_layout(lfr)

    lfr1 = Label(x=647, y=328, x_units='screen', y_units='screen', 
                            text='Home match', render_mode='css', text_font_size='7.5pt', text_color='#2c7fb8',
                            text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    pFR.add_layout(lfr1)



    
    
    
    ovG = Panel(child=pGST, title='Goals')
    ovS = Panel(child=pSO, title='Shots')
    ovC = Panel(child=pCn1, title='Corners')
    ovD = Panel(child=pFR, title='Discipline overall')

    s = sheets(teamS, team, season)




    tabsOV = Tabs(tabs=[ovG, ovS, ovC, ovD])
   

       
    tabs = Tabs(tabs=[t1, t2, t3, t4, t5])
    #c = column([p3, tabs])
    c1 = column([tabs, pRect], spacing=-15, margin=(0,50,0,0))
    r1 = row([piA, piD], spacing=-40)
    #r2 = gridplot([r1], toolbar_location='left', merge_tools=True)
    c2 = column([c1, r1], spacing=-30)
    r2 = row([pDis, pCnM])
    c3 = column([c2, r2], spacing=-170)
    c4 = column([c3, tabsOV, s])

    
    return c4



league1 = ['Barclays Premier League', 'English League Championship', 'French Ligue 1', 'French Ligue 2','Spanish Primera Division', 'Spanish Segunda Division','Italy Serie A',  'Italy Serie B','German Bundesliga', 'German 2. Bundesliga','UEFA Champions League',  'UEFA Europa League','Brasileiro Série A', 'Russian Premier Liga', 'Austrian T-Mobile Bundesliga', 'Swiss Raiffeisen Super League', 'Danish SAS-Ligaen','Belgian Jupiler League' ]



def model_(df):

    dfM = pd.concat([df[['HomeTeam','AwayTeam','GoalsHome','spi1','importance1']].assign(home=1).rename(
                columns={'HomeTeam':'team', 'AwayTeam':'opponent','GoalsHome':'goals','spi1':'rate', 'importance1':'importance'}), 
                      df[['AwayTeam','HomeTeam','GoalsAway','spi2', 'importance2']].assign(home=0).rename(
                columns={'AwayTeam':'team', 'HomeTeam':'opponent','GoalsAway':'goals', 'spi2':'rate', 'importance2':'importance'})])
    return dfM

def possionM(df):
    poissonM = smf.glm(formula='goals~importance + team + opponent', data=df, family=sm.families.Poisson()).fit()
    return poissonM

def rates(df, team,teamA):
    
    team, teamA = str(team), str(teamA)
    t_x_o = df[(df['HomeTeam']== team) & (df['AwayTeam']== teamA)]
    t_x_o = t_x_o[['spi1','spi2','importance1','importance2']][:-1]
            
    return list(t_x_o.values)

def ratesRev(df, teamA,team):
    
    team, teamA = str(team), str(teamA)
    t_x_o = df[(df['AwayTeam']== team) & (df['HomeTeam']== teamA)]
    t_x_o = t_x_o[['spi2','spi1','importance2','importance1']][:-1]
            
    return list(t_x_o.values)

def rates1(df, team,teamA):
    
    team, teamA = str(team), str(teamA)
    t_x_o = df[(df['HomeTeam']== team) & (df['AwayTeam']== teamA)]
    t_x_o = t_x_o[['spi1','spi2','importance1','importance2']]#[:-1]
            
    return list(t_x_o.values)

def goalsWAH(df, team, teamA, p):
    
    team, y = str(team), str(teamA)
    g1 = df[(df['HomeTeam']== team) & (df['AwayTeam']== teamA)]
    gH = average(g1['GoalsHome'], weights =g1['HS'])
    w1 = df[df['HomeTeam'] == team]['GoalsHome'].values
    w2 = df[df['HomeTeam'] == team]['HS'].values
    wH = average(w1, weights=w2)
    #g3 = dfPL[(dfPL['HomeTeam']== y)]['GoalsAway'][-6:].mean()
    gHpast5 = average(df[(df['HomeTeam']== team)]['GoalsHome'][-p:], weights = df[(df['HomeTeam']== team)]['HS'][-p:])
    AHpast5 = average(df[(df['AwayTeam']== teamA)]['GoalsHome'][-p:], weights = df[(df['AwayTeam']== teamA)]['HS'][-p:])
    HGxATpast5 = average(w1[:p], weights=w2[:p])
    total = np.array([gH, wH, gHpast5,AHpast5,HGxATpast5]).sum() / np.array([gH, wH, gHpast5,AHpast5,HGxATpast5]).mean() * np.array([gH, wH, gHpast5,AHpast5,HGxATpast5]).var()
    total =  int(total.mean())
    
    g1a = df[(df['HomeTeam']== team) & (df['AwayTeam']== teamA)]
    gHa = average(g1a['GoalsAway'], weights =g1a['AS'])
    w1a = df[df['AwayTeam'] == team]['GoalsAway'].values
    w2a = df[df['AwayTeam'] == team]['AS'].values
    wHa = average(w1a, weights=w2a)
    #g3 = dfPL[(dfPL['HomeTeam']== y)]['GoalsAway'][-6:].mean()
    gHpast5a = average(df[(df['AwayTeam']== teamA)]['GoalsAway'][-p:], weights = df[(df['AwayTeam']== teamA)]['AS'][-p:])
    AHpast5a = average(df[(df['HomeTeam']== team)]['GoalsAway'][-p:], weights = df[(df['HomeTeam']== team)]['AS'][-p:])
    HGxATpast5a = average(w1a[:p], weights=w2a[:p])
    totala = np.array([gHa, wHa, gHpast5a,AHpast5a,HGxATpast5a]).sum()/ np.array([gHa, wHa, gHpast5a,AHpast5a,HGxATpast5a]).mean() * np.array([gHa, wHa, gHpast5a,AHpast5a,HGxATpast5a]).var()
    totala =  int(totala.mean())
    #ttt = np.array([gHa, wHa, gHpast5a,AHpast5a,HGxATpast5a]).var()

    #ga = df[(df['AwayTeam']== y)]['GoalsAway'][-4:].mean()
    #gavg = int(gHvsA + gHwa + gh) /3
    #return print(f'Score: {x} {total}:{totala} {y}')
    return [total, totala]


def nGoalsAvg(df, team,teamA):
    
    team, teamA = str(team), str(teamA)
    g1 = df[(df['HomeTeam']== team) & (df['AwayTeam']== teamA)]
    g2 = g1[['GoalsHome','GoalsAway']].mean()
    #g3 = dfPL[(dfPL['HomeTeam']== y)]['GoalsAway'][-6:].mean()
    gh = df[(df['HomeTeam']== team)]['GoalsHome'][-4:].mad()
    ga = df[(df['AwayTeam']== teamA)]['GoalsAway'][-4:].mad()
    gavg = int((g2 + gh + ga).mean())
    
    return gavg

def nCorners(team,teamA):
    team, teamA = str(team), str(teamA)
    g1 = dfT[(dfT['HomeTeam']== team) & (dfT['AwayTeam']== teamA)]
    g2 = g1[['HC','AC']].mean()
    gh = dfT[(dfT['HomeTeam']== team)]['HC'][-2:].mean()
    ga = dfT[(dfT['AwayTeam']== teamA)]['AC'][-2:].mean()
    gavg = int((g2 + gh + ga).mean()) / 2
    return gavg




def simulationG(model, homeTeam, awayTeam,rate,rate1, importance, importance1, max_goals=10):
    hg_avg = model.predict(pd.DataFrame(data={'team': homeTeam, 
                                                            'opponent': awayTeam,'home':1, 'rate':rate,'importance':importance},
                                                      index=[1])).values[0]
    ag_avg = model.predict(pd.DataFrame(data={'team': awayTeam, 
                                                            'opponent': homeTeam,'home':0, 'rate':rate,'importance':importance},
                                                      index=[1])).values[0]
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [hg_avg, ag_avg]]
    return(np.outer(np.array(team_pred[0]), np.array(team_pred[1])))



def simMatch(df, team,teamA):
    df1 = model_(df)
    team, teamA = str(team), str(teamA)
    poissonM = possionM(df1)
    
    teams = {'HomeTeam':team,
             'AwayTeam':teamA}
    gavg = nGoalsAvg(df, team,teamA)
    resP = team + ' win' ,'Draw', teamA + ' win'
    r = rates1(df, team,teamA)
    r = np.array(r).flatten().tolist()
    sim = simulationG(poissonM,team, teamA, r[-4], r[-3], r[-2], r[-1], max_goals=gavg)
    odds = [round(np.sum(np.tril(sim, -1)) *100, 2), round(np.sum(np.diag(sim))*100, 2), round(np.sum(np.triu(sim, 1))*100, 2)]
    odds = dict(zip(resP, odds))
    odds = pd.DataFrame(odds,index=range(1))

    #odds1 = {**teams, **odds}
    odds['deviation'] = round(odds.iloc[:,:3].std(1),2)
    odds['nGoals'] = gavg
    odds = odds.T
    odds.columns = ['y']
    odds['color'] = ['#7fcdbb','#ffeda0', '#7fcdbb','#feb24c', '#ffeda0']

    x = odds.index.values.tolist()[:-1]
    #x = team + ' win', 'draw', team + ' win', 'deviaton'
    
    #mapper = CategoricalColorMapper(palette=['#7fcdbb', '#feb24c','#7fcdbb','#ffeda0'], factors=[team,'Draw',teamA, 'deviation'])

    src = ColumnDataSource(data=dict(x=x, y=odds['y'][:-1], c = odds['color']))

    p = figure(x_range=x, plot_height=300, plot_width=400, tools='pan, wheel_zoom, box_zoom, reset',
                 title= team + ' vs ' + teamA + ' prediction')

    p.vbar(x='x', top='y', width=.4, color='c', source=src)


    p.grid.grid_line_alpha = 0.8
    p.grid.grid_line_dash = 'dotted'
    p.grid.grid_line_dash_offset = 5
    p.grid.grid_line_width = 2
    p.axis.major_label_text_font_style = 'bold'
    p.title.text_font_size = '17px'
    p.outline_line_color=None
    p.toolbar.autohide = True
    tick_labels = {'5':'5%','10':'10%','15':'15%','20':'20%','25':'25%','30':'30%','35':'35%','40':'40%','45':'45%','50':'50%','55':'55%','60':'60%','65':'65%','70':'70%','75':'75%','80':'80%','85':'85%','90':'90%'}
    p.yaxis.major_label_overrides = tick_labels
    
    #p.yaxis[0].formatter = NumeralTickFormatter(format="0 %") 


    hTF= HoverTool()
    hTF.tooltips=[('outcome', '@x'),('Probability','@y{0.00} %')]
    p.add_tools(hTF)
    p.y_range.start = 0

    #p.legend.location= 'top_right'#(370,180)
    #p.legend.background_fill_alpha=None
    #p.legend.border_line_color = None

    #p.legend.click_policy="hide"
    #p.legend.orientation = 'horizontal'
    #p.legend.title = '↓ Disable/Enable'

    #p.legend.border_line_color = None
    p.y_range.end = odds['y'].max() *1.2

    lTF = Label(x=270, y=230, x_units='screen', y_units='screen', 
                            text='Expected', render_mode='css', text_font_size='8pt', text_color='black',
                            text_align='left', angle=0, text_alpha=1, text_font_style='bold')
    p.add_layout(lTF)

    lTF1 = Label(x=278, y=215, x_units='screen', y_units='screen', 
                            text='goals', render_mode='css', text_font_size='10pt', text_color='black',
                            text_align='left', angle=0, text_alpha=1, text_font_style='bold')
    p.add_layout(lTF1)

    lTF2 = Label(x=288, y=186, x_units='screen', y_units='screen', 
                            text=str(gavg), render_mode='css', text_font_size='20pt', text_color='#7fcdbb',
                            text_align='left', angle=0, text_alpha=1, text_font_style='bold')
    p.add_layout(lTF2)
    

    
    
    return p


def selectionIT(lg, team, season):
    team = str(team)
    df = DFmerged(lg)
    teamA = tableTeamA(df, team)
    chart1 = teamOverall(teamA, season)
    return chart1

def selectionEng(lg, team, season):
    team = str(team)
    df = DFmergedEngland(lg)
    teamA = tableTeamA(df, team)
    chart1 = teamOverall(teamA, season)
    return chart1

def selectionGer(lg, team, season):
    team = str(team)
    df = DFmergedGermany(lg)
    teamA = tableTeamA(df, team)
    chart1 = teamOverall(teamA, season)
    return chart1

def selectionFR(lg, team, season):
    team = str(team)
    df = DFmergedFrance(lg)
    teamA = tableTeamA(df, team)
    chart1 = teamOverall(teamA, season)
    return chart1
    

def ItalyOverall(season, team, team1):
    
    lg = 'Italy Serie A'
    df = DFmerged(lg)
    
    s = selectionIT(lg, team, season)
    s1 = selectionIT(lg, team1, season)    
    axb = AxBteams(df,team,team1,season)
    
    t1 = Panel(child=s, title=team)
    t2 = Panel(child=s1, title=team1)
    t3 = Panel(child=axb, title=team+' x '+team1)
    
    tabs = Tabs(tabs=[t1, t2,t3], margin=(0,15,0,15))

    
    return tabs

def EnglandOverall(season, team, team1):
    
    lg = 'Barclays Premier League'
    df = DFmergedEngland(lg)
        
    s = selectionEng(lg, team, season)
    s1 = selectionEng(lg, team1, season)    
    axb = AxBteams(df,team,team1,season)
    
    t1 = Panel(child=s, title=team)
    t2 = Panel(child=s1, title=team1)
    t3 = Panel(child=axb, title=team+' x '+team1)
    
    tabs = Tabs(tabs=[t1, t2,t3], margin=(0,15,0,15))

    
    return tabs


def GermanyOverall(season, team, team1):
    
    lg = 'German Bundesliga'
    df = DFmergedGermany(lg)
        
    s = selectionGer(lg, team, season)
    s1 = selectionGer(lg, team1, season)    
    axb = AxBteams(df,team,team1,season)
    
    t1 = Panel(child=s, title=team)
    t2 = Panel(child=s1, title=team1)
    t3 = Panel(child=axb, title=team+' x '+team1) 
    tabs = Tabs(tabs=[t1, t2,t3], margin=(0,15,0,15)) 
    
    return tabs

def FranceOverall(season, team, team1):
    
    lg = 'French Ligue 1'
    df = DFmergedFrance(lg)
    
    s = selectionFR(lg, team, season)
    s1 = selectionFR(lg, team1, season)    
    axb = AxBteams(df,team,team1,season)
    
    t1 = Panel(child=s, title=team)
    t2 = Panel(child=s1, title=team1)
    t3 = Panel(child=axb, title=team+' x '+team1)
    
    tabs = Tabs(tabs=[t1, t2,t3], margin=(0,15,0,15))

    
    return tabs



def GermanyBundesliga():
    from ipywidgets import Dropdown, interact
    
    lg = 'German Bundesliga'
    df = DFmergedGermany(lg)

    seasonY = {'2016':sorted(df[df['season'] == 2016]['HomeTeam'].unique().tolist()[::-1]),
              '2017': sorted(df[df['season'] == 2017]['HomeTeam'].unique().tolist()),
              '2018': sorted(df[df['season'] == 2018]['HomeTeam'].unique().tolist()),
              '2019': sorted(df[df['season'] == 2019]['HomeTeam'].unique().tolist()),
              '2020': sorted(df[df['season'] == 2020]['HomeTeam'].unique().tolist())
              }
    seasonDW = Dropdown(options=seasonY.keys())
    teamDW = Dropdown(options=seasonY[seasonDW.value])
    teamDW1 = Dropdown(options=seasonY[seasonDW.value])
    @interact(season = seasonDW, team = teamDW, team1 = teamDW1)
    def teams(season, team, team1):
        teamDW.options = seasonY[season]
        teamDW1.options = seasonY[season]
        
        t = GermanyOverall(int(season),team,team1)
        #l = [int(season),team,team1]
        #l = {'season':int(season),
        #    'team':team, 'team1':team1}
       
        return show(t)
    
    
def FrenchLigue():
    from ipywidgets import Dropdown, interact
    
    lg = 'French Ligue 1'
    df = DFmergedFrance(lg)

    seasonY = {'2016':sorted(df[df['season'] == 2016]['HomeTeam'].unique().tolist()[::-1]),
              '2017': sorted(df[df['season'] == 2017]['HomeTeam'].unique().tolist()),
              '2018': sorted(df[df['season'] == 2018]['HomeTeam'].unique().tolist()),
              '2019': sorted(df[df['season'] == 2019]['HomeTeam'].unique().tolist()),
              '2020': sorted(df[df['season'] == 2020]['HomeTeam'].unique().tolist())
              }
    seasonDW = Dropdown(options=seasonY.keys())
    teamDW = Dropdown(options=seasonY[seasonDW.value])
    teamDW1 = Dropdown(options=seasonY[seasonDW.value])
    @interact(season = seasonDW, team = teamDW, team1 = teamDW1)
    def teams(season, team, team1):
        teamDW.options = seasonY[season]
        teamDW1.options = seasonY[season]
        
        t = FranceOverall(int(season),team,team1)
        #l = [int(season),team,team1]
        #l = {'season':int(season),
        #    'team':team, 'team1':team1}
       
        return show(t)

def ItalySerieA():
    from ipywidgets import Dropdown, interact
    
    lg = 'Italy Serie A'
    df = DFmerged(lg)

    seasonY = {'2016':sorted(df[df['season'] == 2016]['HomeTeam'].unique().tolist()[::-1]),
              '2017': sorted(df[df['season'] == 2017]['HomeTeam'].unique().tolist()),
              '2018': sorted(df[df['season'] == 2018]['HomeTeam'].unique().tolist()),
              '2019': sorted(df[df['season'] == 2019]['HomeTeam'].unique().tolist()),
              '2020': sorted(df[df['season'] == 2020]['HomeTeam'].unique().tolist())
              }
    seasonDW = Dropdown(options=seasonY.keys())
    teamDW = Dropdown(options=seasonY[seasonDW.value])
    teamDW1 = Dropdown(options=seasonY[seasonDW.value])
    @interact(season = seasonDW, team = teamDW, team1 = teamDW1)
    def teams(season, team, team1):
        teamDW.options = seasonY[season]
        teamDW1.options = seasonY[season]
        
        t = ItalyOverall(int(season),team,team1)
        #l = [int(season),team,team1]
        #l = {'season':int(season),
        #    'team':team, 'team1':team1}
       
        return show(t)
    

def EnglandPL():
    from ipywidgets import Dropdown, interact
    lg = 'Barclays Premier League'
    df = DFmergedEngland(lg)

    seasonY = {'2016':sorted(df[df['season'] == 2016]['HomeTeam'].unique().tolist()[::-1]),
              '2017': sorted(df[df['season'] == 2017]['HomeTeam'].unique().tolist()),
              '2018': sorted(df[df['season'] == 2018]['HomeTeam'].unique().tolist()),
              '2019': sorted(df[df['season'] == 2019]['HomeTeam'].unique().tolist()),
              '2020': sorted(df[df['season'] == 2020]['HomeTeam'].unique().tolist())
              }
    seasonDW = Dropdown(options=seasonY.keys())
    teamDW = Dropdown(options=seasonY[seasonDW.value])
    teamDW1 = Dropdown(options=seasonY[seasonDW.value])
    @interact(season = seasonDW, team = teamDW, team1 = teamDW1)
    def teams(season, team, team1):
        teamDW.options = seasonY[season]
        teamDW1.options = seasonY[season]
        
        t = EnglandOverall(int(season),team,team1)
        #l = [int(season),team,team1]
        #l = {'season':int(season),
        #    'team':team, 'team1':team1}
       
        return show(t)    