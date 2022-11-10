import streamlit as st
import pandas as pd
from scipy.signal import find_peaks
from DATA_LOADER.data_loader import DataReader
import plotly.graph_objects as go

st.title('what a cool page!')

st.checkbox('baseline method')
st.checkbox('method 1')
st.checkbox('method 2')


# Load data for one patient
# change path
ohio = DataReader(name='ohio', filepath='DATA_LOADER/ohio_data/').read_data()
df = ohio[2].copy(True)
df = df.resample('5min').mean()

# for this analysis i keep only the glucose values
df = pd.DataFrame(df[['glucose']])

# defining target thresholds
lb = 70
ub = 180
#start_day='2021-09-16'
#end_day='2021-09-17'

# defining df
#time_mask = (df.index >= start_day) & (df.index <= end_day)
#df_plot = df.loc[time_mask]

df_plot = df

# main plots 
fig1 = go.Figure()
# add stuff to the plot
x1 = df_plot.index
fig1.add_trace(go.Scatter(x=x1, y=df_plot.glucose))
fig1.add_trace(go.Scatter(x=x1, y=[lb]*len(x1)))
fig1.add_trace(go.Scatter(x=x1, y=[ub]*len(x1)))

fig2 = go.Figure()
x2 = df_plot.reset_index().index
fig2.add_trace(go.Scatter(x=x2, y=df_plot.glucose))
fig2.add_trace(go.Scatter(x=x2, y=[lb]*len(x2)))
fig2.add_trace(go.Scatter(x=x2, y=[ub]*len(x2)))

# adding peaks and lows to the plot 
df_peaks_low = df_plot.reset_index(drop=True)
high_idxs, _ = find_peaks(df_peaks_low.glucose, height=ub, prominence=1, width=6)
_low_idxs, _ = find_peaks(-df_peaks_low.glucose+max(df_peaks_low.glucose.dropna()), prominence=1, width=6)
low_idxs = []
for low_value, low_idx in zip(df_peaks_low.iloc[_low_idxs].glucose, _low_idxs):
    if low_value <= lb:
        low_idxs.append(low_idx)

fig3 = go.Figure()
x3 = df_plot.reset_index().index
fig3.add_trace(go.Scatter(x=x3, y=df_plot.glucose))
fig3.add_trace(go.Scatter(x=x3, y=[lb]*len(x3)))
fig3.add_trace(go.Scatter(x=x3, y=[ub]*len(x3)))

#lows
fig3.add_trace(go.Scatter(
                    x=df_peaks_low.iloc[low_idxs].index, 
                    y=df_peaks_low.iloc[low_idxs].glucose,
                    mode = 'markers',
                    marker =dict(
                        color = 'red',
                        size = 4,
                        line=dict(
                            color='purple',
                            width=2
                        )
                    )))

#highs
fig3.add_trace(go.Scatter(
                    x=df_peaks_low.iloc[high_idxs].index, 
                    y=df_peaks_low.iloc[high_idxs].glucose,
                    mode = 'markers',
                    marker =dict(
                        color = 'yellow',
                        size = 4,
                        line=dict(
                            color='purple',
                            width=2
                        )
                    )))

st.plotly_chart(fig3)

# low high summary
l = df_peaks_low.iloc[low_idxs]
h = df_peaks_low.iloc[high_idxs]
l['type'] = 'low'
h['type'] = 'high'
summary_hl = pd.concat([h,l],axis=0).sort_index()
st.dataframe(summary_hl)

