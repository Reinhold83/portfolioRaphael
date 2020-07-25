from flask import Flask, render_template, request
from bokeh.embed import components
from plots1 import houseStockPlot, vacantPlot, Transactions, NewRegistered, nonOccupiers, pie_chart
from tabs import maps, ageGroup, popOverall, naturalincrease, netMigration, mapDev
from flask_bootstrap import Bootstrap

app = Flask(__name__)
#app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'oratoroeuaroupadoreideroma123'
#app.static_folder = 'static'
Bootstrap(app)
#@app.route('/')
#def index():
#    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')



@app.route('/bokeh')
def bokeh():
    script, div = components(houseStockPlot())
    script1, div1 = components(vacantPlot())
    script2, div2 = components(Transactions())
    script3, div3 = components(NewRegistered())
    script4, div4 = components(nonOccupiers())
    script5, div5 = components(pie_chart())
    script6, div6 = components(maps())
    script7, div7 = components(ageGroup())
    script8, div8 = components(popOverall())
    script9, div9 = components(naturalincrease())
    script10, div10 = components(netMigration())
    script11, div11 = components(mapDev())


    return render_template('bokeh.html', script=script, div=div, script1=script1,
    div1=div1, script2=script2, div2=div2, script3= script3, div3=div3, script4=script4, div4=div4,
    script5=script5, div5=div5, script6=script6, div6=div6, script7=script7, div7=div7, script8=script8, div8=div8,
    script9=script9, div9=div9, script10=script10, div10=div10, script11=script11, div11=div11)