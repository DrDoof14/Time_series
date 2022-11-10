import os
import pandas as pd 

print(os.getcwd())
for id in range(2,10):
    cgm_path = '/Users/tommasobassignana/Desktop/all_algos/DATA_LOADER/d1namo/diabetes/CGM/'
    _ = pd.read_csv(f'{cgm_path}cgm_00{id}')
    d = d.set_index(pd.to_datetime(_['dt']))['glucose'] # uses both SMBG and CGM
