import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, DateFormatter
from matplotlib.ticker import FormatStrFormatter
import os, sys, time
import urllib.request as req

python_dir = os.path.dirname(os.path.realpath(__file__))
csv_dir = os.path.join(python_dir, 'csv')

#population values used from https://www.ukpopulation.org
England = ['England', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=E92000001&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&metric=newDeathsByPublishDate&format=csv', 558.9]
London = ['London', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=region&areaCode=E12000007&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&metric=newDeathsByPublishDate&format=csv', 89.5]
Scotland = ['Scotland', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=S92000003&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&metric=newDeathsByPublishDate&format=csv', 54.7]
Wales = ['Wales', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=W92000004&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&metric=newDeathsByPublishDate&format=csv', 32.0]
NI = ['NI', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=nation&areaCode=N92000002&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&metric=newDeathsByPublishDate&format=csv', 18.97]
Oxon = ['Oxfordshire', 'https://api.coronavirus.data.gov.uk/v2/data?areaType=utla&areaCode=E10000025&metric=newCasesByPublishDate&metric=newCasesBySpecimenDate&metric=newDeathsByPublishDate&format=csv', 6.91] #http://insight.oxfordshire.gov.uk/cms/population
admissions = 'https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=newAdmissions&metric=covidOccupiedMVBeds&metric=hospitalCases&format=csv'


pub = ['newCasesByPublishDate', 'New Cases by Publish Date']
spec = ['newCasesBySpecimenDate', 'New Cases by Specimen Date']
deaths = ['newDeathsByPublishDate', 'Deaths by Publish Date']

locations = [England, London, Scotland, Wales, NI]

def csvDownloader():
    #Checks if today's date is in currently downloaded csv, if not checks 1 on the server and only downloads all csvs if they contain today's date and exits the script if nothing new is downloaded
    if not os.path.isfile(os.path.join(csv_dir, London[0] + '.csv')):
        for loc in locations:
            req.urlretrieve(loc[1], os.path.join(csv_dir, loc[0] + '.csv'))
        req.urlretrieve(admissions, os.path.join(csv_dir, 'Admissions.csv'))
    else:
        da = str(datetime.today().date())
        print('Checking downloaded csv.')
        df = pd.read_csv(os.path.join(csv_dir, London[0] + '.csv'), index_col=0)
        df.index = pd.to_datetime(df.index)
        df_test = df.loc[df.index == da]
        if df_test.empty:
            print('Checking server csv.')
            df = pd.read_csv(London[1], index_col=0)
            df.index = pd.to_datetime(df.index)
            df_test = df.loc[df.index == da]
            if not df_test.empty:
                print('Downloading from server.')
                for loc in locations:
                    req.urlretrieve(loc[1], os.path.join(csv_dir, loc[0] + '.csv'))
                req.urlretrieve(admissions, os.path.join(csv_dir, 'Admissions.csv'))
            else:
                print('No new updates. Recreating graphs.')
                #sys.exit()
        else:
            print('No new updates. Recreating graphs.')

def dataFrame():
    df = {}
    for loc in locations:
        csv_file = os.path.join(csv_dir, loc[0] + '.csv')
        df[loc[0]] = pd.read_csv(csv_file, index_col=0)
        df[loc[0]] = df[loc[0]].drop(['areaType', 'areaCode', 'areaName'], axis = 1)
        df[loc[0]].index = pd.to_datetime(df[loc[0]].index)
        df[loc[0]] = df[loc[0]].sort_index()
        for plot_type in (pub, spec):
            df[loc[0]][plot_type[0] + 'per100k'] = df[loc[0]][plot_type[0]].div(loc[2])
            df[loc[0]][plot_type[0] + 'avg'] = df[loc[0]][plot_type[0]].rolling(window=7).mean()
            df[loc[0]][plot_type[0] + 'per100kavg'] = df[loc[0]][plot_type[0] + 'per100k'].rolling(window=7).mean()
    return df

def admissionsDF():
    df = {}
    csv_file = os.path.join(csv_dir, 'Admissions.csv')
    df = pd.read_csv(csv_file, index_col=0)
    df = df.drop(['areaType', 'areaCode', 'areaName'], axis = 1)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df['newAdmissionsavg'] = df['newAdmissions'].rolling(window=7).mean()
    df['covidOccupiedMVBedsavg'] = df['covidOccupiedMVBeds'].rolling(window=7).mean()
    df['hospitalCasesavg'] = df['hospitalCases'].rolling(window=7).mean()
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
    for loc in locations:
        df[loc[0]] = df[loc[0]][startDate:endDate]
        plt.plot(df[loc[0]][multiplot_details[0]], label=loc[0])
    plt.title(multiplot_details[1])
    plt.ylim(0)
    plt.legend()
    ax = plt.gca()
    #ax.set_ylabel('New cases per 100k')
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%b'))
    ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
    
    plt.savefig(os.path.join(python_dir, 'figs', multiplot_details[1] + '.png'))

def admissionsDP(look_back):
    plt.clf()
    startDate = '2020-03-01'
    endDate = pd.to_datetime(datetime.today() - timedelta(days=look_back))
    df = admissionsDF()
    df = df[startDate:endDate]
    plt.plot(df['newAdmissionsavg'], label='New Admissions')
    plt.plot(df['covidOccupiedMVBedsavg'], label='Patients Ventilated')
    plt.plot(df['hospitalCasesavg'], label='Hospitalised Patients')
    plt.title('Hospital Data (7 day average)')
    #plt.ylim(0)
    plt.legend()
    plt.yscale('log')
    ax = plt.gca()
    ax.xaxis.set_major_locator(MonthLocator())
    ax.xaxis.set_major_formatter(DateFormatter('%b'))
    ax.xaxis.set_minor_locator(MonthLocator(bymonthday=15))
    ax.yaxis.set_major_formatter(FormatStrFormatter("%g"))
    plt.savefig(os.path.join(python_dir, 'figs', 'Hospital Data (7 day average).png'))

if __name__ == '__main__':
    csvDownloader()
                       #100k,   avg
    dataPlotter(pub,  0, True,  True)
    dataPlotter(pub,  0, True,  False)
    dataPlotter(pub,  0, False, True)
    dataPlotter(pub,  0, False, False)
    dataPlotter(spec, 7, True,  True)
    dataPlotter(spec, 7, False, True)
    admissionsDP(2)
