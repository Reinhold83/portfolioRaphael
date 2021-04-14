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