import plotly.graph_objs as go
import pandas as pd
import numpy as np




def list_to_options(searchSelection):
    options = []
    for option in searchSelection:
        options.append({'label': option, 'value': option})
    return options


# Plotta selected punktana
def df_to_area_plot_dict(plottable_df,label):
    print(plottable_df.columns)
    time_fixed_df = plottable_df
    time_fixed_df.index = pd.DatetimeIndex(time_fixed_df.date)
    # time_fixed_df.to_csv('tmp_for_analysis.csv')
    tmp_df = time_fixed_df.groupby([pd.Grouper(freq='2m'),'organization']).count().id.sort_values(ascending=False).unstack(fill_value=0).stack()
    x_axis = tmp_df.index.get_level_values(0).unique()
    print(x_axis)
    groups = tmp_df.index.get_level_values(1).unique()
    traces = []

    other = pd.Series(0,index=x_axis)
    group_total = []
    # Til að takmarka aðeins fjölda 
    for group in groups:
        tmp_total = tmp_df[:,group].sum()
        group_total.append(tmp_total)
        if tmp_total == 1:
            other = other+tmp_df[:,group]
    group_sort = np.argsort(group_total)

    # Bæta við öllum others á listann
    traces.append(
        dict(
            x=x_axis,
            y=other,
            mode='lines',
            name='%s (%s)'%('others',other.sum()),
            stackgroup='one',
            line=dict(
                width=1
            ),
        )
    )

    for group in groups[group_sort]:
        tmp_total = tmp_df[:,group].sum()
        if tmp_total > 1:
            traces.append(
                        dict(
                            x=x_axis,
                            y=tmp_df[:,group],
                            mode='lines',
                            name='%s (%s)'%(group,tmp_total),
                            stackgroup='one',
                            line=dict(
                                width=1
                            ),
                        )
                    )
        
    layout = dict(font=dict(family='Aleo'))
    print(traces)
    return {'data': traces, 'layout': layout}

def df_to_plot_dict(plotable_df,label):
    tmp_data = []
    print('columns:',plotable_df.columns)
    for category in label.unique():
        tmp_x = plotable_df.loc[label == category,'x']
        tmp_y = plotable_df.loc[label == category,'y']
        tmp_text = plotable_df.loc[label == category,'title']
        tmp_abstr = plotable_df.loc[label == category,'abstract']
        tmp_dict = go.Scatter(
            x=tmp_x,
            y=tmp_y,
            hovertext=tmp_text,
            customdata=plotable_df.loc[label == category].id,
            name = category,
            mode='markers'
        )
        tmp_data.append(tmp_dict)

    returnable_dict = dict(
        data=tmp_data,
        layout=dict(
            title='t-SNE',
            showlegend=True,
            clickmode = 'event+select',
            legend=dict(
                x=0,
                y=1.0
            ),
            margin=dict(l=40, r=0, t=40, b=30)
        )
    )
    return returnable_dict  