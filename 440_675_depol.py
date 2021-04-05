import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn import linear_model

def read_given_AERONET_file(file_path):
    try:
        file = open(file_path, 'r')
    except:
        print(f'File {file_path} could not be found.')
        
    file = file.readlines()[:]
    header = file[0:6]
    #print(header)
    variables = file[6:7]
    #print(variables[0].split(','))
    
    data = dict.fromkeys(variables[0].split(','), [])
    print(data['Depolarization_Ratio[440nm]'])
    #for line in file[7:]:
    #    print(line)
        
def read_AERONET_file(file_path, filter_depolarization = False):
    """
    Read a given AERONET AOT data file, and return it as a dataframe.
    
    This returns a DataFrame containing the AERONET data, with the index
    set to the timestamp of the AERONET observations. Rows or columns
    consisting entirely of missing data are removed. All other columns
    are left as-is.
    """

    dateparse = lambda x: datetime.strptime(x, "%d:%m:%Y %H:%M:%S")
    aeronet = pd.read_csv(file_path, skiprows=6, na_values=['N/A'],
                          parse_dates={'times':[1,2]},
                          date_parser=dateparse)

    aeronet = aeronet.set_index('times')
    
    # Drop any rows that are all NaN and any cols that are all NaN
    # & then sort by the index
    an = (aeronet.dropna(axis=1, how='all')
                .dropna(axis=0, how='all')
                .rename(columns={'Last_Processing_Date(dd/mm/yyyy)': 'Last_Processing_Date'})
                .sort_index())
    if filter_depolarization:
        filter_aux = an['Depolarization_Ratio[440nm]'] > 0
        an['Depolarization_Ratio[440nm]'] *= filter_aux
        an['Depolarization_Ratio[675nm]'] *= filter_aux
    return an

def plot_depol(data, title = False):
    model = linear_model.LinearRegression(fit_intercept = False)
    model.fit(np.array(data['Depolarization_Ratio[675nm]']).reshape(-1,1), np.array(data['Depolarization_Ratio[440nm]']))
    predict = model.predict(np.array([0,1]).reshape(-1,1))
    slope = model.coef_[0]
    r2 = model.score(np.array(data['Depolarization_Ratio[675nm]']).reshape(-1,1), np.array(data['Depolarization_Ratio[440nm]']))
    plt.figure(figsize = (6,6))
    if title:
        plt.title(title + '\ncomplete database:   ' +  str(round(slope,2)) + '     ' + str(round(r2,2)))
    else:
        plt.title(f'{slope} {r2}')
    plt.ylim([0,0.5])
    plt.xlim([0,0.5])
    plt.xlabel(r'$\delta_{675}$')
    plt.ylabel(r'$\delta_{440}$')
    plt.scatter(data['Depolarization_Ratio[675nm]'], data['Depolarization_Ratio[440nm]'])
    plt.plot([0,1], predict)
    plt.grid()
    x = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4]
    y = 1.77 * np.array(x) ** 2 + 0.03
    plt.plot(x,y)
    x = [0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4]
    y = 1.17 * np.array(x) ** 1.57 + 0.02
    plt.plot(x,y)
    plt.legend(('y = 0.75 x', 'y = 1.77 * x^2 + 0.03', 'y = 1.17 * x^1.57 + 0.02'))
    plt.show()

    
def output_plot_depol(data, title = False, ax = None):
    model = linear_model.LinearRegression(fit_intercept = False)
    model.fit(np.array(data['Depolarization_Ratio[675nm]']).reshape(-1,1), np.array(data['Depolarization_Ratio[440nm]']))
    predict = model.predict(np.array([0,1]).reshape(-1,1))
    slope = model.coef_[0]
    r2 = model.score(np.array(data['Depolarization_Ratio[675nm]']).reshape(-1,1), np.array(data['Depolarization_Ratio[440nm]']))
    ax.scatter(data['Depolarization_Ratio[675nm]'], data['Depolarization_Ratio[440nm]'])
    ax.set_title(title + ':   ' + str(round(slope,2)) + '     ' + str(round(r2,2)))
    ax.set_ylim([0,0.5])
    ax.set_xlim([0,0.5])
    ax.set_xlabel(r'$\delta_{675}$')
    ax.set_ylabel(r'$\delta_{440}$')
    ax.plot([0,1], predict)
    ax.grid()

def perform_analysis(data, title = False, filter_by_AE = False):
    if filter_by_AE:
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize =  (16,5), sharey = True)
        fig.suptitle(title)
        ang_exp = 'Angstrom_Exponent_440-870nm_from_Coincident_Input_AOD'
        #ang_exp = 'Extinction_Angstrom_Exponent_440-870nm-Total'
        #ang_exp = 'Absorption_Angstrom_Exponent_440-870nm'

        #Dust case
        filter_dust = data[ang_exp] < 0.5
        title_dust = 'dust'
        data_dust = data.copy()
        data_dust['Depolarization_Ratio[675nm]'] *= filter_dust
        data_dust['Depolarization_Ratio[440nm]'] *= filter_dust
        output_plot_depol(data_dust, title_dust, ax1)
        #for elem in data_dust['Depolarization_Ratio[440nm]']:
        #    if elem != 0:
        #        print(elem)
        
        #Antopogenic case
        filter_clean = data[ang_exp] > 1
        title_clean = 'antrop.'
        data_clean = data.copy()
        data_clean['Depolarization_Ratio[675nm]'] *= filter_clean
        data_clean['Depolarization_Ratio[440nm]'] *= filter_clean
        output_plot_depol(data_clean, title_clean, ax2)
        
        #Mixed case
        filter_mixed_1 = data[ang_exp] > 0.5
        filter_mixed_2 = data[ang_exp] < 1
        title_mixed = 'mixed'
        data_mixed = data.copy()
        data_mixed['Depolarization_Ratio[675nm]'] *= filter_mixed_1 & filter_mixed_2
        data_mixed['Depolarization_Ratio[440nm]'] *= filter_mixed_1 & filter_mixed_2
        output_plot_depol(data_mixed, title_mixed, ax3)
        plt.show()
        
    else:
        plot_depol(data, title)

level = 'lv2'
#level = 'lv15'
station = 'Granada'
#station = 'Evora'
#station = 'Barcelona'


try:
    file_path = "C:\\Users\\jesus\\Desktop\\" + level + "\\20190101_20201031_" + station + ".all"
    data = read_AERONET_file(file_path, filter_depolarization = True)
    #perform_analysis(data, title = level + ' ' + station + ' 2019-2020', filter_by_AE = True)
except:
    pass

try:
    file_path = "C:\\Users\\jesus\\Desktop\\" + level + "\\20040101_20211231_" + station + ".all"
    data = read_AERONET_file(file_path, filter_depolarization = True)
    #perform_analysis(data, title = level + ' ' + station + ' 2004-2021', filter_by_AE = True)
    perform_analysis(data, title = level + ' ' + station + ' 2004-2021')
except:
    pass