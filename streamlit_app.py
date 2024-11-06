# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(" :cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get active Snowflake session
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Convert the Snowflake DataFrame to a list for multiselect
fruit_options = my_dataframe.to_pandas()['FRUIT_NAME'].tolist()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    fruit_options  # 修正: my_dataframeの代わりにリストを使用
    ,max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)  # 修正: 文字列の結合方法を変更

    # SQL挿入文を修正
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name)
                         VALUES ('{ingredients_string}', '{name_on_order}')"""

    st.write("SQL Insert Statement:", my_insert_stmt)  # SQL文を表示

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        # Execute the SQL statement
        try:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")
        except Exception as e:
            st.error(f"An error occurred: {e}")
