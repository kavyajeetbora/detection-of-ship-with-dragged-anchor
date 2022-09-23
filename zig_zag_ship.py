import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import more_itertools as mit

def find_peaks(ship_ais_data):
    '''
    Given a ship ais data parameter, detects the crest and trough points and returns it
    
    INPUT: Series of a parameter like Heading/COG in ais data of a ship
    
    RETURN: dataframe with tagged crest and trough points 
    '''
    
    ## 1. Detect inflexion points of the given time series
    z = ship_ais_data.reset_index(drop=True).copy()
    z['before'] = z["Heading"].shift(1)
    z['after'] = z["Heading"].shift(-1)

    z["crest"] = (z["Heading"] >= z["after"]) & (z["Heading"] > z["before"]) 
    z["trough"] = (z["Heading"] <= z["after"]) & (z["Heading"] < z["before"])

    ## 2. Remove intermediate peaks 
    z_peaks = z.loc[(z["crest"]) | z["trough"]].copy()

    z_peaks["crest_1"] = z_peaks['trough'].shift(-1, fill_value=False)
    z_peaks["C"] = (z_peaks["crest_1"]) & (z_peaks["crest"])

    z_peaks['trough_1'] = z_peaks['crest'].shift(-1, fill_value=False)
    z_peaks["T"] = (z_peaks["trough_1"]) & (z_peaks["trough"])

    # 3. Filter crest or trough only
    z_peaks = z_peaks.loc[(z_peaks['C']) | (z_peaks["T"])]
    y = z[["# Timestamp", "Heading"]].join(z_peaks[["C","T"]], how="left")
    y[["C", "T"]] = y[["C","T"]].fillna(value=False)
    
    return y

def plot_peaks(df_peaks):    
    
    '''
    Plots the Heading/COG time-series with peaks highlighted 
    '''
    
    fig = go.Figure()

    crest = df_peaks[df_peaks["C"]]
    trough = df_peaks[df_peaks["T"]]

    fig.add_trace(go.Scatter(
        x = df_peaks["# Timestamp"],
        y = df_peaks["Heading"]
    ))

    fig.add_trace(go.Scatter(
        x = crest["# Timestamp"],
        y = crest["Heading"],
        mode = "markers",
        name = "crest"
    ))

    fig.add_trace(go.Scatter(
        x = trough["# Timestamp"],
        y = trough["Heading"],
        mode = "markers",
        name = "trough"
    ))
    
    return fig

def detect_zigzag_motion(ship_ais_data, num_wave_points = 2):
    
    '''
    Function for detecting the zig zag motion of a given ship ais data
    '''
    ## 1. Find peak points of the time series 
    xp = find_peaks(ship_ais_data)
    df = xp[xp["C"]+xp["T"]].copy()
    df = df[::-1].reset_index()
    
    ## 2. Detect the sinusoidal motion in the timeseries
    df["dH"] = df["Heading"].diff(-1).abs()
    df["dH2"] = (df["Heading"].diff(-1) + df["Heading"].shift(-1).diff(-1)).abs()
    df["di"] = (df["index"].diff(-1).abs() - df["index"].shift(-1).diff(-1).abs()).abs()
    ## Some parameter to be given inorder to detect the sinusoidal motion:
    df["wave"] = (df["dH2"]<=5) & (df["dH"]>=3) & (df["di"]<=10) 
    
    ## 3. Group and Filter out non-significant waves based on number of wave points:
    waves_list = {}
    wave_points = 0
    for grp,dfx in df.groupby("wave"):
        for i, c_grp in enumerate(mit.consecutive_groups(dfx.index)):
            c_grp_index = list(c_grp)  ## index of concecutive values for each group
            if (grp==1) and (len(c_grp_index)>=num_wave_points):
                name = "W"+str(i)
                start, end = df.iloc[max(c_grp_index)]['index'], df.iloc[min(c_grp_index)]['index']
                waves_list[name] = (start, end)
                wave_points += end-start
    
    wave_score = wave_points/ship_ais_data.shape[0]
    return waves_list, wave_score


def wave_detection_plot(ais_data, waves_list, score):

    '''
    Plots the time series profile of the Heading and also reports the zigzag motion probability
    '''

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ais_data.index,
        y=ais_data["Heading"],
        name="AIS"
    ))

    for k,v in waves_list.items():
        
        w = ais_data.iloc[v[0]:v[1]]
        
        fig.add_trace(go.Scatter(
            x = w.index,
            y = w["Heading"],
            name=k,
            mode="lines",
            marker = dict(color="red")
        ))
    
    result = (": Detected" if len(waves_list.keys())>0 else ": Not Detected") + f" | Score: {score}"
    
    fig.update_layout(title=f"ZigZag Motion{result}")

    return fig


def ship_zigzag_analysis_report(ship_ais_data):
    '''
    Generates Ship's zigzag motion detection analysis report
    '''
    x = ship_ais_data[["# Timestamp","Heading"]].reset_index(drop=True)
    w,s = detect_zigzag_motion(x)
    return wave_detection_plot(x,w,s)

