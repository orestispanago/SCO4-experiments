import matplotlib.pyplot as plt
import seaborn as sns

params = {'figure.figsize': (9, 6),
          'axes.titlesize': 18,
           # 'axes.titleweight': 'bold',
          'axes.labelsize': 24,
          # 'axes.labelweight': 'bold',
          'xtick.labelsize': 18,
          'ytick.labelsize': 18,
          # 'font.weight' : 'bold',
          'font.size': 18,
          'savefig.dpi': 300.0,
          'savefig.format': 'png',
          'figure.constrained_layout.use': True}
plt.rcParams.update(params)

def plot_col(col, ylabel=''):
    col.plot(style='.')
    plt.ylabel(ylabel)
    plt.xlabel("Time (UTC)")
    plt.grid(which='both')
    plt.savefig(col.name)
    plt.show()

def plot_multiple(df, col_list, ylabel=''):
    for col in col_list:
        df[col].plot(style='.')
    plt.ylabel(ylabel)
    plt.legend()
    plt.xlabel("Time (UTC)")
    plt.grid(which='both')
    plt.show()

def plot_stable(df, stable, col='T_in'):
    df[col].plot()
    stable[col].plot(style='.')
    plt.ylabel('$T_{in} \ (\degree C)$')
    plt.xlabel("Time (UTC)")
    plt.savefig("stable_tin")
    plt.show()

def plot_efficiency_dt_i(df, linregress):
    g = sns.regplot(x=df["Tin_Tamb_I"], 
                    y=df["eff"], 
                    scatter_kws={'s':5},
                    line_kws={'label': "$y={0:.2f}x+{1:.2f}$".\
                              format(linregress.slope, linregress.intercept)})
    g.legend()
    ax = g.axes
    ax.axvline(0, c='black', ls='--', linewidth=0.5)
    ax.axhline(0,  c='black', ls='--', linewidth=0.5)
    ax.set_ylabel('$n$')
    ax.set_xlabel('$\\frac{Tin - Tamb}{I}$')
    ax.set_ylim(-0.05, 1)
    plt.savefig("eff_dt_i")
    plt.show()