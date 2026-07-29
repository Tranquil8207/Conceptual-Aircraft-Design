import plotly.graph_objects as go


def plot_size_matching(output):
    curves = output['curves']
    WS_sweep = output['WS_sweep']
    WS_stall = output['WS_max_stall']
    TW_envelope = output['TW_envelope']
    WL_opt = output['WL_Final']
    TW_opt = output['TW_opt']

    fig = go.Figure()
    for name, tw in curves.items():
        fig.add_trace(go.Scatter(x=WS_sweep, y=tw, mode='lines', name=name))

    fig.add_trace(go.Scatter(
        x=WS_sweep, y=TW_envelope, mode='lines', name='Envelope',
        line=dict(color='black', width=3),
    ))
    fig.add_vline(
        x=WS_stall, line_dash='dash', line_color='black',
        annotation_text='stall limit', annotation_position='top',
    )
    fig.add_trace(go.Scatter(
        x=[WL_opt], y=[TW_opt], mode='markers', name='Design',
        marker=dict(color='black', size=10),
    ))
    fig.update_layout(
        xaxis_title='Wing Loading W/S',
        yaxis_title='Thrust-to-weight ratio T/W',
        showlegend=True,
    )
    fig.write_html('constraint_diagram.html')
    return fig
