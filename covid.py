import pandas as pd
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import os

python_dir = os.path.dirname(os.path.realpath(__file__))

#population values used from https://www.ukpopulation.org

UK = ['UK', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 68.0]
London = ['London', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=region&areaCode=E12000007&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 93.0]
Scotland = ['Scotland', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=S92000003&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 54.7]
Wales = ['Wales', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=W92000004&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv', 32.0]

endDate = pd.to_datetime(datetime.today() - timedelta(days=1))
startDate = '2020-08-01'

adm = ['newAdmissions', 'New Admissions']
pub = ['newCasesByPublishDate', 'New Cases by Publication Date']
spec = ['newCasesBySpecimenDate', 'New Cases by Specimen Date']

def dataManipulator(plot_type):
    plt.title(plot_type[1])
    fig, axes = plt.subplots(nrows=3, ncols=1)
    counter = 0
    for location in (London, Scotland, Wales):
        df = pd.read_csv(location[1], index_col=0)
        df = df.drop(['areaType', 'areaCode', 'areaName'], axis = 1)
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df[startDate:endDate]
#    for dt in (adm, pub, spec):
        #df[plot_type[0] + '7dayRollingAvg'] = df[plot_type[0]].rolling(window=7).mean()
        df[plot_type[0] + 'per100k'] = df[plot_type[0]].div(location[2])
        #df.plot.area(figsize=(12,4),  y=[dt[0], dt[0] + '7dayRollingAvg'], ylim=0, title=location[0] + ' ' + dt[1])
        df.plot.area(figsize=(10,8), ax=axes[counter], y=plot_type[0] + 'per100k', ylim=0, title=location[0], legend=None)
        axes[counter].set_xlabel('')
        counter += 1
    fig.tight_layout()
    fig.suptitle(plot_type[1] + ' per 100k', fontweight='bold')
    plt.subplots_adjust(top=0.9)
    plt.savefig(plot_type[1] + '.png')

dataManipulator(spec)
dataManipulator(pub)
dataManipulator(adm)