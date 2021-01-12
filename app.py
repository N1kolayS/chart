#!/usr/bin/python3.8

from sanic import Sanic
from sanic.response import json
from sanic import response
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns
import pandas as pd


app = Sanic(__name__)

BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(BASE_FOLDER, 'resources')


@app.route("/")
async def test(request):
    data = request.json
    type_data = type(data)
    return json({"data": data, "type": type_data.__name__})


@app.route("/donut")
def make_donut(request):
    data = request.json
    labels = []
    size = []
    colors = []
    explode = []
    for item in data['items']:
        if 'label' in item:
            labels.append(item['label'])
        if 'explode' in item:
            explode.append(float(item['explode']))
        size.append(item['size'])
        colors.append(item['color'])

    wedgeprops = data.get('wedgeprops', {})
    startangle = data.get('startangle', 0)
    autopct = data.get('autopct', None)
    pctdistance = float(data.get('pctdistance', 0.85))
    radius = float(data.get('radius', 0.75))
    dpi = data.get('dpi', 100)

    if not labels:
        labels = None

    if not explode:
        explode = None


    plt.clf()

    plt.pie(
        size,
        labels=labels,
        colors=colors,
        wedgeprops=wedgeprops,
        startangle=startangle,
        autopct=autopct,
        pctdistance=pctdistance,
        radius=radius,
        explode=explode,

    )

    p = plt.gcf()
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    p.gca().add_artist(my_circle)
    plt.tight_layout()
    plt.axis('equal')

    #plt.text(0, 0, 'Hello', ha='center', size=20, fontweight='bold', va='center', color='#115285')
    file = IMG_DIR+'/donut.png'
    plt.savefig(file, dpi=dpi, bbox_inches='tight')
    return response.file(file)


@app.route("/violin")
def make_donut(request):
    data = request.json
    dpi = data.get('dpi', 100)

    items = data.get('items', [])

    fig = plt.figure()

    # Create an axes instance
    ax = fig.add_axes([0, 0, 1, 1])

    # Create the boxplot
    bp = ax.violinplot(items)

    file = IMG_DIR+'/violin.png'
    plt.savefig(file, dpi=dpi, bbox_inches='tight')
    return response.file(file)


@app.route("/violin-sns")
def make_violin_sns(request):
    data = request.json
    dpi = data.get('dpi', 100)
    items = data.get('items', [])
    y = data.get('y', 'col_1')
    showfliers = data.get('showfliers', False)
    showbox = data.get('showbox', False)
    style = data.get('style', 'whitegrid')
    plt.clf()
    sns.set_style(style)

    dt = pd.DataFrame.from_dict(items)

    sns.boxplot(y=y, data=dt, showfliers=showfliers, showbox=showbox, whis=[2.5, 97.5])
    sns.violinplot(y=y, data=dt)

    file = IMG_DIR+'/violin.png'
    plt.savefig(file, dpi=dpi, bbox_inches='tight')
    return response.file(file)


@app.route("/bar2")
def bar(request):
    data = request.json

    dpi = data.get('dpi', 100)
    width = data.get('widthBars', 0.35)
    label1 = data.get('label1', '')
    label2 = data.get('label2', '')
    y_label = data.get('y_label', None)
    title = data.get('title', None)
    x_label_enable = data.get('x_label_enable', False)
    legend_enable = data.get('legend_enable', False)
    size_label_enable = data.get('size_label_enable', False)
    color1 = data.get('color1', '#00ff00')
    color2 = data.get('color2', '#0000ff')
    x_label_angle = data.get('x_label_angle', None)

    plt.clf()
    items1 = []
    items2 = []
    labels = []
    items = data.get('items', [])
    for item in items:
        labels.append(item['label'])
        items1.append(float(item['item1']))
        items2.append(float(item['item2']))

    x = np.arange(len(labels))  # the label locations

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, items1, width, label=label1, color=color1)
    rects2 = ax.bar(x + width / 2, items2, width, label=label2, color=color2)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    if y_label:
        ax.set_ylabel(y_label)
    if title:
        ax.set_title(title)

    if x_label_enable:
        ax.set_xticks(x)

    ax.set_xticklabels(labels)

    if legend_enable:
        ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    if size_label_enable:
        autolabel(rects1)
        autolabel(rects2)

    if x_label_angle:
        plt.xticks(rotation=x_label_angle)

    plt.tight_layout()
    file = IMG_DIR + '/bar2.png'
    plt.savefig(file)
    return response.file(file)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
