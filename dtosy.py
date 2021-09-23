#Scritp to delete technologies from an osemosys datapackage
#%% Packages to import
import os
import sys
import pandas as pd
from shutil import copyfile
#%% Read in datapackage
def read_dp(path):
    # path = '' #for testing
    #datafiles =list()
    datafiles = next(os.walk(path+'data'))
    dic = dict()
    j = 0
    for j in range(len(datafiles[2])):
        dic[datafiles[2][j]] = pd.read_csv(path+'data/'+datafiles[2][j])
    return dic
#%% Function to delete technologies from dataframes
def dp_new(dic,techs):
    dp_new_path = 'dp_new'
    try:
        os.mkdir(dp_new_path)
    except OSError:
        print("Creation of the directory %s failed" % dp_new_path)
    copyfile('datapackage.json',dp_new_path+'/datapackage.json')
    dp_new_path = dp_new_path+'/data'
    try:
        os.mkdir(dp_new_path)
    except OSError:
        print("Creation of the directory %s failed" % dp_new_path)
    for i in dic:
        df = dic[i]
        if i=='TECHNOLOGY.csv':
            #dic[i] = dic[i]['VALUE'].astype('str')
            m = df.VALUE.isin(techs)
            df = df[~m]
            df.to_csv(dp_new_path+'/'+i,index=False)
        elif 'TECHNOLOGY' in df.columns:
            m = df.TECHNOLOGY.isin(techs)
            df = df[~m]
            df.to_csv(dp_new_path+'/'+i,index=False)
        else:
            df.to_csv(dp_new_path+'/'+i, index=False)
    return 
#%% Main Function to execute the script
def main(dp_path,tech_path):
    dic_data = read_dp(dp_path)
    t2d = pd.read_csv(tech_path)
    p_n_dp = dp_new(dic_data,t2d.iloc[:,0])
#%% Delete technology by executing script
if __name__ == '__main__':
    techs = sys.argv[1]
    #techs = 't2d.csv'
    dp_path = ''
    main(dp_path,techs)