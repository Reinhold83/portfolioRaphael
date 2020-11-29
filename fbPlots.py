import pandas as pd
import numpy as np
import time, glob, os, math
import datetime

from scipy.stats import spearmanr
from sklearn.preprocessing import MinMaxScaler
from relativeImp import relativeImp
from sklearn.preprocessing import scale, PolynomialFeatures
from sklearn.linear_model import Ridge
from sklearn.pipeline import make_pipeline

from bokeh.io import export_png, export_svgs
import json
from bokeh.io import show
from bokeh.models import (CDSView, ColorBar, ColumnDataSource,
                          CustomJS, CustomJSFilter, 
                          GeoJSONDataSource, HoverTool,
                          LinearColorMapper, Slider, Tabs, Panel)
from bokeh.layouts import column, row, widgetbox
from bokeh.models import NumeralTickFormatter, PrintfTickFormatter
import geopandas as gpd
from copy import deepcopy

from bokeh.transform import dodge, jitter
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, Band, Slope, TickFormatter,  LinearInterpolator, LabelSet, ColorBar, BasicTicker, LinearColorMapper, FactorRange, Slope, BoxAnnotation, Label, CustomJS, Select, Band, HoverTool, Slider, DatetimeTickFormatter, Range1d, TapTool, HBar, Panel, Tabs
from bokeh.plotting import figure
from bokeh.models.tools import HoverTool, WheelZoomTool, PanTool, CrosshairTool
from bokeh.io import (output_notebook, show, curdoc, output_file)
from bokeh.palettes import Pastel2, viridis, OrRd, Inferno256, Greens, GnBu
import datetime as dt
from bokeh.models.glyphs import Text
from bokeh.transform import stack, factor_cmap, linear_cmap, factor_mark, CategoricalColorMapper
from scipy.integrate import odeint