import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import os

python_dir = os.path.dirname(os.path.realpath(__file__))

#population values used from https://www.ukpopulation.org
London = ['London', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=region&areaCode=E12000007&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 89.5]
Scotland = ['Scotland', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=S92000003&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 54.7]
Wales = ['Wales', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=W92000004&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 32.0]
NI = ['NI', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=N92000002&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 18.97]

pub = ['newCasesByPublishDate', 'New Cases by Publication Date']
spec = ['newCasesBySpecimenDate', 'New Cases by Specimen Date']

def dataFrame():
    df = {}
    for location in (London, Scotland, NI, Wales):
        df[location[0]] = pd.read_csv(location[1], index_col=0)
        df[location[0]] = df[location[0]].drop(['areaType', 'areaCode', 'areaName'], axis = 1)
        df[location[0]].index = pd.to_datetime(df[location[0]].index)
        df[location[0]] = df[location[0]].sort_index()
        for plot_type in (pub, spec):
            df[location[0]][plot_type[0] + 'per100k'] = df[location[0]][plot_type[0]].div(location[2])
            df[location[0]][plot_type[0] + 'avg'] = df[location[0]][plot_type[0]].rolling(window=7).mean()
            df[location[0]][plot_type[0] + 'per100kavg'] = df[location[0]][plot_type[0] + 'per100k'].rolling(window=7).mean()
    return df

def dataPlotter(plot_type, look_back, percapita, avg):
    plt.clf()
    startDate = '2020-08-01'
    endDate = pd.to_datetime(datetime.today() - timedelta(days=look_back))
    df = dataFrame()
    if percapita == True and avg == True:
        multiplot_details = [plot_type[0] + 'per100kavg', plot_type[1] + ' per 100k (7 day average)']
    elif percapita == True and avg == False:
        multiplot_details = [plot_type[0] + 'per100k', plot_type[1] + ' per 100k']
    elif percapita == False and avg == True:
        multiplot_details = [plot_type[0] + 'avg', plot_type[1] + ' (7 day average)']
    else:
        multiplot_details = [plot_type[0], plot_type[1]]
    for location in (London, Scotland, Wales, NI):
        df[location[0]] = df[location[0]][startDate:endDate]
        plt.plot(df[location[0]][multiplot_details[0]], label=location[0])
    plt.title(multiplot_details[1])
    plt.ylim(0)
    plt.legend()
    ax = plt.gca()
    #ax.set_ylabel('New cases per 100k')
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%b'))
    ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
    plt.savefig(os.path.join(python_dir, multiplot_details[1] + '.png'))

if __name__ == '__main__':
    dataPlotter(spec, 5, True, True) #per100k/avg
    dataPlotter(pub, 1, True, True) #per100k/avg
    dataPlotter(spec, 5, True, False) #per100k
    dataPlotter(pub, 1, True, False) #per100k