
import pandas as pd
import numpy as np


# takes a df containing rows of games (only need V, H, Result)
# returns a dict of {team: SRS}
def CalcSRS(df):
    raw = {}
    for t in df.V.unique():
        raw[t] = 0.0  # V diff - H diff
        raw[t] = df.groupby("V").sum().at[t, "Result"] - df.groupby("H").sum().at[t, "Result"]
        raw[t] = raw[t] / (len(df.loc[df.V==t]) + len(df.loc[df.H==t]))
    
    raw = pd.Series(raw).sort_index()
    
    print("Raw Point Diff:")
    print(raw)
    print()
    
    print("Raw Schedule Matrix:")
    m = np.zeros((6, 6))
    for i in range(6):
        m[i, i] = -6.0
    
    for i, r in df.iterrows():
        v_i = raw.index.get_loc(r["V"])
        h_i = raw.index.get_loc(r["H"])
        
        m[v_i, h_i] += 1.0
        m[h_i, v_i] += 1.0
    
    m = m * (1/6)
    print(m)
