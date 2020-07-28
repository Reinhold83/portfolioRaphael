
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
from bokeh.models import ColumnDataSource, PrintfTickFormatter, NumeralTickFormatter, FactorRange, LinearColorMapper, Tabs, Panel, HoverTool, Div, Select, CustomJS, Range1d, ColorBar, BasicTicker
from bokeh.transform import factor_cmap
from bokeh.models.widgets import Panel, Tabs
from bokeh.palettes import viridis
from bokeh.resources import CDN
from bokeh.embed import file_html


def maps():
    
    
    p16 = figure(x_axis_location = None, y_axis_location = None, plot_width=550)
    p16.image_url(url=['/static/images/pp16sub.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p16.title.align='center'    
    p16.grid.grid_line_color=None
    p16.outline_line_color=None
    p16.toolbar.autohide = True
    p16.title.text_font_style = "bold"
        
    p11 = figure(x_axis_location = None, y_axis_location = None, plot_width=550)
    p11.image_url(url=['/static/images/pp11sub.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p11.title.align='center'    
    p11.grid.grid_line_color=None
    p11.outline_line_color=None
    p11.toolbar.autohide = True
    p11.title.text_font_style = "bold"

    p06 = figure(x_axis_location = None, y_axis_location = None, plot_width=550)
    p06.image_url(url=['/static/images/pp06sub.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p06.title.align='center'    
    p06.grid.grid_line_color=None
    p06.outline_line_color=None
    p06.toolbar.autohide = True
    p06.title.text_font_style = "bold"

    p02 = figure(x_axis_location = None, y_axis_location = None, plot_width=550)
    p02.image_url(url=['/static/images/pp02sub.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p02.title.align='center'    
    p02.grid.grid_line_color=None
    p02.outline_line_color=None
    p02.toolbar.autohide = True
    p02.title.text_font_style = "bold"

    t02 = Panel(child=p02, title='2002')
    t06 = Panel(child=p06, title='2006')
    t11 = Panel(child=p11, title='2011')
    t16 = Panel(child=p16, title='2016')
    tabs = Tabs(tabs=[t16,t11,t06,t02])

    return tabs


def ageGroup():

    df = pd.read_csv('BokehApp/Data/popByAgeGroup_v2.csv', delimiter=',', index_col='AgeGroup')
    df_pivot1 = df.pivot_table(values=['2002','2003','2004','2005','2006','2007', '2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019'],index='sex', columns='AgeGroup')
    

    ys= list(df.index.unique())
    source = ColumnDataSource(data=dict(y=ys,x02f=df_pivot1.loc['female']['2002'],x02m=df_pivot1.loc['male']['2002'],x06f=df_pivot1.loc['female']['2006'],x06m=df_pivot1.loc['male']['2006'], x11f=df_pivot1.loc['female']['2011'],x11m=df_pivot1.loc['male']['2011'],x16f=df_pivot1.loc['female']['2016'],x16m=df_pivot1.loc['male']['2016']))

    #tick_labels_g = {'01 - 01':'0 - 1','01 - 04':'1 - 4','05 - 09':'5 - 9','85_+':'85+'}

    #plots
    
    #plot fig right
    p2m = figure(y_axis_location = None, plot_height=300, plot_width=250, y_range=ys)
    p2m.hbar(y="y", height=1, right='x02m', legend_label='male', source=source, line_color="white", fill_color='#FDE724')

    #plot style
    hoverp2m = HoverTool()
    hoverp2m.tooltips=[('Population', '@x02m')]
    p2m.add_tools(hoverp2m)
    p2m.x_range.flipped = True
    p2m.grid.grid_line_color=None
    p2m.outline_line_color=None
    p2m.x_range.range_padding = 0
    p2m.axis.major_label_text_font_style = 'bold'
    p2m.toolbar.autohide = True
    p2m.axis.axis_line_color = None
    p2m.legend.location = 'top_left'
    p2m.legend.background_fill_alpha = None
    p2m.legend.border_line_color = None


    #plot fig left
    p2f = figure(plot_height=300, plot_width=270, y_range=ys)
    p2f.hbar(y="y", height=1, right='x02f', legend_label='female', source=source, line_color="white", fill_color='#440154')

    hoverp2f = HoverTool()
    hoverp2f.tooltips=[('Population', '@x02f')]

    #plot style
    p2f.add_tools(hoverp2f)
    p2f.legend.background_fill_alpha = None
    p2f.legend.border_line_color = None
    p2f.yaxis.major_label_standoff = -1
    p2f.yaxis.major_label_text_font_size = '8pt'
    p2f.grid.grid_line_color=None
    p2f.outline_line_color=None
    p2f.yaxis.major_label_text_align = 'center'
    p2f.axis.major_label_text_font_style = 'bold'
    p2f.yaxis.major_tick_line_color = None
    p2f.axis.axis_line_color = None
    p2f.min_border = 0
    p2f.x_range.range_padding = 0
    p2f.toolbar.autohide = True
    p2f.yaxis.major_label_standoff = 0


    #plot fig right
    p6m = figure(y_axis_location = None, plot_height=300, plot_width=250, y_range=ys)
    p6m.hbar(y="y", height=1, right='x06m', legend_label='male', source=source, line_color="white", fill_color='#FDE724')

    #plot style
    hoverp6m = HoverTool()
    hoverp6m.tooltips=[('Population', '@x06m')]
    p6m.add_tools(hoverp6m)
    p6m.x_range.flipped = True
    p6m.grid.grid_line_color=None
    p6m.outline_line_color=None
    p6m.x_range.range_padding = 0
    p6m.axis.major_label_text_font_style = 'bold'
    p6m.toolbar.autohide = True
    p6m.axis.axis_line_color = None
    p6m.legend.location = 'top_left'
    p6m.legend.background_fill_alpha = None
    p6m.legend.border_line_color = None


    #plot fig left
    p6f = figure(plot_height=300, plot_width=270, y_range=ys)
    p6f.hbar(y="y", height=1, right='x06f', legend_label='female', source=source, line_color="white", fill_color='#440154')

    hoverp6f = HoverTool()
    hoverp6f.tooltips=[('Population', '@x06f')]

    #plot style
    p6f.add_tools(hoverp6f)
    p6f.legend.background_fill_alpha = None
    p6f.legend.border_line_color = None
    p6f.yaxis.major_label_standoff = -1
    p6f.yaxis.major_label_text_font_size = '8pt'
    p6f.grid.grid_line_color=None
    p6f.outline_line_color=None
    p6f.yaxis.major_label_text_align = 'center'
    p6f.axis.major_label_text_font_style = 'bold'
    p6f.yaxis.major_tick_line_color = None
    p6f.axis.axis_line_color = None
    p6f.min_border = 0
    p6f.x_range.range_padding = 0
    p6f.toolbar.autohide = True
    p6f.yaxis.major_label_standoff = 0

    #plot fig right
    p11m = figure(y_axis_location = None, plot_height=300, plot_width=250, y_range=ys)
    p11m.hbar(y="y", height=1, right='x11m', legend_label='male', source=source, line_color="white", fill_color='#FDE724')
    hoverp11m = HoverTool()
    hoverp11m.tooltips=[('Population', '@x11m')]
    p11m.add_tools(hoverp11m)

    #plot style
    p11m.x_range.flipped = True
    p11m.grid.grid_line_color=None
    p11m.outline_line_color=None
    p11m.x_range.range_padding = 0
    p11m.axis.major_label_text_font_style = 'bold'
    p11m.toolbar.autohide = True
    p11m.axis.axis_line_color = None
    p11m.legend.location = 'top_left'
    p11m.legend.background_fill_alpha = None
    p11m.legend.border_line_color = None


    #plot fig left
    p11f = figure(plot_height=300, plot_width=270, y_range=ys)
    p11f.hbar(y="y", height=1, right='x11f', legend_label='female', source=source, line_color="white", fill_color='#440154')

    hoverp11f = HoverTool()
    hoverp11f.tooltips=[('Population', '@x11f')]
    p11f.add_tools(hoverp11f)

    #plot style
    p11f.legend.background_fill_alpha = None
    p11f.legend.border_line_color = None
    p11f.yaxis.major_label_standoff = -1
    p11f.yaxis.major_label_text_font_size = '8pt'
    p11f.grid.grid_line_color=None
    p11f.outline_line_color=None
    p11f.yaxis.major_label_text_align = 'center'
    p11f.axis.major_label_text_font_style = 'bold'
    p11f.yaxis.major_tick_line_color = None
    p11f.axis.axis_line_color = None
    p11f.min_border = 0
    p11f.x_range.range_padding = 0
    p11f.toolbar.autohide = True
    p11f.yaxis.major_label_standoff = 0


    #plot fig right
    p16m = figure(y_axis_location = None, plot_height=300, plot_width=250, y_range=ys)
    p16m.hbar(y="y", height=1, right='x16m', legend_label='male', source=source, line_color="white", fill_color='#FDE724')
    hoverp16m = HoverTool()
    hoverp16m.tooltips=[('Population', '@x16m')]
    p16m.add_tools(hoverp16m)

    #plot style
    
   
    p16m.x_range.flipped = True
    p16m.grid.grid_line_color=None
    
    p16m.outline_line_color=None
    p16m.x_range.range_padding = 0
    p16m.axis.major_label_text_font_style = 'bold'
    p16m.toolbar.autohide = True
    p16m.axis.axis_line_color = None
    p16m.legend.location = 'top_left'
    p16m.legend.background_fill_alpha = None
    p16m.legend.border_line_color = None


    #plot fig left
    p16f = figure(plot_height=300, plot_width=270, y_range=ys)
    p16f.hbar(y="y", height=1, right='x16f', legend_label='female', source=source, line_color="white", fill_color='#440154')

    hoverp16f = HoverTool()
    hoverp16f.tooltips=[('Population', '@x16f')]
    p16f.add_tools(hoverp16f)

    
    #p16m.title_location = 'above'
    #p16m.title.align = 'left'
    #p16m.title.text_font_size = '12pt'
    #p16m.title.text_font_style = 'bold'

    #plot style
    #p16f.yaxis.major_label_overrides = tick_labels_g
    p16f.legend.background_fill_alpha = None
    p16f.legend.border_line_color = None
    p16f.yaxis.major_label_standoff = -1
    p16f.yaxis.major_label_text_font_size = '8pt'
    p16f.grid.grid_line_color=None
    
    p16f.outline_line_color=None
    p16f.yaxis.major_label_text_align = 'center'
    p16f.axis.major_label_text_font_style = 'bold'
    p16f.yaxis.major_tick_line_color = None
    p16f.axis.axis_line_color = None
    p16f.min_border = 0
    p16f.x_range.range_padding = 0
    p16f.toolbar.autohide = True
    p16f.yaxis.major_label_standoff = 0




    #Divs for griplot

    #Gridplots
    p02 = gridplot([[p2m, p2f]], toolbar_location='right', merge_tools=True)   
    p06 = gridplot([[p6m, p6f]], toolbar_location='right', merge_tools=True)
    p11 = gridplot([[p11m, p11f]], toolbar_location='right', merge_tools=True)
    p16 = gridplot([[p16m, p16f]], toolbar_location='right', merge_tools=True)



    #Tabs
    t02 = Panel(child=p02, title='2002')
    t06 = Panel(child=p06, title='2006')
    t11 = Panel(child=p11, title='2011')
    t16 = Panel(child=p16, title='2016')
    tabs = Tabs(tabs=[t16,t11,t06,t02])


    return tabs



def popByGroup():
    df1 = pd.read_csv('BokehApp/Data/ageGroupYear.csv', delimiter=',', index_col='Age Groups')
    df1['color'] = viridis(len(df1.index))

    source = ColumnDataSource(data=dict(x=df1.index, _2009=df1['2009'], _2010=df1['2010'], _2011=df1['2011'], _2012=df1['2012'], _2013=df1['2013'], _2014=df1['2014'], _2015=df1['2015'],  _2016=df1['2016'], _2017=df1['2017'], _2018=df1['2018'], c=df1['color'], _2009a=df1['2009']))
    source1 = ColumnDataSource(data=dict(x=df1.index, _2016=df1['2016'],c=df1['color']))


    p = figure(x_range=list(df1.index.values), plot_height=350, plot_width=550,title='Irish Population Breakdown by Age Group', tools='pan, wheel_zoom, box_zoom, reset')
    p.vbar(x='x', top='_2009a', width=0.5, source=source, color='c')

    #plot style
    p.xaxis.major_label_orientation = 45
    p.grid.grid_line_color=None
    p.outline_line_color=None
    p.axis.major_label_text_font_style = 'bold'
    p.toolbar.autohide = True

    hoverp = HoverTool()
    hoverp.tooltips=[('Group Population', '@_2009a')]
    p.add_tools(hoverp)


    tick_labels_p = {'100':'100K','200':'200K','300':'300K','400':'400K'}
    p.yaxis.major_label_overrides = tick_labels_p

    select = Select(title="Year:", align='start', value='_2009a', width=80, height=30, options=['_2009','_2010', '_2011', '_2012','_2013','_2014','_2015','_2016','_2017','_2018'])
    callback = CustomJS(args={'source':source},code="""
            console.log(' changed selected option', cb_obj.value);

            var data = source.data;

            // allocate column
            data['_2009a'] = data[cb_obj.value];


            // register the change 
            source.change.emit();
    """)

    select.callback = callback


    layout = row(select,p)
    return layout

def popOverall():
    df1 = pd.read_csv('BokehApp/Data/ageGroupYear.csv', delimiter=',')
    df1['color'] = viridis(len(df1.index))
    df1['2009.'] = df1['2009'].values

    source1 = ColumnDataSource(data=dict(df1))


    p1 = figure(x_range=list(df1['Age Groups'].values), plot_height=300, plot_width=500,title='Irish Population Breakdown by Age Group',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    p1.vbar(x='Age Groups', top='2009.', width=0.5, source=source1, color='color')

    #plot style
    p1.xaxis.major_label_orientation = 45
    
    #p1.grid.grid_line_color=None
    p1.outline_line_color=None
    p1.axis.major_label_text_font_style = 'bold'
    #p1.toolbar.autohide = True
    p1.grid.grid_line_alpha = 0.6
    p1.grid.grid_line_dash = 'dotted'
    p1.grid.grid_line_dash_offset = 5
    p1.grid.grid_line_width = 2

    hoverp1 = HoverTool()
    hoverp1.tooltips=[('Group Population', '@2009')]
    p1.add_tools(hoverp1)


    tick_labels_p1 = {'100':'100K','200':'200K','300':'300K','400':'400K'}
    p1.yaxis.major_label_overrides = tick_labels_p1
    

    df = pd.read_csv('BokehApp/Data/OverAll.csv', delimiter=',', index_col='Year')
    df['color'] = viridis(len(df.index))


    xrange = (2009,2018)
    xrange
    yrange = (df['Population'].min(), df['Population'].max())

    source = ColumnDataSource(df)


    p = figure(plot_height=300, plot_width=400,title='Irish Population Growth by Year',
               y_range=Range1d(*yrange),tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='above')

    p.vbar(x='Year', top='Population', source=source, width=0.5, color='color')
    
    #plot style
    #p.xaxis.major_label_orientation = 45
    #p.grid.grid_line_color=None
    #p.x_range.start = 2009
    p.x_range.end = 2018.5
    p.grid.grid_line_alpha = 0.6
    p.y_range.start = 4500
    p.y_range.end = df['Population'].max()*1.003
    p.outline_line_color=None
    p.axis.major_label_text_font_style = 'bold'
    p.toolbar.autohide = True
    p.grid.grid_line_dash = 'dotted'
    p.grid.grid_line_dash_offset = 5
    p.grid.grid_line_width = 2
    p.toolbar.autohide=True
    #p.yaxis.axis_line_color = None

    hoverp = HoverTool()
    hoverp.tooltips=[('Year','@Year'),('Population', '@Population{int}')]
    p.add_tools(hoverp)


    tick_labels_p = {'4500':'450M','4550':'455M','4600':'460M','4650':'465M','4700':'470M','4750':'475M', '4800':'480M','4850':'485M'}
    p.yaxis.major_label_overrides = tick_labels_p


    select = Select(title="Year:", align='center', value='2009.', width=60, height=25, options=['2009','2010', '2011', '2012','2013','2014','2015','2016','2017','2018'])
    p1.title.text = 'Irish Population by Age Group ' +  str(select.value)

    callback = CustomJS(args={'source':source1, 'title':p1.title},code="""
            console.log(' changed selected option', cb_obj.value);

            var data = source.data;
            title.text = 'Irish Population by Age Group ' + cb_obj.value

            // allocate column
            data['2009.'] = data[cb_obj.value];



            // register the change 
            source.change.emit()""")

    select.js_on_change('value', callback)


    layout = row(p,select, p1, margin=5) 
    return layout

def naturalincrease():
    df = pd.read_csv('BokehApp/Data/PopChange.csv', delimiter=',', index_col='Components')
    df = df.iloc[:-2].T

    source = ColumnDataSource(data=dict(x=df.index, y=df['Annual births'], y2=df['Annual deaths'], y3=df['Natural increase']))
    xp = '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'

    p = figure(x_range=xp, title='Natural Increase', plot_width=550, plot_height=350, tools='pan, wheel_zoom, box_zoom, reset')
    p.line(x='x', y='y', line_width=2.5, line_color='#440154', source=source, legend_label='Annual births')
    p.line(x='x', y='y2', line_width=2.5, line_color='#FDE724', source=source, legend_label='Annual deaths')
    p.line(x='x', y='y3', line_width=2.5, line_color='#208F8C', source=source, legend_label='Natural increase')
    p.circle(x='x', y='y', size=5, color='#B2DD2C', source=source, legend_label='Annual births')
    p.circle(x='x', y='y2', size=5, color='#365A8C', source=source, legend_label='Annual deaths')#365A8C
    p.circle(x='x', y='y3', size=5, color='#3E4989', source=source, legend_label='Natural increase')

    tick_labels_p = {'30':'30K','40':'40K','50':'50K','60':'60K','70':'70K'}
    p.yaxis.major_label_overrides = tick_labels_p

    hoverp = HoverTool()
    hoverp.tooltips=[('Year', '@x'), ('Annual births', '@y'), ('Annual deaths','@y2'), ('Natural increase','@y3')]
    p.add_tools(hoverp)

    p.legend.border_line_alpha=0
    p.legend.location = (360,220)
    p.legend.background_fill_alpha = None
    p.legend.label_text_font_size = "11px"
    p.legend.click_policy="hide"
    p.title.text_font_size = '15px'
        #pti.axis.major_label_text_font_style = 'bold'
    p.xaxis.major_label_text_font_style = 'bold'

    p.outline_line_color=None
    p.axis.major_label_text_font_style = 'bold'
    #p1.toolbar.autohide = True
    p.grid.grid_line_dash = 'dotted'
    p.grid.grid_line_dash_offset = 5
    p.grid.grid_line_width = 2
    p.grid.grid_line_alpha = 0.6
    p.toolbar.autohide = True


    return p


def netMigration():
    df = pd.read_csv('BokehApp/Data/PopChange.csv', delimiter=',', index_col='Components')
    df1 = df.iloc[3:].T
    
    source1 = ColumnDataSource(data=dict(x=df1.index, y=df1['Immigrants'], y2=df1['Emigrants']))
    xp1 = '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'

    p1 = figure(x_range=xp1, title='Net Migration', plot_width=550, plot_height=350, tools='pan, wheel_zoom, box_zoom, reset')
    p1.line(x='x', y='y', line_width=2.5, line_color='#440154', source=source1, legend_label='Immigrants')
    p1.line(x='x', y='y2', line_width=2.5, line_color='#FDE724', source=source1, legend_label='Emigrants')

    p1.circle(x='x', y='y', size=5, color='#B2DD2C', source=source1, legend_label='Immigrants')
    p1.circle(x='x', y='y2', size=5, color='#365A8C', source=source1, legend_label='Emigrants')

    tick_labels_p1 = {'40':'40K','50':'50K','60':'60K','70':'70K','80':'80K','90':'90K','100':'100K','110':'110K'}
    p1.yaxis.major_label_overrides = tick_labels_p1

    hoverp1 = HoverTool()
    hoverp1.tooltips=[('Year', '@x'), ('Immigrants', '@y'), ('Emigrants','@y2')]
    p1.add_tools(hoverp1)

    p1.legend.border_line_alpha=0
    p1.legend.background_fill_alpha = None
    p1.legend.label_text_font_size = "11px"
    p1.legend.click_policy="hide"
    p1.title.text_font_size = '15px'
        #pti.axis.major_label_text_font_style = 'bold'
    p1.xaxis.major_label_text_font_style = 'bold'

    p1.outline_line_color=None
    p1.axis.major_label_text_font_style = 'bold'
    #p1.toolbar.autohide = True
    p1.grid.grid_line_dash = 'dotted'
    p1.grid.grid_line_dash_offset = 5
    p1.grid.grid_line_width = 2
    p1.grid.grid_line_alpha = 0.6
    p1.toolbar.autohide = True

    return p1

def mapDev():
    
    
    p = figure(x_axis_location = None, y_axis_location = None, plot_width=430, plot_height=650) #, match_aspect=True
    p.image_url(url=['/static/images/devmapS.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p.title.align='center'    
    p.grid.grid_line_color=None
    p.outline_line_color=None
    p.toolbar.autohide = True
    #p.toolbar.Save = None
    #p.tools = ['pan, wheel_zoom, box_zoom, reset']
    p.title.text_font_style = "bold"

    return p

def heatmap():
    dfl = pd.read_csv('BokehApp/Data/rentAvgByBeds.csv', delimiter=',', index_col=0)
    dfl1 = pd.DataFrame(dfl.stack(), columns=['rent(avg)']).reset_index()
    dfl1.columns =['Bed','Year', 'Rent']

    x = list(dfl.columns)
    y = list(reversed(dfl.index.values))
    #v = dfb.values
    colors1 = viridis(9)[::-1]
    mapper = LinearColorMapper(palette=colors1, low=400, high=1800)

    hm1 = figure(title="Heatmap average rent by bedroom", x_range=x, y_range=y, x_axis_location="above", plot_width=900, plot_height=500,
               tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='below', y_axis_label='Number of bedrooms')


    hm1.title.text_font_size = '20px'
    hm1.rect(x='Year', y='Bed', width=1, height=1, source=dfl1,
           fill_color={'field': 'Rent', 'transform': mapper}, line_color='white', line_width=0.05)
    
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="10px", major_label_text_font_style='bold',
                         ticker=BasicTicker(desired_num_ticks=len(colors1)),
                         label_standoff=6, border_line_color=None, location=(0, 0))

    hoverhm1 = HoverTool()
    hoverhm1.tooltips=[('Year', '@Year'), ('Beds', '@Bed'), ('€', '@Rent{int}')]
    hm1.add_tools(hoverhm1)
    hm1.grid.grid_line_color = None
    hm1.axis.axis_line_color = None
    hm1.axis.major_tick_line_color = None
    #hm1.axis.major_label_text_font_size = '10px'
    hm1.xaxis.major_label_text_font_size = '12px'
    hm1.axis.major_label_text_font_style = 'bold'
    hm1.axis.major_label_standoff = 0
    hm1.toolbar.autohide = True
    hm1.yaxis.major_label_text_font_size = '10px'
    hm1.yaxis.axis_label_text_font_style = 'italic'
    hm1.add_layout(color_bar, 'right')
    
    dfc = pd.read_csv('BokehApp/Data/Counties_rentAvg.csv', delimiter=',', index_col=0)
    dfc1 = pd.DataFrame(dfc.stack(), columns=['Rent']).reset_index()
    dfc1.columns =['Counties','Year', 'Rent']

    xc = list(dfc.columns)
    yc = list(reversed(dfc.index.values))
   
    colors1c = viridis(10)[::-1]
    mapperc = LinearColorMapper(palette=colors1c, low=400, high=1650)

    hmc = figure(title="Heatmap average rent by county", x_range=xc, y_range=yc, x_axis_location="above", plot_width=900, plot_height=650,
               tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='below')

    hmc.title.text_font_size = '20px'
    hmc.rect(x='Year', y='Counties', width=1, height=1, source=dfc1,
           fill_color={'field': 'Rent', 'transform': mapperc}, line_color='white', line_width=0.05)
    
    color_barc = ColorBar(color_mapper=mapperc, major_label_text_font_size="10px", major_label_text_font_style='bold',
                         ticker=BasicTicker(desired_num_ticks=len(colors1c)),
                         label_standoff=6, border_line_color=None, location=(0, 0))

    hoverhmc = HoverTool()
    hoverhmc.tooltips=[('Year', '@Year'),('County', '@Counties'), ('€', '@Rent{int}')]
    hmc.add_tools(hoverhmc)
    hmc.grid.grid_line_color = None
    hmc.axis.axis_line_color = None
    hmc.axis.major_tick_line_color = None
    hmc.axis.major_label_text_font_size = '10px'
    hmc.xaxis.major_label_text_font_size = '12px'
    hmc.axis.major_label_text_font_style = 'bold'
    hmc.axis.major_label_standoff = 0
    hmc.toolbar.autohide = True
    #hmc.yaxis.axis_label_text_font_size = '15px'
    hmc.yaxis.axis_label_text_font_style = 'bold'
    hmc.add_layout(color_barc, 'right')
    
    dfd = pd.read_csv('BokehApp/Data/avgRentDublinArea.csv', delimiter=',', index_col=0)
    dfd1 = pd.DataFrame(dfd.stack(), columns=['Rent']).reset_index()
    dfd1.columns =['District','Year', 'Rent']

    xd = list(dfd.columns)
    yd = list(reversed(dfd.index.values))

    colors1d = viridis(11)[::-1]
    mapperd = LinearColorMapper(palette=colors1d, low=800, high=2150)

    hmd = figure(title="Heatmap average rent in Dublin", x_range=xd, y_range=yd, x_axis_location="above", plot_width=900, plot_height=650,
               tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='below')

    hmd.title.text_font_size = '20px'
    hmd.rect(x='Year', y='District', width=1, height=1, source=dfd1,
           fill_color={'field': 'Rent', 'transform': mapperd}, line_color='white', line_width=0.05)

    color_bard = ColorBar(color_mapper=mapperc, major_label_text_font_size="10px", major_label_text_font_style='bold',
                         ticker=BasicTicker(desired_num_ticks=len(colors1d)),
                         label_standoff=6, border_line_color=None, location=(0, 0))

    hoverhmd = HoverTool()
    hoverhmd.tooltips=[('Year', '@Year'),('District', '@District'), ('€', '@Rent{int}')]
    hmd.add_tools(hoverhmd)
    hmd.grid.grid_line_color = None
    hmd.axis.axis_line_color = None
    hmd.axis.major_tick_line_color = None
    hmd.axis.major_label_text_font_size = '10px'
    hmd.xaxis.major_label_text_font_size = '12px'
    hmd.axis.major_label_text_font_style = 'bold'
    hmd.axis.major_label_standoff = 0
    hmd.toolbar.autohide = True
    hmd.yaxis.axis_label_text_font_style = 'bold'
    hmd.add_layout(color_barc, 'right')
    
    dfct = pd.read_csv('BokehApp/Data/rentAvgCities.csv', delimiter=',', index_col=0)
    dfct1 = pd.DataFrame(dfct.stack(), columns=['Rent']).reset_index()
    dfct1.columns =['City_Town','Year', 'Rent']

    xt = list(dfct.columns)
    yt = list(reversed(dfct.index.values))
    colors1t = viridis(11)[::-1]
    mappert = LinearColorMapper(palette=colors1t, low=400, high=1600)

    hmt = figure(title="Heatmap average rent by city/town", x_range=xt, y_range=yt, x_axis_location="above", plot_width=1000, plot_height=650,
               tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='below')

    hmt.title.text_font_size = '20px'
    hmt.rect(x='Year', y='City_Town', width=1, height=1, source=dfct1,
           fill_color={'field': 'Rent', 'transform': mappert}, line_color='white', line_width=0.05)

    color_bart = ColorBar(color_mapper=mappert, major_label_text_font_size="10px", major_label_text_font_style='bold',
                         ticker=BasicTicker(desired_num_ticks=len(colors1t)),
                         label_standoff=6, border_line_color=None, location=(0, 0))

    hoverhmt = HoverTool()
    hoverhmt.tooltips=[('Year', '@Year'),('City/Town', '@City_Town'), ('€', '@Rent{int}')]
    hmt.add_tools(hoverhmt)
    hmt.grid.grid_line_color = None
    hmt.axis.axis_line_color = None
    hmt.axis.major_tick_line_color = None
    hmt.xaxis.major_label_text_font_size = '12px'
    hmt.axis.major_label_text_font_style = 'bold'
    hmt.axis.major_label_standoff = 0
    hmt.toolbar.autohide = True
    hmt.yaxis.major_label_text_font_size = '9px'
    hmt.yaxis.axis_label_text_font_style = 'bold'
    hmt.add_layout(color_bart, 'right')
    
    tc = Panel(child=hmc, title='County')
    tt = Panel(child=hmt, title='City/Town')
    td = Panel(child=hmd, title='Dublin')
    tb = Panel(child=hm1, title='Bedroom')
    tabs = Tabs(tabs=[tc,tt,td,tb])
    return tabs