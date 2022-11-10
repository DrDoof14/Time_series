import pandas as pd
from .data_loader import DataReader


class GlucoReader(DataReader):
    def __init__(self, name, filepath, format):
        super().__init__(name, filepath)
        self.format = format
        
        if format not in ['cgm', 'smbg']:
            raise ValueError('only cgm and smbg data supported') 

    def get_ohio_cgm(self) -> dict:
        i = self.read_data()
        o = {}
        for k in i.keys():
            o[k] = pd.DataFrame(i[k]['glucose'].astype(float))
            o[k].rename(columns={'glucose':'cgm'}, inplace=True)
        return o
    
    def get_ohio_smbg(self) -> dict:
        i = self.read_data()
        o = {}
        for k in i.keys():
            o[k] = pd.DataFrame(i[k]['finger_stick'].astype(float))
            o[k].rename(columns={'finger_stick':'smbg'}, inplace=True)
        return o
    
    def get_dally_cgm(self):
        raise NotImplementedError('dally dosen t has CGM for now')
    
    def get_dally_smbg(self) -> dict:
        i = self.read_data()
        o = {}
        for k in i.keys():
            o[k] = pd.DataFrame(i[k]['gpm'].astype(float))
            o[k].rename(columns={'gpm':'smbg'}, inplace=True)
        return o
    
    def get_d1namo_cgm(self) -> dict:
        i = self.read_data()
        o = {}
        for k in i.keys():
            o[k] = pd.DataFrame(i[k].loc[i[k]['type'] == 'cgm','glucose'].astype(float))
            o[k].rename(columns={'glucose':'cgm'}, inplace=True)
        return o
    
    def get_d1namo_smbg(self) -> dict:
        i = self.read_data()
        o = {}
        for k in i.keys():
            o[k] = pd.DataFrame(i[k].loc[i[k]['type'] == 'manual','glucose'].astype(float))
            o[k].rename(columns={'glucose':'smbg'}, inplace=True)
        return o
    
    def get_glucose(self) -> dict:
        if self.name == 'ohio' and self.format == 'cgm':
            return self.get_ohio_cgm()
        elif self.name == 'ohio' and self.format == 'smbg':
            return self.get_ohio_smbg()
        elif self.name == 'dally' and self.format == 'smbg':
            return self.get_dally_smbg()
        elif self.name == 'dally' and self.format == 'cgm':
            return self.get_dally_cgm()
        elif self.name == 'd1namo' and self.format == 'smbg':
            return self.get_d1namo_smbg()
        elif self.name == 'd1namo' and self.format == 'cgm':
            return self.get_d1namo_cgm()
        else:
            return 'check get_glucose() in GlucoReader class'


# tests
if __name__ == '__main__':
    ohio_cgm = GlucoReader(name = 'ohio',
                        filepath='/Users/tommasobassignana/Desktop/all_algos/T6_hypo_detection/ohio_data/',
                        format = 'cgm').get_glucose()
    
    print(ohio_cgm[1].columns)
    print(ohio_cgm[1].index)
    
    ohio_smbg = GlucoReader(name = 'ohio',
                        filepath='/Users/tommasobassignana/Desktop/all_algos/T6_hypo_detection/ohio_data/',
                        format = 'smbg').get_glucose()
    
    print(ohio_cgm[1].columns)
    print(ohio_cgm[1].index)
    
    try:
        dally_cgm = GlucoReader(name = 'dally',
                            filepath='/Users/tommasobassignana/Desktop/all_algos/lightmed_db/dati_utenti_reali/',
                            format = 'cgm').get_glucose()
    except NotImplementedError as e:
        print(f'{e} catched as wanted')
        pass

    dally_smbg = GlucoReader(name = 'dally',
                        filepath='/Users/tommasobassignana/Desktop/all_algos/lightmed_db/dati_utenti_reali/',
                        format = 'smbg').get_glucose()
    
    print(dally_smbg[1].columns)
    print(dally_smbg[1].index)
    
    print('-'*100)    
    d1n_cgm = GlucoReader(name = 'd1namo',
                        filepath='/Users/tommasobassignana/Desktop/all_algos/DATA_LOADER/d1namo/diabetes/CGM/',
                        format = 'cgm').get_glucose()
    
    print(d1n_cgm[2].columns)
    print(d1n_cgm[2].index)
    
    d1n_smbg = GlucoReader(name = 'd1namo',
                        filepath='/Users/tommasobassignana/Desktop/all_algos/DATA_LOADER/d1namo/diabetes/CGM/',
                        format = 'smbg').get_glucose()
    
    print(d1n_smbg[2].columns)
    print(d1n_smbg[2].index)

    print('gluco loader test passed')

