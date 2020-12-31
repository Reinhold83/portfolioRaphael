from flask import Flask, render_template, request
from bokeh.embed import components
from plots1 import houseStockPlot, vacantPlot, Transactions, NewRegistered, nonOccupiers, pie_chart
from tabs import maps, ageGroup, naturalincrease, netMigration, mapDev, popOverall, heatmap, dublinArea, sol, transactionstype, gridMortgage, corrMatrix, social, homeless, austria
from flask_bootstrap import Bootstrap
from form import ContactForm
from flask_mail import Message, Mail
from rightA import (swedishpop, swedishpop1, irishpop, wwpop, pandemics, pandemics1, R0, pandAgeGroups, pandAgeGroups1, corrplot, irishDeaths, swedishdeaths, irishswedishDeaths,
                    irlDD, SwDD, r01, r0Table)
from fbPlots import fb_figs, fb_vars, heatmaps, predic
from os import environ

#from django.contrib.gis import gdal

GEOS_LIBRARY_PATH = environ.get('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = environ.get('GDAL_LIBRARY_PATH')

mail = Mail()

app = Flask(__name__)


app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'ds.rran@gmail.com'
app.config["MAIL_PASSWORD"] = ''
 
mail.init_app(app)

#app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = ''
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


  

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if request.method == 'POST':
        if form.validate() == False:
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender=form.email.data, recipients=['ds.rran@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return 'Message sent successfully.<br>Thanks for getting in touch, I will get back to you as soon as possible.'
    
    elif request.method == 'GET':
        return render_template('contact.html', form=form)



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

@app.route('/rightApproach')
def rightApproach():
    script, div = components(swedishpop())
    script1, div1 = components(swedishpop1())
    script2, div2 = components(irishpop())
    script3, div3 = components(wwpop())
    script4, div4 = components(pandemics())
    script5, div5 = components(pandemics1())
    script6, div6 = components(R0())
    script7, div7 = components(pandAgeGroups())
    script8, div8 = components(pandAgeGroups1())
    script9, div9 = components(corrplot())
    script10, div10 = components(irishDeaths())
    script11, div11 = components(swedishdeaths())
    script12, div12 = components(irishswedishDeaths())
    script13, div13 = components(irlDD())
    script14, div14 = components(SwDD())
    script15, div15 = components(r01())
    script16, div16 = components(r0Table())



    return render_template('rightApproach.html', script=script, div=div, script1=script1, div1=div1, script2=script2, div2=div2, script3=script3, div3=div3,
                            script4=script4, div4=div4, script5=script5, div5=div5, script6=script6, div6=div6, script7=script7, div7=div7, script8=script8, div8=div8,
                            script9=script9, div9=div9, script10=script10, div10=div10, script11=script11, div11=div11, script12=script12, div12=div12,
                            script13=script13, div13=div13, script14=script14, div14=div14, script15=script15, div15=div15, script16=script16, div16=div16)



@app.route('/FB')
def FB():
    script, div = components(fb_figs())
    script1, div1 = components(fb_vars())
    script2, div2 = components(heatmaps())
    script3, div3 = components(predic())



    return render_template('FB.html', script=script, div=div, script1=script1, div1=div1, script2=script2, div2=div2, script3=script3, div3=div3)