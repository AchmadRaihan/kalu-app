import streamlit as st
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go


#---------------------------------#
# Page layout
# Page expands to full width
st.set_page_config(page_title='Water Level App',
    layout='wide')


#---------------------------------#
# Build model
def build_model(df):
	m = Prophet().fit(df)
	future = m.make_future_dataframe(periods=period, freq='h')
	forecast = m.predict(future)
    # Plot forecast
	st.write(f'Forecast plot for {n_days} days')
	fig1 = plot_plotly(m, forecast)
	st.plotly_chart(fig1)

def plot_raw_data(df):
    df['ds'] = pd.to_datetime(df['ds'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['ds'], y=df['y'], name="stock_open"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


#---------------------------------#
# Sidebar - Collects user input features into dataframe
with st.sidebar.header('Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
	[Example CSV input file](https://github.com/AchmadRaihan/kalu-data/blob/main/c.csv)
	""")
# Sidebar - Days of prediction
n_days = st.sidebar.slider('Days of prediction:', 0, 7)
period = n_days * 24


#---------------------------------#
# Main panel
# Displays the dataset
st.write("""
# Simple Water Level Prediction App
This app predicts the **Water Level**.
""")
st.subheader('Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('**Glimpse of dataset**')
    plot_raw_data(df)
    build_model(df)
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
	df = pd.read_csv('kalu.csv')
	build_model(df)
	plot_raw_data(df)
        # Diabetes dataset
        #diabetes = load_diabetes()
        #X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
        #Y = pd.Series(diabetes.target, name='response')
        #df = pd.concat( [X,Y], axis=1 )

        #st.markdown('The Diabetes dataset is used as the example.')
        #st.write(df.head(5))

        # Boston housing dataset
        #boston = load_boston()
        #X = pd.DataFrame(boston.data, columns=boston.feature_names)
        #Y = pd.Series(boston.target, name='response')
        #df = pd.read_csv('kalu.csv')

        #st.markdown('The Boston housing dataset is used as the example.')
        #st.write(df.head(5))

        #build_model(df)
