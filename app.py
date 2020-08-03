from flask import Flask, render_template, request
from bokeh.embed import components
from plots1 import houseStockPlot, vacantPlot, Transactions, NewRegistered, nonOccupiers, pie_chart
from tabs import maps, ageGroup, naturalincrease, netMigration, mapDev, popOverall, heatmap, dublinArea, sol, transactionstype, gridMortgage, corrMatrix, social, homeless, austria
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
    script12, div12 = components(heatmap())
    script13, div13 = components(dublinArea())
    script14, div14 = components(transactionstype())
    script15, div15 = components(gridMortgage())
    script16, div16 = components(corrMatrix())
    script17, div17 = components(social())
    script18, div18 = components(homeless())
    script19, div19 = components(austria())
    script20, div20 = components(sol())





    return render_template('bokeh.html', script=script, div=div, script1=script1, div1=div1, script2=script2, div2=div2, script3= script3, div3=div3, script4=script4, div4=div4,
    script5=script5, div5=div5, script6=script6, div6=div6, script7=script7, div7=div7, script8=script8, div8=div8, script9=script9, div9=div9,
    script10=script10, div10=div10, script11=script11, div11=div11, script12=script12, div12=div12, script13=script13, div13=div13, script14=script14, div14=div14,
    script15=script15, div15=div15, script16=script16, div16=div16, script17=script17, div17=div17, script18=script18, div18=div18, script19=script19, div19=div19,
    script20=script20, div20=div20)
