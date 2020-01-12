from flask import Flask,request, render_template
import pandas as pd
from bokeh.embed import components
#from .extensions import db
#from .commands import create_tables
from bokeh.models import ColumnDataSource,Legend
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.palettes import Dark2_5 as palette
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from itertools import cycle
import requests
#from .routes import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

#    db.init_app(app)

#    app.register_blueprint(main)


#    app.cli.add_command(create_tables)

    def plot_lines_multi(df,prices,ticker,lw=2,pw=700,ph=400,t_str="save,pan,box_zoom,reset,wheel_zoom",t_loc='above'):
        '''...
        '''
        source = ColumnDataSource(df)
        col_names = prices
        p = figure(x_axis_type="datetime",plot_width=pw, plot_height=ph,toolbar_location=t_loc, tools=t_str)
        colors = cycle(palette)
        p_dict = dict()
        for price in prices:
        #for col, c, col_name in zip(df.columns,color,col_names):
            p_dict[price] = p.line(x='date', y=price, source=source, color=next(colors),line_width=lw)
        legend = Legend(items=[(x, [p_dict[x]]) for x in p_dict])
        p.add_layout(legend,'right')
        p.title.text = ticker
        return(p)

    def getdataframe(ticker):
        data=requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?qopts.columns=ticker,date,adj_open,adj_close&date.gte=2017-11-01&ticker='+ticker+'&api_key=EvoK-tD2UzfdszEHwWJE').json()
        df=pd.DataFrame(data['datatable']['data'],columns=['ticker','date','adj_open','adj_close'])
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        return df

    app.vars={}

    @app.route('/',methods=['GET','POST'])
    def index():
        if request.method == 'GET':
            return render_template('index_new.html')
        else:
            #request was a post
            app.vars['stock_ticker']=request.form['stock_ticker']
            app.vars['data_plotted']=request.form.getlist('data_plotted')

            df = getdataframe(app.vars['stock_ticker'])
            plot = plot_lines_multi(df,app.vars['data_plotted'],app.vars['stock_ticker'])
            script, div = components(plot)
            # grab the static resources
            js_resources = INLINE.render_js()
            css_resources = INLINE.render_css()
            html=render_template('graph.html', plot_script=script, plot_div=div, js_resources=js_resources,css_resources=css_resources)
            return encode_utf8(html)


    return app
