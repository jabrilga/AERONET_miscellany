import os
import numpy as np
import pandas as pd
import datetime as _datetime
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn import linear_model
import seaborn as sns
sns.set_theme(style="darkgrid")
import matplotlib.dates as mdates


def read_AERONET_file(file_path, filter_depolarization = False, _parse_dates = [0,1], _skiprows = 6):
    """
    Read a given AERONET AOT data file, and return it as a dataframe.
    
    This returns a DataFrame containing the AERONET data, with the index
    set to the timestamp of the AERONET observations. Rows or columns
    consisting entirely of missing data are removed. All other columns
    are left as-is.
    """

    dateparse = lambda x: datetime.strptime(x, "%d:%m:%Y %H:%M:%S")
    aeronet = pd.read_csv(file_path, skiprows = _skiprows, na_values=['N/A'],
                          parse_dates={'times':_parse_dates},
                          date_parser=dateparse)

    aeronet = aeronet.set_index('times')
    
    # Drop any rows that are all NaN and any cols that are all NaN
    # & then sort by the index
    an = (aeronet.dropna(axis=1, how='all')
                .dropna(axis=0, how='all')
                .rename(columns={'Last_Processing_Date(dd/mm/yyyy)': 'Last_Processing_Date'})
                .sort_index())
    return an

Evora = False
Granada = False
Barcelona = True

if Evora:
    file_path = r"AERONET\20190628_20190628_Evora.lev20"
    data = read_AERONET_file(file_path, _parse_dates = [0,1])
    AODs = [key for key in data.keys() if "AOD_" in key and 'nm' in key]
    plt.ylim(0,0.4); plt.ylabel("AOD"); plt.xlabel("Time UTC")
    for wl in AODs:
        if data[wl].mean() > 0:
            plt.plot(data[wl], label = wl.replace("_","").replace("nm", ""))
    plt.legend()
    plt.show()
    AEs = [key for key in data.keys() if "Angstrom" in key]
    plt.ylim(0,1.6); plt.ylabel("AE"); plt.xlabel("Time UTC")
    for wl in AEs:
        if data[wl].mean() > 0:
            plt.plot(data[wl], label = ("AE" + wl[0:7]))
    plt.legend()
    plt.show()

if Evora:
    fig,ax = plt.subplots()#; fig.suptitle("Photometer AOD and AE")
    file_path = r"AERONET\20190628_20190628_Evora.lev20"
    data = read_AERONET_file(file_path, _parse_dates = [0,1])
    #data.index = data.index.strftime('%H:%M')
    AODs = [key for key in data.keys() if "AOD_" in key and 'nm' in key and'675' in key]
    AEs = [key for key in data.keys() if "Angstrom" in key and '440-870' in key]
    AODs_overpass = data[AODs].iloc[-11]
    AEs_overpass = data[AEs].iloc[-11]
    data_overpass = pd.DataFrame(-1, columns = data.columns, index = data.index)
    data_overpass.iloc[-11, data_overpass.columns.get_loc(AODs[0])] = AODs_overpass[AODs].iloc[0]
    data_overpass.iloc[-11, data_overpass.columns.get_loc(AEs[0])] = AEs_overpass[AEs].iloc[0]
    #data_
    #data_overpass = data.iloc[-11]
    #print(data_overpass[AODs])
    #print(data[AODs])
    ax.plot(data[AODs], color="red", label = ("AOD 675"))
    ax.plot(data_overpass[AODs], color = 'black', marker = 's', linestyle = '')
    ax.set_xlabel("Time UTC"); ax.set_ylabel("AOD"); ax.set_ylim(0,0.25)
    ax2=ax.twinx()
    ax2.plot(data[AEs], color="blue", label = ("AE 440-870"), linestyle = 'dashed')
    ax2.plot(data_overpass[AEs], color = 'black', marker = 's', linestyle = '')
    ax2.set_ylabel("AE"); ax2.set_ylim(0,1.25); ax2.set_yticks([0,0.25, 0.5, 0.75, 1, 1.25])
    #ax.set_xticks(['06:00:00'])
    #ax2.set_xticks(['06:00:00'])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    #ax.set_xticks([data.index[0], data.index[int(len(data)/6)], data.index[int(2*len(data)/6)], data.index[int(3*len(data)/6)], data.index[int(4*len(data)/6)], data.index[int(5*len(data)/6)], data.index[-1]])
    #ax2.set_xticks([data.index[0], data.index[int(len(data)/6)], data.index[int(2*len(data)/6)], data.index[int(3*len(data)/6)], data.index[int(4*len(data)/6)], data.index[int(5*len(data)/6)], data.index[-1]])
    #ax.set_xticks([data.index[0], data.index[int(len(data)/3)], data.index[int(2*len(data)/3)]], data.index[-1]), ax2.set_xticks([data.index[0], data.index[int(len(data)/3)], data.index[int(2*len(data)/3)], data.index[-1]])
    #ax.set_xticks(xticks.index)
    #ax2.set_xticks(xticks.index)
    fig.legend(loc = (0.13, 0.17))
    plt.show()
    
    #pd.set_option("display.max_rows", None, "display.max_columns", None)
    #print(data[AODs].tail)
    #xprint(data[AEs])

