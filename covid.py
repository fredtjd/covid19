import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

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

for i in 'newAdmissions', 'newCasesByPublishDate', 'newCasesBySpecimenDate':
    df.plot(y=[i, i + '7dayRollingAvg'], ylim=0)
    plt.savefig(i + '.png')

df.plot(y=['newCasesByPublishDate7dayRollingAvg', 'newCasesBySpecimenDate7dayRollingAvg'], ylim=0)
plt.savefig('RollingAverages.png')