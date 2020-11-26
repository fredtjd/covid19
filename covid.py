import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os

python_dir = os.path.dirname(os.path.realpath(__file__))

UK = ['UK', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv']
London = ['London', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=region&areaCode=E12000007&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv']

endDate = pd.to_datetime(datetime.today() - timedelta(days=2))

adm = ['newAdmissions', 'New Admissions']
pub = ['newCasesByPublishDate', 'New Cases by Publication Date']
spec = ['newCasesBySpecimenDate', 'New Cases by Specimen Date']      

def dataManipulator(location):
    df = pd.read_csv(location[1], index_col=0)
    df = df.drop(['areaType', 'areaCode', 'areaName'], axis = 1)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df = df['2020-03-01':endDate]
    for dt in (adm, pub, spec):
        df[dt[0] + '7dayRollingAvg'] = df[dt[0]].rolling(window=7).mean()
        df.plot(y=[dt[0], dt[0] + '7dayRollingAvg'], ylim=0, title=dt[1])
        plt.savefig(location[0] + ' ' + dt[0] + '.png')

dataManipulator(London)
dataManipulator(UK)
