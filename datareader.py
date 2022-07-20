import pandas as pd


def read(fname):
    start = pd.to_datetime(fname.split(".")[0], format="%y%m%d_%H%M%S")
    df = pd.read_csv(fname)
    df['Time'] = start + pd.to_timedelta(df['Time'], unit='s')
    df.set_index('Time', inplace=True)
    df =  df.resample('1s').mean()
    return df

df = read("220719_122000.csv")