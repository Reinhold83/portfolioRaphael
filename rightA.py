#imports
import pandas as pd
import numpy as np
from bokeh.resources import INLINE
from bokeh.plotting import figure, show, curdoc
#from bokeh.util.string import encode_utf8
from bokeh.transform import dodge
from math import pi
from bokeh.transform import cumsum
from bokeh.layouts import column, row, gridplot
#from bokeh.core.properties import value
from bokeh.models import ColumnDataSource, Label, GeoJSONDataSource, LabelSet, DatetimeTickFormatter, BoxAnnotation,BasicTicker, PrintfTickFormatter, NumeralTickFormatter, FactorRange, Paragraph, LinearColorMapper, Tabs, Panel, HoverTool, Div, Select, CustomJS, Range1d, ColorBar, BasicTicker
from bokeh.transform import factor_cmap
from bokeh.models.widgets import Panel, Tabs
from bokeh.palettes import viridis, GnBu, Greens
from bokeh.resources import CDN
from bokeh.embed import file_html


def wwpop():
    dfpp = pd.read_csv('BokehApp/DataRA/wwpop18th.csv', delimiter=',', index_col=0)
    dfpp = dfpp.iloc[1:]

    source1 = ColumnDataSource(dfpp)

    pp = figure(plot_height=400, plot_width=900, title='World Population Growth', tools='reset')


    pp.line(x='Year', y='Population', line_width=2.5, line_color='#FFCD00', source=source1)
    pp.circle(x='Year', y='Population', line_width=2.5, line_color='#440154', source=source1)

    pp.x_range.start=1745
    pp.x_range.end = 2022
    #pp.y_range.start=.0001
    pp.yaxis.formatter.use_scientific = False

    pp.grid.grid_line_alpha = 0.6
    pp.grid.grid_line_dash = 'dotted'
    pp.grid.grid_line_dash_offset = 5
    pp.grid.grid_line_width = 2
    tick_labels_pp = {'1000000000':'1b','2000000000':'2b','3000000000':'3b','4000000000':'4b','5000000000':'5b','6000000000':'6b','7000000000':'7b','8000000000':'8b'}
    pp.yaxis.major_label_overrides = tick_labels_pp
    pp.title.text_font_size = '15px'
    #pti.axis.major_label_text_font_style = 'bold'
    pp.axis.major_label_text_font_style = 'bold'
    pp.toolbar.autohide = True

    hoverpp = HoverTool()
    hoverpp.tooltips=[('Year', '@Year'),('Population', '@Population{int}')]
    pp.add_tools(hoverpp)


    ir = BoxAnnotation(right=1760, left=1840, fill_alpha=0.5, fill_color='#CF142B')#00247D
    irc = Label(x=27, y=100, x_units='screen', y_units='screen',
                     text='Industrial', render_mode='css', text_font_size='22.5pt', text_color='white',
                     text_align='left', angle=1.568, text_alpha=0.6)
    irc1 = Label(x=143, y=190, x_units='screen', y_units='screen',
                     text='Revolution', render_mode='css', text_font_size='22.5pt', text_color='white',
                     text_align='left', angle=1.568, text_alpha=0.6)

    fr = BoxAnnotation(right=1789, left=1799, fill_alpha=0.5, fill_color='#0055A4')
    frc = Label(x=46, y=160, x_units='screen', y_units='screen',
                     text='French Revolution', render_mode='css', text_font_size='20pt', text_color='white',
                     text_align='left', angle=1.568, text_alpha=0.6)

    wwi = BoxAnnotation(right=1914, left=1918, fill_alpha=0.5, fill_color='#CF142B')
    wwic = Label(x=507, y=160, x_units='screen', y_units='screen',
                     text='WWI', render_mode='css', text_font_size='12pt', text_color='white',
                     text_align='left', angle=1.568, text_alpha=0.6)

    wwii = BoxAnnotation(right=1938, left=1945, fill_alpha=0.5, fill_color='#CF142B')
    wwiic = Label(x=577, y=240, x_units='screen', y_units='screen',
                     text='WWII', render_mode='css', text_font_size='16pt', text_color='white',
                     text_align='left', angle=1.568, text_alpha=0.6)

    gp = BoxAnnotation(right=1929, left=1933, fill_alpha=0.5, fill_color='#CF142B')
    gpc = Label(x=519.5, y=160, x_units='screen', y_units='screen',
                     text='Great Depression', render_mode='css', text_font_size='9.5pt', text_color='white',
                     text_align='left', angle=1.568, text_alpha=0.6)
    cw = BoxAnnotation(right=1947, left=1991, fill_alpha=0.5, fill_color='#CF142B')#FFD900
    cwc = Label(x=680, y=220, x_units='screen', y_units='screen',
                     text='War', render_mode='css', text_font_size='30pt', text_color='white',
                     text_align='center', angle=1.568, text_alpha=0.6)
    cwc1 = Label(x=710, y=50, x_units='screen', y_units='screen',
                     text='Cold', render_mode='css', text_font_size='30pt', text_color='white',
                     text_align='center', angle=1.568, text_alpha=0.6)

    wt = BoxAnnotation(right=2001, left=2020.9, fill_alpha=0.5, fill_color='#CF142B')
    wtc = Label(x=807, y=130, x_units='screen', y_units='screen',
                     text='War on Terrorism', render_mode='css', text_font_size='13pt', text_color='white',
                     text_align='center', angle=1.568, text_alpha=0.6)

    pp.add_layout(ir)
    pp.add_layout(irc)
    pp.add_layout(irc1)
    pp.add_layout(fr)
    pp.add_layout(frc)
    pp.add_layout(wwi)
    pp.add_layout(wwic)
    pp.add_layout(wwii)
    pp.add_layout(wwiic)
    pp.add_layout(gp)
    pp.add_layout(gpc)
    pp.add_layout(cw)
    pp.add_layout(cwc)
    pp.add_layout(cwc1)
    pp.add_layout(wt)
    pp.add_layout(wtc)

    return pp