if Evora:
    file_path = r"AERONET\20190628_20190628_Evora.all"
    data = read_AERONET_file(file_path, _parse_dates = [1,2])
    plt.plot(data['REff-T'], label = "total")
    plt.plot(data['REff-F'], label = "fine")
    plt.plot(data['REff-C'], label = "coarse")
    plt.legend()
    plt.show()
    #print(data['REff-T'])

if Evora:
    file_path = r"AERONET\20190628_20190628_Evora.ssa"
    data = read_AERONET_file(file_path, _parse_dates = [1,2])
    SSAs = [key for key in data.keys() if "Single_Scattering_Albedo" in key]
    plt.ylim(0.90, 1); plt.ylabel("SSA"); plt.xlabel("Time UTC")
    #print(SSAs)
    for wl in SSAs:
        if data[wl].mean() > 0:
            #print(data[wl])
            plt.plot(data[wl], label = wl.replace("Single_Scattering_Albedo[","SSA ").replace("nm]", ""))
    plt.legend()
    plt.show()
    #print(data['Single_Scattering_Albedo[1020nm]'] - data['Single_Scattering_Albedo[440nm]'])

if Granada:
    fig,ax = plt.subplots()#; fig.suptitle("Photometer AOD and AE")
    file_path = r"AERONET\190905_190905_Granada.lev15"
    data = read_AERONET_file(file_path, _parse_dates = [0,1], _skiprows = 4)
    #data.index = data.index.strftime('%H:%M')
    #print(data)
    AODs = [key for key in data.keys() if "AOT_" in key and '675' in key]
    AEs = [key for key in data.keys() if "Angstrom" in key and '440-870' in key]
    #print(AODs, AEs)
    ax.plot(data[AODs], color="red", label = ("AOD 675"))
    ax.set_xlabel("Time UTC"); ax.set_ylabel("AOD"); ax.set_ylim(0,0.40)
    ax2=ax.twinx()
    ax2.plot(data[AEs], color="blue", label = ("AE 440-870"), linestyle = 'dashed')
    ax2.set_ylabel("AE"); ax2.set_ylim(0,2)#; ax2.set_yticks([0,0.25, 0.5, 0.75, 1, 1.25])
    #ax.set_xticks([data.index[0], data.index[int(len(data)/6)], data.index[int(2*len(data)/6)], data.index[int(3*len(data)/6)], data.index[int(4*len(data)/6)], data.index[int(5*len(data)/6)], data.index[-1]])
    #ax2.set_xticks([data.index[0], data.index[int(len(data)/6)], data.index[int(2*len(data)/6)], data.index[int(3*len(data)/6)], data.index[int(4*len(data)/6)], data.index[int(5*len(data)/6)], data.index[-1]])
    fig.legend(loc = (0.13, 0.17))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.show()
    #print(data[AODs], data[AEs])

