import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from git import Repo
import os

python_dir = os.path.dirname(os.path.realpath(__file__))

latestData = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newAdmissions&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&format=csv'
endDate = pd.to_datetime(datetime.today() - timedelta(days=2))

df = pd.read_csv(latestData, index_col=0)
df = df.drop(['areaType', 'areaCode', 'areaName'], axis = 1)
df.index = pd.to_datetime(df.index)
df = df.sort_index()

df['newAdmissions7dayRollingAvg'] = df['newAdmissions'].rolling(window=7).mean()
df['newCasesByPublishDate7dayRollingAvg'] = df['newCasesByPublishDate'].rolling(window=7).mean()
df['newCasesBySpecimenDate7dayRollingAvg'] = df['newCasesBySpecimenDate'].rolling(window=7).mean()

df = df['2020-03-01':endDate]

repo = Repo(os.path.join(python_dir, '.git'))

def grapher(graphData, graphTitle):
    df.plot(y=[graphData, graphData + '7dayRollingAvg'], ylim=0, title=graphTitle, xlabel='Date', ylabel='n')
    plt.savefig(graphData + '.png')
    repo.git.add(graphData + '.png')

grapher('newAdmissions', 'New Admissions')
grapher('newCasesByPublishDate', 'New Cases by Publication Date')
grapher('newCasesBySpecimenDate', 'New Cases by Specimen Date')

repo.index.commit('Updated graphs')
repo.remote(name='origin').push()