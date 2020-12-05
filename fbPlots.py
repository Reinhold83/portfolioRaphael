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

def fb_figs():
    dfDayPE = pd.read_csv('BokehApp/DataFB/dfDayPE.csv', delimiter=',', index_col=0)
    dfDayPE['date1'] = pd.to_datetime(dfDayPE['date1'], format=('%Y/%m/%d'))

    dfWeekPE = pd.read_csv('BokehApp/DataFB/dfWeekPE.csv', delimiter=',', index_col=0)
    dfWeekPE['week1'] = pd.to_datetime(dfWeekPE['week1'], format=('%Y/%m/%d'))
    
    dfMonthPE = pd.read_csv('BokehApp/DataFB/dfMonthPE.csv', delimiter=',', index_col=0)
    dfMonthPE['month1'] = pd.to_datetime(dfMonthPE['month1'], format=('%Y/%m/%d'))


    xrday = dfDayPE['date1'].to_list()


    sourceday = ColumnDataSource(data=dict(x=xrday ,x1=dfDayPE['date1'], y=dfDayPE['Close'], y1=dfDayPE['Open'], y2=dfDayPE['PE'], y3=dfDayPE['Volume'], y4=dfDayPE['MovingAvg'], y5=dfDayPE['Returns'],
                                          y6=dfDayPE['MovingAvgReturn'], ub=dfDayPE['UB'], lb=dfDayPE['LB'], sd=dfDayPE['STD'], pctma=dfDayPE['pct_ma']))
    #color_mapperday = LinearColorMapper(palette= coloursDD[::-1], low=60, high=100)

    pday = figure(title='Daily Facebook, Inc.', plot_height=500, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')
    pday.line(y='y', x='x1', source=sourceday, line_width = 1.2, line_color='#3b5998', legend_label='Close')
    #pday.circle(x='x1', y='y', size=1, color='darkblue', source=sourceday)
    pday.line(y='y4', x='x1', source=sourceday, line_width=1.8, line_color='orange', legend_label='Moving avg')

    ppBand = Band(base='x1', lower='lb', upper='ub', source=sourceday, level='glyph', fill_color='#3b5998',
                fill_alpha=.1, line_width=1, line_color='black')
    pday.add_layout(ppBand)
    pday.yaxis[0].formatter = NumeralTickFormatter(format="$0")

    hoverday = HoverTool(tooltips=[('Date', '@x1{%F}'),('Open','$@y1{0.00}'),('Close','$@y{0.00}'), ('Volume','@y3{0.00 a}'),('PE','@y2{0.00}'), ('Returns','@y5{0.000}')], formatters={'@x1': 'datetime'})
    pday.add_tools(hoverday)


    box_left = pd.to_datetime('2018-07-26')
    box_right = pd.to_datetime('2018-07-31')

    lowest = BoxAnnotation(right=box_right, left=box_left, fill_alpha=.5, fill_color='#CF142B')#00247D
    pday.add_layout(lowest)

    lowestD = Label(x=627, y=415, x_units='screen', y_units='screen',
                         text='2018-07-26', render_mode='css', text_font_size='7pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pday.add_layout(lowestD)
    lowestL = Label(x=620, y=400, x_units='screen', y_units='screen',
                         text='⬇-19.42%', render_mode='css', text_font_size='10pt', text_color='darkred', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6) #←
    pday.add_layout(lowestL)

    pday.title.text_font_size = '15pt'
    pday.legend.click_policy="hide"
    pday.legend.location = 'top_left'
    pday.legend.background_fill_alpha=None
    pday.legend.border_line_alpha = None
    pday.legend.title = '↓ Disable/Enable'
    pday.yaxis.major_label_standoff = -2
    pday.yaxis.major_label_text_font_size = '9.5pt'
    pday.xaxis.major_label_text_font_size = '8.5pt'
    pday.outline_line_color=None
    pday.axis.major_label_text_font_style = 'bold'
    pday.axis.major_label_text_color = '#3b5998'
  
    pday.min_border = 0
    pday.x_range.range_padding = 0
    pday.toolbar.autohide = True
    pday.grid.grid_line_dash = 'dotted'
    pday.grid.grid_line_dash_offset = 5
    pday.grid.grid_line_width = 2
    pday.xaxis.ticker.desired_num_ticks = 10
    pday.xaxis.formatter=DatetimeTickFormatter(months= ['%G']) #days=['%d/%m'], months=['%d/%m'])months= ['%B/%G']
    pday.xaxis.axis_line_color = None
    pday.y_range.start=0


    pdp = figure(title='PE ratio', plot_height=200, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')#, y_axis_label='PE ratio')
    pdp.line(y='y2', x='x1', source=sourceday, line_color='#3b5998', line_width = 1)

    pdp.add_tools(hoverday)
    pdp.yaxis.major_label_standoff = -2
    pdp.yaxis.major_label_text_font_size = '6.5pt'
    pdp.xaxis.major_label_text_font_size = '8.5pt'
    pdp.outline_line_color=None
    pdp.axis.major_label_text_font_style = 'bold'
    pdp.axis.major_label_text_color = '#3b5998'
    pdp.min_border = 0
    pdp.x_range.range_padding = 0
    pdp.toolbar.autohide = True
    pdp.grid.grid_line_dash = 'dotted'
    pdp.grid.grid_line_dash_offset = 5
    pdp.grid.grid_line_width = 2
    pdp.xaxis.ticker.desired_num_ticks = 10
    pdp.xaxis.formatter=DatetimeTickFormatter(months= ['%G'])
  
    pdp.yaxis.minor_tick_line_color = None


    peg1 = Label(x=800, y=125, x_units='screen', y_units='screen',
                         text='Trailing', render_mode='css', text_font_size='7pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdp.add_layout(peg1)

    peg2 = Label(x=800, y=110, x_units='screen', y_units='screen',
                         text='PEG', render_mode='css', text_font_size='12pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdp.add_layout(peg2)

    peg3 = Label(x=800, y=92, x_units='screen', y_units='screen',
                         text='0.44', render_mode='css', text_font_size='14pt', text_color='green', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdp.add_layout(peg3)

    peg4 = Label(x=798, y=82, x_units='screen', y_units='screen',
                         text='2019-12-31', render_mode='css', text_font_size='6pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdp.add_layout(peg4)



    pdr = figure(title='Expected Return', plot_height=200, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')#, y_axis_label='PE ratio')
    pdr.line(y='y5', x='x1', source=sourceday, line_color='#3b5998', line_width = 1)

    pdr.add_tools(hoverday)
    pdr.yaxis.major_label_standoff = -2
    pdr.yaxis.major_label_text_font_size = '6.5pt'
    pdr.xaxis.major_label_text_font_size = '8.5pt'
    pdr.outline_line_color=None
    pdr.axis.major_label_text_font_style = 'bold'
    pdr.axis.major_label_text_color = '#3b5998'
    pdr.min_border = 0
    pdr.x_range.range_padding = 0
    pdr.toolbar.autohide = True
    pdr.grid.grid_line_dash = 'dotted'
    pdr.grid.grid_line_dash_offset = 5
    pdr.grid.grid_line_width = 2
    pdr.xaxis.ticker.desired_num_ticks = 11
    pdr.xaxis.formatter=DatetimeTickFormatter(months= ['%G'])
  
    pdr.yaxis.minor_tick_line_color = None
    pdr.xaxis.visible = False


    cday = column([pday, pdr, pdp], spacing=2)
    cday = gridplot([[cday]], toolbar_location='right', merge_tools=True, sizing_mode='fixed')


    xrw = dfWeekPE['week'].to_list()

    sourcew = ColumnDataSource(data=dict(x=dfWeekPE['week'] ,x1=dfWeekPE['week1'], y=dfWeekPE['Close'], y1=dfWeekPE['Open'], y2=dfWeekPE['PE'], y3=dfWeekPE['Volume'], y4=dfWeekPE['MovingAvg'], y5=dfWeekPE['Returns'], y6=dfWeekPE['MovingAvgReturn'],
                                        ub=dfWeekPE['UB'], lb=dfWeekPE['LB'], sd=dfWeekPE['STD'], pctma=dfWeekPE['pct_ma'], l=dfWeekPE['line']))

    pw = figure(title='Weekly Facebook, Inc.', plot_height=500, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')
    pw.line(y='y', x='x1', source=sourcew, line_width = 1.2, line_color='#3b5998', legend_label='Close')

    pw.line(y='y4', x='x1', source=sourcew, line_width=1.8, line_color='orange', legend_label='Moving avg')

    pwBand = Band(base='x1', lower='lb', upper='ub', source=sourcew, level='glyph', fill_color='#3b5998',
                fill_alpha=.1, line_width=1, line_color='black')
    pw.add_layout(pwBand)



    hoverw = HoverTool(tooltips=[('Date', '@x'),('Open','$@y1{0.00}'),('Close','$@y{0.00}'), ('Volume','@y3{0.00 a}'),('PE','@y2{0.00}'), ('Returns','@y5{0.000}')])
    pw.add_tools(hoverw)
    
    
    box_leftw = pd.to_datetime('2018-07-26')
    box_rightw = pd.to_datetime('2018-07-31')

    lowestw = BoxAnnotation(right=box_rightw, left=box_leftw, fill_alpha=.5, fill_color='#CF142B')#00247D
    pw.add_layout(lowestw)

    lowestwd = Label(x=627, y=415, x_units='screen', y_units='screen',
                         text='2018-07-26', render_mode='css', text_font_size='7pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pw.add_layout(lowestwd)
    lowestLw = Label(x=620, y=400, x_units='screen', y_units='screen',
                         text='⬇-19.42%', render_mode='css', text_font_size='10pt', text_color='darkred', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6) #←
    pw.add_layout(lowestLw)

    pw.title.text_font_size = '15pt'
    pw.legend.click_policy="hide"
    pw.legend.location = 'top_left'
    pw.legend.background_fill_alpha=None
    pw.legend.border_line_alpha = None
    pw.legend.title = '↓ Disable/Enable'
    pw.yaxis.major_label_standoff = -2
    pw.yaxis.major_label_text_font_size = '9.5pt'
    pw.xaxis.major_label_text_font_size = '8.5pt'
    pw.outline_line_color=None
    pw.axis.major_label_text_font_style = 'bold'
    pw.axis.major_label_text_color = '#3b5998'
    pw.min_border = 0
    pw.x_range.range_padding = 0
    pw.toolbar.autohide = True
    pw.grid.grid_line_dash = 'dotted'
    pw.grid.grid_line_dash_offset = 5
    pw.grid.grid_line_width = 2
    pw.xaxis.ticker.desired_num_ticks = 12
    pw.xaxis.formatter=DatetimeTickFormatter(months= ['%b/%g']) #days=['%d/%m'], months=['%d/%m'])months= ['%B/%G']
    pw.xaxis.axis_line_color = None
    pw.y_range.start=0
    pw.yaxis[0].formatter = NumeralTickFormatter(format="$0")




    pdw = figure(title='PE ratio', plot_height=200, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')#, y_axis_label='PE ratio')
    pdw.line(y='y2', x='x1', source=sourcew, line_color='#3b5998', line_width = 1)


    pegw1 = Label(x=800, y=125, x_units='screen', y_units='screen',
                         text='Trailing', render_mode='css', text_font_size='7pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdw.add_layout(pegw1)

    pegw2 = Label(x=800, y=110, x_units='screen', y_units='screen',
                         text='PEG', render_mode='css', text_font_size='12pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdw.add_layout(pegw2)

    pegw3 = Label(x=800, y=92, x_units='screen', y_units='screen',
                         text='0.44', render_mode='css', text_font_size='14pt', text_color='green', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdw.add_layout(pegw3)

    peg4 = Label(x=798, y=82, x_units='screen', y_units='screen',
                         text='2019-12-31', render_mode='css', text_font_size='6pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pdw.add_layout(peg4)

    pdw.add_tools(hoverw)
    pdw.yaxis.major_label_standoff = -2
    pdw.yaxis.major_label_text_font_size = '6.5pt'
    pdw.xaxis.major_label_text_font_size = '8.5pt'
    pdw.outline_line_color=None
    pdw.axis.major_label_text_font_style = 'bold'
    pdw.axis.major_label_text_color = '#3b5998'
    pdw.min_border = 0
    pdw.x_range.range_padding = 0
    pdw.toolbar.autohide = True
    pdw.grid.grid_line_dash = 'dotted'
    pdw.grid.grid_line_dash_offset = 5
    pdw.grid.grid_line_width = 2
    pdw.xaxis.ticker.desired_num_ticks = 12
    pdw.xaxis.formatter=DatetimeTickFormatter(months= ['%b/%g'])
    pdw.yaxis.minor_tick_line_color = None




    pdrw = figure(title='Expected Return', plot_height=200, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')#, y_axis_label='PE ratio')
    pdrw.line(y='y5', x='x1', source=sourcew, line_color='#3b5998', line_width = 1, legend_label='Expected Return')
    pdrw.line(y='y6', x='x1', source=sourcew, line_color='orange', line_width = 1.7, line_alpha=.6, legend_label='E.R. Moving Avg')


    pdrw.legend.click_policy="hide"
    pdrw.legend.location = (0,0)#'bottom_left'
    pdrw.legend.orientation = 'horizontal'
    pdrw.legend.background_fill_alpha=None
    pdrw.legend.border_line_alpha = None
    #pdrw.legend.title = '↓ Disable/Enable'
    pdrw.add_tools(hoverw)
    pdrw.yaxis.major_label_standoff = -2
    pdrw.yaxis.major_label_text_font_size = '6.5pt'
    pdrw.xaxis.major_label_text_font_size = '8.5pt'
    pdrw.outline_line_color=None
    pdrw.axis.major_label_text_font_style = 'bold'
    pdrw.axis.major_label_text_color = '#3b5998'
    pdrw.min_border = 0
    pdrw.x_range.range_padding = 0
    pdrw.toolbar.autohide = True
    pdrw.grid.grid_line_dash = 'dotted'
    pdrw.grid.grid_line_dash_offset = 5
    pdrw.grid.grid_line_width = 2
    pdrw.xaxis.ticker.desired_num_ticks = 12
    pdrw.xaxis.formatter=DatetimeTickFormatter(months= ['%b/%g'])

    pdrw.yaxis.minor_tick_line_color = None
    pdrw.xaxis.visible = False

    wc = column([pw, pdrw, pdw])
    wcg = gridplot([[wc]], toolbar_location='right', merge_tools=True, sizing_mode='fixed')
    
    
    
    
    xrmonth = dfMonthPE['month1'].to_list()

    sourcemonth = ColumnDataSource(data=dict(x=xrmonth ,x1=dfMonthPE['month1'], x2=dfMonthPE['monthN'], y=dfMonthPE['Close'], y1=dfMonthPE['Open'], y2=dfMonthPE['PE'], y3=dfMonthPE['Volume'], y4=dfMonthPE['MovingAvg'], y5=dfMonthPE['Returns'],
                                              y6=dfMonthPE['MovingAvgReturn'], ub=dfMonthPE['UB'], lb=dfMonthPE['LB'], sd=dfMonthPE['STD'], pctma=dfMonthPE['pct_ma']))

    pmon = figure(title='Monthly Facebook, Inc.', plot_height=500, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')
    pmon.line(y='y', x='x1', source=sourcemonth, line_width = 1.2, line_color='#3b5998', legend_label='Close')
        #pday.circle(x='x1', y='y', size=1, color='darkblue', source=sourceday)
    pmon.line(y='y4', x='x1', source=sourcemonth, line_width=1.8, line_color='orange', legend_label='Moving avg')

    pmonBand = Band(base='x1', lower='lb', upper='ub', source=sourcemonth, level='glyph', fill_color='#3b5998',
                fill_alpha=.1, line_width=1, line_color='black')
    pmon.add_layout(pmonBand)
    pmon.yaxis[0].formatter = NumeralTickFormatter(format="$0")

    hovermon = HoverTool(tooltips=[('Month', '@x2'),('Date', '@x1{%F}'),('Open','$@y1{0.00}'),('Close','$@y{0.00}'), ('Volume','@y3{0.00 a}'),('PE','@y2{0.00}'), ('Returns','@y5{0.000}')], formatters={'@x1': 'datetime'})
    pmon.add_tools(hovermon)

    pmon.title.text_font_size = '15pt'
    pmon.legend.click_policy="hide"
    pmon.legend.location = 'top_left'
    pmon.legend.background_fill_alpha=None
    pmon.legend.border_line_alpha = None
    pmon.legend.title = '↓ Disable/Enable'
    pmon.yaxis.major_label_standoff = -2
    pmon.yaxis.major_label_text_font_size = '9.5pt'
    pmon.xaxis.major_label_text_font_size = '8.5pt'
    pmon.outline_line_color=None
    pmon.axis.major_label_text_font_style = 'bold'
    pmon.axis.major_label_text_color = '#3b5998'

    pmon.min_border = 0
    pmon.x_range.range_padding = 0
    pmon.toolbar.autohide = True
    pmon.grid.grid_line_dash = 'dotted'
    pmon.grid.grid_line_dash_offset = 5
    pmon.grid.grid_line_width = 2
    pmon.xaxis.ticker.desired_num_ticks = 10
    pmon.xaxis.formatter=DatetimeTickFormatter(months= ['%G']) #days=['%d/%m'], months=['%d/%m'])months= ['%B/%G']
    pmon.xaxis.axis_line_color = None
    pmon.y_range.start=0

    pdrm = figure(title='Expected Return', plot_height=200, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')#, y_axis_label='PE ratio')
    pdrm.line(y='y5', x='x1', source=sourcemonth, line_color='#3b5998', line_width = 1)
    #pdrm.line(y='y6', x='x1', source=sourcemonth, line_color='orange', line_width = 1.7, line_alpha=.6, legend_label='E.R. Moving Avg')


    pdrm.add_tools(hovermon)
    pdrm.yaxis.major_label_standoff = -2
    pdrm.yaxis.major_label_text_font_size = '6.5pt'
    pdrm.xaxis.major_label_text_font_size = '8.5pt'
    pdrm.outline_line_color=None
    pdrm.axis.major_label_text_font_style = 'bold'
    pdrm.axis.major_label_text_color = '#3b5998'
    pdrm.min_border = 0
    pdrm.x_range.range_padding = 0
    pdrm.toolbar.autohide = True
    pdrm.grid.grid_line_dash = 'dotted'
    pdrm.grid.grid_line_dash_offset = 5
    pdrm.grid.grid_line_width = 2
    pdrm.xaxis.ticker.desired_num_ticks = 12
    pdrm.xaxis.formatter=DatetimeTickFormatter(months= ['%b/%g'])

    pdrm.yaxis.minor_tick_line_color = None
    pdrm.xaxis.visible = False


    pdm = figure(title='PE ratio', plot_height=200, plot_width=950, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')#, y_axis_label='PE ratio')
    pdm.line(y='y2', x='x1', source=sourcemonth, line_color='#3b5998', line_width = 1)


    pegm1 = Label(x=800, y=125, x_units='screen', y_units='screen',
                  text='Trailing', render_mode='css', text_font_size='7pt', text_color='black', text_font_style='bold',
                  text_align='left', angle=0, text_alpha=0.6)
    pdm.add_layout(pegm1)

    pegm2 = Label(x=800, y=110, x_units='screen', y_units='screen',
                  text='PEG', render_mode='css', text_font_size='12pt', text_color='black', text_font_style='bold',
                  text_align='left', angle=0, text_alpha=0.6)
    pdm.add_layout(pegm2)

    pegm3 = Label(x=800, y=92, x_units='screen', y_units='screen',
                  text='0.44', render_mode='css', text_font_size='14pt', text_color='green', text_font_style='bold',
                  text_align='left', angle=0, text_alpha=0.6)
    pdm.add_layout(pegm3)

    pegm4 = Label(x=798, y=82, x_units='screen', y_units='screen',
                  text='2019-12-31', render_mode='css', text_font_size='6pt', text_color='black', text_font_style='bold',
                  text_align='left', angle=0, text_alpha=0.6)
    pdm.add_layout(pegm4)

    pdm.add_tools(hovermon)
    pdm.yaxis.major_label_standoff = -2
    pdm.yaxis.major_label_text_font_size = '6.5pt'
    pdm.xaxis.major_label_text_font_size = '8.5pt'
    pdm.outline_line_color=None
    pdm.axis.major_label_text_font_style = 'bold'
    pdm.axis.major_label_text_color = '#3b5998'
    pdm.min_border = 0
    pdm.x_range.range_padding = 0
    pdm.toolbar.autohide = True
    pdm.grid.grid_line_dash = 'dotted'
    pdm.grid.grid_line_dash_offset = 5
    pdm.grid.grid_line_width = 2
    pdm.xaxis.ticker.desired_num_ticks = 12
    pdm.xaxis.formatter=DatetimeTickFormatter(months= ['%b/%g'])
    pdm.yaxis.minor_tick_line_color = None

    cmon = column([pmon, pdrm, pdm])

    monthGrid = gridplot([[cmon]], toolbar_location='right', merge_tools=True, sizing_mode='fixed')

    t1 = Panel(child=cday, title='Daily')
    t2 = Panel(child=wcg, title='Weekly')
    t3 = Panel(child=monthGrid, title='Monthly')


    tabs = Tabs(tabs=[t2, t1, t3])

    return tabs



def fb_vars():
    
    dfDayPE = pd.read_csv('BokehApp/DataFB/dfDayPE.csv', delimiter=',', index_col=0)
    dfDayPE['date1'] = pd.to_datetime(dfDayPE['date1'], format=('%Y/%m/%d'))


    
    sourcedf = ColumnDataSource(data=dict(x=dfDayPE['day'] ,x1=dfDayPE['date1'], y=dfDayPE['Close'], y1=dfDayPE['Open'], y2=dfDayPE['PE'], y3=dfDayPE['Volume'], y4=dfDayPE['MovingAvg'], y5=dfDayPE['Returns'], y6=dfDayPE['MovingAvgReturn'],
                                        ub=dfDayPE['UB'], lb=dfDayPE['LB'], sd=dfDayPE['STD'], pctma=dfDayPE['pct_ma'], l=dfDayPE['line']))

    histdf, edgesdf = np.histogram(dfDayPE['Close'], density=False, bins=30, range=[50,250])

    dfdf = pd.DataFrame({'closeD': histdf, 'left':edgesdf[:-1], 'right':edgesdf[1:]})
    dfdf['f_close'] = ['%d' % count for count in dfdf['closeD']]
    dfdf['f_interval'] = ['%d to %d' % (left,right) for left, right in zip(dfdf['left'], dfdf['right'])]

    sourcef = ColumnDataSource(dfdf)

    phf = figure( plot_height=200, plot_width=300, title='Close histogram', y_axis_label='Frequency', x_axis_label='Close',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')



    phf.quad(top='closeD', bottom=0, left='left', right='right', source=sourcef,
            fill_color='#3b5998', line_color='lightblue',  hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='#FF0800' )


    hoverphf = HoverTool()
    hoverphf.tooltips=[('Close range', '@f_interval'),('Frequency','@closeD{int}')]
    phf.add_tools(hoverphf)
    phf.xaxis[0].formatter = NumeralTickFormatter(format="$0")


    phf.axis.major_label_text_font_style = 'bold'
    phf.axis.major_label_text_font_size = '8px'
    phf.axis.axis_label_text_font_style = 'bold'



    phf.grid.grid_line_alpha = 0.8
    phf.grid.grid_line_dash = 'dotted'
    phf.grid.grid_line_dash_offset = 5
    phf.grid.grid_line_width = 2
    phf.toolbar.autohide = True
    phf.title.text_font_size = '12px'
    phf.outline_line_color=None

    phf.x_range.range_padding =  0.02
    phf.y_range.start = 0


    pfp = figure(plot_height=250, plot_width=407, title='Close Moving Average deviation in %', 
                    tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime') # ['#b32134', '#e1888f']
    pfp.line(y='pctma', x='x1', line_width=1.5, line_color='#3b5998', source=sourcedf) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]
    pfp.line(y='l', x='x1', line_width=.3, line_color='black', source=sourcedf) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]

    pfp.grid.grid_line_alpha = 0.5
    pfp.grid.grid_line_dash = 'dotted'
    pfp.grid.grid_line_dash_offset = 5
    pfp.grid.grid_line_width = 1
    pfp.toolbar.autohide = True
    pfp.title.text_font_size = '12px'
    pfp.outline_line_color=None

    pfp.x_range.range_padding =  0.02
    pfp.xaxis.axis_line_color = None

    hoverpfp = HoverTool()
    hoverpfp.tooltips=[('Date', '@x'),('Deviation in %','@pctma{0.00}')]
    pfp.add_tools(hoverpfp)

    tick_labelspfp = {'0.06':'0.06%','0.04':'0.04%','0.02':'0.02%','-0.02':'-0.02%','-0.04':'-0.04%','-0.06':'-0.06%'}
    pfp.yaxis.major_label_overrides = tick_labelspfp
    pfp.axis.major_label_text_font_style = 'bold'
    pfp.axis.major_label_text_font_size = '12px'

    wfl = Label(x=80, y=10, x_units='screen', y_units='screen',
                         text='⬇33.14%', render_mode='css', text_font_size='10pt', text_color='darkred', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6) #←
    pfp.add_layout(wfl)

    wfh = Label(x=34, y=25, x_units='screen', y_units='screen',
                         text='66.85%⬆', render_mode='css', text_font_size='10pt', text_color='green', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6) #←

    
    pmdd = figure(x_axis_location = None, y_axis_location = None, plot_width=320, plot_height=130)
    pmdd.image_url(url=['/static/imagesFB/violinD.png'], x=0, y=0, w=2, h=1.2, anchor="bottom_left")
    pmdd.title.align='center'    
    pmdd.grid.grid_line_color=None
    pmdd.outline_line_color=None
    pmdd.toolbar.autohide = True
    
    
    
    pfp.add_layout(wfh)

    dfAmpf = dfDayPE[['Close', 'year']]
    dfAmpf.head()

    dfAmpf['delta'] = np.append(np.array([0]),
                              np.diff(dfAmpf['Close'].values))

    spf = np.fft.fft(dfAmpf['delta'].values)
    spf[:5]

    dfAmpf['theta'] = np.arctan(spf.imag/spf.real)
    lendff = len(dfAmpf)

    lendfHf = lendff/2
    dfAmpf['amp'] = np.sqrt(spf.real**2+spf.imag**2)/lendfHf
    dfAmpf['freq'] =  np.fft.fftfreq(spf.size, d=1)
    dfAmpf['line'] = 0


    size_mapperf=LinearInterpolator(x=[dfAmpf['amp'].min(),dfAmpf['amp'].max()],    y=[2,20])

    pAf = figure(plot_height=310, plot_width=530, title='FFT Close', x_axis_label='frequency', y_axis_label='amplitude($)',
                    tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')

    hoverpAf = HoverTool()
    hoverpAf.tooltips=[('frequency', '@freq{0.000}'),('amplitude','@amp{0.000}'), ('year','@year')]
    pAf.add_tools(hoverpAf)
    pAf.scatter('freq','amp',source=dfAmpf,fill_alpha=0.6, line_width=.2, size={'field':'amp','transform': size_mapperf}, color='#3b5998')
    pAf.y_range.start= 0

    pAf.grid.grid_line_alpha = 1
    pAf.grid.grid_line_dash = 'dotted'
    pAf.grid.grid_line_dash_offset = 5
    pAf.grid.grid_line_width = 4
    pAf.toolbar.autohide = True
    pAf.title.text_font_size = '12px'
    pAf.outline_line_color=None
    pAf.axis.axis_line_color = None

    pAf.axis.major_label_text_font_style = 'bold'
    pAf.axis.major_label_text_font_size = '10px'
    pAf.axis.axis_label_text_font_style = 'bold'
    pAf.title.align = 'center'


    sourcefj = ColumnDataSource(dfDayPE)
    size_mapperfj = LinearInterpolator(x=[dfDayPE['Close'].min(),dfDayPE['Close'].max()],    y=[2,20])
    xrfj = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    colorsfj = GnBu[6][::-1]

    index_cmap = factor_cmap('day', palette=GnBu[6][::-1], 
                             factors=sorted(dfDayPE.day.unique()))


    pfj = figure(y_range=xrfj[::-1], plot_width=815, plot_height=350, title='Price per share')
    pfj.circle(x='Close', y=jitter('day', width=1, range=pfj.y_range), source=sourcefj, alpha=.4, size={'field':'Close','transform': size_mapperfj},
              color=index_cmap, line_color='black', line_width=.2)

    pfj.x_range.range_padding = .04
    pfj.y_range.range_padding = .08

    pfj.grid.grid_line_alpha = .2
    pfj.grid.grid_line_dash = 'dotted'
    pfj.grid.grid_line_dash_offset = 5
    pfj.grid.grid_line_width = 2

    pfj.grid.grid_line_color = 'black'
    pfj.toolbar.autohide = True
    pfj.title.text_font_size = '16px'
    pfj.outline_line_color=None
    pfj.axis.axis_line_color = None

    pfj.axis.major_label_text_font_style = 'bold'
    pfj.axis.major_label_text_font_size = '12px'
    pfj.axis.axis_label_text_font_style = 'bold'
    pfj.title.align = 'center'
    pfj.xaxis[0].formatter = NumeralTickFormatter(format="$0")

    
    hoverfj = HoverTool(tooltips=[('Close', '@Close{0.000}'),('day','@day'), ('date','@date1{%F}')], formatters={'@date1': 'datetime'})

    pfj.add_tools(hoverfj)



    pVf = figure(plot_height=250, plot_width=408, title='Volume trading',
                    tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')

    size_mapperVf=LinearInterpolator(x=[dfDayPE['Volume'].min(),dfDayPE['Volume'].max()], y=[1,10])

    sourceVf = ColumnDataSource(data=dict(x=dfDayPE['date1'], x1=dfDayPE['day'], y=dfDayPE['Volume'],
                                         y1=dfDayPE['Volume'].rolling(window=21).mean(), y2=dfDayPE['Volume'].rolling(window=21).std()))

    pVf.line(x='x', y='y2', line_color='black', line_width=3, source=sourceVf, legend_label='Moving std.')
    pVf.line(x='x', y='y1', line_color='orange', line_width=3, source=sourceVf, legend_label='Moving avg.')
    pVf.circle(x='x', y='y', fill_alpha=.6, line_color='#3b5998', line_width=.2, source=sourceVf, size={'field':'y','transform':size_mapperVf})


    hoverpVf = HoverTool()
    hoverpVf.tooltips=[('Date', '@x1'),('Volume','@y{0.0 a}'),('Moving avg','@y1{0.0 a}'), ('Moving std','@y2{0.0 a}')]
    pVf.add_tools(hoverpVf)
    pVf.xaxis.ticker.desired_num_ticks = 8
    pVf.yaxis.formatter.use_scientific = False

    tick_labelsVf = {'100000000':'100M','50000000':'50M','150000000':'150M'}
    pVf.yaxis.major_label_overrides = tick_labelsVf

    pVf.legend.background_fill_alpha = None
    pVf.legend.border_line_color = None
    pVf.legend.label_text_font_size = '11px'
    pVf.legend.click_policy="hide"
    
    pVf.grid.grid_line_alpha = 1
    pVf.grid.grid_line_dash = 'dotted'
    pVf.grid.grid_line_dash_offset = 5
    pVf.grid.grid_line_width = 4
    pVf.toolbar.autohide = True
    pVf.title.text_font_size = '16px'
    pVf.outline_line_color=None
    pVf.axis.axis_line_color = None

    pVf.axis.major_label_text_font_style = 'bold'
    pVf.axis.major_label_text_font_size = '10px'
    pVf.axis.axis_label_text_font_style = 'bold'
    pVf.title.align = 'left'

    pVf.x_range.range_padding = .04
    pVf.y_range.range_padding = .2



    wrf = column([phf, pmdd], spacing= -10)
    wr1f = row([wrf, pAf], spacing=10)
    wrr1 = row([pVf, pfp])
    cwrf = column([pfj, wr1f, wrr1])
    dayGrid = gridplot([[cwrf]], toolbar_location='right', merge_tools=True)#, sizing_mode='fixed' )
    

    dfWeekPE = pd.read_csv('BokehApp/DataFB/dfWeekPE.csv', delimiter=',', index_col=0)
    dfWeekPE['week1'] = pd.to_datetime(dfWeekPE['week1'], format=('%Y/%m/%d'))

    
    sourcew = ColumnDataSource(data=dict(x=dfWeekPE['week'] ,x1=dfWeekPE['week1'], y=dfWeekPE['Close'], y1=dfWeekPE['Open'], y2=dfWeekPE['PE'], y3=dfWeekPE['Volume'], y4=dfWeekPE['MovingAvg'], y5=dfWeekPE['Returns'], y6=dfWeekPE['MovingAvgReturn'],
                                        ub=dfWeekPE['UB'], lb=dfWeekPE['LB'], sd=dfWeekPE['STD'], pctma=dfWeekPE['pct_ma'], l=dfWeekPE['line']))

    histw, edgesw = np.histogram(dfWeekPE['Close'], density=False, bins=30, range=[50,250])

    dfhw = pd.DataFrame({'closeW': histw, 'left':edgesw[:-1], 'right':edgesw[1:]})
    dfhw['f_close'] = ['%d' % count for count in dfhw['closeW']]
    dfhw['f_interval'] = ['%d to %d' % (left,right) for left, right in zip(dfhw['left'], dfhw['right'])]

    sourcehw = ColumnDataSource(dfhw)

    phw = figure( plot_height=200, plot_width=300, title='Close histogram', y_axis_label='Frequency',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')



    phw.quad(top='closeW', bottom=0, left='left', right='right', source=sourcehw,
            fill_color='#3b5998', line_color='lightblue',  hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='#FF0800' )


    hoverphw = HoverTool()
    hoverphw.tooltips=[('Close range', '@f_interval'),('Frequency','@closeW{int}')]
    phw.add_tools(hoverphw)


    phw.axis.major_label_text_font_style = 'bold'
    phw.axis.major_label_text_font_size = '8px'
    phw.axis.axis_label_text_font_style = 'bold'



    phw.grid.grid_line_alpha = 0.8
    phw.grid.grid_line_dash = 'dotted'
    phw.grid.grid_line_dash_offset = 5
    phw.grid.grid_line_width = 2
    phw.toolbar.autohide = True
    phw.title.text_font_size = '12px'
    phw.outline_line_color=None

    phw.x_range.range_padding =  0.02
    phw.y_range.start = 0
    phw.xaxis[0].formatter = NumeralTickFormatter(format="$0")



    pwp = figure(plot_height=250, plot_width=407, title='Close Moving Average deviation in %', 
                    tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime') # ['#b32134', '#e1888f']
    pwp.line(y='pctma', x='x1', line_width=1.5, line_color='#3b5998', source=sourcew) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]
    pwp.line(y='l', x='x1', line_width=.3, line_color='black', source=sourcew) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]

    pwp.grid.grid_line_alpha = 0.5
    pwp.grid.grid_line_dash = 'dotted'
    pwp.grid.grid_line_dash_offset = 5
    pwp.grid.grid_line_width = 1
    pwp.toolbar.autohide = True
    pwp.title.text_font_size = '12px'
    pwp.outline_line_color=None

    pwp.x_range.range_padding =  0.02
    pwp.xaxis.axis_line_color = None

    hoverpwp = HoverTool()
    hoverpwp.tooltips=[('Date', '@x'),('Deviation in %','@pctma{0.00}')]
    pwp.add_tools(hoverpwp)

    tick_labelspwp = {'0.06':'0.06%','0.04':'0.04%','0.02':'0.02%','-0.02':'-0.02%','-0.04':'-0.04%','-0.06':'-0.06%'}
    pwp.yaxis.major_label_overrides = tick_labelspwp
    pwp.axis.major_label_text_font_style = 'bold'
    pwp.axis.major_label_text_font_size = '12px'


    wml = Label(x=80, y=10, x_units='screen', y_units='screen',
                         text='⬇33.14%', render_mode='css', text_font_size='10pt', text_color='darkred', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6) #←
    pwp.add_layout(wml)

    wmh = Label(x=34, y=25, x_units='screen', y_units='screen',
                         text='66.85%⬆', render_mode='css', text_font_size='10pt', text_color='green', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6) #←

    pwp.add_layout(wmh)

    dfAmp = dfWeekPE[['Close','year']]
    dfAmp.head()

    dfAmp['delta'] = np.append(np.array([0]),
                              np.diff(dfAmp['Close'].values))

    sp = np.fft.fft(dfAmp['delta'].values)
    sp[:5]

    dfAmp['theta'] = np.arctan(sp.imag/sp.real)
    lendf = len(dfAmp)

    lendfH = lendf/2
    dfAmp['amp'] = np.sqrt(sp.real**2+sp.imag**2)/lendfH
    dfAmp['freq'] =  np.fft.fftfreq(sp.size, d=1)
    dfAmp['line'] = 0


    size_mapper=LinearInterpolator(x=[dfAmp['amp'].min(),dfAmp['amp'].max()],    y=[2,20])

    pA = figure(plot_height=310, plot_width=530, title='FFT Close', x_axis_label='frequency', y_axis_label='amplitude($)',
                    tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')

    hoverpA = HoverTool()
    hoverpA.tooltips=[('frequency', '@freq{0.000}'),('amplitude','@amp{0.000}'), ('year','@year')]
    pA.add_tools(hoverpA)
    pA.scatter('freq','amp',source=dfAmp,fill_alpha=0.6, line_width=.2, size={'field':'amp','transform': size_mapper}, color='#3b5998')
    pA.y_range.start= 0

    pA.grid.grid_line_alpha = 1
    pA.grid.grid_line_dash = 'dotted'
    pA.grid.grid_line_dash_offset = 5
    pA.grid.grid_line_width = 4
    pA.toolbar.autohide = True
    pA.title.text_font_size = '12px'
    pA.outline_line_color=None
    pA.axis.axis_line_color = None

    pA.axis.major_label_text_font_style = 'bold'
    pA.axis.major_label_text_font_size = '10px'
    pA.axis.axis_label_text_font_style = 'bold'
    pA.title.align = 'center'

    pwv = figure(x_axis_location = None, y_axis_location = None, plot_width=320, plot_height=130)
    pwv.image_url(url=['/static/imagesFB/violinW.png'], x=0, y=0, w=2, h=1.2, anchor="bottom_left")
    pwv.title.align='center'    
    pwv.grid.grid_line_color=None
    pwv.outline_line_color=None
    pwv.toolbar.autohide = True

    dfWeekJ = dfWeekPE[['weekN','Close', 'week1','Volume', 'year']]
    dfWeekJ['weekNum'] = dfWeekJ['weekN'].apply(str) + ' week'

    sourcewj = ColumnDataSource(dfWeekJ)
    size_mapperwj = LinearInterpolator(x=[dfWeekJ['Close'].min(),dfWeekJ['Close'].max()],  y=[3,30])
    xrwj = list(dfWeekJ.weekN.unique())
    xrwj = sorted(xrwj)
   

    colorswj = viridis(len(dfWeekJ.weekNum.unique()))


    pwj = figure(y_range=(-3,59), plot_width=815, plot_height=350, title='Price per share', y_axis_label='week', x_axis_label='Share price($)')
    pwj.circle(y='weekN', x=jitter('Close', width=1, range=pwj.x_range), source=sourcewj, alpha=.4, size={'field':'Close','transform': size_mapperwj}, color='#3b5998')
   
    hoverwj = HoverTool()
    hoverwj.tooltips=[('Close', '@Close{0.000}'),('week','@weekN'), ('year','@year')]
    pwj.add_tools(hoverwj)

    pwj.grid.grid_line_alpha = .1
    pwj.grid.grid_line_dash = 'dotted'
    pwj.grid.grid_line_dash_offset = 5
    pwj.grid.grid_line_width = 2

    pwj.grid.grid_line_color = 'black'
    pwj.toolbar.autohide = True
    pwj.title.text_font_size = '16px'
    pwj.outline_line_color=None
    pwj.axis.axis_line_color = None

    pwj.axis.major_label_text_font_style = 'bold'
    pwj.axis.major_label_text_font_size = '10px'

    pwj.axis.axis_label_text_font_style = 'bold'
    pwj.title.align = 'center'
    pwj.axis.axis_label_text_font_style = 'bold'
    pwj.xaxis[0].formatter = NumeralTickFormatter(format="$0")


    pV = figure(plot_height=250, plot_width=408, title='Volume trading',
                    tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')

    size_mapperV=LinearInterpolator(x=[dfWeekPE['Volume'].min(),dfWeekPE['Volume'].max()], y=[2,20])

    sourceV = ColumnDataSource(data=dict(x=dfWeekPE['week1'], x1=dfWeekPE['week'], y=dfWeekPE['Volume'],
                                         y1=dfWeekPE['Volume'].rolling(window=21).mean(), y2=dfWeekPE['Volume'].rolling(window=21).std()))

    #pV.scatter('freq','amp',source=dfV,fill_alpha=0.6, size=5, color='#3b5998')
    pV.line(x='x', y='y1', line_color='black', line_width=1.5, source=sourceV, legend_label='Moving std.')
    pV.line(x='x', y='y2', line_color='orange', line_width=1.5, source=sourceV, legend_label='Moving avg.')
    pV.circle(x='x', y='y', fill_alpha=.5, line_color='#3b5998', line_width=.2, source=sourceV, size={'field':'y','transform':size_mapperV})


    hoverpV = HoverTool()
    hoverpV.tooltips=[('Date', '@x1'),('Volume','@y{0.0 a}'),('Moving avg','@y1{0.0 a}'), ('Moving std','@y2{0.0 a}')]
    pV.add_tools(hoverpV)
    pV.xaxis.ticker.desired_num_ticks = 8
    pV.yaxis.formatter.use_scientific = False

    tick_labelsV = {'100000000':'100M','200000000':'200M','300000000':'300M','400000000':'400M','500000000':'500M'}
    pV.yaxis.major_label_overrides = tick_labelsV

    pV.legend.background_fill_alpha = None
    pV.legend.border_line_color = None
    pV.legend.label_text_font_size = '11px'
    pV.legend.click_policy="hide"
 

    pV.grid.grid_line_alpha = 1
    pV.grid.grid_line_dash = 'dotted'
    pV.grid.grid_line_dash_offset = 5
    pV.grid.grid_line_width = 4
    pV.toolbar.autohide = True
    pV.title.text_font_size = '12px'
    pV.outline_line_color=None
    pV.axis.axis_line_color = None

    pV.axis.major_label_text_font_style = 'bold'
    pV.axis.major_label_text_font_size = '10px'
    pV.axis.axis_label_text_font_style = 'bold'
    pV.title.align = 'left'

    pV.x_range.range_padding = .04
    pV.y_range.range_padding = .2
    
    
    dfMonthPE = pd.read_csv('BokehApp/DataFB/dfMonthPE.csv', delimiter=',', index_col=0)
    dfMonthPE['month1'] = pd.to_datetime(dfMonthPE['month1'], format=('%Y/%m/%d'))




    sourcemonth = ColumnDataSource(data=dict(x=dfMonthPE.index, x1=dfMonthPE['month1'], x2=dfMonthPE['monthN'], y=dfMonthPE['Close'], y1=dfMonthPE['Open'], y2=dfMonthPE['PE'], y3=dfMonthPE['Volume'], y4=dfMonthPE['MovingAvg'], y5=dfMonthPE['Returns'], y6=dfMonthPE['MovingAvgReturn'],
                                            ub=dfMonthPE['UB'], lb=dfMonthPE['LB'], sd=dfMonthPE['STD'], pctma=dfMonthPE['pct_ma'], l=dfMonthPE['line']))

    histm, edgesm = np.histogram(dfMonthPE['Close'], density=False, bins=25, range=[50,250])

    dfhm = pd.DataFrame({'closeM': histm, 'left':edgesm[:-1], 'right':edgesm[1:]})
    dfhm['f_close'] = ['%d' % count for count in dfhm['closeM']]
    dfhm['f_interval'] = ['%d to %d' % (left,right) for left, right in zip(dfhm['left'], dfhm['right'])]

    sourcehm = ColumnDataSource(dfhm)

    phm = figure(plot_height=200, plot_width=300, title='Close histogram', y_axis_label='Frequency',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right') # x_axis_label='Close',



    phm.quad(top='closeM', bottom=0, left='left', right='right', source=sourcehm,
            fill_color='#3b5998', line_color='lightblue',  hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='#FF0800' )


    hoverphm = HoverTool()
    hoverphm.tooltips=[('Close range', '@f_interval'),('Frequency','@closeM{int}')]
    phm.add_tools(hoverphm)


    phm.axis.major_label_text_font_style = 'bold'
    phm.axis.major_label_text_font_size = '7px'
    phm.axis.axis_label_text_font_style = 'bold'



    phm.grid.grid_line_alpha = 0.8
    phm.grid.grid_line_dash = 'dotted'
    phm.grid.grid_line_dash_offset = 5
    phm.grid.grid_line_width = 2
    phm.toolbar.autohide = True
    phm.title.text_font_size = '12px'
    phm.outline_line_color=None

    phm.x_range.range_padding =  0.02
    phm.y_range.start = 0
    phm.xaxis[0].formatter = NumeralTickFormatter(format="$0")

    pmp = figure(plot_height=250, plot_width=407, title='Close Moving Average deviation in %', 
                        tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime') # ['#b32134', '#e1888f']
    pmp.line(y='pctma', x='x1', line_width=1.5, line_color='#3b5998', source=sourcemonth) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]
    pmp.line(y='l', x='x1', line_width=.3, line_color='black', source=sourcemonth) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]

    pmp.grid.grid_line_alpha = 1
    pmp.grid.grid_line_dash = 'dotted'
    pmp.grid.grid_line_dash_offset = 5
    pmp.grid.grid_line_width = 2
    pmp.toolbar.autohide = True
    pmp.title.text_font_size = '12px'
    pmp.outline_line_color=None

    pmp.x_range.range_padding =  0.02
    pmp.xaxis.axis_line_color = None

    hoverpmp = HoverTool()
    hoverpmp.tooltips=[('Date', '@x'),('Month','@x2'),('Deviation','@pctma{0.00 %}')]
    pmp.add_tools(hoverpmp)

    tick_labelspmp = {'0.06':'0.06%','0.04':'0.04%','0.02':'0.02%','-0.02':'-0.02%','-0.04':'-0.04%','-0.06':'-0.06%'}
    pmp.yaxis.major_label_overrides = tick_labelspmp
    pmp.axis.major_label_text_font_style = 'bold'
    pmp.axis.major_label_text_font_size = '12px'


    dfAmpM = dfMonthPE[['Close', 'year']]
    dfAmpM.head()
    dfAmpM['delta'] = np.append(np.array([0]),
                                  np.diff(dfAmpM['Close'].values))

    spM = np.fft.fft(dfAmpM['delta'].values)
    spM[:5]

    dfAmpM['theta'] = np.arctan(spM.imag/spM.real)
    lendfM = len(dfAmpM)

    lendfHM = lendfM/2
    dfAmpM['amp'] = np.sqrt(spM.real**2+spM.imag**2)/lendfHM
    dfAmpM['freq'] =  np.fft.fftfreq(spM.size, d=1)
    dfAmpM['line'] = 0

    yAM = ['2014','2015','2016','2017','2018','2019','2020']
    #xAM = for m, y in zip(yAM, dfAmpM['Year'])
    cAM = GnBu[7][::-1]

    cmapAM = factor_cmap('year', palette=cAM, factors=yAM )

    size_mapperM=LinearInterpolator(x=[dfAmpM['amp'].min(),dfAmpM['amp'].max()],    y=[2,20])

    pAM = figure(plot_height=310, plot_width=530, title='FFT Close', x_axis_label='frequency', y_axis_label='amplitude($)',
                        tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')

    hoverpAM = HoverTool()
    hoverpAM.tooltips=[('frequency', '@freq{0.000}'),('amplitude','@amp{0.000}'), ('year','@year')]
    pAM.add_tools(hoverpAM)
    pAM.scatter('freq','amp',source=dfAmpM,fill_alpha=0.6, line_width=.2, size={'field':'amp','transform': size_mapperM},
                color='#3b5998')
    pAM.y_range.start= 0

    pAM.grid.grid_line_alpha = 1
    pAM.grid.grid_line_dash = 'dotted'
    pAM.grid.grid_line_dash_offset = 5
    pAM.grid.grid_line_width = 4
    pAM.toolbar.autohide = True
    pAM.title.text_font_size = '12px'
    pAM.outline_line_color=None
    pAM.axis.axis_line_color = None

    pAM.axis.major_label_text_font_style = 'bold'
    pAM.axis.major_label_text_font_size = '10px'
    pAM.axis.axis_label_text_font_style = 'bold'
    pAM.axis.axis_label_text_font_size = '11.5px'
    pAM.title.align = 'center'


    pmv = figure(x_axis_location = None, y_axis_location = None, plot_width=320, plot_height=130)
    pmv.image_url(url=['/static/imagesFB/violinM.png'], x=0, y=0, w=2, h=1.2, anchor="bottom_left")
    pmv.title.align='center'    
    pmv.grid.grid_line_color=None
    pmv.outline_line_color=None
    pmv.toolbar.autohide = True


    dfMonthJ = pd.read_csv('BokehApp/DataFB/dfMonthJ.csv', index_col=0, delimiter=',')

    sourcemj = ColumnDataSource(dfMonthJ)
    size_mappermj = LinearInterpolator(x=[dfMonthJ['Close'].min(),dfMonthJ['Close'].max()],  y=[3,30])
    xrmj = list(dfMonthJ.monthN.unique())
    xrmj = [ 'January', 'February', 'March', 'April','May', 'June', 'July', 'August','September', 'October', 'November', 'December']
    xmjc = GnBu[8][::-1]
    xmjy = ['2014','2015','2016','2017','2018','2019','2020']
    xcmap = factor_cmap('monthN', palette=xmjc, factors=xrmj )

    pmj = figure(y_range=xrmj[::-1], plot_width=815, plot_height=350, title='Price per share')
    pmj.circle(y='monthN', x=jitter('Close', width=1, range=pmj.x_range), source=sourcemj, alpha=.7, size={'field':'Close','transform': size_mappermj},
               color='#3b5998')#xcmap)

    hovermj = HoverTool()
    hovermj.tooltips=[('Close', '@Close{0.000}'),('month','@monthN'), ('year','@year')]
    pmj.add_tools(hovermj)

    pmj.grid.grid_line_alpha = .1
    pmj.grid.grid_line_dash = 'dotted'
    pmj.grid.grid_line_dash_offset = 5
    pmj.grid.grid_line_width = 2

    pmj.grid.grid_line_color = 'black'
    pmj.toolbar.autohide = True
    pmj.title.text_font_size = '16px'
    pmj.outline_line_color=None
    pmj.axis.axis_line_color = None

    pmj.axis.major_label_text_font_style = 'bold'
    pmj.axis.major_label_text_font_size = '10px'
    pmj.yaxis.major_label_text_font_size = '12px'


    pmj.axis.axis_label_text_font_style = 'bold'
    pmj.title.align = 'center'
    pmj.axis.axis_label_text_font_style = 'bold'
    pmj.xaxis[0].formatter = NumeralTickFormatter(format="$0")
    


    pVm = figure(plot_height=250, plot_width=408, title='Volume trading',
                    tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')

    size_mapperVm=LinearInterpolator(x=[dfMonthPE['Volume'].min(),dfMonthPE['Volume'].max()], y=[2,20])

    sourceVm = ColumnDataSource(data=dict(x=dfMonthPE['month1'], x1=dfMonthPE['monthN'], y=dfMonthPE['Volume'],
                                             y1=dfMonthPE['Volume'].rolling(window=2).mean(), y2=dfMonthPE['Volume'].rolling(window=2).std()))

    pVm.line(x='x', y='y1', line_color='black', line_width=1.5, source=sourceVm, legend_label='Moving avg.')
    pVm.line(x='x', y='y2', line_color='orange', line_width=1.5, source=sourceVm, legend_label='Moving std.')
    pVm.circle(x='x', y='y', fill_alpha=.7, line_color='black', line_width=.2, source=sourceVm, size={'field':'y','transform':size_mapperVm})


    hoverpVm = HoverTool()
    hoverpVm.tooltips=[('Date', '@x1'),('Volume','@y{0.0 a}'),('Moving avg','@y1{0.0 a}'), ('Moving std','@y2{0.0 a}')]
    pVm.add_tools(hoverpVm)
    pVm.xaxis.ticker.desired_num_ticks = 8
    pVm.yaxis.formatter.use_scientific = False

    tick_labelsVm = {'100000000':'100M','200000000':'200M','300000000':'300M','400000000':'400M','500000000':'500M'}
    pVm.yaxis.major_label_overrides = tick_labelsVm

    pVm.legend.background_fill_alpha = None
    pVm.legend.border_line_color = None
    pVm.legend.label_text_font_size = '11px'
    pVm.legend.click_policy="hide"


    pVm.grid.grid_line_alpha = 1
    pVm.grid.grid_line_dash = 'dotted'
    pVm.grid.grid_line_dash_offset = 5
    pVm.grid.grid_line_width = 4
    pVm.toolbar.autohide = True
    pVm.title.text_font_size = '12px'
    pVm.outline_line_color=None
    pVm.axis.axis_line_color = None

    pVm.axis.major_label_text_font_style = 'bold'
    pVm.axis.major_label_text_font_size = '10px'
    pVm.axis.axis_label_text_font_style = 'bold'
    pVm.title.align = 'left'

    pVm.x_range.range_padding = .04
    pVm.y_range.range_padding = .2
    pVm.yaxis[0].formatter = NumeralTickFormatter(format='0.00 a')

    mr = column([phm, pmv], spacing=-5)
    mr1a = row([mr, pAM], spacing=-15)
    #mr1 = row([mr1a, pAM])
    mr1b = row([pVm, pmp])
    mr2 = column([pmj, mr1a, mr1b])
    monthGrid = gridplot([[mr2]], toolbar_location='right', merge_tools=True)



    wr = column([phw, pwv])
    wr1 = row([wr, pA])
    cwr = row([pV, pwp])
    cwr1 = column([pwj, wr1, cwr])
    weekGrid = gridplot([[cwr1]], toolbar_location='right', merge_tools=True)#, sizing_mode='fixed' )

    t1 = Panel(child=dayGrid, title='Daily')
    t2 = Panel(child=weekGrid, title='Weekly')
    t3 = Panel(child=monthGrid, title='Monthly')


    tabs = Tabs(tabs=[t2, t1,t3])

    return tabs





def heatmaps():
    dfdv1 = pd.read_csv('BokehApp/DataFB/dfdv1.csv', index_col=0, delimiter=',')

    xv = (7.5,23.5)
    yv = list(reversed(dfdv1.day.unique()))
    colorsv = OrRd[8][::-1]
    mapperv = LinearColorMapper(palette=colorsv, low=170.5, high=180.5)
    formatterv = NumeralTickFormatter(format="$0")

    cbtlv = {'600000000':'0.6B','800000000':'0.8B','1000000000':'1B','1200000000':'1.2B','1400000000':'1.4B','1600000000':'1.6B'}

    ptv = figure(title='Median share price per hour', x_range=xv, y_range=yv, x_axis_location='below',
                plot_width=900, plot_height=350, tools='pan, wheel_zoom, box_zoom, reset',
                 toolbar_location='right', x_axis_label='hour')
    ptv.rect(x='hour', y='day', width=1, height=1, source=dfdv1,
            fill_color={'field':'Close','transform': mapperv}, line_color='darkblue', line_width=.1, line_dash='dashed')

    color_barv = ColorBar(color_mapper=mapperv, major_label_text_font_size="10px", major_label_text_font_style='bold',
                        ticker=(BasicTicker(desired_num_ticks=len(colorsv))), formatter=formatterv, major_label_overrides=cbtlv,
                        label_standoff=10, border_line_color=None, location=(0, 0))
    ptv.add_layout(color_barv, 'right')

    hovertv = HoverTool()
    hovertv.tooltips=[('Hour', '@hour'), ('day', '@day'),('Close', '@Close{0.00 a}')]
    ptv.add_tools(hovertv)

    ptv.axis[0].formatter.use_scientific = False
    ptv.title.text_font_size = '13pt'

    ptv.yaxis.major_label_standoff = -1
    ptv.yaxis.major_label_text_font_size = '9.5pt'
    ptv.xaxis.major_label_text_font_size = '8.5pt'
    ptv.outline_line_color=None
    ptv.axis.major_label_text_font_style = 'bold'
    ptv.axis.axis_line_alpha= 0
    ptv.xaxis.axis_label_text_font_style = 'bold'

    ptv.min_border = None
    ptv.toolbar.autohide = True
    ptv.grid.grid_line_dash = 'dotted'

    ptv.grid.grid_line_dash_offset = 5
    ptv.grid.grid_line_width = 2

    dfdt = pd.read_csv('BokehApp/DataFB/dfdt.csv', delimiter=',', index_col=0)

    xt = (7.5,23.5)
    yt = list(reversed(dfdt.day.unique()))
    colorst = OrRd[7][::-1]
    mappert = LinearColorMapper(palette=colorst, low=int(dfdt.Volume.median()), high=int(dfdt.Volume.max()))
    formatter = PrintfTickFormatter(format='%0f')

    cbtl = {'400000000':'0.4B','600000000':'0.6B','800000000':'0.8B','1000000000':'1B','1200000000':'1.2B','1400000000':'1.4B','1600000000':'1.6B'}

    pth = figure(title='Volume per hour', x_range=xt, y_range=yt, x_axis_location='below',
                plot_width=900, plot_height=350, tools='pan, wheel_zoom, box_zoom, reset',
                 toolbar_location='right', x_axis_label='hour')
    pth.rect(x='hour', y='day', width=1, height=1, source=dfdt,
            fill_color={'field':'Volume','transform': mappert}, line_color='darkblue', line_width=.1, line_dash='dashed')

    color_bart = ColorBar(color_mapper=mappert, major_label_text_font_size="10px", major_label_text_font_style='bold',
                        ticker=(BasicTicker(desired_num_ticks=len(colorst))), formatter=formatter, major_label_overrides=cbtl,
                        label_standoff=10, border_line_color=None, location=(0, 0))
    pth.add_layout(color_bart, 'right')

    hoverth = HoverTool()
    hoverth.tooltips=[('Hour', '@hour'), ('day', '@day'),('Volume', '@Volume{0.00 a}')]
    pth.add_tools(hoverth)

    pth.axis[0].formatter.use_scientific = False
    pth.title.text_font_size = '13pt'

    pth.yaxis.major_label_standoff = -1
    pth.yaxis.major_label_text_font_size = '9.5pt'
    pth.xaxis.major_label_text_font_size = '8.5pt'
    pth.outline_line_color=None
    pth.axis.major_label_text_font_style = 'bold'
    pth.axis.axis_line_alpha= 0

    pth.min_border = None
    pth.toolbar.autohide = True
    pth.grid.grid_line_dash = 'dotted'

    pth.grid.grid_line_dash_offset = 5
    pth.grid.grid_line_width = 2

    
    

    
    dfdh = pd.read_csv('BokehApp/DataFB/dfdh.csv', delimiter=',', index_col=0)
    
    xhd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    sourceHD = ColumnDataSource(dfdh)
    colorshd = GnBu[9][::-1]

    phd = figure( title='Median share price per hour', plot_width=900, plot_height=350, x_range=(8,23),
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_label='Hours')


    phd.title.text_font_size = '20px'
    phd.line(x='hour', y='Monday', width=1, source=sourceHD, line_color='#0868ac', line_width=1.5, legend_label='Monday')
            #hover_line_alpha=1.0, hover_line_color='red')
    phd.line(x='hour', y='Tuesday', width=1, source=sourceHD, line_dash='dotdash',line_color='#43a2ca', line_width=3, legend_label='Tuesday')
    phd.line(x='hour', y='Wednesday', width=1, source=sourceHD, line_dash='dashdot',line_color='#7bccc4', line_width=3, legend_label='Wednesday')
    phd.line(x='hour', y='Thursday', width=1, source=sourceHD, line_dash='dotted', line_color='#bae4bc', line_width=3, legend_label='Thursday')
    phd.line(x='hour', y='Friday', width=1, source=sourceHD, line_dash='dashed',line_color='#4eb3d3', line_width=1.5, legend_label='Friday')



    hoverhd = HoverTool(show_arrow=False,
                          line_policy='nearest')
    hoverhd.tooltips=[('Hour', '@hour'), ('Monday', '@Monday{0.00$}'),('Tuesday', '@Tuesday{0.00$}'),
                     ('Wednesday', '@Wednesday{0.00$}'), ('Thursday', '@Thursday{0.00$}'), ('Friday', '@Friday{0.00$}')]
    phd.add_tools(hoverhd)


    phd.legend.border_line_color = 'black'
    phd.legend.border_line_width = .2
    phd.axis.major_label_text_font_style = 'bold'

    phd.title.text_font_size = '13pt'
    phd.legend.click_policy="hide"
    phd.legend.location = 'top_right'
    #phd.legend.background_fill_alpha=None
    phd.legend.border_line_alpha = None
    phd.legend.title = '↓ Disable/Enable'
    phd.yaxis.major_label_standoff = -2
    phd.yaxis.major_label_text_font_size = '9.5pt'
    phd.xaxis.major_label_text_font_size = '8.5pt'
    #p1.grid.grid_line_color=None
    phd.outline_line_color=None
    #p1.yaxis.major_label_text_align = 'center'
    phd.axis.major_label_text_font_style = 'bold'
    phd.axis.major_label_text_color = '#3b5998'

    phd.min_border = 0
    phd.toolbar.autohide = True
    phd.grid.grid_line_dash = 'dotted'

    phd.grid.grid_line_dash_offset = 5
    phd.grid.grid_line_width = 2

    phd.legend.orientation = 'horizontal'
    phd.yaxis[0].formatter = NumeralTickFormatter(format="$0")
    phd.axis.major_label_text_font_style = 'bold'

    dfhcs = pd.read_csv('BokehApp/DataFB/dfhcs.csv', delimiter=',', index_col=0)

    wnum = sorted(list(dfhcs.weekNum.unique()))
    ynum = sorted(list(dfhcs.year.unique().astype(str)))
    chc = OrRd[7][::-1]
    mapperwy = LinearColorMapper(palette=chc, low=60, high=230)
    forwy = NumeralTickFormatter(format='$0')

    pwy = figure(title='Median share price per week', x_range=wnum, y_range=(2013.5,2020.5), x_axis_location='below',
                    plot_width=900, plot_height=350, tools='pan, wheel_zoom, box_zoom, reset',
                     toolbar_location='right')

    pwy.rect(x='weekNum', y='year', width=1, height=1, source=dfhcs,
            fill_color={'field':'Close','transform': mapperwy}, line_color='darkblue', line_width=.1, line_dash='dashed')

    color_barwy = ColorBar(color_mapper=mapperwy, major_label_text_font_size="10px", major_label_text_font_style='bold',
                        ticker=(BasicTicker(desired_num_ticks=len(chc))), formatter=forwy,
                        label_standoff=10, border_line_color=None, location=(0, 0))
    pwy.add_layout(color_barwy, 'right')

    hovertwy = HoverTool()
    hovertwy.tooltips=[('week', '@weekNum'), ('year','@year'),('Close', '@Close{0.00 a}')]
    pwy.add_tools(hovertwy)

    #pwy.axis[0].formatter.use_scientific = False
    pwy.title.text_font_size = '13pt'

    pwy.yaxis.major_label_standoff = 1
    pwy.yaxis.major_label_text_font_size = '9.5pt'
    pwy.xaxis.major_label_text_font_size = '7.5pt'
    pwy.outline_line_color=None
    pwy.axis.major_label_text_font_style = 'bold'
    pwy.axis.axis_line_alpha= 0
    pwy.xaxis.axis_label_text_font_style = 'bold'

    pwy.min_border = None
    pwy.toolbar.autohide = True
    pwy.grid.grid_line_dash = 'dotted'

    pwy.grid.grid_line_dash_offset = 5
    pwy.grid.grid_line_width = 2
    pwy.xaxis.major_label_orientation = 45
    #pwy.y_range.range_padding = .08


    dfhdy = pd.read_csv('BokehApp/DataFB/dfhdy.csv', delimiter=',',index_col=0)



    dn = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    cdn = OrRd[8][::-1]
    mapperdy = LinearColorMapper(palette=cdn, low=60, high=230)
    fordy = NumeralTickFormatter(format='$0')

    pdy = figure(title='Median share price per day', x_range=dn, y_range=(2013.5,2020.5), x_axis_location='below',
                    plot_width=700, plot_height=350, tools='pan, wheel_zoom, box_zoom, reset',
                     toolbar_location='right')

    pdy.rect(x='day', y='year', width=1, height=1, source=dfhdy,
            fill_color={'field':'Close','transform': mapperdy}, line_color='darkblue', line_width=.1, line_dash='dashed')

    color_bardy = ColorBar(color_mapper=mapperdy, major_label_text_font_size="10px", major_label_text_font_style='bold',
                        ticker=(BasicTicker(desired_num_ticks=len(cdn))), formatter=fordy,
                        label_standoff=10, border_line_color=None, location=(0, 0))
    pdy.add_layout(color_bardy, 'right')


    hovertdy = HoverTool()
    hovertdy.tooltips=[('day', '@day'), ('year','@year'),('Close', '@Close{0.00 a}')]
    pdy.add_tools(hovertdy)

    pdy.title.text_font_size = '13pt'

    pdy.yaxis.major_label_standoff = 1
    pdy.yaxis.major_label_text_font_size = '9.5pt'
    pdy.xaxis.major_label_text_font_size = '7.5pt'
    pdy.outline_line_color=None
    pdy.axis.major_label_text_font_style = 'bold'
    pdy.axis.axis_line_alpha= 0
    pdy.xaxis.axis_label_text_font_style = 'bold'
    pdy.min_border = None
    pdy.toolbar.autohide = True
    pdy.grid.grid_line_dash = 'dotted'
    pdy.grid.grid_line_dash_offset = 5
    pdy.grid.grid_line_width = 2


    dfhmy = pd.read_csv('BokehApp/DataFB/dfhmy.csv', delimiter=',', index_col=0)

    dnm = list(dfhmy['monthN'].unique())
    dnm = [ 'January', 'February', 'March', 'April','May', 'June', 'July', 'August','September', 'October', 'November', 'December']

    cdnm = OrRd[8][::-1]
    mappermy = LinearColorMapper(palette=cdn, low=60, high=230)
    formy = NumeralTickFormatter(format='$0')

    pmy = figure(title='Median share price per month', x_range=dnm, y_range=(2013.5,2020.5), x_axis_location='below',
                    plot_width=800, plot_height=350, tools='pan, wheel_zoom, box_zoom, reset',
                     toolbar_location='right')

    pmy.rect(x='monthN', y='year', width=1, height=1, source=dfhmy,
            fill_color={'field':'Close','transform': mappermy}, line_color='darkblue', line_width=.1, line_dash='dashed')

    color_barmy = ColorBar(color_mapper=mappermy, major_label_text_font_size="10px", major_label_text_font_style='bold',
                        ticker=(BasicTicker(desired_num_ticks=len(cdnm))), formatter=formy,
                        label_standoff=10, border_line_color=None, location=(0, 0))
    pmy.add_layout(color_barmy, 'right')


    hovermy = HoverTool()
    hovermy.tooltips=[('month', '@monthN'), ('year','@year'),('Close', '@Close{0.00 a}')]
    pmy.add_tools(hovermy)


    pmy.title.text_font_size = '13pt'

    pmy.yaxis.major_label_standoff = 1
    pmy.yaxis.major_label_text_font_size = '9.5pt'
    pmy.xaxis.major_label_text_font_size = '7.5pt'
    pmy.outline_line_color=None
    pmy.axis.major_label_text_font_style = 'bold'
    pmy.axis.axis_line_alpha= 0
    pmy.xaxis.axis_label_text_font_style = 'bold'
    pmy.min_border = None
    pmy.toolbar.autohide = True
    pmy.grid.grid_line_dash = 'dotted'
    pmy.grid.grid_line_dash_offset = 5
    pmy.grid.grid_line_width = 2
    #pmy.xaxis.major_label_orientation = 45


    t1 = Panel(child=phd, title='Day/hour Line chart')
    t2 = Panel(child=ptv, title='Day/hour Heatmap share')
    t3 = Panel(child=pth, title='Day/hour Heatmap volume')

    tabs = Tabs(tabs=[t1, t2, t3])

    tmy = Panel(child=pmy, title='Year/month Heatmap share')
    tdy = Panel(child=pdy, title='Year/day Heatmap share')
    twy = Panel(child=pwy, title='Year/week Heatmap share')
    #thy = Panel(child=tabs, title['Year/hour Heatmap share'])

    tabs1 = Tabs(tabs=[twy, tdy, tmy, t1, t2, t3])

    return tabs1


def predic():
    dfd = pd.read_csv('BokehApp/DataFB/dfd.csv', delimiter=',', index_col=0)

    dfd['date1'] = pd.to_datetime(dfd['date1'], format=('%Y/%m/%d'))

    dfd = dfd.set_index('date1')
    dfd['hl_pct'] = (dfd['High'] - dfd['Low']) / dfd['Close'] *100
    dfd['pct_c'] = (dfd['Close'] - dfd['Open']) / dfd['Open'] *100

    forc_out = int(math.ceil(0.01*len(dfd)))
    #forc_cl = 'Close'
    dfd['label'] = dfd['Close'].shift(-forc_out)
    #dfW_fc.fillna(value=99999, inplace=True)

    Xw = np.array(dfd.drop('label', 1))
    Xw = scale(Xw)

    Xw_latter = Xw[-forc_out:]
    Xw = Xw[:-forc_out]

    yw = np.array(dfd['label'])
    yw = yw[:-forc_out]

    poly2 = make_pipeline(PolynomialFeatures(2), Ridge())
    poly2.fit(Xw, yw)
    confpoly2 = poly2.score(Xw, yw)
    confpoly2

    poly5 = make_pipeline(PolynomialFeatures(5), Ridge())
    poly5.fit(Xw, yw)
    confpoly5 = poly5.score(Xw, yw)
    confpoly5

    poly3 = make_pipeline(PolynomialFeatures(3), Ridge())
    poly3.fit(Xw, yw)
    confpoly3 = poly3.score(Xw, yw)
    confpoly3, confpoly2, confpoly5

    forc_set = poly3.predict(Xw_latter)

    dfF = dfd.iloc[-19:]
    dfF['forc'] = forc_set
    dfF = pd.DataFrame(dfF)

    forc_set = poly3.predict(Xw_latter)
    dfd['forc'] = np.nan

    ldate = dfd.index[0]
    lUnix = ldate
    nUnix = lUnix + datetime.timedelta(days=1)

    for i in forc_set:
        nDate = nUnix
        nUnix += datetime.timedelta(days=1)
        dfd.loc[nDate] = [np.nan for _ in range(len(dfd.columns)-1)]+[i]


    dfpp = deepcopy(dfd.loc['2020-06-01':'2020-09-30'])
    dfpp['forc'] = np.nan
    dfpp['forc'][-19:] = dfF['forc']

    xpp = dfpp.index.to_list()

    sourcepp = ColumnDataSource(data=dict(x=xpp, x1=dfpp.index, y=dfpp['Close'], y1=dfpp['forc']))

    pp = figure(title='Forecast Share Prices', plot_height=350, plot_width=750, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right', x_axis_type = 'datetime')
    pp.line(y='y', x='x1', source=sourcepp, line_width = 1.2, line_color='#3b5998', legend_label='Close')
    #pday.circle(x='x1', y='y', size=1, color='darkblue', source=sourceday)
    pp.line(y='y1', x='x1', source=sourcepp, line_width=1.8, line_color='orange', legend_label='Forecast')

    hoverpp = HoverTool(tooltips=[('Date', '@x1{%F}'),('Close','$@y{0.00}'),('Forecast','$@y1{0.00}')], formatters={'@x1': 'datetime'})
    pp.add_tools(hoverpp)


    pp.legend.location = 'top_left'
    pp.title.text_font_size = '13pt'
    pp.legend.click_policy="hide"
    pp.legend.location = 'top_left'
    pp.legend.background_fill_alpha=None
    pp.legend.border_line_alpha = None
    pp.legend.title = '↓ Disable/Enable'
    pp.yaxis.major_label_standoff = -2
    pp.yaxis.major_label_text_font_size = '9.5pt'
    pp.xaxis.major_label_text_font_size = '8.5pt'
    pp.outline_line_color=None
    pp.axis.major_label_text_font_style = 'bold'
    pp.axis.major_label_text_color = '#3b5998'
    pp.min_border = 0
    pp.x_range.range_padding = 0
    pp.toolbar.autohide = True
    pp.grid.grid_line_dash = 'dotted'
    pp.grid.grid_line_dash_offset = 5
    pp.grid.grid_line_width = 2
    pp.xaxis.ticker.desired_num_ticks = 10
    pp.xaxis.formatter=DatetimeTickFormatter(months= ['%d/%m/%g']) #days=['%d/%m'], months=['%d/%m'])months= ['%B/%G']
    pp.xaxis.axis_line_color = None
    pp.yaxis[0].formatter = NumeralTickFormatter(format="$0")

    lowestDp = Label(x=480, y=62, x_units='screen', y_units='screen',
                         text='Polynomial', render_mode='css', text_font_size='6.5pt', text_color='black', text_font_style='bold',
                         text_align='center', angle=0, text_alpha=0.6)
    pp.add_layout(lowestDp)

    lowestDp1 = Label(x=480, y=50, x_units='screen', y_units='screen',
                         text='Features', render_mode='css', text_font_size='8pt', text_color='black', text_font_style='bold',
                         text_align='center', angle=0, text_alpha=0.6)
    pp.add_layout(lowestDp1)

    lowestDp2 = Label(x=480, y=25, x_units='screen', y_units='screen',
                         text='Accuracy', render_mode='css', text_font_size='7pt', text_color='black', text_font_style='bold',
                         text_align='center', angle=0, text_alpha=0.6)
    pp.add_layout(lowestDp2)

    lowestLp = Label(x=250, y=30, x_units='screen', y_units='screen',
                         text='⬆95%', render_mode='css', text_font_size='120pt', text_color='green', text_font_style='bold',
                         text_align='center', angle=0, text_alpha=0.06) #←
    pp.add_layout(lowestLp)

    lowestLp1 = Label(x=480, y=37, x_units='screen', y_units='screen',
                         text='⬆95%', render_mode='css', text_font_size='12pt', text_color='green', text_font_style='bold',
                         text_align='center', angle=0, text_alpha=0.7) #←
    pp.add_layout(lowestLp1)
           
    return pp
