
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
from bokeh.models import ColumnDataSource, PrintfTickFormatter, NumeralTickFormatter, FactorRange, Paragraph, LinearColorMapper, Tabs, Panel, HoverTool, Div, Select, CustomJS, Range1d, ColorBar, BasicTicker
from bokeh.transform import factor_cmap
from bokeh.models.widgets import Panel, Tabs
from bokeh.palettes import viridis
from bokeh.resources import CDN
from bokeh.embed import file_html


def maps():
    
    
    p16 = figure(x_axis_location = None, y_axis_location = None, plot_width=550, title='Irish Population')
    p16.image_url(url=['/static/images/pp16sub.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p16.title.align='center'    
    p16.grid.grid_line_color=None
    p16.outline_line_color=None
    p16.toolbar.autohide = True
    p16.title.text_font_style = "bold"
        
    p11 = figure(x_axis_location = None, y_axis_location = None, plot_width=550, title='Irish Population')
    p11.image_url(url=['/static/images/pp11sub.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p11.title.align='center'    
    p11.grid.grid_line_color=None
    p11.outline_line_color=None
    p11.toolbar.autohide = True
    p11.title.text_font_style = "bold"

    p06 = figure(x_axis_location = None, y_axis_location = None, plot_width=550, title='Irish Population')
    p06.image_url(url=['/static/images/pp06sub.png'], x=0, y=0, w=3, h=3, anchor="bottom_left")
    p06.title.align='center'    
    p06.grid.grid_line_color=None
    p06.outline_line_color=None
    p06.toolbar.autohide = True
    p06.title.text_font_style = "bold"

    p02 = figure(x_axis_location = None, y_axis_location = None, plot_width=550, title='Irish Population')
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
    df1['2009_'] = df1['2009'].values

    source1 = ColumnDataSource(data=dict(df1))


    p1 = figure(x_range=list(df1['AgeGroups'].values), plot_height=270, plot_width=450,title='Irish Population Breakdown by Age Group',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='right')
    p1.vbar(x='AgeGroups', top='2009_', width=0.5, source=source1, color='color')

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
    hoverp1.tooltips=[('Group', '@AgeGroups'),('Population', '@2009_')]
    p1.add_tools(hoverp1)


    tick_labels_p1 = {'100':'100K','200':'200K','300':'300K','400':'400K'}
    p1.yaxis.major_label_overrides = tick_labels_p1
    

    df = pd.read_csv('BokehApp/Data/OverAll.csv', delimiter=',', index_col='Year')
    df['color'] = viridis(len(df.index))


    xrange = (2009,2018)
    xrange
    yrange = (df['Population'].min(), df['Population'].max())

    source = ColumnDataSource(df)


    p = figure(plot_height=270, plot_width=370,title='Irish Population Growth by Year',
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


    select = Select(title="Year:", align='center', value='2009_', width=60, height=25, options=['2009','2010', '2011', '2012','2013','2014','2015','2016','2017','2018'])
    p1.title.text = 'Irish Population by Age Group ' +  str(select.value)

    callback = CustomJS(args={'source':source1, 'title':p1.title},code="""
            console.log(' changed selected option', cb_obj.value);

            var data = source.data;
            title.text = 'Irish Population by Age Group ' + cb_obj.value

            // allocate column
            data['2009_'] = data[cb_obj.value];



            // register the change 
            source.change.emit()""")

    select.js_on_change('value', callback)


    layout = row(p,select, p1, margin=2) 
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

    hmc = figure(title="Heatmap average rent by county", x_range=xc, y_range=yc, x_axis_location="above", plot_width=900, plot_height=600,
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

    hmd = figure(title="Heatmap average rent in Dublin", x_range=xd, y_range=yd, x_axis_location="above", plot_width=900, plot_height=600,
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

    hmt = figure(title="Heatmap average rent by city/town", x_range=xt, y_range=yt, x_axis_location="above", plot_width=900, plot_height=600,
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
    tabs = Tabs(tabs=[tc, tt,td,tb])
    return tabs

def dublinArea():
    dft = pd.read_csv('BokehApp/Data/DublinDistrictsRentAvg_t1.csv', delimiter=',')
    source = ColumnDataSource(dft)

    xt = list(dft.columns[2:].values)
    yt = '2008' ,'2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'

    p = figure(plot_height=350, plot_width=550, x_axis_label='rent in €', tools = 'pan, wheel_zoom, box_zoom, reset')
    p.line(x='Dublin_1', y='Year', line_width=2.5, line_color='#FDE724', source=source)
    p.circle(x='Dublin_1', y='Year', size=5, color='#365A8C', source=source)
    #p.hbar(y='Year', right='Dublin1.', height=0.15, source=source, color='#440154')
    hoverp = HoverTool()
    hoverp.tooltips=[('Year','@Year'),('€', '@Dublin_1{int}') ]
    p.add_tools(hoverp)


    p.xaxis.major_label_text_font_style = 'bold'

    p.outline_line_color=None
    p.axis.major_label_text_font_style = 'bold'
    p.grid.grid_line_dash = 'dotted'
    p.grid.grid_line_dash_offset = 5
    p.grid.grid_line_width = 2
    p.grid.grid_line_alpha = 0.6
    p.toolbar.autohide = True

    select = Select(title="Dublin area/district:", align='start', value='Dublin1.', width=120, height=25, options=xt)
    p.title.text = 'Rent average ' +  str(select.value)
    p.title.text_font_size = '15px'

    callback = CustomJS(args={'source':source, 'title':p.title},code="""
                console.log(' changed selected option', cb_obj.value);

                var data = source.data;
                title.text = 'Rent average ' + cb_obj.value

                // allocate column
                data['Dublin_1'] = data[cb_obj.value];



                // register the change 
                source.change.emit()""")

    select.js_on_change('value', callback)
    layout = row(select, p, margin=10)
    return layout


def transactionstype():
    dfh = pd.read_csv('BokehApp/Data/transac_avg.csv', delimiter='\t', index_col=0)

    dfh.columns = ['Ireland new properties', 'Dublin new properties', 'Ireland existing properties', 'Dublin existing properties']
    sourceh = ColumnDataSource(data=dict(x=dfh.index, y=dfh['Ireland new properties'], y1=dfh['Dublin new properties'],
                                        y2=dfh['Ireland existing properties'], y3=dfh['Dublin existing properties']))

    xph = '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'
    ph = figure(x_axis_type='log', plot_height=350, plot_width=600, title='Transaction average price in €', tools = 'pan, wheel_zoom, box_zoom, reset') # x_range=xph
    ph.line(x='x', y='y', line_width=2.5, line_color='#440154', source=sourceh, legend_label='Ireland new properties')
    ph.circle(x='x', y='y', size=5, color='#70CE56', source=sourceh, legend_label='Ireland new properties')
    ph.line(x='x', y='y1', line_width=2.5, line_color='#FDE724', source=sourceh, legend_label='Dublin new properties')
    ph.circle(x='x', y='y1', size=5, color='#440154', source=sourceh, legend_label='Dublin new properties')
    ph.line(x='x', y='y2', line_width=2.5, line_color='#9DD93A', source=sourceh, legend_label='Ireland existing properties')
    ph.circle(x='x', y='y2', size=5, color='#365A8C', source=sourceh, legend_label='Ireland existing properties')
    ph.line(x='x', y='y3', line_width=2.5, line_color='#482172', source=sourceh, legend_label='Dublin existing properties')
    ph.circle(x='x', y='y3', size=5, color='#FDE724', source=sourceh, legend_label='Dublin existing properties')

    tick_labels_ph = {'200000':'200K','250000':'250K','300000':'300K','350000':'350K','400000':'400K','450000':'450K'}
    ph.yaxis.major_label_overrides = tick_labels_ph

    hoverph = HoverTool()
    hoverph.tooltips=[('Year', '@x'), ('Ireland new', '€ @y'), ('Dublin new','€ @y1'), ('Ireland existing','€ @y2'), ('Dublin existing','€ @y3')]
    ph.add_tools(hoverph)

    ph.title.text_font_size = '15px'
    ph.legend.location = (0,190)
    ph.legend.border_line_alpha=0
    ph.legend.background_fill_alpha = None
    ph.legend.label_text_font_size = "11px"
    ph.legend.click_policy="hide"
    ph.xaxis.major_label_text_font_style = 'bold'
    ph.yaxis.formatter.use_scientific = False
    ph.outline_line_color=None
    ph.axis.major_label_text_font_style = 'bold'
    ph.grid.grid_line_dash = 'dotted'
    ph.grid.grid_line_dash_offset = 5
    ph.grid.grid_line_width = 2
    ph.grid.grid_line_alpha = 0.6
    ph.toolbar.autohide = True

    return ph

def gridMortgage():
    dfap = pd.read_csv('BokehApp/Data/Mortg_05_16.csv', delimiter='\t', index_col=0)
    sourceap = ColumnDataSource(data=dict(x=dfap.index, y=dfap['New Properties'], y1=dfap['Existing Properties']))
    #xap = '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016'

    pap = figure(plot_height=250, plot_width=400, title='Mortgages approvals', tools = 'pan, wheel_zoom, box_zoom, reset')
    pap.line(x='x', y='y', line_width=2.5, line_color='#440154', source=sourceap, legend_label='New Properties')
    pap.circle(x='x', y='y', size=5, color='#CDE01D', source=sourceap, legend_label='New Properties')
    pap.line(x='x', y='y1', line_width=2.5, line_color='#FDE724', source=sourceap, legend_label='Existing Properties')
    pap.circle(x='x', y='y1', size=5, color='#440154', source=sourceap, legend_label='Existing Properties')


    tick_labels_pap = {'10000':'10K','20000':'20K','30000':'30K','40000':'40K','50000':'50K','60000':'60K'}
    pap.yaxis.major_label_overrides = tick_labels_pap


    hoverpap = HoverTool()
    hoverpap.tooltips=[('Year', '@x'), ('New Properties', '@y'), ('Existing Properties','@y1')]
    pap.add_tools(hoverpap)

    pap.title.text_font_size = '15px'
    pap.legend.location = 'top_right'
    pap.legend.border_line_alpha=0
    pap.legend.background_fill_alpha = None
    pap.legend.label_text_font_size = "11px"
    pap.legend.click_policy="hide"
    pap.xaxis.major_label_text_font_style = 'bold'
    pap.yaxis.formatter.use_scientific = False
    pap.outline_line_color=None
    pap.axis.major_label_text_font_style = 'bold'
    pap.yaxis.major_label_text_font_size = '10px'
    pap.grid.grid_line_dash = 'dotted'
    pap.grid.grid_line_dash_offset = 5
    pap.grid.grid_line_width = 2
    pap.grid.grid_line_alpha = 0.6
    pap.toolbar.autohide = True
    
    dfa = pd.read_csv('BokehApp/Data/MortgAll_Variables.csv', delimiter='\t', index_col=0)
    dfa1 = pd.DataFrame(dfa['VolumeMortgage'])
    dfa1['color'] = viridis(len(dfa.index))[::-1]
    sourcepa = ColumnDataSource(data=dict(x=dfa1.index, y=dfa1['VolumeMortgage'], c=dfa1['color']))

    pa = figure(plot_height=250, plot_width=400,  title='Mortgages approvals overall', tools = 'pan, wheel_zoom, box_zoom, reset')
    pa.vbar(x='x', top='y', source=sourcepa, color='c', width=0.5)
    pa.y_range.end = dfa1['VolumeMortgage'].max()*1.03

    tick_labels_pa = {'10000':'10K','20000':'20K','30000':'30K','40000':'40K','50000':'50K'}
    pa.yaxis.major_label_overrides = tick_labels_pa

    hoverpa = HoverTool()
    hoverpa.tooltips=[('Year', '@x'), ('Approvals', '@y')]
    pa.add_tools(hoverpa)

    pa.title.text_font_size = '15px'
    pa.xaxis.major_label_text_font_style = 'bold'
    pa.yaxis.major_label_text_font_size = '10px'
    pa.yaxis.formatter.use_scientific = False
    pa.outline_line_color=None
    pa.axis.major_label_text_font_style = 'bold'
    pa.grid.grid_line_dash = 'dotted'
    pa.grid.grid_line_dash_offset = 5
    pa.grid.grid_line_width = 2
    pa.grid.grid_line_alpha = 0.6
    pa.toolbar.autohide = True
    
    dff = pd.read_csv('BokehApp/Data/Mortg_10_16.csv', delimiter=',', index_col=0)
    dff = dff[['New Properties', 'FTB']]

    sourcef = ColumnDataSource(data=dict(x=dff.index, y=dff['New Properties'], y1=dff['FTB']))

    pf = figure(plot_height=250, plot_width=400,  title='First Time Buyers', tools = 'pan, wheel_zoom, box_zoom, reset')
    pf.line(x='x', y='y', line_width=2.5, line_color='#440154', source=sourcef, legend_label='New Properties')
    pf.circle(x='x', y='y', size=5, color='#CDE01D', source=sourcef, legend_label='New Properties')
    pf.line(x='x', y='y1', line_width=2.5, line_color='#FDE724', source=sourcef, legend_label='First Time Buyers')
    pf.circle(x='x', y='y1', size=5, color='#440154', source=sourcef, legend_label='First Time Buyers')

    tick_labels_pf = {'1000':'1K','2000':'2K','3000':'3K','4000':'4K','5000':'5K','6000':'6K', '7000':'7K'}
    pf.yaxis.major_label_overrides = tick_labels_pf


    hoverpf = HoverTool()
    hoverpf.tooltips=[('Year', '@x'), ('New Properties', '@y'), ('First Time Buyers','@y1')]
    pf.add_tools(hoverpf)

    pf.title.text_font_size = '15px'
    pf.legend.location = 'top_center'
    pf.yaxis.major_label_text_font_size = '10px'
    pf.legend.border_line_alpha=0
    pf.legend.background_fill_alpha = None
    pf.legend.label_text_font_size = "11px"
    pf.legend.click_policy="hide"
    pf.xaxis.major_label_text_font_style = 'bold'
    pf.yaxis.formatter.use_scientific = False
    pf.outline_line_color=None
    pf.axis.major_label_text_font_style = 'bold'
    pf.grid.grid_line_dash = 'dotted'
    pf.grid.grid_line_dash_offset = 5
    pf.grid.grid_line_width = 2
    pf.grid.grid_line_alpha = 0.6
    pf.toolbar.autohide = True
    
    dfd = pd.read_csv('BokehApp/Data/MortgageDeposit.csv', delimiter=',', index_col=0)
    sourced = ColumnDataSource(data=dict(x=dfd.index, y=dfd['Dublin'], y1=dfd['Dublin Commuter'], y2=dfd['National']))

    pd1 = figure(plot_height=250, plot_width=400, title='Average deposit in €', tools = 'pan, wheel_zoom, box_zoom, reset')
    pd1.line(x='x', y='y', line_width=2.5, line_color='#9DD93A', source=sourced, legend_label='Dublin')
    pd1.circle(x='x', y='y', size=5, color='#365A8C', source=sourced, legend_label='Dublin')
    pd1.line(x='x', y='y1', line_width=2.5, line_color='#FDE724', source=sourced, legend_label='Dublin Commuter')
    pd1.circle(x='x', y='y1', size=5, color='#440154', source=sourced, legend_label='Dublin Commuter')
    pd1.line(x='x', y='y2', line_width=2.5, line_color='#440154', source=sourced, legend_label='National') #
    pd1.circle(x='x', y='y2', size=5, color='#CDE01D', source=sourced, legend_label='National') #

    tick_labels_pd = {'20000':'20K','25000':'24K','30000':'30K','35000':'35K','40000':'40K','45000':'45K','50000':'50K','55000':'55K'}
    pd1.yaxis.major_label_overrides = tick_labels_pd


    hoverpd1 = HoverTool()
    hoverpd1.tooltips=[('Year', '@x'), ('Dublin', '€ @y'), ('Dublin Commuter','€ @y1'), ('National','€ @y2')]
    pd1.add_tools(hoverpd1)

    pd1.title.text_font_size = '15px'
    pd1.legend.location = 'top_left'
    pd1.yaxis.major_label_text_font_size = '10px'
    pd1.legend.border_line_alpha=0
    pd1.legend.background_fill_alpha = None
    pd1.legend.label_text_font_size = "11px"
    pd1.legend.click_policy="hide"
    pd1.xaxis.major_label_text_font_style = 'bold'
    pd1.yaxis.formatter.use_scientific = False
    pd1.outline_line_color=None
    pd1.axis.major_label_text_font_style = 'bold'
    pd1.grid.grid_line_dash = 'dotted'
    pd1.grid.grid_line_dash_offset = 5
    pd1.grid.grid_line_width = 2
    pd1.grid.grid_line_alpha = 0.6
    pd1.toolbar.autohide = True
    #pd1.xaxis.minor_tick_line_cap = '5px'
    pd1.xaxis.major_tick_line_color = None 
    
    grid = gridplot([[pap, pa], [pf, pd1]], merge_tools=True, toolbar_location='below')#scale_both sizing_mode='fixed', plot_height=300, plot_width=500,
    
    return grid

def corrMatrix():
    dfr = pd.read_csv('BokehApp/Data/RentMatrix.csv', delimiter=',', index_col=0)

    dfr1 = pd.DataFrame(dfr.corr().stack(), columns=['corr']).reset_index()
    dfr1.columns =['x', 'y', 'corr']
    dfr1['corr'] = pd.to_numeric(dfr1["corr"], downcast="float")

    xr = list(dfr1['x'].unique())
    yr = xr[::-1]

    colorsr = viridis(20)#[::-1]
    mapper1 = LinearColorMapper(palette=colorsr, low=-1, high=1)#

    cmr = figure(title="Correlation matrix", x_range=xr, y_range=yr, x_axis_location="below", plot_width=950, plot_height=600,
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='above')

    cmr.title.text_font_size = '20px'
    cmr.rect(x='x', y='y', width=1, height=1, source=dfr1, dilate=True,
            fill_color={'field': 'corr', 'transform': mapper1}, line_color='red',  line_dash='dotted', line_width=0.08)
    #cmr.rect(x='x', y='y', width={'field': 'corr', 'transform': cmr.width}, height={'field': 'corr', 'transform': cmr.height}, source=dfr1, dilate=True,

    hovercmr = HoverTool()
    hovercmr.tooltips=[('var1', '@x'),('var2', '@y'), ('Correlation', '@corr')]
    cmr.add_tools(hovercmr)

    cmr.xaxis.major_label_orientation =45
    color_bar1 = ColorBar(color_mapper=mapper1, major_label_text_font_size="10px", major_label_text_font_style='bold',
                             ticker=BasicTicker(desired_num_ticks=len(colorsr)),
                             label_standoff=6, border_line_color=None, location=(0, 0))

    cmr.grid.grid_line_color = None
    cmr.axis.axis_line_color = None
    cmr.axis.major_tick_line_color = None
    cmr.axis.major_label_text_font_size = '10px'
    cmr.xaxis.major_label_text_font_size = '12px'
    cmr.axis.major_label_text_font_style = 'bold'
    cmr.axis.major_label_standoff = 0
    cmr.toolbar.autohide = True
    #hmc.yaxis.axis_label_text_font_size = '15px'
    cmr.yaxis.axis_label_text_font_style = 'bold'

    cmr.add_layout(color_bar1, 'right')
    
    return cmr

def social():
    dfs = pd.read_csv('BokehApp/Data/_SH_total.csv', delimiter=',', index_col=0)
    dfs1 = dfs.iloc[::,:-1]

    sources = ColumnDataSource(dfs1)

    a = figure(plot_width=450, plot_height=280, title='Social Housing development', toolbar_location='above', tools = 'pan, wheel_zoom, box_zoom, reset')
    colors = viridis(4)

    a.varea_stack(['Build','Acquisition','Leasing','RAS/HAP'], x='Year', source=sources, color=colors[::-1], legend_label=('Build','Acquisition','Leasing','RAS/HAP'), muted_alpha=0.2)

    a.legend.location='top_left'
    a.legend.click_policy="mute"
    #a.yaxis[0].formatter = NumeralTickFormatter(format="0 M")
    tick_labels = {'5000':'5K','10000':'10K','15000':'15K','20000':'20K','25000':'25K'}
    a.yaxis.major_label_overrides = tick_labels
    a.xaxis.ticker = dfs.index.values
    a.title.text_font_size = '15px'
    a.legend.background_fill_alpha=None
    a.legend.border_line_alpha=0
    a.legend.label_text_font_size = "11px"
    a.xaxis.major_label_text_font_size = '10px'
    a.axis.major_label_text_font_style = 'bold'
    #a.grid.grid_line_color=None
    a.toolbar.autohide = True
    a.outline_line_color=None

    a.grid.grid_line_dash = 'dotted'
    a.grid.grid_line_dash_offset = 5
    a.grid.grid_line_width = 2
    a.grid.grid_line_alpha = 0.6
    a.toolbar.autohide = True


    dfs2 = pd.DataFrame(dfs.iloc[::,-1])
    dfs2['color'] = viridis(len(dfs2.index))

    sources2 = ColumnDataSource(dfs2)
    xs2 = '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'


    ps2 = figure(plot_height=280, plot_width=450, title='Total of families reached',
                tools='pan, wheel_zoom, box_zoom, reset', toolbar_location='above')
    ps2.vbar(x='Year', top='TotalSupport', width=0.6, source=sources2, color='color')
    ps2.y_range.start = 3000#dfs2['Total Support'].min()tick_labels = {'5000':'5K','10000':'10K','15000':'15K','20000':'20K','25000':'25K'}
    #ps2.line(x='Year', y='TotalSupport', source=sources2, line_width=2.5)

    tick_labels2 = {'5000':'5K','10000':'10K','15000':'15K','20000':'20K','25000':'25K'}
    ps2.yaxis.major_label_overrides = tick_labels2
    ps2.xaxis.ticker = dfs2.index.values
    ps2.title.text_font_size = '15px'

    hoverp2 = HoverTool()
    hoverp2.tooltips=[('Year', '@Year'),('Total support','@TotalSupport')]
    ps2.add_tools(hoverp2)

    ps2.axis.major_label_text_font_style = 'bold'
    ps2.xaxis.major_label_text_font_size = '10px'
    #ps2.xaxis.major_label_orientation = 45
    #a.grid.grid_line_color=None
    #ps2.toolbar.autohide = True
    ps2.outline_line_color=None

    ps2.grid.grid_line_dash = 'dotted'
    ps2.grid.grid_line_dash_offset = 5
    ps2.grid.grid_line_width = 2
    ps2.grid.grid_line_alpha = 0.6


    layout = row(a,ps2, margin=5)
    return layout

def homeless():
    df = pd.read_csv('BokehApp/Data/Homeless_Numbers1.csv', delimiter=',', index_col=0)
    #df = df.iloc[::,:-2]
    cl = df.columns[[0,-1,1,2,]]
    df = df[cl]
    df['color'] = viridis(len(df.index.values))[::-1]

    source = ColumnDataSource(df)

    p = figure(plot_width=900, plot_height=450, title='Homelessness in Ireland Adults', tools='pan, wheel_zoom, box_zoom, reset',
              x_range=list(df.index.values))
    p.line(x='Date', y='Adults', line_width=2.5, line_color='#440154', source=source, legend_label='Nationwide')
    p.circle(x='Date', y='Adults', size=5, color='#DAE218', source=source, legend_label='Nationwide')
    p.line(x='Date', y='DublinAdults', line_width=2.5, line_color='#FDE724', source=source, legend_label='Dublin')
    p.circle(x='Date', y='DublinAdults', size=5, color='#365A8C', source=source, legend_label='Dublin')#365A8C


    tick_labels_p = {'2000':'2K','3000':'3K','4000':'4K','4000':'4K','8000':'8K','6000':'6K','5000':'5K'}
    p.yaxis.major_label_overrides = tick_labels_p

    hoverp = HoverTool()
    hoverp.tooltips=[('Date', '@Date'), ('Nationwide', '@Total'), ('Dublin','@DublinAdults')]
    p.add_tools(hoverp)

    p.legend.border_line_alpha=0
    p.legend.location = 'top_left'
    p.legend.background_fill_alpha = None
    p.legend.label_text_font_size = "11px"
    p.legend.click_policy="hide"
    p.title.text_font_size = '15px'
    p.xaxis.major_label_text_font_style = 'bold'

    p.outline_line_color=None
    p.axis.major_label_text_font_style = 'bold'
    p.xaxis.major_label_orientation = 45
    p.grid.grid_line_dash = 'dotted'
    p.grid.grid_line_dash_offset = 5
    p.grid.grid_line_width = 2
    p.grid.grid_line_alpha = 0.6
    p.toolbar.autohide = True



    p1 = figure(plot_width=900, plot_height=450, title='Homelessness in Ireland', tools='pan, wheel_zoom, box_zoom, reset',
              x_range=list(df.index.values))
    p1.line(x='Date', y='Total', line_width=2.5, line_color='#9DD93A', source=source, legend_label='Overall')
    p1.circle(x='Date', y='Total', size=5, color='#365A8C', source=source, legend_label='Overall')
    p1.line(x='Date', y='Adults', line_width=2.5, line_color='#440154', source=source, legend_label='Adults')
    p1.circle(x='Date', y='Adults', size=5, color='#DAE218', source=source, legend_label='Adults')
    p1.line(x='Date', y='Children', line_width=2.5, line_color='#FDE724', source=source, legend_label='Children')
    p1.circle(x='Date', y='Children', size=5, color='#365A8C', source=source, legend_label='Children')#365A8C



    tick_labels_p1 = {'1000':'1K','2000':'2K','3000':'3K','4000':'4K','4000':'4K','8000':'8K','6000':'6K','5000':'5K','10000':'10K'}
    p1.yaxis.major_label_overrides = tick_labels_p1

    hoverp1 = HoverTool()
    hoverp1.tooltips=[('Date', '@Date'), ('Adults', '@Adults'), ('Children','@Children'), ('Overall','@Total')]
    p1.add_tools(hoverp1)

    p1.legend.border_line_alpha=0
    p1.legend.location = 'top_left'
    p1.legend.background_fill_alpha = None
    p1.legend.label_text_font_size = "11px"
    p1.legend.click_policy="hide"
    p1.title.text_font_size = '15px'
    p1.xaxis.major_label_text_font_style = 'bold'

    p1.outline_line_color=None
    p1.axis.major_label_text_font_style = 'bold'
    p1.xaxis.major_label_orientation = 45
    p1.grid.grid_line_dash = 'dotted'
    p1.grid.grid_line_dash_offset = 5
    p1.grid.grid_line_width = 2
    p1.grid.grid_line_alpha = 0.6
    p1.toolbar.autohide = True

    t1 = Panel(child=p1, title='Overall')
    t2 = Panel(child=p, title='Adults')

    tabs = Tabs(tabs=[t1, t2])
    return tabs

def austria():
    dfv = pd.read_csv('BokehApp/Data/SocialHousingViennaDublin.csv', delimiter=',', index_col=0)
    dfv1 = dfv.iloc[::,3:5]
    dfv1.columns =['HouseStock','SocialHousing']

    xl = list(dfv1.index.values)
    lDict = {'House Stock':xl,'Social Housing':xl}
    source = ColumnDataSource(dfv1)
    p = figure(x_range=FactorRange(*xl), plot_height=350, plot_width=550, title='House Stock 2011 in %', x_axis_label=None, y_axis_label=None, tools = 'pan, wheel_zoom, box_zoom, reset')


    p.vbar(x=dodge('Geo', -0.25, range=p.x_range), top='HouseStock', width=0.2, source=source, color='#208F8C', legend_label='House Stock')
    p.vbar(x=dodge('Geo', 0.0, range=p.x_range), top='SocialHousing', width=0.2, source=source, color='#FDE724', legend_label='Social Housing')

    hover = HoverTool()
    hover.tooltips=[('Location', ' @Geo'),('House Stock','@HouseStock %'),('Social Housing','@SocialHousing %')]
    p.add_tools(hover)


    p.legend.location= 'top_right'#(370,180)
    p.legend.background_fill_alpha=None
    p.legend.border_line_alpha=0
    p.legend.label_text_font_size = "11px"
    #p.y_range.end = dfv.values.max()*1.1+1
    p.legend.click_policy="hide"
    p.title.text_font_size = '15px'
    p.axis.major_label_text_font_style = 'bold'
    p.grid.grid_line_alpha = 0.6
    p.grid.grid_line_dash = 'dotted'
    p.grid.grid_line_dash_offset = 5
    p.grid.grid_line_width = 2
        #p.grid.grid_line_color=None
    p.toolbar.autohide = True
    p.outline_line_color=None

    return p

def sol():
    dfsol = pd.read_csv('BokehApp/Data/dfmap1.csv', delimiter=',', index_col=0)
    dfsol['color'] = viridis(len(dfsol.index.values))[::-1]
    sourcesol = ColumnDataSource(dfsol)

    ps = figure(x_range=list(dfsol.index.values), plot_height=350, plot_width=650, title='Possibly number of social houses needed', x_axis_label=None, y_axis_label=None, tools = 'pan, wheel_zoom, box_zoom, reset')
    ps.vbar(x='County', top='Solution', width=.6, color='color', source=sourcesol)

    hovers = HoverTool()
    hovers.tooltips=[('County', ' @County'),('Possibly number of houses','@Solution')]
    ps.add_tools(hovers)

    tick_labels = {'10000':'10K','20000':'20K','30000':'30K','40000':'40K'}
    ps.yaxis.major_label_overrides = tick_labels

    ps.xaxis.major_label_orientation = 45
    ps.title.text_font_size = '15px'
    ps.axis.major_label_text_font_style = 'bold'
    ps.grid.grid_line_alpha = 0.6
    ps.grid.grid_line_dash = 'dotted'
    ps.grid.grid_line_dash_offset = 5
    ps.grid.grid_line_width = 2
        #p.grid.grid_line_color=None
    ps.toolbar.autohide = True
    ps.outline_line_color=None

    return ps