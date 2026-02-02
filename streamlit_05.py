import streamlit as st
import pandas as pd

st.title('支店別売上推移')

df = pd.read_csv('retail_sales_branch.csv')

with st.sidebar:
    branch = st.multiselect('支店を選択してください（複数選択可）',
                            df['支店'].unique())
    year = st.number_input('年を指定してください',
                           min_value=df['年'].min(),
                           max_value=df['年'].max(),
                           value=df['年'].min(),
                           step=1)
    option = st.radio('表示形式を選択してください',
                      ['表','グラフ'])
    

df = df[df['支店'].isin(branch)]
df = df[df['年']==year]
df.drop('年',axis=1,inplace=True)
df.set_index('支店',inplace=True)

st.write('単位:万円')
if option == '表':
    st.dataframe(df, width=800, height=220)
elif option == 'グラフ':
    st.line_chart(df.T)
