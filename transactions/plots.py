# transactions/plots.py

import plotly.express as px

def create_transaction_line_plot(df):
    fig = px.line(
        df,
        x='date',
        y='total_price_cdf',
        color='type',
        markers=True,
        title='Transaction Values Over Time',
        labels={'total_price_cdf': 'Total Price (CDF)'}
    )
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Total Price (CDF)',
        title={'x': 0.5},  # Centrer le titre
        margin={'l': 40, 'r': 40, 't': 40, 'b': 40},
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig

def create_transaction_bar_plot(df):
    fig = px.bar(
        df,
        x='product',
        y='total_price_cdf',
        color='type',
        title='Total Transaction Value by Product',
        labels={'total_price_cdf': 'Total Price (CDF)'}
    )
    fig.update_layout(
        xaxis_title='Product',
        yaxis_title='Total Price (CDF)',
        title={'x': 0.5},  # Centrer le titre
        margin={'l': 40, 'r': 40, 't': 40, 'b': 40},
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig

def create_transaction_pie_chart(df):
    fig = px.pie(
        df,
        names='type',
        values='total_price_cdf',
        title='Transaction Type Distribution',
        labels={'total_price_cdf': 'Total Price (CDF)'}
    )
    fig.update_layout(
        title={'x': 0.5},  # Centrer le titre
        margin={'l': 40, 'r': 40, 't': 40, 'b': 40},
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig

def create_transaction_scatter_plot(df):
    fig = px.scatter(
        df,
        x='quantity',
        y='total_price_cdf',
        color='type',
        size='total_price_cdf',
        title='Quantity vs Total Price',
        labels={'total_price_cdf': 'Total Price (CDF)', 'quantity': 'Quantity'}
    )
    fig.update_layout(
        xaxis_title='Quantity',
        yaxis_title='Total Price (CDF)',
        title={'x': 0.5},  # Centrer le titre
        margin={'l': 40, 'r': 40, 't': 40, 'b': 40},
        paper_bgcolor='white',
        plot_bgcolor='white'
    )
    return fig
