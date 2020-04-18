from app import app
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, NumeralTickFormatter
from bokeh.plotting import figure, show
from bokeh.palettes import brewer

def formatter(val, type='number'):
    if 10**3 < val < 10**6:
        val = str(round(val / 10**3, 3)) + ' Thousand'
    elif 10**6 < val < 10**9:
        val = str(round(val / 10**6, 3)) + ' Million'
    elif 10**9 < val < 10**12:
        val = str(round(val / 10**9, 3)) + ' Billion'
    elif val >= 10**12:
        val = str(round(val / 10**12, 3)) + ' Trillion'
    return '$ ' + val if type == 'dollar' else val

def line(data, x, y, y_type='number'):
    x_range = data.loc[:, x]
    data_source = ColumnDataSource(data)
    # print(x_range)
    formats = '$ 0.00 a' if y_type == 'dollar' else '0.00 a'
    if x == 'date':
        data_hover = HoverTool(tooltips=[('Date', '@date{%F}'), (y.capitalize(), '@'+y+'{'+formats+'}')], 
            formatters={'@date': 'datetime'})
        data_fig = figure(x_axis_type='datetime', sizing_mode='scale_width', height=300, tools=[data_hover], 
            toolbar_location=None)
    else:
        data_hover = HoverTool(tooltips=[(x.capitalize(), '@'+x), (y.capitalize(), '@'+y+'{'+formats+'}')])
        data_fig = figure(x_range = x_range, sizing_mode='scale_width', height=300, tools=[data_hover], 
            toolbar_location=None)
    # styling visual
    data_fig.line(x=x, y=y, source=data_source, line_width=2)
    data_fig.xaxis.axis_label = x.capitalize()
    data_fig.xaxis.axis_label_text_font_size = "12pt"
    data_fig.xaxis.axis_label_standoff = 10
    data_fig.yaxis.axis_label = y.capitalize()
    data_fig.yaxis.axis_label_text_font_size = "12pt"
    data_fig.yaxis.axis_label_standoff = 10
    data_fig.xaxis.major_label_text_font_size = '10pt'
    data_fig.yaxis.major_label_text_font_size = '11pt'
    data_fig.yaxis[0].formatter = NumeralTickFormatter(format=formats)
    return components(data_fig)

def vbar(data, x, y, y_type='number'):
    x_range = data.loc[:, x]
    data_source = ColumnDataSource(data)
    # print(x_range)
    formats = '$ 0.00 a' if y_type == 'dollar' else '0.00 a'
    data_hover = HoverTool(tooltips=[(x.capitalize(), '@'+x), (y.capitalize(), '@'+y+'{'+formats+'}')])
    data_fig = figure(x_range = x_range, sizing_mode='scale_width', height=300, tools=[data_hover], 
        toolbar_location=None)
    # plot
    data_fig.vbar(x=x, top=y, source=data_source, width=0.9, hover_color='red', hover_fill_alpha=0.8)
    # styling visual
    data_fig.xaxis.axis_label = x.capitalize()
    data_fig.xaxis.axis_label_text_font_size = "12pt"
    data_fig.xaxis.axis_label_standoff = 10
    data_fig.yaxis.axis_label = y.capitalize()
    data_fig.yaxis.axis_label_text_font_size = "12pt"
    data_fig.yaxis.axis_label_standoff = 10
    data_fig.xaxis.major_label_text_font_size = '10pt'
    data_fig.yaxis.major_label_text_font_size = '11pt'
    data_fig.yaxis[0].formatter = NumeralTickFormatter(format=formats)
    return components(data_fig)

def hbar(data, x, y, x_type='number'):
    y_range = data.loc[:, y]
    x_data = data.loc[:, x]
    x_range = (x_data.min() - (x_data.max()-x_data.min())/10, x_data.max())
    data_source = ColumnDataSource(data)
    formats = '$ 0.00 a' if x_type == 'dollar' else '0.00 a'
    data_hover = HoverTool(tooltips=[(y.capitalize(), '@'+y), (x.capitalize(), '@'+x+'{'+formats+'}')])
    data_fig = figure(y_range=y_range, x_range=x_range, sizing_mode='scale_width', height=300, tools=[data_hover], 
        toolbar_location=None)
    # plot
    data_fig.hbar(y=y, right=x, source=data_source, height=0.8, hover_color='red', hover_fill_alpha=0.8)
    # styling visual
    data_fig.xaxis.axis_label = x.capitalize()
    data_fig.xaxis.axis_label_text_font_size = "12pt"
    data_fig.xaxis.axis_label_standoff = 10
    data_fig.yaxis.axis_label = y.capitalize()
    data_fig.yaxis.axis_label_text_font_size = "12pt"
    data_fig.yaxis.axis_label_standoff = 10
    data_fig.xaxis.major_label_text_font_size = '10pt'
    data_fig.yaxis.major_label_text_font_size = '11pt'
    data_fig.xaxis[0].formatter = NumeralTickFormatter(format=formats)
    return components(data_fig)

def multiline(data, x, y, y_type='number', *args):
    x_range = data.loc[:, x]
    data_source = ColumnDataSource(data)
    formats = '$ 0.00 a' if y_type == 'dollar' else '0.00 a'
    if x == 'date':
        # data_hover = HoverTool(tooltips=[('Date', '@date{%F}'), (y.capitalize(), '@'+y+'{'+formats+'}')], 
        #    formatters={'@date': 'datetime'})
        data_fig = figure(x_axis_type='datetime', sizing_mode='scale_width', height=300, toolbar_location=None)
    else:
        data_fig = figure(x_range = x_range, sizing_mode='scale_width', height=300, toolbar_location=None)
    # plot
    color = brewer['Spectral'][len(args)]
    i = 0
    for i in range(len(args)):
        plot = data_fig.line(x=x, y=args[i], line_color=color[i], line_width=5, source=data_source)
        data_fig.add_tools(HoverTool(renderers=[plot], tooltips=[(x.capitalize(), '@'+x), (args[i].capitalize(), '@'+args[i]+'{'+formats+'}')],
            mode='vline'))
        i += 1
    # styling visual
    data_fig.xaxis.axis_label = x.capitalize()
    data_fig.xaxis.axis_label_text_font_size = "12pt"
    data_fig.xaxis.axis_label_standoff = 10
    data_fig.yaxis.axis_label = y.capitalize()
    data_fig.yaxis.axis_label_text_font_size = "12pt"
    data_fig.yaxis.axis_label_standoff = 10
    data_fig.xaxis.major_label_text_font_size = '10pt'
    data_fig.yaxis.major_label_text_font_size = '11pt'
    data_fig.yaxis[0].formatter = NumeralTickFormatter(format=formats)
    return components(data_fig)