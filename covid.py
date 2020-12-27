import pandas as pd
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
import os

python_dir = os.path.dirname(os.path.realpath(__file__))

#population values used from https://www.ukpopulation.org

UK = ['UK', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 68.0]
London = ['London', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=region&areaCode=E12000007&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 93.0]
Liverpool = ['Liverpool', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&areaCode=E08000012&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 4.9]
Manchester = ['Manchester', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&areaCode=E08000003&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 5.4]
Birmingham = ['Birmingham', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&areaCode=E08000025&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 13.0]
Scotland = ['Scotland', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=S92000003&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 54.7]
Wales = ['Wales', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=W92000004&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 32.0]
NI = ['NI', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=N92000002&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 18.97]

#endDate = pd.to_datetime(datetime.today() - timedelta(days=1))
#startDate = '2020-08-01'

adm = ['newAdmissions', 'New Admissions']
pub = ['newCasesByPublishDate', 'New Cases by Publication Date']
spec = ['newCasesBySpecimenDate', 'New Cases by Specimen Date']

def dataPlotter(plot_type):
    plt.clf()
    startDate = '2020-08-01'
    if plot_type == spec:
        endDate = pd.to_datetime(datetime.today() - timedelta(days=5))
    else:
        endDate = pd.to_datetime(datetime.today() - timedelta(days=1))
    plt.title(plot_type[1])
    for location in (London, Scotland, Wales, NI):
        df = pd.read_csv(location[1], index_col=0)
        df = df.drop(['areaType', 'areaCode', 'areaName'], axis = 1)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df[startDate:endDate]
#    for dt in (adm, pub, spec):
        #df[plot_type[0] + '7dayRollingAvg'] = df[plot_type[0]].rolling(window=7).mean()
        df[plot_type[0] + 'per100k'] = df[plot_type[0]].div(location[2])
        #df[plot_type[0] + 'avg'] = df[plot_type[0]].rolling(window=7).mean()
        df[plot_type[0] + 'per100kavg'] = df[plot_type[0] + 'per100k'].rolling(window=7).mean()
        plt.plot(df[plot_type[0] + 'per100kavg'], label=location[0])
    plt.ylim(0)
    plt.legend()
    ax = plt.gca()
    ax.set_ylabel('New cases per 100k')
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%b'))
    ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
    plt.savefig(plot_type[1] + '.png')
dataPlotter(spec)
dataPlotter(pub)
#dataManipulator(adm)