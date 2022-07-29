import json
from scipy import stats
import pandas as pd
from plotting import plot_col, plot_efficiency_dt_i, plot_multiple, plot_stable

def read(fname):
    start = pd.to_datetime(fname.split(".")[0], format="%y%m%d_%H%M%S")
    df = pd.read_csv(fname)
    df['Time'] = start + pd.to_timedelta(df['Time'], unit='s')
    df.set_index('Time', inplace=True)
    df =  df.resample('1min').mean()
    df = df.tz_localize('Europe/Berlin').tz_convert('UTC')
    return df

def save_regresults(linregress):
    linregress_dict = {
        "slope": linregress.slope,
        "intercept": linregress.intercept,
        "slope_stderr":linregress.stderr,
        "intercept_stderr": linregress.intercept_stderr,
        "rvalue": linregress.rvalue,
        "pvalue":linregress.pvalue
        }
    with open("linregress_stats.json", "w") as f:
        json.dump(linregress_dict,f, indent=4)
    
df = read("220719_122000.csv")

df = df.loc['2022-07-19 10:40:00+0000' : '2022-07-19 14:00:00+0000']

df['Tout_Tin'] = df['T_out'] - df['T_in']
df['q_dot'] = 4.2 * df['m_dot'] * df['Tout_Tin']
df['eff'] = df['q_dot']/(df['I_dir'] * 1.15*1.79)

df['Tin_Tamb'] = df['T_in'] - df['T_amb']
df['Tin_Tamb_I'] = df['Tin_Tamb']/df['I_dir']

plot_col(df['m_dot'], ylabel="$\dot m \ (g \cdot s^{-1})$")
plot_col(df['I_dir'], ylabel='$DNI \ (W \cdot m^{-2})$')
# plot_col(df['I_dif'], ylabel='$DHI \ (W \cdot m^{-2})$')
# plot_multiple(df, ['I_dir', 'I_dif'], ylabel='$W \cdot m^{-2}$')
plot_multiple(df, ['T_amb', 'T_in', 'T_out'], ylabel='$ \degree C$')

plot_col(df['Tout_Tin'],  ylabel='$T_{out} - T_{in} \ (\degree C)$')
# plot_col(df['eff'], ylabel="Efficiency")
plot_col(df['q_dot'], ylabel='$\dot Q \ (W)$')

df = df[df['T_in']>80]
stable = df[df['T_in'].diff().rolling(window=10).max() <= 0.5]
# stable = stable.resample('1min').mean()
plot_stable(df, stable)

linregress = stats.linregress(stable["Tin_Tamb_I"], stable["eff"])
save_regresults(linregress)
plot_efficiency_dt_i(stable, linregress)
