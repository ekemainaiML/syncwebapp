# Load libraries
#!pip3 install scikit-learn
import streamlit as st
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

pd.options.display.max_columns = None
pd.options.display.max_rows = 10

# Load Data Set
@st.cache_data
def load_data():
    dataset = pd.read_csv("synchronous_machine.csv", delimiter=";")
    return dataset

dataset = load_data()

# Remove "commas" from dataset
@st.cache_data
def clean_and_change_to_numeric(data: pd.DataFrame):
    c = 0
    for col in data.columns:
        for j in range(len(data[col])):
            newstr = data.iloc[j,c].replace(",", ".")
            data.iloc[j,c] = newstr
        c += 1
    df = data.astype(np.float64)
    print(df.dtypes)
    return df

data = clean_and_change_to_numeric(dataset)

@st.cache_data
def view_scatterplot(data: pd.DataFrame, nrows, ncols, titles):
    nn = 0
    n = data.shape
    cols = data.columns.tolist()
    fig1, ax1 = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15,10))
    fig1.suptitle(titles, fontsize=10)
    for i in range(0,nrows):
        for j in range(ncols): 
            sns.set_style("darkgrid")
            sns.set_context("notebook", font_scale = 5, rc={"grid.linewidth": 1})
            sns.scatterplot(x=data.index, y=data[cols[nn]], ax=ax1[i,j])
        nn += 1
        if i >= len(data):
            break
    
    #plt.show
    return fig1


@st.cache_data
def view_heatmap(data):
    fig = px.imshow(data, text_auto=True, aspect="auto")

    tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
    with tab1:
        st.plotly_chart(fig, theme="streamlit")
    with tab2:
        st.plotly_chart(fig, theme=None)
    return fig


def show_explore_page():
    st.title("Explore Synchronous motor datasets")
    st.markdown(""" ####
        Synchronous motors (SMs) are AC motors with constant speed.A SM dataset is obtained from
        a real experimental set. The task is to create the strong models to estimate the excitation
        current of SM. Source: Ramazan BAYINDIR (bayindir '@' gazi.edu.tr);Hamdi Tolga KAHRAMAN
        (holgakahraman '@' ktu.edu.tr); Data Set Information: Synchronous machine data were obtained 
        in real time from the experimental operating environment. Attribute Information: Iy 
        (Load Current) PF (Power factor) e (Power factor error) dIf (Changing of excitation 
        current of synchronous machine) If (Excitation current of synchronous machine) Relevant 
        Papers: Kahraman, H. T. (2014). Metaheuristic linear modeling technique for estimating the 
        excitation current of a synchronous motor.Â Turkish Journal of Electrical Engineering & 
        Computer Sciences,Â 22(6), 1637-1652. Kahraman, H. T., Bayindir, R, & Sagiroglu, S. (2012).
        A new approach to predict the excitation current and parameter weightings of synchronous 
        machines based on genetic algorithm-based k-NN estimator.Â Energy Conversion and Management,
        Â 64, 129-138.
        """)
    st.markdown("**♟ General Statistics ♟**")
    st.write(data)
    st.write(""" ### 
        This is the scatter plot to show data distribution
    """)
    # Call method
    fig1 = view_scatterplot(pd.DataFrame(data.iloc[:,0:3], columns=data.columns), 2, 2, "Data Enumeration")
    st.pyplot(fig1)

    st.write(""" ### 
        Pearson Features Correlation
    """)
    # Call heatmap plot
    data_corr1 = data.corr('pearson')
    data_corr2 = data.corr('spearman')
    data_corr3 = data.corr('kendall')

    view_heatmap(data_corr1)
    st.write(""" ### 
        Spearman Features Correlation
    """)
    view_heatmap(data_corr2)
    st.write(""" ### 
        Kendall Features Correlation"
    """)
    view_heatmap(data_corr3)

