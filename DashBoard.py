import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
    

with st.sidebar:
    st.header("Upload Your Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="xlsx")
    
    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        df = pd.read_excel(uploaded_file)

    else:
        st.info("Please upload a CSV file to get started.")
        st.stop()

    df.dropna(inplace=True)
    df.columns = df.columns.str.strip()
    df.drop_duplicates()

    st.title("Slicers")

    # Slicer_Of_Year = st.multiselect("Slicer Of Year", options=df['Year'].unique())
    # if not Slicer_Of_Year:
    #     Slicer_Of_Year = df['Year'].unique()
    # df = df[df['Year'].isin(Slicer_Of_Year)]

    # Slicer_Of_Country = st.multiselect("Slicer Of Country", options=df['Country'].unique())
    # if not Slicer_Of_Country:
    #     Slicer_Of_Country = df['Country'].unique()
    # df = df[df['Country'].isin(Slicer_Of_Country)]

    # Slicer_Of_Product = st.multiselect("Slicer Of Product", options=df['Product'].unique())
    # if not Slicer_Of_Product:
    #     Slicer_Of_Product = df['Product'].unique()
    # df = df[df['Product'].isin(Slicer_Of_Product)]
    
    st.subheader('Country')
    cols = st.columns(2)
    selected_countries = []
    for i, country in enumerate(df["Country"].unique()):
        col = cols[i%2]
        with col:
            if st.checkbox(country, value=True):
                selected_countries.append(country)

    df = df[df["Country"].isin(selected_countries)]

    st.subheader('Year')
    cols = st.columns(2)
    selected_Years = []
    for i, Year in enumerate(df["Year"].unique()):
        col = cols[i%2]
        with col:
            if st.checkbox(str(Year), value=True):
                selected_Years.append(Year)

    df = df[df["Year"].isin(selected_Years)]
    
    st.subheader('Product')
    cols = st.columns(2)
    selected_Products = []
    for i, Product in enumerate(df["Product"].unique()):
        col = cols[i%2]
        with col:
            if st.checkbox(str(Product), value=True):
                selected_Products.append(Product)

    df = df[df["Product"].isin(selected_Products)]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Sales", (df['Sales'].sum() / 1e6).round(1).astype(str) + "M")
with col2:
    st.metric("Units Sold", (df['Units Sold'].sum() / 1e3).round(1).astype(str) + "K")
with col3:
    st.metric("Profit", (df['Profit'].sum() / 1e6).round(1).astype(str) + "M")
with col4:
    st.metric("COGS", (df['COGS'].sum() / 1e6).round(1).astype(str) + "M")

col1, col2 = st.columns([2, 1])

with col1:
    df_grouped = df.groupby(["Segment", "Year"], as_index=False)["Sales"].sum()


    fig = go.Figure()

    years = df_grouped["Year"].unique()
    for year in years:
        df_year = df_grouped[df_grouped["Year"] == year]
        fig.add_trace(go.Bar(
            x=df_year["Sales"],
            y=df_year["Segment"],
            name=str(year),
            orientation='h',
            text=(df_year["Sales"] / 1e6).round(1).astype(str) + "M",
            textposition='outside'
        ))

    fig.update_layout(
        barmode='group',
        title="Sales by Segment",
        yaxis={'categoryorder':'total ascending'},
        xaxis=dict(showticklabels=False),
        height=250,
        uniformtext_minsize=14,
        # uniformtext_mode='hide',
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02
        )
    )
    st.plotly_chart(fig, use_container_width=True)



with col2:
    df_grouped = df.groupby('Product', as_index=False)['Sales'].sum()

    pg = px.pie(df_grouped, values='Sales', names='Product', title="Sales by Product", height=250)
    pg.update_layout(uniformtext_minsize=14,
        uniformtext_mode='hide',
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02
        )
    )
    st.plotly_chart(pg, use_container_width=True)

col1, col2, col3 = st.columns(3)

with col1:
    df_grouped = df.groupby("Date", as_index=False)["Sales"].sum()

    pg = px.line(df_grouped, x='Date', y='Sales', title="Trend Line Of Sales", height=360)
    pg.update_layout(uniformtext_minsize=14,
        uniformtext_mode='hide',
        margin=dict(l=20, r=20, t=21, b=170),
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02
        )
    )
    st.plotly_chart(pg, use_container_width=True)

with col2:
    pg = px.treemap(df, path=['Country'], values='Sales', title='Sales by Country', height=250)
    pg.update_layout(uniformtext_minsize=14,
        margin=dict(l=20, r=20, t=21, b=13),
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1
        )
    )
    pg.update_traces(texttemplate="%{label}<br>Sales: %{value}")

    st.plotly_chart(pg, use_container_width=True)

with col3:
    df_grouped = df.groupby(['Country', 'Segment'], as_index=False)['Sales'].sum()

    pg = px.bar(df_grouped, x='Country', y='Sales', color='Segment', barmode='group', title="Sales by Country and Segment", text='Sales')
    pg.update_layout(
        uniformtext_minsize=7,   
        margin=dict(l=0, r=0, t=50, b=170),
        legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.02
        ),
        yaxis=dict(showticklabels=False),
        yaxis_title=None
    )

    pg.update_traces(
    text=(df_year["Sales"] / 1e6).round(1).astype(str) + "M",
    textposition="outside"
    )

    st.plotly_chart(pg, use_container_width=True)