if Granada:
    file_path = r"AERONET\20190905_20190905_Granada.all"
    data = read_AERONET_file(file_path, _parse_dates = [1,2])
    plt.plot(data['REff-T'], label = "total")
    plt.plot(data['REff-F'], label = "fine")
    plt.plot(data['REff-C'], label = "coarse")
    plt.legend()
    plt.show()
    #print(data['REff-T'])  

    SSAs = [key for key in data.keys() if "Single_Scattering_Albedo" in key]
    plt.ylim(0.90, 1); plt.ylabel("SSA"); plt.xlabel("Time UTC")
    print(SSAs)
    for wl in SSAs:
        if data[wl].mean() > 0:
            print(data[wl])
            plt.plot(data[wl], label = wl.replace("Single_Scattering_Albedo[","SSA ").replace("nm]", ""))
    plt.legend()
    plt.show()
    print(data['Single_Scattering_Albedo[1020nm]'] - data['Single_Scattering_Albedo[440nm]'])


if Barcelona:
    fig,ax = plt.subplots()#; fig.suptitle("Photometer AOD and AE")
    file_path = r"AERONET\190702_190702_Barcelona.lev15"
    data = read_AERONET_file(file_path, _parse_dates = [0,1], _skiprows = 4)
    #data.index = data.index.strftime('%H:%M')
    AODs = [key for key in data.keys() if "AOT_" in key and '675' in key]
    AEs = [key for key in data.keys() if "Angstrom" in key and '440-870' in key]
    AODs_overpass = data[AODs].iloc[-7]
    AEs_overpass = data[AEs].iloc[-7]
    data_overpass = pd.DataFrame(-1, columns = data.columns, index = data.index)
    data_overpass.iloc[-7, data_overpass.columns.get_loc(AODs[0])] = AODs_overpass[AODs].iloc[0]
    data_overpass.iloc[-7, data_overpass.columns.get_loc(AEs[0])] = AEs_overpass[AEs].iloc[0]

    _filter = data[AODs] > 0.1
    ax.plot(data[AODs]/_filter, color="red", label = ("AOD 675"))
    ax.plot(data_overpass[AODs], color = 'black', marker = 's', linestyle = '')
    ax.set_xlabel("Time UTC"); ax.set_ylabel("AOD"); ax.set_ylim(0,0.25)
    ax2=ax.twinx()
    _filter = data[AEs] > 1.25
    ax2.plot(data[AEs]/_filter, color="blue", label = ("AE 440-870"), linestyle = 'dashed')
    ax2.plot(data_overpass[AEs], color = 'black', marker = 's', linestyle = '')
    ax2.set_ylabel("AE"); ax2.set_ylim(0,2); ax2.set_yticks([0,0.4, 0.8, 1.2, 1.6, 2])
    #ax.set_xticks([data.index[0], data.index[int(len(data)/6)], data.index[int(2*len(data)/6)], data.index[int(3*len(data)/6)], data.index[int(4*len(data)/6)], data.index[int(5*len(data)/6)], data.index[-1]])
    #ax2.set_xticks([data.index[0], data.index[int(len(data)/6)], data.index[int(2*len(data)/6)], data.index[int(3*len(data)/6)], data.index[int(4*len(data)/6)], data.index[int(5*len(data)/6)], data.index[-1]])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.legend(loc = (0.13, 0.17))
    plt.show()
    print(data[AODs].iloc[-7], data[AEs].iloc[-7])

if Barcelona:
    file_path = r"AERONET\20190702_20190702_Barcelona.all"
    data = read_AERONET_file(file_path, _parse_dates = [1,2])
    plt.plot(data['REff-T'], label = "total")
    plt.plot(data['REff-F'], label = "fine")
    plt.plot(data['REff-C'], label = "coarse")
    plt.legend()
    plt.show()
    #print(data['REff-T'])

    SSAs = [key for key in data.keys() if "Single_Scattering_Albedo" in key]
    plt.ylim(0.85, 1); plt.ylabel("SSA"); plt.xlabel("Time UTC")
    #print(SSAs)
    for wl in SSAs:
        if data[wl].mean() > 0:
            #print(data[wl])
            plt.plot(data[wl], label = wl.replace("Single_Scattering_Albedo[","SSA ").replace("nm]", ""))
    plt.legend()
    plt.show()
    print(data['Single_Scattering_Albedo[1020nm]'] - data['Single_Scattering_Albedo[440nm]'])