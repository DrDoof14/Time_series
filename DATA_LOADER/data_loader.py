import json
import pandas as pd

# done: dictionaries >> dataframe? maybe better when you scale, its easy to concat a subset of keys
# done: all index must be datetime 
# done: id (df_column or dict_keys) must be integer
# done: choose between smbg and cgm!?!?!? -> do it in another class, this class is reserved to load data in a dict!
# todo: add http://direcnet.jaeb.org/Studies.aspx?RecID=155tblADataCGMS.csv
# todo: mettere path opzionale 

class DataReader():
    """
    read data from all sources: THIS CLASS READS ALL(!) DATA (do not change)
    all data in dict
    """
    def __init__(self, name:str, filepath:str) -> None:
        self.name = name
        self.filepath = filepath
        if name not in ['ohio','d1namo','dally']:
            raise ValueError(f'Data not valid, can obly be: ohio, d1namo, dally')

    def read_ohio(self) -> dict:
        """read all ohio 2018-2020 data for every patient

        Returns:
            dict: combined train and test, all variables
        """
        tr, te, oh = {}, {}, {}
        for i in range(1,13):
            p = pd.read_csv(f'{self.filepath}tr{i}.csv')
            p.drop(columns='Unnamed: 0', inplace=True)
            p['datetime'] = pd.to_datetime(p['datetime'])
            tr[i] = p.rename(columns={'datetime':'dt_idx'}).set_index('dt_idx')
            p = pd.read_csv(f'{self.filepath}te{i}.csv')
            p.drop(columns='Unnamed: 0', inplace=True)
            p['datetime'] = pd.to_datetime(p['datetime'])
            te[i] = p.rename(columns={'datetime':'dt_idx'}).set_index('dt_idx')
            
        for k in tr.keys():
            oh[k] = pd.concat([tr[k],te[k]])
        
        return oh 

    def read_d1namo(self) -> dict:
        dic = {}
        for id in range(2,10):
            d = pd.read_csv(f'{self.filepath}00{id}_cgm').rename(columns={'dt':'dt_idx'})
            dic[id] = pd.DataFrame(d.set_index(pd.to_datetime(d['dt_idx']))) # uses both SMBG and CGM
        return dic

    def _get_non_meal_data(self, d:list) -> pd.DataFrame:
            """
            :param d: list containing all insert of a user
            :return: dict containing sport correction index, glucose measure, bolus taken by user,
            bolus suggested by program, timestamp of record isert for each subject.
            """
            meal_rows = []
            for inserimento in d:
                sci_provided = inserimento['sport_correction_index']['provided']
                sci = inserimento['sport_correction_index'][sci_provided]
                gpm_provided = inserimento['glycemia_pre_meal']['provided']
                gpm = inserimento['glycemia_pre_meal'][gpm_provided]
                uu = inserimento['user_units']
                su_provided = inserimento['system_units']['provided']
                su = inserimento['system_units'][su_provided]
                tms = inserimento['timestamp']
                meal_rows.append([sci, gpm, uu, su, tms])
                
            df = pd.DataFrame(meal_rows, columns=['sci', 'gpm', 'uu', 'su', 'tms'])
            df['tms'] = pd.to_datetime(df['tms'], unit='s')
            return df.rename(columns={'tms':'dt_idx'}).set_index('dt_idx')

    def read_dally(self) -> dict:
        dic = {}
        for i in range(1,11):
            jname = f'{self.filepath}utente ({i})'
            jdata = []
            with open(jname) as f:
                for line in f:
                    jdata.append(json.loads(line))
            data = jdata[0]['diary']
            dic[i] = self._get_non_meal_data(d = data) # compatibile with new data
            
        return dic
    

    def read_data(self):
        if self.name == 'ohio':
            return self.read_ohio()
        elif self.name == 'd1namo':
            return self.read_d1namo()
        elif self.name == 'dally':
            return self.read_dally()


# tests
if __name__ == '__main__':
    ohio = DataReader(name = 'ohio', filepath='/Users/tommasobassignana/Desktop/all_algos/DATA_LOADER/ohio_data/').read_data()
    #print(ohio)
    d1n = DataReader(name = 'd1namo', filepath='/Users/tommasobassignana/Desktop/all_algos/DATA_LOADER/d1namo/diabetes/CGM/').read_data()
    #print(d1n)
    dally = DataReader(name = 'dally', filepath='/Users/tommasobassignana/Desktop/all_algos/lightmed_db/dati_utenti_reali/').read_data()
    #print(dally)

    for i in list(ohio.keys()) + list(d1n.keys()) + list(dally.keys()):
        if type(i) is not int: 
            print(type(i))
            print('wrong key datatype')


    for i in list(ohio.values()) + list(d1n.values()) + list(dally.values()):
        if type(i.index) is not pd.core.indexes.datetimes.DatetimeIndex:
            print('not the right index format')
        #if 'dt_idx' not in i.columns:
        #    print('indice con il nome sbagliato')
        if i.index.name != 'dt_idx':
            print('wrong idx name')

    print('data loader tests passed')

