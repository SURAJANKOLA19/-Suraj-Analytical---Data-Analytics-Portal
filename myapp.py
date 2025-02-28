import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Suraj Analytical"
)
st.title(":red[Data] Analytics Portal")
st.header(":gray[Explore data with ease]",divider="rainbow")

file=st.file_uploader('Drop your CSV file here',type=['csv,xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)
   
    st.dataframe(data)
    st.info("File is successfully uploaded and displayed")


    st.subheader(":rainbow[Basic Info of the dataset]",divider="rainbow")
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top and Bottom rows',"Data Type","Columns"])

    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset')
        st.subheader(":gray[Statistical summary of the dataset]")

        st.dataframe(data.describe())

    with tab2:
        st.subheader(":gray[Top rows of the dataset]")
        toprows=st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))

        st.subheader(":gray[Bottoms rows of the dataset]")
        Bottomrows=st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(Bottomrows))

    with tab3:
        st.subheader(':gray[Data type of the dataset]')
        st.dataframe(data.dtypes)

    with tab4:
        st.subheader('Column Names in Dataset')
        st.dataframe(list(data.columns))

    st.subheader(":rainbow[Column Values Count]",divider="rainbow")
    with st.expander('Value count'):
        col1,col2=st.columns(2)

        with col1:
            column=st.selectbox("Choose column name",options=list(data.columns))
        
        with col2:
            toprows =st.number_input('Top rows',min_value=1,step=1)

        count=st.button('Count')

        if (count==True):
            result=data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)

            st.subheader("Vizualiation",divider="rainbow")

            fig =px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)

            fig=px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)

            fig=px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)


    st.subheader(":rainbow[Groupby:Simplify Your Data Analysis]",divider="rainbow")
    st.write('The groupby  lets you summarize the data by specific categories and groups') 
    with st.expander('Group By your columns'):
        col1,col2,col3 = st.columns(3) 
        with col1:
            group_cols= st.multiselect('Choose your column to groupby',options = list(data.columns))     
        with col2:
            operations_col=st.selectbox('Choose column for operations',options = list(data.columns))
        with col3:
            operation=st.selectbox('Choose operations',options=['sum','max','min','mean','median','count'])

        if (group_cols):
            result=data.groupby(group_cols).agg(
                newcol =(operations_col,operation)
            ).reset_index() 

            st.dataframe(result)   

            st.subheader(":rainbow[Data Vizualization]",divider="rainbow")
            graphs = st.selectbox('Choose your graphs ', options=['line','bar','scatter','pie','sunburst'])
            if (graphs == 'line'):
                x_axis =st.selectbox("Choose X axis",options=list(result.columns))
                y_axis =st.selectbox("Choose Y axis",options=list(result.columns))
                color =st.selectbox('Color Information ',options=[None]+list(result.columns))
                fig = px.line(data_frame=result,x=x_axis,y=y_axis,color=color,template='plotly_white',markers='o')

                st.plotly_chart(fig)
            
            elif (graphs == 'bar'):
                x_axis =st.selectbox("Choose X axis",options=list(result.columns))
                y_axis =st.selectbox("Choose Y axis",options=list(result.columns))
                color =st.selectbox('Color Information ',options=[None]+list(result.columns))
                facet_col = st.selectbox('Column Informations',options=[None]+list(result.columns))
                fig = px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group',template='plotly_white')

                st.plotly_chart(fig)

            elif(graphs=='scatter'):
                x_axis =st.selectbox("Choose X axis",options=list(result.columns))
                y_axis =st.selectbox("Choose Y axis",options=list(result.columns))
                color =st.selectbox('Color Information ',options=[None]+list(result.columns))
                size=st.selectbox('Size columns',options=[None]+list(result.columns))
                if size is not None and not pd.api.types.is_numeric_dtype(result[size]):
                    st.warning(f"⚠️ The selected column '{size}' is not numeric. Please choose a numeric column for size.")
                    size = None  # Reset to prevent errors
                fig = px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)

                st.plotly_chart(fig)
            elif(graphs=='pie'):
                values =st.selectbox('Choose Numerical Values ',options=list(result.columns))
                names =st.selectbox('Choose labels ',options=list(result.columns))
                fig = px.pie(data_frame=result,values=values,names=names)

                st.plotly_chart(fig)
            elif(graphs=='sunburst'):
                path=st.multiselect('Choose Your Path ',options=list(result.columns))
                fig=px.sunburst(data_frame=result,path=path,values='newcol')

                st.plotly_chart(fig)