def swedishpop():

    dfswpop = pd.read_csv('BokehApp/DataRA/SwedishPop_5ys.csv', delimiter=',')
    df_pivot = dfswpop.pivot_table(values=['2007', '2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'], index='sex', columns='ageGroup')
    yrs = ['2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
    dfswpopM = pd.DataFrame(df_pivot.loc['male'][yrs])
    dfswpopF = pd.DataFrame(df_pivot.loc['female'][yrs])

    gs = list(dfswpop['ageGroup'].unique())

    sourceSm = ColumnDataSource(data=dict(y=gs, _2019_=df_pivot.loc['male']['2019'],_2015=df_pivot.loc['male']['2015'], _2016=df_pivot.loc['male']['2016'], _2017=df_pivot.loc['male']['2017'], _2018=df_pivot.loc['male']['2018'], _2019=df_pivot.loc['male']['2019']))
    sourceSf = ColumnDataSource(data=dict(y=gs, _2019_=df_pivot.loc['female']['2019'],_2015=df_pivot.loc['female']['2015'], _2016=df_pivot.loc['female']['2016'], _2017=df_pivot.loc['female']['2017'], _2018=df_pivot.loc['female']['2018'], _2019=df_pivot.loc['female']['2019']))

    pm = figure(y_axis_location = None, plot_height=320, plot_width=260, y_range=gs, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pm.hbar(y='y', height=1, right='_2019_',  source=sourceSm, legend_label='male', line_color="white", fill_color='#FFCD00')

    #plot style
    hoverpm = HoverTool()
    hoverpm.tooltips=[('Age Group', '@y'),('Population', '@_2019_{0.00 a}')]
    pm.add_tools(hoverpm)
    pm.x_range.flipped = True
    pm.grid.grid_line_color=None
    pm.outline_line_color=None
    pm.x_range.range_padding = 0
    pm.axis.major_label_text_font_style = 'bold'
    pm.toolbar.autohide = True
    pm.axis.axis_line_color = None
    pm.legend.location = 'top_left'
    pm.legend.background_fill_alpha = None
    pm.legend.border_line_color = None
    pm.xaxis.formatter.use_scientific = False
    pm.xaxis.major_label_text_font_size = '7pt'
    tick_labels_pm = {'50000':'50K','100000':'100K','150000':'150K','200000':'200K','250000':'250K', '300000':'300K', '350000':'350K'}
    pm.xaxis.major_label_overrides = tick_labels_pm

    pf = figure(plot_height=320, plot_width=285, y_range=gs, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pf.hbar(y='y', height=1, right='_2019_',  source=sourceSf, legend_label='female', line_color="white", fill_color='#004B87')

    hoverpf = HoverTool()
    hoverpf.tooltips=[('Age Group', '@y'), ('Population', '@_2019_{0.00 a}')]

    #plot style
    pf.add_tools(hoverpf)
    pf.legend.background_fill_alpha = None
    pf.legend.border_line_color = None
    pf.yaxis.major_label_standoff = -2
    pf.yaxis.major_label_text_font_size = '8pt'
    pf.xaxis.major_label_text_font_size = '7pt'
    pf.grid.grid_line_color=None
    pf.outline_line_color=None
    pf.yaxis.major_label_text_align = 'center'
    pf.axis.major_label_text_font_style = 'bold'
    pf.yaxis.major_tick_line_color = None
    pf.axis.axis_line_color = None
    pf.min_border = 0
    pf.x_range.range_padding = 0
    pf.toolbar.autohide = True
    pf.yaxis.major_label_standoff = 0
    pf.xaxis.formatter.use_scientific = False
    tick_labels_pf = {'50000':'50K','100000':'100K','150000':'150K','200000':'200K','250000':'250K', '300000':'300K', '350000':'350K'}
    pf.xaxis.major_label_overrides = tick_labels_pf
    pm.title.text_font_size = '8pt'
    pm.title.text = 'Swedish Population by Age/Gender Group 2019'
    pm.title.align = 'left'


    #Population by ageGroup
    df_ageOverall = pd.read_csv('BokehApp/DataRA/SwedishPop_ageGroupOverall.csv', delimiter=',')
    df_ageOverall = df_ageOverall.iloc[::, 8:]
    df_ageOverall['color'] = viridis(len(df_ageOverall.index))
    df_ageOverall.head()

    sourceOverall = ColumnDataSource(data=dict(x=gs, color=df_ageOverall['color'], _2019_=df_ageOverall['2019'], _2015=df_ageOverall['2015'], _2016=df_ageOverall['2016'], _2017=df_ageOverall['2017'], _2018=df_ageOverall['2018'],_2019=df_ageOverall['2019']))

    pO = figure(x_range=gs, plot_height=320, plot_width=410,title='Swedish Population by Age Group 2019',
               tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')

    pO.vbar(x='x', top='_2019_', source=sourceOverall, width=0.55, color='#FFCD00')

    #plot style
    pO.outline_line_color=None
    pO.axis.major_label_text_font_style = 'bold'
    pO.grid.grid_line_dash = 'dotted'
    pO.grid.grid_line_dash_offset = 5
    pO.grid.grid_line_width = 2
    pO.y_range.start = 0
    #pO.toolbar.autohide=True
    pO.yaxis.formatter.use_scientific = False
    pO.xaxis.major_label_orientation = 45


    hoverpO = HoverTool()
    hoverpO.tooltips=[('Age Group','@x'),('Population', '@_2019_{0.00 a}')]
    pO.add_tools(hoverpO)

    tick_labels_pO = {'100000':'100K','200000':'200K','300000':'300K','400000':'400K','500000':'500K','600000':'600K','700000':'700K'}
    pO.yaxis.major_label_overrides = tick_labels_pO

    select = Select(title="Select year:", align='start', value='_2019_', width=70, height=25, options=['_2015','_2016','_2017','_2018','_2019'])

    callback = CustomJS(args={'source':sourceSm,  'source1':sourceSf, 'source2':sourceOverall, 'title':pm.title, 'title1':pO.title},code="""
            console.log(' changed selected option', cb_obj.value);

            var data = source.data;
            var data1 = source1.data
            var data2 = source2.data
            title.text = 'Swedish Population by Age/Gender Group ' + cb_obj.value
            title1.text = 'Swedish Population by Age Group ' + cb_obj.value

            // allocate column
            data['_2019_'] = data[cb_obj.value];
            data1['_2019_'] = data1[cb_obj.value];
            data2['_2019_'] = data2[cb_obj.value];



            // register the change 
            source.change.emit()
            source1.change.emit()
            source2.change.emit()""")

    select.js_on_change('value', callback)

    p = gridplot([[pm, pf]], toolbar_location='left', merge_tools=True)#, toolbar_options = {'autohide':True})

    layout = row([select, p, pO], margin=(10,40), spacing=10, align='center')

    return layout

def swedishpop1():
    #yearly growth
    dfpopSw = pd.read_csv('BokehApp/DataRA/swedishPopOverall.csv', delimiter=',', index_col=0)
    dfpopSw = dfpopSw.iloc[2:] 
    ys = list(dfpopSw.index.values)
    xrange = '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'

    dfpopSw['color'] = viridis(len(dfpopSw.index))

    yrange = (9000000, dfpopSw['Population'].max())

    source = ColumnDataSource(dfpopSw)

    pS = figure(plot_height=320, plot_width=370,title='Swedish Population Growth by Year',
               y_range=Range1d(*yrange),tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='below')
    pS.vbar(x='Year', top='Population', source=source, width=0.5, color='#004B87')

    pS.y_range.end = dfpopSw['Population'].max()*1.003
    pS.outline_line_color=None
    pS.axis.major_label_text_font_style = 'bold'
    pS.grid.grid_line_dash = 'dotted'
    pS.grid.grid_line_dash_offset = 5
    pS.grid.grid_line_width = 2
    pS.toolbar.autohide=True
    pS.yaxis.formatter.use_scientific = False


    hoverpS = HoverTool()
    hoverpS.tooltips=[('Year','@Year'),('Population', '@Population{0.00 a}')]
    pS.add_tools(hoverpS)

    tick_labels_pS = {'9000000':'9M','9200000':'9.2M','9400000':'9.4M','9600000':'9.6M','9800000':'9.8M','10000000':'10M', '10200000':'10.2M'}
    pS.yaxis.major_label_overrides = tick_labels_pS



    #piechart
    pIS = figure(x_axis_location = None, y_axis_location = None, plot_width=400, plot_height=330, tools='')
    pIS.image_url(url=['static/imagesRA/SwedishChart_edit.png'], x=0, y=0, w=2, h=2, anchor="bottom_left")
    pIS.title.align='center'    
    pIS.grid.grid_line_color=None
    pIS.outline_line_color=None
    pIS.toolbar.logo=None

    
    layout1 = row([pS, pIS], spacing=-5, align='start')
    
    return layout1

def irishpop():

    #population pyramid
    dfIrl = pd.read_csv('BokehApp/DataRA/popByAgeGroup_v2.csv', delimiter=',', index_col='AgeGroup')
    df_pivotIrl = dfIrl.pivot_table(values=['2002','2003','2004','2005','2006','2007', '2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'],index='sex', columns='AgeGroup')

    gs1 = list(dfIrl.index.unique())

    sourceIm = ColumnDataSource(data=dict(y=gs1, _2019_=df_pivotIrl.loc['male']['2019'],_2015=df_pivotIrl.loc['male']['2015'], _2016=df_pivotIrl.loc['male']['2016'], _2017=df_pivotIrl.loc['male']['2017'], _2018=df_pivotIrl.loc['male']['2018'], _2019=df_pivotIrl.loc['male']['2019']))
    sourceIf = ColumnDataSource(data=dict(y=gs1, _2019_=df_pivotIrl.loc['female']['2019'],_2015=df_pivotIrl.loc['female']['2015'], _2016=df_pivotIrl.loc['female']['2016'], _2017=df_pivotIrl.loc['female']['2017'], _2018=df_pivotIrl.loc['female']['2018'], _2019=df_pivotIrl.loc['female']['2019']))

    pmI = figure(y_axis_location = None, plot_height=320, plot_width=270, y_range=gs1, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pmI.hbar(y='y', height=1, right='_2019_',  source=sourceIm, legend_label='male', line_color="white", fill_color='#169B62')


    #plot style
    hoverpmI = HoverTool()
    hoverpmI.tooltips=[('Age Group', '@y'), ('Population', '@_2019_')]
    pmI.add_tools(hoverpmI)
    pmI.x_range.flipped = True
    pmI.grid.grid_line_color=None
    pmI.outline_line_color=None
    pmI.x_range.range_padding = 0
    pmI.axis.major_label_text_font_style = 'bold'
    pmI.toolbar.autohide = True
    pmI.axis.axis_line_color = None
    pmI.legend.location = 'top_left'
    pmI.legend.background_fill_alpha = None
    pmI.legend.border_line_color = None
    pmI.xaxis.formatter.use_scientific = False
    pmI.xaxis.major_label_text_font_size = '8pt'
    tick_labels_pmI = {'50':'50K','100':'100K','150':'150K','200':'200K'}
    pmI.xaxis.major_label_overrides = tick_labels_pmI
    #title
    pmI.title.text_font_size = '9pt'
    pmI.title.text = 'Irish Population by Age/Gender Group 2019'
    pmI.title.align = 'left'


    pfI = figure(plot_height=320, plot_width=295, y_range=gs1, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pfI.hbar(y='y', height=1, right='_2019_',  source=sourceIf, legend_label='female', line_color="white", fill_color='#FF883E')

    hoverpfI = HoverTool()
    hoverpfI.tooltips=[('Age Group', '@y'),('Population', '@_2019_')]

    #plot style
    pfI.add_tools(hoverpfI)
    pfI.legend.background_fill_alpha = None
    pfI.legend.border_line_color = None
    pfI.yaxis.major_label_standoff = -2
    pfI.yaxis.major_label_text_font_size = '8pt'
    pfI.xaxis.major_label_text_font_size = '8pt'
    pfI.grid.grid_line_color=None
    pfI.outline_line_color=None
    pfI.yaxis.major_label_text_align = 'center'
    pfI.axis.major_label_text_font_style = 'bold'
    pfI.yaxis.major_tick_line_color = None
    pfI.axis.axis_line_color = None
    pfI.min_border = 0
    pfI.x_range.range_padding = 0
    pfI.toolbar.autohide = True
    pfI.yaxis.major_label_standoff = 0
    pfI.xaxis.formatter.use_scientific = False
    tick_labels_pfI = {'50':'50K','100':'100K','150':'150K','200':'200K'}
    pfI.xaxis.major_label_overrides = tick_labels_pfI

    pI = gridplot([[pmI, pfI]], toolbar_location='left', merge_tools=True)



    #Yearly growth
    dfIO = pd.read_csv('BokehApp/DataRA/IrlOverAll.csv', delimiter=',', index_col='Year')

    xrange = (2009,2018)
    xrange
    yrange = (dfIO['Population'].min(), dfIO['Population'].max())

    sourceIO = ColumnDataSource(dfIO)

    pIO = figure(plot_height=320, plot_width=400,title='Irish Population Growth by Year',
               y_range=Range1d(*yrange),tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='below')

    pIO.vbar(x='Year', top='Population', source=sourceIO, width=0.5, color='#169B62')


    #plot style
    pIO.x_range.end = 2019.5
    pIO.y_range.start = 4500
    pIO.y_range.end = dfIO['Population'].max()*1.003
    pIO.outline_line_color=None
    pIO.axis.major_label_text_font_style = 'bold'
    pIO.grid.grid_line_dash = 'dotted'
    pIO.grid.grid_line_dash_offset = 5
    pIO.grid.grid_line_width = 2


    hoverpIO = HoverTool()
    hoverpIO.tooltips=[('Year','@Year'),('Population', '@Population{int}')]
    pIO.add_tools(hoverpIO)


    tick_labels_pIO = {'4500':'4.5M','4550':'4.55M','4600':'4.6M','4650':'4.65M','4700':'4.7M','4750':'4.75M', '4800':'4.8M','4850':'4.85M'}
    pIO.yaxis.major_label_overrides = tick_labels_pIO


    #population by age group
    dfIG = pd.read_csv('BokehApp/DataRA/IrlAgeGroupYear.csv', delimiter=',', index_col=0)

    sourceIG = ColumnDataSource(data=dict(x=gs1, _2019_=dfIG['2019'], _2015=dfIG['2015'], _2016=dfIG['2016'], _2017=dfIG['2017'], _2018=dfIG['2018'],_2019=dfIG['2019']))

    pIG = figure(x_range=gs1, plot_height=320, plot_width=470,title='Irish Population by Age Group 2019',
               tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')

    pIG.vbar(x='x', top='_2019_', source=sourceIG, width=0.55, color='#FF883E')

    #plot style
    pIG.outline_line_color=None
    pIG.axis.major_label_text_font_style = 'bold'
    pIG.grid.grid_line_dash = 'dotted'
    pIG.grid.grid_line_dash_offset = 5
    pIG.grid.grid_line_width = 2
    pIG.yaxis.formatter.use_scientific = False
    pIG.xaxis.major_label_orientation = 45
    pIG.y_range.start = 0

    hoverpIG = HoverTool()
    hoverpIG.tooltips=[('Age Group','@x'),('Population', '@_2019_')]
    pIG.add_tools(hoverpIG)

    tick_labels_pIG = {'50':'50K','100':'100K','150':'150K','200':'200K','250':'250K','300':'300K','350':'350K','400':'400K'}
    pIG.yaxis.major_label_overrides = tick_labels_pIG

    selectIrl = Select(title="Select year:", align='start', value='_2019_', width=80, height=25, options=['_2015','_2016','_2017','_2018','_2019'])

    callbackIrl = CustomJS(args={'source':sourceIm,  'source1':sourceIf, 'source2':sourceIG, 'title':pmI.title, 'title1':pIG.title},code="""
            console.log(' changed selected option', cb_obj.value);

            var data = source.data;
            var data1 = source1.data
            var data2 = source2.data
            title.text = 'Irish Population by Age/Gender Group ' + cb_obj.value
            title1.text = 'Irish Population by Age Group ' + cb_obj.value

            // allocate column
            data['_2019_'] = data[cb_obj.value];
            data1['_2019_'] = data1[cb_obj.value];
            data2['_2019_'] = data2[cb_obj.value];



            // register the change 
            source.change.emit()
            source1.change.emit()
            source2.change.emit()""")

    selectIrl.js_on_change('value', callbackIrl)

    layoutIrl = row([selectIrl, pI, pIG, pIO], margin=(10,40), spacing=25, align='end')

    return layoutIrl

def pandemics():
    pRF = figure(x_axis_location = None, y_axis_location = None, plot_width=800, plot_height=1200)
    pRF.image_url(url=['static/imagesRA/allPieCharts.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pRF.title.align='center'    
    pRF.grid.grid_line_color=None
    pRF.outline_line_color=None
    pRF.toolbar.autohide = True
    pRF.title.text_font_style = "bold"
    pRF.toolbar.active_drag = None

    return pRF

def pandemics1():
    pF = figure(x_axis_location = None, y_axis_location = None, plot_width=445, plot_height=310, tools='wheel_zoom, box_zoom, reset')
    pF.image_url(url=['static/imagesRA/06_Flu_.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pF.title.align='center'    
    pF.grid.grid_line_color=None
    pF.outline_line_color=None
    pF.toolbar.autohide = True
    pF.title.text_font_style = "bold"

    return pF

def R0():
    dft = pd.read_csv('BokehApp/DataRA/transmissibilityPandemics.csv', delimiter=',', index_col=0)

    pandemics = list(dft.columns.values)
    trans = str(['Minimum','Maximum'])
    df3 = dft.iloc[:-1].reset_index()
    lower = [1.4, 1.47, 1.53, 1.56, 1.3, 1.4, 1.19]
    high = [2.8, 2.27, 1.7, 1.85, 1.7, 3.9, 1.37]
    avg = [2.1 , 1.87, 1.62, 1.71, 1.5 , 2.65, 1.28]
    d3 = {'pandemics':pandemics, 'low': lower, 'high': high, 'avg':avg}


    pt = figure(x_range=pandemics, plot_height=320, plot_width=525, title='Transmissibility',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right') # ['#b32134', '#e1888f']
    pt.vbar_stack(['low','high'], x='pandemics', width=.35, fill_color=['#e1888f', '#5E1914'], line_color='#b32134', source=d3, legend_label=['low','high']) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]
    pt.line(x='pandemics', y='avg', line_width=2, line_dash='dashdot', line_color='orange', source=d3, legend_label='average')
    pt.circle(x='pandemics', y='avg', size=6, color='#DAE218', source=d3, legend_label='average')
    hoverpt = HoverTool()

    hoverpt.tooltips=[('Pandemic', '@pandemics'),('Lower', '@low'), ('Higher','@high'), ('Average','@avg')]
    pt.add_tools(hoverpt)

    #plot style

    pt.legend.background_fill_alpha = None
    pt.legend.border_line_color = None
    pt.yaxis.major_label_standoff = -2
    pt.yaxis.major_label_text_font_size = '8pt'
    pt.xaxis.major_label_text_font_size = '8pt'
    pt.title.text_font_size = '15px'
    pt.grid.grid_line_dash = 'dotted'
    pt.grid.grid_line_dash_offset = 5
    pt.grid.grid_line_width = 2
    pt.grid.grid_line_alpha = 0.6

    pt.outline_line_color=None
    pt.yaxis.major_label_text_align = 'center'
    pt.axis.major_label_text_font_style = 'bold'
    pt.min_border = 0
    pt.x_range.range_padding = 0
    pt.toolbar.autohide = True
    pt.yaxis.major_label_standoff = 0
    pt.y_range.start=0

    return pt

        
def pandAgeGroups():    
    dfag = pd.read_csv('BokehApp/DataRA/USPandemicsAgeGroup.csv', delimiter=',', index_col=0)
    x1 = list(dfag.index)
    df_ag = dfag[['Swine Hospitalization pct', 'Flu Hospitalization pct', 'Covid Hospitalization pct', 'Swine Flu Deaths pct',
            'Flu Deaths pct','Covid Deaths pct']]
    
    sourceag = ColumnDataSource(data=dict(x=x1, y=df_ag['Swine Hospitalization pct'], y1=df_ag['Flu Hospitalization pct'], y2=df_ag['Covid Hospitalization pct'],
                     y3=df_ag['Swine Flu Deaths pct'], y4=df_ag['Flu Deaths pct'], y5=df_ag['Covid Deaths pct']))

    pag = figure(x_range=FactorRange(*x1), plot_height=320, plot_width=450, tools='pan, wheel_zoom, box_zoom, reset', title='Pandemic hospitalization by age group')
    pag.vbar(x=dodge('x', -0.25, range=pag.x_range), top='y', width=0.2, color= '#e1888f', source=sourceag, legend_label='Swine Flu')
    pag.vbar(x=dodge('x', 0, range=pag.x_range), top='y1', width=0.2, color='#b32134', source=sourceag, legend_label='Seasonal Flu')
    pag.vbar(x=dodge('x', 0.25, range=pag.x_range), top='y2', width=0.2, color='#5E1914',source=sourceag, legend_label='Covid-19')

    pag.grid.grid_line_alpha = 0.8
    pag.grid.grid_line_dash = 'dotted'
    pag.grid.grid_line_dash_offset = 5
    pag.grid.grid_line_width = 2
    pag.toolbar.autohide = True
    pag.outline_line_color=None
    pag.legend.location= 'top_left'#(370,180)
    pag.legend.background_fill_alpha=None
    pag.axis.major_label_text_font_style = 'bold'
    tick_labels_ag = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%'}
    pag.yaxis.major_label_overrides = tick_labels_ag
    pag.legend.click_policy="hide"
    pag.title.text_font_size = '15px'
    pag.legend.border_line_color = None
    hoverag = HoverTool()
    hoverag.tooltips=[('Age Group Hospitalization', '@x'),('Swine Flu','@y{0.00}%'),('Seasonal Flu','@y1{0.00}%'),('Covid-19','@y2{0.00}%')]
    pag.add_tools(hoverag)
    pag.y_range.start = 0
    pag.y_range.end = 80
    pag.legend.visible = False

    pp = figure(x_range=FactorRange(*x1), plot_height=320, plot_width=450, tools='pan, wheel_zoom, box_zoom, reset', title='Pandemic deaths by age group')
    pp.vbar(x=dodge('x', -0.25, range=pag.x_range), top='y3', width=0.2, color= '#e1888f', source=sourceag, legend_label='Swine Flu')
    pp.vbar(x=dodge('x', 0, range=pag.x_range), top='y4', width=0.2, color='#b32134', source=sourceag, legend_label='Seasonal Flu')
    pp.vbar(x=dodge('x', 0.25, range=pag.x_range), top='y5', width=0.2, color='#5E1914',source=sourceag, legend_label='Covid-19')
    pp.grid.grid_line_alpha = 0.8
    pp.grid.grid_line_dash = 'dotted'
    pp.grid.grid_line_dash_offset = 5
    pp.grid.grid_line_width = 2
    pp.toolbar.autohide = True
    pp.outline_line_color=None
    pp.legend.location= 'top_left'#(370,180)
    pp.legend.background_fill_alpha=None
    pp.axis.major_label_text_font_style = 'bold'
    tick_labels_pp = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%'}
    pp.legend.title = 'USA'
    pp.yaxis.major_label_overrides = tick_labels_pp
    #pp.legend.click_policy="hide"
    pp.title.text_font_size = '15px'
    pp.legend.border_line_color = None
    hoverpp = HoverTool()
    hoverpp.tooltips=[('Age Group Deaths', '@x'),('Swine Flu','@y3{0.00}%'),('Seasonal Flu','@y4{0.00}%'),('Covid-19','@y5{0.00}%')]
    pp.add_tools(hoverpp)
    pp.y_range.start = 0
    pp.y_range.end = 80
    pp.yaxis.visible = False
    ppg = gridplot([[pag, pp]], toolbar_location='right', merge_tools=True, sizing_mode='fixed' )#, toolbar_options = {'autohide':True})

    return ppg

def pandAgeGroups1():
    
    dfag = pd.read_csv('BokehApp/DataRA/USPandemicsAgeGroup.csv', delimiter=',', index_col=0)
    x1 = list(dfag.index)
    df_ag = dfag[['Swine Hospitalization pct', 'Flu Hospitalization pct', 'Covid Hospitalization pct', 'Swine Flu Deaths pct','Flu Deaths pct','Covid Deaths pct']]
    
    sourceag = ColumnDataSource(data=dict(x=x1, y=df_ag['Swine Hospitalization pct'], y1=df_ag['Flu Hospitalization pct'], y2=df_ag['Covid Hospitalization pct'],
                     y3=df_ag['Swine Flu Deaths pct'], y4=df_ag['Flu Deaths pct'], y5=df_ag['Covid Deaths pct']))
    
    pwf = figure(x_range=FactorRange(*x1), plot_height=220, plot_width=300, tools='pan, wheel_zoom, box_zoom, reset', title='Swine Flu by age group')
    pwf.vbar(x=dodge('x', -0.25, range=pwf.x_range), top='y', width=0.2, color= '#e1888f', source=sourceag, legend_label='Hospitalization')
    pwf.vbar(x=dodge('x', 0, range=pwf.x_range), top='y3', width=0.2, color='#5E1914', source=sourceag, legend_label='Deaths')

    pwf.grid.grid_line_alpha = 0.8
    pwf.grid.grid_line_dash = 'dotted'
    pwf.grid.grid_line_dash_offset = 5
    pwf.grid.grid_line_width = 2
    pwf.legend.visible = False
    pwf.outline_line_color=None
    pwf.legend.location= 'top_left'#(370,180)
    pwf.legend.background_fill_alpha=None
    pwf.axis.major_label_text_font_style = 'bold'
    tick_labels_pwf = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%'}
    pwf.yaxis.major_label_overrides = tick_labels_pwf
    pwf.legend.click_policy="hide"
    pwf.title.text_font_size = '12px'
    pwf.legend.border_line_color = None
    hoverpwf = HoverTool()
    hoverpwf.tooltips=[('Swine Flu Age Group', '@x'),('Hospitalization','@y{0.00}%'),('Deaths','@y3{0.00}%')]
    pwf.add_tools(hoverpwf)
    pwf.y_range.start = 0
    pwf.y_range.end = 80


    psf = figure(x_range=FactorRange(*x1), plot_height=220, plot_width=300, tools='pan, wheel_zoom, box_zoom, reset', title='Seasonal Flu by age group')
    psf.vbar(x=dodge('x', -0.25, range=psf.x_range), top='y1', width=0.2, color= '#e1888f', source=sourceag, legend_label='Hospitalization*')
    psf.vbar(x=dodge('x', 0, range=psf.x_range), top='y4', width=0.2, color='#5E1914', source=sourceag, legend_label='Deaths**')

    psf.grid.grid_line_alpha = 0.8
    psf.grid.grid_line_dash = 'dotted'
    psf.grid.grid_line_dash_offset = 5
    psf.grid.grid_line_width = 2
    psf.outline_line_color=None
    psf.legend.location= 'top_left'#(370,180)
    psf.legend.background_fill_alpha=None
    psf.axis.major_label_text_font_style = 'bold'
    tick_labels_psf = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%'}
    psf.yaxis.major_label_overrides = tick_labels_psf
    psf.title.text_font_size = '12px'
    psf.legend.border_line_color = None
    psf.legend.title = 'USA'
    hoverpsf = HoverTool()
    hoverpsf.tooltips=[(' Seasonal Flu Age Group ', '@x'),('Hospitalization','@y1{0.00}%'),('Deaths','@y4{0.00}%')]
    psf.add_tools(hoverpsf)
    psf.y_range.start = 0
    psf.y_range.end = 80
    psf.yaxis.visible = False


    pcd = figure(x_range=FactorRange(*x1), plot_height=220, plot_width=300, tools='pan, wheel_zoom, box_zoom, reset', title='Covid-19 by age group')
    pcd.vbar(x=dodge('x', -0.25, range=pcd.x_range), top='y2', width=0.2, color= '#e1888f', source=sourceag, legend_label='Hospitalization*')
    pcd.vbar(x=dodge('x', 0, range=pcd.x_range), top='y5', width=0.2, color='#5E1914', source=sourceag, legend_label='Deaths**')

    pcd.grid.grid_line_alpha = 0.8
    pcd.grid.grid_line_dash = 'dotted'
    pcd.grid.grid_line_dash_offset = 5
    pcd.grid.grid_line_width = 2
    pcd.outline_line_color=None
    pcd.legend.location= 'top_center'#(370,180)
    pcd.legend.background_fill_alpha=None
    pcd.axis.major_label_text_font_style = 'bold'
    tick_labels_pcd = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%'}
    pcd.yaxis.major_label_overrides = tick_labels_pcd
    pcd.title.text_font_size = '12px'
    pcd.legend.border_line_color = None
    hoverpcd = HoverTool()
    hoverpcd.tooltips=[('Covid-19 Age Group ', '@x'),('Hospitalization','@y2{0.00}%'),('Deaths','@y5{0.00}%')]
    pcd.add_tools(hoverpcd)
    pcd.y_range.start = 0
    pcd.y_range.end = 80
    pcd.yaxis.visible = False
    pcd.legend.visible = False

    psfc = gridplot([[pwf, psf, pcd]], toolbar_location='right', merge_tools=True, sizing_mode='fixed')

    return psfc

def corrplot():
    dfc = pd.read_csv('BokehApp/DataRA/pandMatrix.csv', delimiter=',', index_col=0)
    dfcc = pd.DataFrame(dfc.corr().stack(), columns=['corr']).reset_index()
    dfcc.columns = ['x', 'y', 'corr']
    dfcc['corr'] = dfcc['corr'].astype(float)

    xcc = list(dfcc['x'].unique())
    ycc = xcc[::-1]
    colorc = ['#942d1d', '#bb302d','#ed403c','#f98a74','#fad2d0','#bce1e9','#56c4c5','#00acac','#018989','#006e6f']
    colorc = colorc[::-1]
    mapperc = LinearColorMapper(palette=colorc, low=-1, high=1)

    cmc = figure(title='Correlation Matrix', x_range=xcc, y_range=ycc, x_axis_location='below', plot_width=500, plot_height=415,
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='above')
    cmc.title.text_font_size = '20px'
    cmc.rect(x='x', y='y', width=1, height=1, source=dfcc, dilate=True,
            fill_color={'field':'corr', 'transform':mapperc}, line_color='yellow', line_dash='dotted', line_width=.25)

    hoverc = HoverTool()
    hoverc.tooltips=[('var1','@x'),('var2','@y'), ('Correlation','@corr{0.000}')]
    cmc.add_tools(hoverc)

    cmc.xaxis.major_label_orientation = 45
    color_barc = ColorBar(color_mapper=mapperc, major_label_text_font_size='10px', major_label_text_font_style='bold',
                        ticker=BasicTicker(desired_num_ticks=len(colorc)), height=230,
                        label_standoff=6, border_line_color=None, location='center')

    cmc.grid.grid_line_color = None
    cmc.axis.axis_line_color = None
    cmc.axis.major_tick_line_color = None
    cmc.axis.major_label_text_font_size = '10px'
    #cmc.axis.major_label_text_font_size = '12px'
    cmc.axis.major_label_text_font_style = 'bold'
    cmc.axis.major_label_standoff = 0
    cmc.toolbar.autohide = True
    cmc.yaxis.axis_label_text_font_style = 'bold'

    cmc.add_layout(color_barc, 'right')


    dfc = pd.read_csv('BokehApp/DataRA/pandMatrix2.csv', delimiter=',', index_col=0)
    xcl = list(dfc.index.values)
    sourcecl = ColumnDataSource(data=dict(x = xcl , y = dfc['Swine Flu D%'], y1 = dfc['Covid-19 D%'], y2 = dfc['Flu D%'], y3 = dfc['Spanish Flu D%'],
                                y4= dfc['Hong Kong D%'], y5= dfc['Asian Flu D%']))

    pcc = figure( x_range=xcl, plot_height=390, plot_width=500, title='Deaths by Age Group', tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')

    pcc.line(x='x', y='y3', line_width=2, line_dash='dashdot', line_color='#7C0A02', source=sourcecl, legend_label='Spanish Flu*')
    pcc.circle(x='x', y='y3', size=3, color='lime', source=sourcecl, legend_label='Spanish Flu*')
    pcc.line(x='x', y='y', line_width=2, line_dash='dotted', line_color='#FF2400', source=sourcecl, legend_label='Swine Flu')
    pcc.circle(x='x', y='y', size=5, color='orange', source=sourcecl, legend_label='Swine Flu')
    pcc.line(x='x', y='y1', line_width=2, line_dash='dotdash', line_color='#b32134', source=sourcecl, legend_label='Covid-19')
    pcc.circle(x='x', y='y1', size=5, color='cyan', source=sourcecl, legend_label='Covid-19')
    pcc.line(x='x', y='y2', line_width=2, line_dash='solid', line_color='#e1888f', source=sourcecl, legend_label='Seasonal Flu')
    pcc.circle(x='x', y='y2', size=5, color='darkgreen', line_join='bevel', source=sourcecl, legend_label='Seasonal Flu')
    pcc.line(x='x', y='y5', line_width=2, line_dash='dotdash', line_color='#e1888f', source=sourcecl, legend_label='Asian Flu**')
    pcc.circle(x='x', y='y5', size=5, color='#ed403c', line_join='bevel', source=sourcecl, legend_label='Asian Flu**')
    pcc.line(x='x', y='y4', line_width=2, line_dash='solid', line_color='#006e6f', source=sourcecl, legend_label='Hong Kong Flu***')
    pcc.circle(x='x', y='y4', size=5, color='#fad2d0', line_join='bevel', source=sourcecl, legend_label='Hong Kong Flu***')

    


    pcc.grid.grid_line_alpha = 0.8
    pcc.grid.grid_line_dash = 'dotted'
    pcc.grid.grid_line_dash_offset = 5
    pcc.grid.grid_line_width = 2
    pcc.toolbar.autohide = True
    pcc.outline_line_color=None
    pcc.legend.location= 'top_center'#(370,180)
    pcc.legend.background_fill_alpha=None
    pcc.axis.major_label_text_font_style = 'bold'
    pcc.legend.click_policy="hide"
    pcc.legend.title='↓ Disable/Enable'
    pcc.y_range.end = 90
    pcc.title.text_font_size = '15px'

    pcc.legend.border_line_color = None
    pcc.yaxis.major_label_standoff = -2
    pcc.yaxis.major_label_text_font_size = '8pt'
    pcc.xaxis.major_label_text_font_size = '8pt'
    pcc.min_border = 0
    pcc.x_range.range_padding = -0.15
    pcc.toolbar.autohide = True
    pcc.yaxis.major_label_standoff = 0
    pcc.y_range.start=0

    tick_labelscc = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%'}
    pcc.yaxis.major_label_overrides = tick_labelscc
    hovercc = HoverTool()
    hovercc.tooltips=[('Age Group ', '@x'),('Spanish Flu','@y3{0.00}%'),('Swine Flu','@y{0.00}%'), ('Covid-19','@y1{0.00}%'), ('Seasonal Flu','@y2{0.00}%')]
    pcc.add_tools(hovercc)
    
    pcm = gridplot([[pcc, cmc]], toolbar_location='right', merge_tools=True, sizing_mode='fixed')

    return pcm            

def irishDeaths():
    dfw = pd.read_csv('BokehApp/DataRA/covid19_upto3008.csv', delimiter=',', index_col=0)
    dfh = dfw[dfw['countriesAndTerritories'] == 'Ireland']
    dfh = dfh[['deaths']]
    dfh = dfh[dfh['deaths'] >0]
    dfh = dfh.reset_index()
    dfh['dateRep1'] = pd.to_datetime(dfh['dateRep'], format=('%d/%m/%Y'))

    dfh = dfh[15:110]

    sourcept = ColumnDataSource(data=dict(x=list(dfh['dateRep'].values), y=dfh['deaths'], x1=dfh['dateRep1']))
    pt = figure( plot_height=450, plot_width=530, title='Covid-19 deaths in Ireland',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right',
            y_axis_label='Number of Deaths', x_axis_label='113 days period', x_axis_type = 'datetime')
    pt.line(x='x1', y='y', source=sourcept, color='#b32134', line_width=2)
    pt.circle(x='x1', y='y', size=6, color='#e1888f', source=sourcept)


    pt.axis.major_label_text_color = '#800000'
    pt.yaxis.axis_label_text_font_style = 'bold'
    pt.xaxis.axis_label_text_font_style = 'italic'



    box_left = pd.to_datetime('27-04-2020')
    box_right = pd.to_datetime('18-05-2020')

    ir = BoxAnnotation(right=box_right, left=box_left, fill_alpha=0.15, fill_color='#CF142B')#00247D

    irc = Label(x=205, y=348, x_units='screen', y_units='screen',
                        text='Full Lockdown', render_mode='css', text_font_size='8.5pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    ird = Label(x=205, y=337, x_units='screen', y_units='screen',
                        text='27/April - 18/May', render_mode='css', text_font_size='6.5pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1)

    irm = Label(x=430, y=348, x_units='screen', y_units='screen',
                        text='Median', render_mode='css', text_font_size='6.5pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    irmv = Label(x=430, y=328, x_units='screen', y_units='screen',
                        text='6.42', render_mode='css', text_font_size='15pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    irmd = Label(x=430, y=315, x_units='screen', y_units='screen',
                        text='✝ per/day', render_mode='css', text_font_size='6.5pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    irmr = Label(x=430, y=280, x_units='screen', y_units='screen',
                        text='Mortality rate', render_mode='css', text_font_size='6pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    irmr1 = Label(x=430, y=260, x_units='screen', y_units='screen',
                        text='0.31%', render_mode='css', text_font_size='15pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    pt.add_layout(ir)
    pt.add_layout(irc)
    pt.add_layout(ird)
    pt.add_layout(irm)
    pt.add_layout(irmv)
    pt.add_layout(irmd)
    pt.add_layout(irmr)
    pt.add_layout(irmr1)


    pt.xaxis.ticker.desired_num_ticks = 3
    pt.xaxis.formatter=DatetimeTickFormatter(months= ['%B/%G']) #days=['%d/%m'], months=['%d/%m'])


    hoverpt = HoverTool()
    hoverpt.tooltips=[('Date', '@x'),('Deaths','@y')]
    pt.add_tools(hoverpt)


    pt.axis.major_label_text_font_style = 'bold'
    pt.axis.major_label_text_font_size = '12px'

    pt.grid.grid_line_alpha = 0.8
    pt.grid.grid_line_dash = 'dotted'
    pt.grid.grid_line_dash_offset = 5
    pt.grid.grid_line_width = 2
    pt.toolbar.autohide = True
    pt.title.text_font_size = '20px'
    pt.outline_line_color=None
    pt.y_range.start = 0
    pt.y_range.end = 79
    pt.x_range.range_padding =  0.02


    #histS, edgesS = np.histogram(dfs['deaths'], density=False, bins=30, range=[1,115])

    hist, edges = np.histogram(dfh['deaths'], density=True, bins=20, range=[1,77])

    dfhi = pd.DataFrame({'deaths': hist, 'left':edges[:-1], 'right':edges[1:]})
    dfhi['f_deaths'] = ['%d' % count for count in dfhi['deaths']]
    dfhi['f_interval'] = ['%d to %d' % (left,right) for left, right in zip(dfhi['left'], dfhi['right'])]
    dfhi['death_'] = dfhi['deaths'] *1000
    dfhi['death_'] = dfhi['death_'].astype(float)

    sourcehs = ColumnDataSource(dfhi)

    phS = figure( plot_height=300, plot_width=350, title='Deaths histogram', y_axis_label='Frequency', x_axis_label='Deaths',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')



    phS.quad(top='deaths', bottom=0, left='left', right='right', source=sourcehs,
        fill_color='#b32134', line_color='#e1888f',  hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='#FF0800' )

    phS.x_range.start = 0
    #phS.x_range.end = 117
    phS.axis.major_label_text_font_style = 'bold'
    phS.axis.major_label_text_font_size = '12px'
    phS.axis.major_label_text_color = '#080000'

    tick_labels_phs = {'0.01':'10','0.02':'20','0.03':'30','0.04':'40','0.05':'50','0.06':'60','0.07':'70'}
    phS.yaxis.major_label_overrides = tick_labels_phs

    hoverphs = HoverTool()
    hoverphs.tooltips=[('Death range', '@f_interval'),('Frequency','@death_{0.00}')]
    phS.add_tools(hoverphs)

    phS.grid.grid_line_alpha = 0.8
    phS.grid.grid_line_dash = 'dotted'
    phS.grid.grid_line_dash_offset = 5
    phS.grid.grid_line_width = 2
    phS.toolbar.autohide = True
    phS.title.text_font_size = '16px'
    phS.outline_line_color=None

    phS.x_range.range_padding =  0.02
    phS.y_range.start = 0

    pv = figure(x_axis_location = None, y_axis_location = None, plot_width=370, plot_height=120)
    pv.image_url(url=['static/imagesRA/violindetahsIrl2.png'], x=0, y=0, w=1, h=1, anchor="bottom_left")
    pv.title.align='center'    
    pv.grid.grid_line_color=None
    pv.outline_line_color=None
    pv.toolbar.autohide = True

    phSc = column([phS,pv], align='start')#, sizing_mode='scale_width')
    phSg = gridplot([[pt, phSc]], toolbar_location='right', merge_tools=True, sizing_mode='fixed')


    return phSg

def swedishdeaths():
    dfw = pd.read_csv('BokehApp/DataRA/covid19_upto3008.csv', delimiter=',', index_col=0)
    dfs = dfw[dfw['countriesAndTerritories'] == 'Sweden']
    dfs = dfs[['deaths']]
    dfs = dfs[dfs['deaths'] >0]
    dfs = dfs.reset_index()
    dfs['dateRep1'] = pd.to_datetime(dfs['dateRep'], format=('%d/%m/%Y'))

    sourceps = ColumnDataSource(data=dict(x=list(dfs['dateRep'].values), y=dfs['deaths'], x1=dfs['dateRep1']))

    ps = figure( plot_height=450, plot_width=530, title='Covid-19 deaths in Sweden',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right',
            y_axis_label='Number of Deaths', x_axis_label='162 days period', x_axis_type = 'datetime')


    ps.line(x='x1', y='y', source=sourceps, color='#b32134', line_width=2)
    ps.circle(x='x1', y='y', size=6, color='#e1888f', source=sourceps)

    ps.xaxis.ticker.desired_num_ticks = 5
    ps.xaxis.formatter=DatetimeTickFormatter(months= ['%B/%G']) #days=['%d/%m'], months=['%d/%m'])


    ps.axis.major_label_text_color = '#800000'
    ps.yaxis.axis_label_text_font_style = 'bold'
    ps.xaxis.axis_label_text_font_style = 'italic'


    box_lefts = pd.to_datetime('16-03-2020')
    box_rights = pd.to_datetime('15-06-2020')

    #irbs = BoxAnnotation(right=box_rights, left=box_lefts, fill_alpha=0.15, fill_color='#CF142B')#00247D


    irs = Label(x=430, y=348, x_units='screen', y_units='screen',
                        text='Median', render_mode='css', text_font_size='6.5pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    irsv = Label(x=430, y=328, x_units='screen', y_units='screen',
                        text='7.5', render_mode='css', text_font_size='15pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')
    irsd = Label(x=430, y=315, x_units='screen', y_units='screen',
                        text='✝ per/day', render_mode='css', text_font_size='6.5pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    irsr = Label(x=430, y=280, x_units='screen', y_units='screen',
                        text='Mortality rate', render_mode='css', text_font_size='6pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    irsr1 = Label(x=430, y=260, x_units='screen', y_units='screen',
                        text='0.58%', render_mode='css', text_font_size='15pt', text_color='#800000',
                        text_align='center', angle=0, text_alpha=1, text_font_style='bold')

    ps.add_layout(irs)
    ps.add_layout(irs)
    ps.add_layout(irsv)
    ps.add_layout(irsd)
    ps.add_layout(irsr)
    ps.add_layout(irsr1)

    hoverps = HoverTool()
    hoverps.tooltips=[('Date', '@x'),('Deaths','@y')]
    ps.add_tools(hoverps)


    ps.axis.major_label_text_font_style = 'bold'
    ps.axis.major_label_text_font_size = '12px'

    ps.grid.grid_line_alpha = 0.8
    ps.grid.grid_line_dash = 'dotted'
    ps.grid.grid_line_dash_offset = 5
    ps.grid.grid_line_width = 2
    ps.toolbar.autohide = True
    ps.title.text_font_size = '20px'
    ps.outline_line_color=None
    ps.y_range.start = 0
    ps.y_range.end = 117
    ps.x_range.range_padding =  0.02


    histS, edgesS = np.histogram(dfs['deaths'], density=False, bins=30, range=[1,115])

    dfhs = pd.DataFrame({'deaths': histS, 'left':edgesS[:-1], 'right':edgesS[1:]})
    dfhs['f_deaths'] = ['%d' % count for count in dfhs['deaths']]
    dfhs['f_interval'] = ['%d to %d' % (left,right) for left, right in zip(dfhs['left'], dfhs['right'])]


    sourcehS = ColumnDataSource(dfhs)

    phSs = figure( plot_height=300, plot_width=350, title='Deaths histogram', y_axis_label='Frequency', x_axis_label='Deaths',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')



    phSs.quad(top='deaths', bottom=0, left='left', right='right', source=sourcehS,
        fill_color='#b32134', line_color='#e1888f',  hatch_alpha=1.0, hover_fill_alpha=0.7, hover_fill_color='#FF0800' )

    phSs.x_range.start = 0
    phSs.x_range.end = 117
    phSs.axis.major_label_text_font_style = 'bold'
    phSs.axis.major_label_text_font_size = '12px'
    phSs.axis.major_label_text_color = '#080000'

    tick_labels_phS = {'0.01':'10','0.02':'20','0.03':'30','0.04':'40','0.05':'50','0.06':'60','0.07':'70'}
    phSs.yaxis.major_label_overrides = tick_labels_phS

    hoverphS = HoverTool()
    hoverphS.tooltips=[('Death range', '@f_interval'),('Frequency','@deaths{int}')]
    phSs.add_tools(hoverphS)

    phSs.grid.grid_line_alpha = 0.8
    phSs.grid.grid_line_dash = 'dotted'
    phSs.grid.grid_line_dash_offset = 5
    phSs.grid.grid_line_width = 2
    phSs.toolbar.autohide = True
    phSs.title.text_font_size = '16px'
    phSs.outline_line_color=None

    phSs.x_range.range_padding =  0.02
    phSs.y_range.start = 0

    pvs = figure(x_axis_location = None, y_axis_location = None, plot_width=370, plot_height=120)
    pvs.image_url(url=['static/imagesRA/violindetahsSw1.png'], x=0, y=0, w=1, h=1, anchor="bottom_left")
    pvs.title.align='center'    
    pvs.grid.grid_line_color=None
    pvs.outline_line_color=None
    pvs.toolbar.autohide = True

    phSw = column([phSs,pvs], align='start')#, sizing_mode='scale_width')
    pw = gridplot([[ps, phSw]], toolbar_location='right', merge_tools=True, sizing_mode='fixed')

    return pw

def irishswedishDeaths():
    dfw = pd.read_csv('BokehApp/DataRA/covid19_upto3008.csv', delimiter=',', index_col=0)
    dfs = dfw[dfw['countriesAndTerritories'] == 'Sweden']
    dfs = dfs[['deaths']]
    dfs = dfs[dfs['deaths'] >0]
    dfs = dfs.reset_index()
    dfs['dateRep1'] = pd.to_datetime(dfs['dateRep'], format=('%d/%m/%Y'))

    sourceps = ColumnDataSource(data=dict(x=list(dfs['dateRep'].values), y=dfs['deaths'], x1=dfs['dateRep1']))

    dfh = dfw[dfw['countriesAndTerritories'] == 'Ireland']
    dfh = dfh[['deaths']]
    dfh = dfh[dfh['deaths'] >0]
    dfh = dfh.reset_index()
    dfh['dateRep1'] = pd.to_datetime(dfh['dateRep'], format=('%d/%m/%Y'))

    dfh = dfh[15:110]

    sourcept = ColumnDataSource(data=dict(x=list(dfh['dateRep'].values), y=dfh['deaths'], x1=dfh['dateRep1']))

    ps = figure( plot_height=450, plot_width=650, title='Covid-19 deaths',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right',
                y_axis_label='Number of Deaths', x_axis_type = 'datetime')


    ps.line(x='x1', y='y', source=sourceps, color='#FFCD00', line_width=2, legend_label='Sweden')
    ps.circle(x='x1', y='y', size=6, color='#004B87', source=sourceps, legend_label='Sweden')

    ps.line(x='x1', y='y', source=sourcept, color='#FF883E', line_width=2, legend_label='Ireland')
    ps.circle(x='x1', y='y', size=6, color='#169B62', source=sourcept, legend_label='Ireland')

    ps.xaxis.ticker.desired_num_ticks = 5
    ps.xaxis.formatter=DatetimeTickFormatter(months= ['%B/%G']) #days=['%d/%m'], months=['%d/%m'])


    ps.axis.major_label_text_color = '#800000'
    ps.yaxis.axis_label_text_font_style = 'bold'
    ps.xaxis.axis_label_text_font_style = 'italic'


    box_lefts = pd.to_datetime('16-03-2020')
    box_rights = pd.to_datetime('15-06-2020')

    hoverps = HoverTool()
    hoverps.tooltips=[('Date', '@x'),('Deaths','@y')]
    ps.add_tools(hoverps)


    ps.axis.major_label_text_font_style = 'bold'
    ps.axis.major_label_text_font_size = '12px'

    ps.grid.grid_line_alpha = 0.8
    ps.grid.grid_line_dash = 'dotted'
    ps.grid.grid_line_dash_offset = 5
    ps.grid.grid_line_width = 2
    ps.toolbar.autohide = True
    ps.title.text_font_size = '20px'
    ps.outline_line_color=None
    ps.y_range.start = 0
    ps.y_range.end = 117
    ps.x_range.range_padding =  0.02
    ps.legend.background_fill_alpha=None
    ps.legend.click_policy="hide"
    ps.title.text_font_size = '12px'
    ps.legend.border_line_color = None
    ps.title.text_font_size = '20px'
    ps.legend.title='↓ Disable/Enable'


    return ps
        
def geoIrl():
    with open('BokehApp/DataRA/dfjson.json', 'r', encoding='utf8') as openfile: 
        # Reading from json file 
        geo_json = GeoJSONDataSource(geojson=openfile.read())

    p = figure(title = 'Ireland Covid-19 deaths by county', x_axis_location = None, y_axis_location = None, match_aspect=True,
                tools = 'pan, wheel_zoom, box_zoom, reset, hover, save', tooltips = [('County', '@COUNTY'),('Deaths','@deaths')])

    palette = ['#420D09','#960018','#b32134', '#bb302d','#ed403c','#f98a74','#fad2d0']
    #coloursP = ['#FA8072', '#ED2939','#D21F3C','#BF0A30','#7C0A02', '#5E1914', '#420D09'] #960018#BD021F#7E191B
    coloursP = ['#FA8072', '#ED2939','#D21F3C','#BF0A30','#B80F0A', '#7C0A02', '#BD021F'] #960018#7E191B

    #palette = OrRd[8][::-1]
    color_mapper = LinearColorMapper(palette = coloursP, low = 0, high = 70)
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=6, width = 250, height = 20, ticker=BasicTicker(desired_num_ticks=len(coloursP)),
                        border_line_color=None, location = 'center', orientation = 'horizontal', bar_line_color='#50C878', bar_line_alpha=0.7)#, major_label_overrides = tick_labels)

    p.title.align='center'
    p.patches('xs', 'ys', fill_alpha = 0.7, line_width = 0.5, source = geo_json,
                fill_color = {'field' :'deaths', 'transform' : color_mapper})
    p.add_layout(color_bar, 'below')
    p.grid.grid_line_color=None
    p.outline_line_color=None
    p.toolbar.autohide = True

    p.title.text_font_style = "bold"
    p.title.text_font_size = '20px'
    return p

def irlDD():

    dfdd = pd.read_csv('BokehApp/DataRA/irl16DD1.csv', delimiter=',', index_col=0)

    df_d = pd.DataFrame(dfdd['DD_2016'].nlargest(len(dfdd.index.values)))
    df_d = df_d[1:]
    yrange = list(df_d.index.values)
    yrange= yrange[::-1]
    colours_d = ['#ff0000','#ff2424','#ff4747','#ff6b6b','#ff8f8f','#ffb3b3','#ffd6d6']


    source_d = ColumnDataSource(data=dict(y=yrange[::-1], x=df_d['DD_2016']))
    color_mapper_d = LinearColorMapper(palette = colours_d[::-1], low = 20, high = 80)


    p1 = figure(y_range=yrange, title='Demographic Density', plot_height=350, plot_width=330, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    p1.hbar(y='y', height=.5, right='x',  left=0, source=source_d, line_color="white", fill_color={'field':'x','transform':color_mapper_d})

    hoverp1 = HoverTool()
    hoverp1.tooltips=[('County', '@y'), ('Demographic Density', '@x{0.00} People p/km2')]

        #plot style
    p1.add_tools(hoverp1)
    p1.yaxis.major_label_standoff = -2
    p1.yaxis.major_label_text_font_size = '5pt'
    p1.xaxis.major_label_text_font_size = '7pt'
    p1.outline_line_color=None
    p1.axis.major_label_text_font_style = 'bold'
    p1.yaxis.major_tick_line_color = None
    p1.axis.axis_line_color = None
    p1.min_border = 0
    p1.x_range.range_padding = -0.1
    p1.toolbar.autohide = True
    p1.xaxis.formatter.use_scientific = False

    p1.grid.grid_line_dash = 'dotted'
    p1.grid.grid_line_dash_offset = 5
    p1.grid.grid_line_width = 2

    p2 = figure(x_axis_location = None, y_axis_location = None, plot_width=420)
    p2.image_url(url=['static/imagesRA/mapIrlDD.png'], x=0, y=0, w=1, h=2, anchor="bottom_left")
    p2.title.align='center'    
    p2.grid.grid_line_color=None
    p2.outline_line_color=None
    p2.toolbar.autohide = True
    p2.title.text_font_style = "bold"

    df3 = dfdd[['Urbanpop_pct','Ruralpop_pct']]

    ruvsurb = str(['Rural','Urban'])
    df3 = df3.sort_values('Urbanpop_pct',ascending=False)
    xrange = list(df3.index.values)
    colourspru = ['#ff0000','#ff2424','#ff4747','#ff6b6b','#ff8f8f','#ffb3b3','#ffd6d6']
    color_mapperpru = LinearColorMapper(palette = colourspru[::-1], low = 20, high = 80)


    sourcepru = ColumnDataSource(data=dict(x=list(df3.index.values), y=df3['Urbanpop_pct'], y1=df3['Ruralpop_pct']))

    pru = figure(x_range=xrange, plot_height=200, plot_width=330, title='Urban Population in percentage',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right') # ['#b32134', '#e1888f']
    pru.vbar(top='y', x='x', width=.6, fill_color={'field':'y','transform':color_mapperpru}, line_color=None, source=sourcepru) #source=sourcet ['data','top'] [ factor_cmap(c, palette=['#b32134', '#e1888f'], factors=pandemics) for c in dft1['pandemics'].unique()]

    hoverpru = HoverTool()

    hoverpru.tooltips=[('County', '@x'),('Rural', '@y1{0.00}%'), ('Urban','@y{0.00}%')]
    pru.add_tools(hoverpru)


        #plot style
    tick_labelspru = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%','100':'100%'}
    pru.yaxis.major_label_overrides = tick_labelspru


    pru.yaxis.major_label_standoff = -2
    pru.yaxis.major_label_text_font_size = '6pt'
    pru.xaxis.major_label_text_font_size = '4.5pt'
    pru.title.text_font_size = '11px'
    pru.grid.grid_line_dash = 'dotted'
    pru.grid.grid_line_dash_offset = 5
    pru.grid.grid_line_width = 2
    pru.grid.grid_line_alpha = 0.6

    pru.outline_line_color=None
    pru.yaxis.major_label_text_align = 'center'
    pru.axis.major_label_text_font_style = 'bold'
    pru.min_border = 0
    pru.x_range.range_padding = 0
    pru.toolbar.autohide = True
    pru.yaxis.major_label_standoff = 0
    pru.y_range.start=0
    pru.xaxis.major_label_orientation = 45

    pl = figure(x_axis_location = None, y_axis_location = None, plot_width=185, plot_height=570)
    pl.image_url(url=['static/imagesRA/irlleftLay4.png'], x=0, y=0, w=1, h=3, anchor="bottom_left")
    pl.title.align='center'    
    pl.grid.grid_line_color=None
    pl.outline_line_color=None
    pl.toolbar.autohide = True
    pl.title.text_font_style = "bold"

    p2 = figure(x_axis_location = None, y_axis_location = None, plot_width=420)
    p2.image_url(url=['static/imagesRA/mapIrlDD.png'], x=0, y=0, w=1, h=2, anchor="bottom_left")
    p2.title.align='center'    
    p2.grid.grid_line_color=None
    p2.outline_line_color=None
    p2.toolbar.autohide = True
    p2.title.text_font_style = "bold"

    p2b = row([pl, p2], spacing=-38)
    p2a = column([p1,pru])
    p3 = row([p2b,p2a], align='center', spacing=-50)#, sizing_mode='fixed')

    prm = figure(x_axis_location = None, y_axis_location = None, plot_width=420)
    prm.image_url(url=['static/imagesRA/RuralMapEdit.png'], x=0, y=0, w=1, h=2, anchor="bottom_left")
    #prm.title.align='center'    
    prm.grid.grid_line_color=None
    prm.outline_line_color=None
    prm.toolbar.autohide = True
    #prm.title.text_font_style = "bold"

    dfr =pd.DataFrame(df3.sort_values('Ruralpop_pct', ascending=False))

    yranger = list(dfr.index.values)
    yranger= yranger[::-1]

    coloursr = Greens[7][::-1]


    sourcer = ColumnDataSource(data=dict(y=yranger[::-1], x=dfr['Ruralpop_pct']))
    color_mapperr = LinearColorMapper(palette = coloursr, low = 0, high = 70)


    pr = figure(y_range=yranger, title='Rural Population by County in %', plot_height=400, plot_width=330, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pr.hbar(y='y', height=.7, right='x',  left=0, source=sourcer, line_color="white", fill_color={'field':'x','transform':color_mapperr})

    hoverpr = HoverTool()
    hoverpr.tooltips=[('County', '@y'), ('Rural', '@x{0.00} %')]
    tick_labelsr = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%','100':'100%'}
    pr.xaxis.major_label_overrides = tick_labelsr
        #plot style
    pr.add_tools(hoverpr)
    pr.yaxis.major_label_standoff = -2
    pr.yaxis.major_label_text_font_size = '5pt'
    pr.xaxis.major_label_text_font_size = '7pt'
    pr.outline_line_color=None
    pr.axis.major_label_text_font_style = 'bold'
    pr.yaxis.major_tick_line_color = None
    pr.axis.axis_line_color = None
    pr.min_border = 0
    pr.x_range.range_padding = -0.1
    pr.toolbar.autohide = True
    pr.xaxis.formatter.use_scientific = False
    pr.x_range.end = 92

    pr.grid.grid_line_dash = 'dotted'
    pr.grid.grid_line_dash_offset = 5
    pr.grid.grid_line_width = 2


    dfadd = pd.read_csv('BokehApp/DataRA/irlPopRvsU.csv', delimiter=',', index_col=0)
    dfadd

    xrange_a = list(dfadd.index.values)
    colours_a = Greens[5][::-1]
    color_mapper_a = LinearColorMapper(palette = colours_a[::-1], low = dfadd.values.min(), high = dfadd.values.max())

    source_a = ColumnDataSource(data=dict(x=xrange_a, y=dfadd['RuralPop'], y1=dfadd['UrbanPop']))

    p_a = figure(x_range=xrange_a, plot_height=180, plot_width=320, title='Rural Population by Age Group',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right') # ['#b32134', '#e1888f']
    p_a.vbar(top='y', x='x', width=.45, fill_color='#74c476', line_color=None, source=source_a)
    p_a.yaxis.formatter.use_scientific = False
    hover_a = HoverTool()

    hover_a.tooltips=[('Age Group', '@x'),('Rural Population', '@y{0.0 a}'), ('Urban Population','@y1{0.0 a}')]
    p_a.add_tools(hover_a)

    tick_labels_a = {'100000':'100K','200000':'200K','300000':'300K','400000':'400K','500000':'500K'}
    p_a.yaxis.major_label_overrides = tick_labels_a


    p_a.yaxis.major_label_standoff = -2
    p_a.yaxis.major_label_text_font_size = '6pt'
    p_a.xaxis.major_label_text_font_size = '6.5pt'
    p_a.title.text_font_size = '11px'
    p_a.grid.grid_line_dash = 'dotted'
    p_a.grid.grid_line_dash_offset = 5
    p_a.grid.grid_line_width = 2
    p_a.grid.grid_line_alpha = 0.6

    p_a.outline_line_color=None
    p_a.yaxis.major_label_text_align = 'center'
    p_a.axis.major_label_text_font_style = 'bold'
    p_a.min_border = 0
    p_a.x_range.range_padding = 0
    p_a.toolbar.autohide = True
    p_a.yaxis.major_label_standoff = 0
    p_a.y_range.start=0

    pum = figure(x_axis_location = None, y_axis_location = None, plot_width=420)
    pum.image_url(url=['static/imagesRA/UrbanMapEdit.png'], x=0, y=0, w=1, h=2, anchor="bottom_left")
    pum.grid.grid_line_color=None
    pum.outline_line_color=None
    pum.toolbar.autohide = True


    dfr1 = pd.DataFrame(dfr.sort_values('Urbanpop_pct', ascending=False))

    yrangepu = dfr1.index.tolist()
    coloursu = GnBu[7][::-1]


    sourceu = ColumnDataSource(data=dict(y=list(dfr1.index.values), x=dfr1['Urbanpop_pct']))
    color_mapperu = LinearColorMapper(palette = coloursu, low = 0, high = 70)


    pu = figure(y_range=yrangepu[::-1], title='Urban Population by County in %', plot_height=400, plot_width=330, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pu.hbar(y='y', height=.7, right='x',  left=0, source=sourceu, line_color="white", fill_color={'field':'x','transform':color_mapperu})

    hoverpu = HoverTool()
    hoverpu.tooltips=[('County', '@y'), ('Urban', '@x{0.00} %')]
    tick_labelsu = {'10':'10%','20':'20%','30':'30%','40':'40%','50':'50%','60':'60%','70':'70%','80':'80%','100':'100%'}
    pu.xaxis.major_label_overrides = tick_labelsu
        #plot style
    pu.add_tools(hoverpu)
    pu.yaxis.major_label_standoff = -2
    pu.yaxis.major_label_text_font_size = '5pt'
    pu.xaxis.major_label_text_font_size = '7pt'
    pu.outline_line_color=None
    pu.axis.major_label_text_font_style = 'bold'
    pu.yaxis.major_tick_line_color = None
    pu.axis.axis_line_color = None
    pu.min_border = 0
    pu.x_range.range_padding = -0.1
    pu.toolbar.autohide = True
    pu.xaxis.formatter.use_scientific = False
    pu.x_range.end = 92

    pu.grid.grid_line_dash = 'dotted'
    pu.grid.grid_line_dash_offset = 5
    pu.grid.grid_line_width = 2


    xrange_u = list(dfadd.index.values)
    colours_u = GnBu[5][::-1]
    color_mapper_u = LinearColorMapper(palette = colours_u[::-1], low = dfadd.values.min(), high = dfadd.values.max())

    source_u = ColumnDataSource(data=dict(x=xrange_u, y=dfadd['RuralPop'], y1=dfadd['UrbanPop']))

    p_u = figure(x_range=xrange_u, plot_height=180, plot_width=320, title='Urban Population by Age Group',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right') # ['#b32134', '#e1888f']
    p_u.vbar(top='y1', x='x', width=.45, fill_color='#2b8cbe', line_color=None, source=source_u)
    p_u.yaxis.formatter.use_scientific = False
    hover_u = HoverTool()

    hover_u.tooltips=[('Age Group', '@x'), ('Urban Population','@y1{0.0 a}'), ('Rural Population', '@y{0.0 a}')]
    p_u.add_tools(hover_u)

    tick_labels_u = {'100000':'100K','200000':'200K','300000':'300K','400000':'400K','600000':'600K','800000':'800K','1000000':'1M','1200000':'1.2M'}
    p_u.yaxis.major_label_overrides = tick_labels_u

    p_u.yaxis.major_label_standoff = -2
    p_u.yaxis.major_label_text_font_size = '6pt'
    p_u.xaxis.major_label_text_font_size = '6.5pt'
    p_u.title.text_font_size = '11px'
    p_u.grid.grid_line_dash = 'dotted'
    p_u.grid.grid_line_dash_offset = 5
    p_u.grid.grid_line_width = 2
    p_u.grid.grid_line_alpha = 0.6

    p_u.outline_line_color=None
    p_u.yaxis.major_label_text_align = 'center'
    p_u.axis.major_label_text_font_style = 'bold'
    p_u.min_border = 0
    p_u.x_range.range_padding = 0
    p_u.toolbar.autohide = True
    p_u.yaxis.major_label_standoff = 0
    p_u.y_range.start=0

    prr = column([pr, p_a])
    prr1 = row([prm, prr], spacing=-50)

    pru1 = column([pu, p_u])
    pru2 = row([pum, pru1], spacing=-50)

    tr = Panel(child=prr1, title='Rural Population 2016')
    tu = Panel(child=pru2, title='Urban Population 2016')
    tdd = Panel(child=p3, title='Demographic Density 2016')
    tabs = Tabs(tabs=[tdd,tu,tr])

    return tabs

def SwDD():

    dfus = pd.read_csv('BokehApp/DataRA/swCpop.csv', delimiter=',', index_col=0)
    sw1 = pd.read_csv('BokehApp/DataRA/sw1.csv', delimiter=',', index_col=0)
    with open('BokehApp/DataRA/dfjsonsSW.json', 'r', encoding='utf8') as openfilesw: 
            # Reading from json file 
            geo_jsonswd = GeoJSONDataSource(geojson=openfilesw.read())

    pmsw = figure(title = 'Urban Population in %', x_axis_location = None, y_axis_location = None, plot_height=680, plot_width=380,
                tools = 'pan, wheel_zoom, box_zoom, reset, hover, save', tooltips = [('County', '@county'),('Urban Population','@Urban_16pct{0.00} %')])

    coloursDD = ['#ff0000','#ff2424','#ff4747','#ff6b6b','#ff8f8f','#ffb3b3','#ffd6d6']
    coloursw = GnBu[8][::-1]
    tick_labelsw = {'60':'60%','65':'65%','70':'70%','75':'75%','80':'80%','85':'85%','90':'90%','95':'95%','100':'100%'}

    color_mappersw = LinearColorMapper(palette = coloursw, low = 60, high = 100)
    color_barsw = ColorBar(color_mapper=color_mappersw, label_standoff=6, width = 300, height = 20, ticker=BasicTicker(desired_num_ticks=len(coloursw)), major_label_text_font_style='bold',
                         border_line_color=None, location = 'center', orientation = 'horizontal', bar_line_color='#50C878', bar_line_alpha=0.7, major_label_overrides = tick_labelsw)
    #color_bar.label_text_style = 'bold'

    pmsw.patches('xs', 'ys', fill_alpha = 0.7, line_width = 0.5, source = geo_jsonswd, line_cap=None, line_color='black',
                fill_color = {'field' :'Urban_16pct', 'transform' : color_mappersw})
    pmsw.add_layout(color_barsw, 'below')
    pmsw.grid.grid_line_color=None
    pmsw.outline_line_color=None
    pmsw.toolbar.autohide = True

    pmsw.title.text_font_style = "bold"
    pmsw.title.text_font_size = '20px'
    pmsw.title.align ='left'

    y16 = Label(x=0, y=550, x_units='screen', y_units='screen',
                         text='2016', render_mode='css', text_font_size='22.5pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsw.add_layout(y16)

    dfswu = pd.DataFrame(dfus.sort_values('Urban_16pct', ascending=False))

    yrangeswu = dfswu.index.to_list()
    #yrangeswu = reverse(yrangeswu)

    sourceswu = ColumnDataSource(data=dict(y=yrangeswu,x=dfswu['Urban_16pct']))
    color_mapperswu = LinearColorMapper(palette= coloursw, low=60, high=100)

    pswu = figure(y_range=yrangeswu[::-1], title='Urban Population by County in %', plot_height=500, plot_width=330, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pswu.hbar(y='y', height=.7, right='x',  left=0, source=sourceswu, line_color="black", line_width = 0.1, fill_color={'field':'x','transform':color_mapperswu})


    hoverpswu = HoverTool()
    hoverpswu.tooltips=[('county', '@y'), ('Urban Population', '@x{0.00} %')]

    pswu.add_tools(hoverpswu)
    pswu.yaxis.major_label_standoff = -2
    pswu.yaxis.major_label_text_font_size = '7.5pt'
    pswu.xaxis.major_label_text_font_size = '7pt'
    #p1.grid.grid_line_color=None
    pswu.outline_line_color=None
    #p1.yaxis.major_label_text_align = 'center'
    pswu.axis.major_label_text_font_style = 'bold'
    pswu.yaxis.major_tick_line_color = None
    pswu.axis.axis_line_color = None
    pswu.min_border = 0
    pswu.x_range.range_padding = -0.1
    pswu.toolbar.autohide = True
    #p1.yaxis.major_label_standoff = 0
    pswu.xaxis.formatter.use_scientific = False
    pswu.x_range.end = 103

    tick_labelswu = {'20':'20%','40':'40%','60':'60%','80':'80%','100':'100%'}
    pswu.xaxis.major_label_overrides = tick_labelswu

    pswu.grid.grid_line_dash = 'dotted'
    pswu.grid.grid_line_dash_offset = 5
    pswu.grid.grid_line_width = 2


    psf = figure(x_axis_location = None, y_axis_location = None, plot_width=185, plot_height=750, tools='')
    psf.image_url(url=['static/imagesRA/swleaflet3.png'], x=0, y=0, w=1, h=3.5, anchor='bottom_left', level='image')
    #psf.title.align='center'    
    psf.grid.grid_line_color=None
    psf.outline_line_color=None
    #psf.toolbar = None
    #psf.toolbar.autohide = True
    psf.toolbar.logo = None
    psf.title.text_font_style = "bold"
    psf.y_range.bounds=(-30,750)
    #psf.y_range.start=0

    dfsur = pd.read_csv('BokehApp/DataRA/SwPopRuralUrbanAgeGroup.csv', delimiter=',', index_col=0)

    xr = dfsur.index.tolist()
    sourcesur = ColumnDataSource(data=dict(x=xr, y=dfsur['UrbanMale'], y1=dfsur['UrbanFemale']))

    psur = figure(x_range=FactorRange(*xr), plot_height=180, plot_width=330, title='Urban Population by Age Group and Sex',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    psur.vbar(x=dodge('x',-0.25, range=psur.x_range), top='y', width=.2, color='#43a2ca', source=sourcesur, legend_label='Male')
    psur.vbar(x=dodge('x',0, range=psur.x_range), top='y1', width=.2, color='#ccebc5', source=sourcesur, legend_label='Female')
    psur.yaxis.formatter.use_scientific = False
    hoversur = HoverTool()

    hoversur.tooltips=[('Age Group', '@x'), ('Male Population','@y{0.0 a}'), ('Female Population', '@y1{0.0 a}')]
    psur.add_tools(hoversur)

    tick_labelsur = {'500000':'0.5M','2000000':'2M','1500000':'1.5M','2500000':'2.5M','600000':'600K','800000':'800K','1000000':'1M','1200000':'1.2M'}
    psur.yaxis.major_label_overrides = tick_labelsur

    psur.legend.location= 'top_right'#(370,180)
    psur.legend.background_fill_alpha=None
    psur.legend.click_policy="hide"
    psur.legend.border_line_alpha=None

    psur.yaxis.major_label_standoff = -2
    psur.yaxis.major_label_text_font_size = '6pt'
    psur.xaxis.major_label_text_font_size = '6.5pt'
    psur.title.text_font_size = '9px'
    psur.grid.grid_line_dash = 'dotted'
    psur.grid.grid_line_dash_offset = 5
    psur.grid.grid_line_width = 2
    psur.grid.grid_line_alpha = 0.6

    psur.outline_line_color=None
    psur.yaxis.major_label_text_align = 'center'
    psur.axis.major_label_text_font_style = 'bold'
    psur.min_border = 0
    psur.x_range.range_padding = 0
    psur.toolbar.autohide = True
    psur.yaxis.major_label_standoff = 0
    psur.y_range.start=0


    dfswu = pd.DataFrame(dfus.sort_values('Urban_16pct', ascending=False))


    pmsdd = figure(title = 'Sweden Demographic Density', x_axis_location = None, y_axis_location = None, plot_height=680, plot_width=380,
                tools = 'pan, wheel_zoom, box_zoom, reset, hover, save', tooltips = [('County', '@county'),('Demographic Density','@PopDDkm2_16{0.00} pp/km2')])

    coloursDD = ['#ff0000','#ff2424','#ff4747','#ff6b6b','#ff8f8f','#ffb3b3','#ffd6d6']

    #tick_labelsw = {'60':'60%','65':'65%','70':'70%','75':'75%','80':'80%','85':'85%','90':'90%','95':'95%','100':'100%'}

    color_mappersdd = LinearColorMapper(palette = coloursDD[::-1], low = 0, high = 70)
    color_barsdd = ColorBar(color_mapper=color_mappersdd, label_standoff=6, width = 275, height = 20, ticker=BasicTicker(desired_num_ticks=len(coloursDD)), major_label_text_font_style='bold',
                         border_line_color=None, location = 'center', orientation = 'horizontal', bar_line_color='#50C878', bar_line_alpha=0.7)#, major_label_overrides = tick_labelsw)
    #color_bar.label_text_style = 'bold'
    #color_barsdd.title_text_align = (0,0)
    #title='Population p/Km2', title_text_align='left', 

    pmsdd.patches('xs', 'ys', fill_alpha = 0.7, line_width = 0.5, source = geo_jsonswd, line_cap=None, line_color='black',
                fill_color = {'field' :'PopDDkm2_16', 'transform' : color_mappersdd})
    pmsdd.add_layout(color_barsdd, 'below')
    pmsdd.grid.grid_line_color=None
    pmsdd.outline_line_color=None
    pmsdd.toolbar.autohide = True

    pmsdd.title.text_font_style = "bold"
    pmsdd.title.text_font_size = '20px'
    pmsdd.title.align ='left'

    y16d = Label(x=0, y=550, x_units='screen', y_units='screen',
                         text='2016', render_mode='css', text_font_size='22.5pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(y16d)

    sdd1 = Label(x=30, y=490, x_units='screen', y_units='screen',
                         text='Stockholm', render_mode='css', text_font_size='11pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(sdd1)

    sdd = Label(x=15, y=470, x_units='screen', y_units='screen',
                         text='347.8', render_mode='css', text_font_size='14pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(sdd)

    sdp = Label(x=10, y=454, x_units='screen', y_units='screen',
                         text='People', render_mode='css', text_font_size='9pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(sdp)

    sdp1 = Label(x=35, y=442, x_units='screen', y_units='screen',
                         text='per Km', render_mode='css', text_font_size='9pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(sdp1)

    sdp2 = Label(x=76, y=448, x_units='screen', y_units='screen',
                         text='2', render_mode='css', text_font_size='5pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(sdp2)

    scb = Label(x=125, y=-13, x_units='screen', y_units='screen',
                         text='Population per km', render_mode='css', text_font_size='8pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(scb)

    scb1 = Label(x=218, y=-9, x_units='screen', y_units='screen',
                         text='2', render_mode='css', text_font_size='5pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsdd.add_layout(scb1)



    dfsdd = pd.DataFrame(dfus.sort_values('PopDDkm2_16', ascending=False))
    dfsdd = dfsdd[1:]
    dfsdd

    yrangesdd = dfsdd.index.to_list()

    sourcesdd = ColumnDataSource(data=dict(y=yrangesdd, x=dfsdd['PopDDkm2_16']))
    color_mappersdd = LinearColorMapper(palette=coloursDD[::-1], low=0, high=70)

    psdd  = figure(y_range=yrangesdd[::-1], title='Demographic Density by County', plot_height=470, plot_width=330, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    psdd.hbar(y='y', height=.7, right='x',  left=0, source=sourcesdd, line_color="black", line_width = 0.1, fill_color={'field':'x','transform':color_mappersdd})

    hoverpsdd = HoverTool()
    hoverpsdd.tooltips=[('county', '@y'), ('Demographic Density', '@x{0.00} People p/km2')]

    psdd.add_tools(hoverpsdd)
    psdd.yaxis.major_label_standoff = -2
    psdd.yaxis.major_label_text_font_size = '7.5pt'
    psdd.xaxis.major_label_text_font_size = '7pt'
    #p1.grid.grid_line_color=None
    psdd.outline_line_color=None
    #p1.yaxis.major_label_text_align = 'center'
    psdd.axis.major_label_text_font_style = 'bold'
    psdd.yaxis.major_tick_line_color = None
    psdd.axis.axis_line_color = None
    psdd.min_border = 0
    psdd.x_range.range_padding = -0.1
    psdd.toolbar.autohide = True
    #p1.yaxis.major_label_standoff = 0
    psdd.xaxis.formatter.use_scientific = False

    tick_labelsdd = {'20':'20%','40':'40%','60':'60%','80':'80%','100':'100%','120':'120%','140':'140%'}
    psdd.xaxis.major_label_overrides = tick_labelsdd

    psdd.grid.grid_line_dash = 'dotted'
    psdd.grid.grid_line_dash_offset = 5
    psdd.grid.grid_line_width = 2
    psdd.x_range.end = 150

    labelsdd = LabelSet(x='x', y='y', text='x', level='glyph', text_font_size='6.5pt', text_font_style='bold',
            x_offset=10, y_offset=-4, source=sourcesdd, render_mode='canvas')
    psdd.add_layout(labelsdd)


    dfsd = pd.DataFrame(dfus.sort_values('Urban_16pct', ascending=False))

    xrangesd = dfsd.index.to_list()
    #yrangeswu = reverse(yrangeswu)

    sourcesd = ColumnDataSource(data=dict(x=xrangesd ,y=dfsd['Urban_16pct'], y1=dfsd['Rural_16pct']))
    color_mappersd = LinearColorMapper(palette= coloursDD[::-1], low=60, high=100)

    psd = figure(x_range=xrangesd, title='Urban Population by County in %', plot_height=200, plot_width=330, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    psd.vbar(top='y', width=.55, x='x', source=sourcesd, line_color="black", line_width = 0.1, fill_color={'field':'y','transform':color_mappersd})


    hoverpsd = HoverTool()
    hoverpsd.tooltips=[('county', '@x'), ('Urban Population', '@y{0.00} %'), ('Rural Population', '@y1{0.00} %')]

    psd.add_tools(hoverpsd)
    psd.yaxis.major_label_standoff = -2
    psd.yaxis.major_label_text_font_size = '7.5pt'
    psd.xaxis.major_label_text_font_size = '5pt'
    psd.outline_line_color=None
    psd.axis.major_label_text_font_style = 'bold'
    psd.min_border = 0
    psd.x_range.range_padding = -0.1
    psd.toolbar.autohide = True

    tick_labelsd = {'70':'70%','75':'75%','85':'85%','80':'80%','90':'90%'}
    psd.yaxis.major_label_overrides = tick_labelsd

    psd.grid.grid_line_dash = 'dotted'
    psd.grid.grid_line_dash_offset = 5
    psd.grid.grid_line_width = 2
    psd.y_range.start = 70
    psd.y_range.end = 92
    psd.xaxis.major_label_orientation = 45


    pmsr = figure(title = 'Rural Population in %', x_axis_location = None, y_axis_location = None, plot_height=680, plot_width=380,
                tools = 'pan, wheel_zoom, box_zoom, reset, hover, save', tooltips = [('County', '@county'),('Rural Population','@Rural_16pct{0.00} %')])

    coloursr = Greens[7][::-1]
    tick_labelsr = {'5':'5%','10':'10%','15':'15%','20':'20%','25':'25%','30':'30%','35':'35%','40':'40%'}

    color_mappersr = LinearColorMapper(palette = coloursr, low = 0, high = 35)
    color_barsr = ColorBar(color_mapper=color_mappersr, label_standoff=6, width = 300, height = 20, ticker=BasicTicker(desired_num_ticks=len(coloursr)), major_label_text_font_style='bold',
                         border_line_color=None, location = 'center', orientation = 'horizontal', bar_line_color='#50C878', bar_line_alpha=0.7, major_label_overrides = tick_labelsr)
    #color_bar.label_text_style = 'bold'

    pmsr.patches('xs', 'ys', fill_alpha = 0.7, line_width = 0.5, source = geo_jsonswd, line_cap=None, line_color='black',
                fill_color = {'field' :'Rural_16pct', 'transform' : color_mappersr})
    pmsr.add_layout(color_barsr, 'below')
    pmsr.grid.grid_line_color=None
    pmsr.outline_line_color=None
    pmsr.toolbar.autohide = True

    pmsr.title.text_font_style = "bold"
    pmsr.title.text_font_size = '20px'
    pmsr.title.align ='left'

    y16r = Label(x=0, y=550, x_units='screen', y_units='screen',
                         text='2016', render_mode='css', text_font_size='22.5pt', text_color='black', text_font_style='bold',
                         text_align='left', angle=0, text_alpha=0.6)
    pmsr.add_layout(y16r)



    dfsr = pd.DataFrame(dfus.sort_values('Rural_16pct', ascending=False))

    yrsr = dfsr.index.to_list()

    sourcesr = ColumnDataSource(data=dict(y=yrsr, x=dfsr['Rural_16pct']))

    phsr = figure(y_range=yrsr[::-1], title='Rural Population by County in %', plot_height=500, plot_width=330, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    phsr.hbar(y='y', height=.7, right='x',  left=0, source=sourcesr, line_color="black", line_width = 0.1, fill_color={'field':'x','transform':color_mappersr})


    hoverphsr = HoverTool()
    hoverphsr.tooltips=[('county', '@y'), ('Rural Population', '@x{0.00} %')]

    phsr.add_tools(hoverphsr)
    phsr.yaxis.major_label_standoff = -2
    phsr.yaxis.major_label_text_font_size = '7.5pt'
    pswu.xaxis.major_label_text_font_size = '5.5pt'
    #p1.grid.grid_line_color=None
    phsr.outline_line_color=None
    #p1.yaxis.major_label_text_align = 'center'
    phsr.axis.major_label_text_font_style = 'bold'
    phsr.yaxis.major_tick_line_color = None
    phsr.axis.axis_line_color = None
    phsr.min_border = 0
    phsr.x_range.range_padding = -0.1
    phsr.toolbar.autohide = True
    #p1.yaxis.major_label_standoff = 0
    phsr.xaxis.formatter.use_scientific = False
    phsr.x_range.end = 40

    tick_labelshsr = {'5':'5%','10':'10%','15':'15%','20':'20%','25':'25%','30':'30%','35':'35%','40':'40%'}
    phsr.xaxis.major_label_overrides = tick_labelshsr

    phsr.grid.grid_line_dash = 'dotted'
    phsr.grid.grid_line_dash_offset = 5
    phsr.grid.grid_line_width = 2


    xru = dfsur.index.tolist()
    sourcesru = ColumnDataSource(data=dict(x=xr, y=dfsur['RuralMale'], y1=dfsur['RuralFemale']))

    psru = figure(x_range=FactorRange(*xru), plot_height=180, plot_width=330, title='Rural Population by Age Group and Sex',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    psru.vbar(x=dodge('x',-0.25, range=psru.x_range), top='y', width=.2, color='#31a354', source=sourcesru, legend_label='Male')
    psru.vbar(x=dodge('x',0, range=psur.x_range), top='y1', width=.2, color='#c7e9c0', source=sourcesru, legend_label='Female')
    psru.yaxis.formatter.use_scientific = False
    hoversru = HoverTool()

    hoversru.tooltips=[('Age Group', '@x'), ('Male Population','@y{0.0 a}'), ('Female Population', '@y1{0.0 a}')]
    psru.add_tools(hoversur)

    tick_labelsru = {'50000':'50K','100000':'100K','150000':'150K','250000':'250K','200000':'200K','300000':'300K','350000':'350K'}
    psru.yaxis.major_label_overrides = tick_labelsru

    psru.legend.location= 'top_right'#(370,180)
    psru.legend.background_fill_alpha=None
    psru.legend.click_policy="hide"
    psru.legend.border_line_alpha=None

    psru.yaxis.major_label_standoff = -2
    psru.yaxis.major_label_text_font_size = '6pt'
    psru.xaxis.major_label_text_font_size = '6.5pt'
    psru.title.text_font_size = '9px'
    psru.grid.grid_line_dash = 'dotted'
    psru.grid.grid_line_dash_offset = 5
    psru.grid.grid_line_width = 2
    psru.grid.grid_line_alpha = 0.6

    psru.outline_line_color=None
    psru.yaxis.major_label_text_align = 'center'
    psru.axis.major_label_text_font_style = 'bold'
    psru.min_border = 0
    psru.x_range.range_padding = 0
    psru.toolbar.autohide = True
    psru.yaxis.major_label_standoff = 0
    psru.y_range.start=0

    ptt1 = column([pswu, psur])
    ptt = row([pmsw, ptt1])

    pdd2 = column([psdd, psd])
    pdd1 = row([psf, pmsdd, pdd2], align='center', spacing=-5)

    c = column([phsr, psru])
    r = row([pmsr, c])

    tr = Panel(child=r, title='Rural Population 2016')
    tu = Panel(child=ptt, title='Urban Population 2016')
    tdd = Panel(child=pdd1, title='Demographic Density 2016')
    tabs = Tabs(tabs=[tdd,tu,tr])

    return tabs