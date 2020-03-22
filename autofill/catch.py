import pandas as pd

def read_csv(location,*argv:None):
    file_reader = pd.read_csv(str(location))
    return file_reader
