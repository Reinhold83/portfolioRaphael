#imports
import pandas as pd
from bokeh.resources import INLINE
from bokeh.plotting import figure, show, curdoc
#from bokeh.util.string import encode_utf8
from bokeh.transform import dodge
from math import pi
from bokeh.transform import cumsum
from bokeh.layouts import column, row, gridplot
#from bokeh.core.properties import value
from bokeh.models import ColumnDataSource, Label, BoxAnnotation, PrintfTickFormatter, NumeralTickFormatter, FactorRange, Paragraph, LinearColorMapper, Tabs, Panel, HoverTool, Div, Select, CustomJS, Range1d, ColorBar, BasicTicker
from bokeh.transform import factor_cmap
from bokeh.models.widgets import Panel, Tabs
from bokeh.palettes import viridis
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

    pm = figure(y_axis_location = None, plot_height=320, plot_width=270, y_range=gs, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pm.hbar(y='y', height=1, right='_2019_',  source=sourceSm, legend_label='male', line_color="white", fill_color='#FFCD00')

    #plot style
    hoverpm = HoverTool()
    hoverpm.tooltips=[('Age Group', '@y'),('Population', '@_2019_')]
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
    #pm.x_range.end = 370000*1.003
    #pm.xaxis.major_label_orientation = 45
    tick_labels_pm = {'50000':'50K','100000':'100K','150000':'150K','200000':'200K','250000':'250K', '300000':'300K', '350000':'350K'}
    pm.xaxis.major_label_overrides = tick_labels_pm

    pf = figure(plot_height=320, plot_width=295, y_range=gs, tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    pf.hbar(y='y', height=1, right='_2019_',  source=sourceSf, legend_label='female', line_color="white", fill_color='#004B87')

    hoverpf = HoverTool()
    hoverpf.tooltips=[('Age Group', '@y'), ('Population', '@_2019_')]

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
    #pf.xaxis.major_label_orientation = 45
    tick_labels_pf = {'50000':'50K','100000':'100K','150000':'150K','200000':'200K','250000':'250K', '300000':'300K', '350000':'350K'}
    pf.xaxis.major_label_overrides = tick_labels_pf
    #pf.x_range.end = 370000*1.003
    pm.title.text_font_size = '8.5pt'
    pm.title.text = 'Swedish Population by Age/Gender Group 2019'
    pm.title.align = 'left'


    #Population by ageGroup
    df_ageOverall = pd.read_csv('BokehApp/DataRA/SwedishPop_ageGroupOverall.csv', delimiter=',')
    df_ageOverall = df_ageOverall.iloc[::, 8:]
    df_ageOverall['color'] = viridis(len(df_ageOverall.index))
    df_ageOverall.head()

    sourceOverall = ColumnDataSource(data=dict(x=gs, color=df_ageOverall['color'], _2019_=df_ageOverall['2019'], _2015=df_ageOverall['2015'], _2016=df_ageOverall['2016'], _2017=df_ageOverall['2017'], _2018=df_ageOverall['2018'],_2019=df_ageOverall['2019']))

    pO = figure(x_range=gs, plot_height=320, plot_width=460,title='Swedish Population by Age Group 2019',
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
    hoverpO.tooltips=[('Age Group','@x'),('Population', '@_2019_')]
    pO.add_tools(hoverpO)

    tick_labels_pO = {'100000':'100K','200000':'200K','300000':'300K','400000':'400K','500000':'500K','600000':'600K','700000':'700K'}
    pO.yaxis.major_label_overrides = tick_labels_pO

    select = Select(title="Select year:", align='start', value='_2019_', width=80, height=25, options=['_2015','_2016','_2017','_2018','_2019'])

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


    #yearly growth
    dfpopSw = pd.read_csv('BokehApp/DataRA/swedishPopOverall.csv', delimiter=',', index_col=0)
    dfpopSw = dfpopSw.iloc[2:] 
    ys = list(dfpopSw.index.values)
    xrange = '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'

    dfpopSw['color'] = viridis(len(dfpopSw.index))

    yrange = (9000000, dfpopSw['Population'].max())

    source = ColumnDataSource(dfpopSw)

    pS = figure(plot_height=320, plot_width=400,title='Swedish Population Growth by Year',
               y_range=Range1d(*yrange),tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='below')
    pS.vbar(x='Year', top='Population', source=source, width=0.5, color='#004B87')

    pS.y_range.end = dfpopSw['Population'].max()*1.003
    pS.outline_line_color=None
    pS.axis.major_label_text_font_style = 'bold'
    pS.grid.grid_line_dash = 'dotted'
    pS.grid.grid_line_dash_offset = 5
    pS.grid.grid_line_width = 2
    #pS.toolbar.autohide=True
    pS.yaxis.formatter.use_scientific = False


    hoverpS = HoverTool()
    hoverpS.tooltips=[('Year','@Year'),('Population', '@Population{int}')]
    pS.add_tools(hoverpS)

    tick_labels_pS = {'9000000':'9M','9200000':'9.2M','9400000':'9.4M','9600000':'9.6M','9800000':'9.8M','10000000':'10M', '10200000':'10.2M'}
    pS.yaxis.major_label_overrides = tick_labels_pS

    p = gridplot([[pm, pf]], toolbar_location='left', merge_tools=True)#, toolbar_options = {'autohide':True})

    layout = row([select, p, pO, pS], margin=(10,40), spacing=25, align='center')
    #layout1 = row([pS, pIS], spacing=-10)#, sizing_mode='fixed')
    
    return layout

def swedishpop1():
    #piechart
    pIS = figure(x_axis_location = None, y_axis_location = None, plot_width=530, plot_height=330, tools='')
    pIS.image_url(url=['static/imagesRA/SwedishChart_edit.png'], x=0, y=0, w=2, h=2, anchor="bottom_left")
    pIS.title.align='center'    
    pIS.grid.grid_line_color=None
    pIS.outline_line_color=None
    pIS.toolbar.logo=None

    pIrl = figure(x_axis_location = None, y_axis_location = None, plot_width=450, plot_height=330, tools='')
    pIrl.image_url(url=['static/imagesRA/Irish_pie.png'], x=0, y=0, w=2, h=2, anchor="bottom_left")
    pIrl.title.align='center'    
    pIrl.grid.grid_line_color=None
    pIrl.outline_line_color=None
    pIrl.toolbar.logo=None

    layout = row([pIS, pIrl])

    return layout

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
    #pm.x_range.end = 370000*1.003
    #pm.xaxis.major_label_orientation = 45
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
    #pf.xaxis.major_label_orientation = 45
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
    pIO.x_range.end = 2018.5
    pIO.y_range.start = 4500
    pIO.y_range.end = dfIO['Population'].max()*1.003
    pIO.outline_line_color=None
    pIO.axis.major_label_text_font_style = 'bold'
    pIO.grid.grid_line_dash = 'dotted'
    pIO.grid.grid_line_dash_offset = 5
    pIO.grid.grid_line_width = 2
    #pIO.toolbar.autohide=True
    #p.yaxis.axis_line_color = None

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
    #pO.toolbar.autohide = True
    pIG.grid.grid_line_dash = 'dotted'
    pIG.grid.grid_line_dash_offset = 5
    pIG.grid.grid_line_width = 2
    #pO.toolbar.autohide=True
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
    pRF = figure(x_axis_location = None, y_axis_location = None, plot_width=400, plot_height=295)
    pRF.image_url(url=['static/imagesRA/01_RFlu1.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pRF.title.align='center'    
    pRF.grid.grid_line_color=None
    pRF.outline_line_color=None
    pRF.toolbar.autohide = True
    pRF.title.text_font_style = "bold"

    pSF = figure(x_axis_location = None, y_axis_location = None, plot_width=380, plot_height=290)
    pSF.image_url(url=['static/imagesRA/02_spFlu.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pSF.title.align='center'    
    pSF.grid.grid_line_color=None
    pSF.outline_line_color=None
    pSF.toolbar.autohide = True
    pSF.title.text_font_style = "bold"

    pRA = figure(x_axis_location = None, y_axis_location = None, plot_width=410, plot_height=300)
    pRA.image_url(url=['static/imagesRA/03_AsianFlu_2.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pRA.title.align='center'    
    pRA.grid.grid_line_color=None
    pRA.outline_line_color=None
    pRA.toolbar.autohide = True
    pRA.title.text_font_style = "bold"

    pHK = figure(x_axis_location = None, y_axis_location = None, plot_width=400, plot_height=300)
    pHK.image_url(url=['static/imagesRA/04_HKFlu_1.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pHK.title.align='center'    
    pHK.grid.grid_line_color=None
    pHK.outline_line_color=None
    pHK.toolbar.autohide = True
    pHK.title.text_font_style = "bold"

    pSW = figure(x_axis_location = None, y_axis_location = None, plot_width=410, plot_height=300)
    pSW.image_url(url=['static/imagesRA/05_swineFlu.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pSW.title.align='center'    
    pSW.grid.grid_line_color=None
    pSW.outline_line_color=None
    pSW.toolbar.autohide = True
    pSW.title.text_font_style = "bold"

    pCV = figure(x_axis_location = None, y_axis_location = None, plot_width=400, plot_height=300)
    pCV.image_url(url=['static/imagesRA/07_covid19__.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pCV.title.align='center'    
    pCV.grid.grid_line_color=None
    pCV.outline_line_color=None
    pCV.toolbar.autohide = True
    pCV.title.text_font_style = "bold"

    grid = gridplot([[pRF, pSF, pRA], [pHK, pSW, pCV], []], merge_tools=True, sizing_mode='fixed',toolbar_location='right')
    #layout = row([pRF, pSF], margin=(10,40), spacing=10, align='center')
    return grid

def pandemics1():
    pF = figure(x_axis_location = None, y_axis_location = None, plot_width=430, plot_height=310)
    pF.image_url(url=['static/imagesRA/06_Flu_.png'], x=0, y=0, w=2, h=1, anchor="bottom_left")
    pF.title.align='center'    
    pF.grid.grid_line_color=None
    pF.outline_line_color=None
    pF.toolbar.autohide = True
    pF.title.text_font_style = "bold"

    return pF