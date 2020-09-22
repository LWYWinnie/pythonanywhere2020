from flask import Flask, render_template, request
import pandas as pd
import cufflinks as cf
import plotly as py
import plotly.graph_objs as go
from pyecharts import options as opts
from pyecharts.globals import ChartType, SymbolType
from pyecharts.charts import Bar, Grid, Line,Scatter

app = Flask(__name__)
df = pd.read_csv('junfei.csv',encoding='gbk')
jf_available = ['世界军费情况','世界军费占gdp比重'] #下拉菜单
cf.set_config_file(offline=True, theme="ggplot")
py.offline.init_notebook_mode()

@app.route('/',methods=['GET'])
def jf():
    data_str = df[:40].to_html()
    with open("世界军费.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    return render_template('ge_data.html',
                           the_plot_all=plot_all,
                           the_select_jf=jf_available,
                           the_res = data_str)

@app.route('/jf_response',methods=['POST'])
def jf_response() -> 'html':
    jf_available = ['世界军费情况','世界军费占gdp比重']
    data_str = df.to_html()
    with open("军费占gdp比.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())

    return render_template('ge_data.html',
                            the_plot_all=plot_all,
                            the_res = data_str,
                            the_select_jf=jf_available,
                           )

@app.route('/zd_jf',methods=['GET'])
def zd_jr():
    df = pd.read_csv('junfeizhanbi.csv', encoding='gbk')
    jf_available = ['高收入国家','低收入国家'] # 列表下拉值赋予给regions_available
    cf.set_config_file(offline=True, theme="ggplot")
    py.offline.init_notebook_mode()
    data_str = df[:40].to_html()
    return render_template('zd_jf.html',
                           the_select_jf=jf_available,
                           the_res = data_str)
#数据循环模块
@app.route('/zd_jf_response',methods=['POST'])
def zd_jr_response() -> 'html':
    jf_available = ['高收入国家','低收入国家']  # 列表下拉值赋予给regions_available
    cf.set_config_file(offline=True, theme="ggplot")
    py.offline.init_notebook_mode()
    the_jf = request.form["the_jf_selected"]
    dfs = df.query("Country=='{}'".format(the_jf))

    # 数据循环模块
    def line_markline() -> Line:
        a = []
        times = []
        for i in range(1960, 2018):
            a.append(int(int(dfs[str(i)]) / 100000000))
            times.append(str(i))
        c = (
            Line()
                .add_xaxis(times)
                .add_yaxis(
                "{}".format(the_jf),
                a,
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average")]),
            )

                .set_global_opts(title_opts=opts.TitleOpts(title="{}军费占比趋势".format(the_jf)))
        )
        return c

    line_markline().render()
    with open("render.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    data_str = dfs[:40].to_html()
    return render_template('zd_jf.html',
                            the_plot_all=plot_all,
                            the_res = data_str,
                            the_select_jf=jf_available,
                           )


@app.route('/zm_jr',methods=['GET'])
def zm_jr():
    data_str = df[:40].to_html()
    with open("中美军人对比.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    return render_template('zm_jr.html',
                           the_plot_all=plot_all,
                           the_select_jf=jf_available,
                           the_res = data_str)

@app.route('/zm_jf',methods=['GET'])
def zm_jf():
    data_str = df[:40].to_html()
    with open("中美军费增长.html", encoding="utf8", mode="r") as f:
        plot_all = "".join(f.readlines())
    return render_template('zm_jf.html',
                           the_plot_all = plot_all,
                           the_select_jf = jf_available,
                           the_res = data_str)


if __name__ == '__main__':
    app.run(debug=True,port=8000)
