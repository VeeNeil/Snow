# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

pd_df = my_dataframe.to_pandas()
# st.dataframe(pd_df)


ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

name= st.text_input('Name on Smoothie')



if ingredients_list:
    ingredients_string=''
    for x in ingredients_list:
        ingredients_string += x + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == x, 'SEARCH_ON'].iloc[0]
        # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(x + 'Nutrition Information')
        fruit = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=fruit.json(), use_container_width=True)
    
    insert = """insert into smoothies.public.orders(ingredients, name_on_order)
            values('"""+ingredients_string+""", '"""+ name + """')"""
    submit = st.button('Submit Order')
    
   
    if submit:
        session.sql(insert).collect()
        
        st.success('Your Smoothie is ordered!'+ name, icon="✅")
    
