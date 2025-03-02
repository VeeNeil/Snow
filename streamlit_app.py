# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

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
    
    insert = """insert into smoothies.public.orders(ingredients)
            values('"""+ingredients_string+""", """+ name + """')"""
    submit = st.button('Submit Order')
    
   
    if submit:
        session.sql(insert).collect()
        
        st.success('Your Smoothie is ordered!'+ name, icon="✅")
    
