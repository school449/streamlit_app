import streamlit as st
import pandas as pd
import plotly.express as px
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_csv('data.csv', encoding='UTF-8')

col_pref = df.columns[0]
col_year = df.columns[1]
col_total = df.columns[2]
col_male = df.columns[3]
col_female = df.columns[4]

st.title('都道府県別 人口詳細分析ダッシュボード')

st.markdown("""
### 概要
このアプリは、日本の各都道府県における人口推移（2010年〜2015年）を可視化したものです。

### 目的
人口の減少が進んでいると言われているのを、一目でわかりやすくするためのアプリです。
""")

st.divider()

pref_list = df[col_pref].unique()
selected_pref = st.sidebar.selectbox('分析する都道府県を選択', pref_list)

st.subheader('分析対象年の切り替え')
selected_year = st.radio("表示するデータを選択してください", [2010, 2015], horizontal=True)

pref_df = df[df[col_pref] == selected_pref].copy()
target_row = pref_df[pref_df[col_year] == selected_year]
pop_selected = target_row[col_total].values[0]
m_pop = target_row[col_male].values[0]
f_pop = target_row[col_female].values[0]

pop_2010 = pref_df[pref_df[col_year] == 2010][col_total].values[0]
pop_2015 = pref_df[pref_df[col_year] == 2015][col_total].values[0]
diff_count = pop_2015 - pop_2010
diff_rate = (diff_count / pop_2010) * 100

df_yearly = df[df[col_year] == selected_year].copy()
df_yearly['順位'] = df_yearly[col_total].rank(ascending=False, method='min').astype(int)
current_rank = df_yearly[df_yearly[col_pref] == selected_pref]['順位'].values[0]

st.header(f'{selected_pref} ({selected_year}年) の分析結果')

c1, c2, c3 = st.columns(3)
c1.metric(f"{selected_year}年 総人口", f"{pop_selected:,}人")
c2.metric(f"{selected_year}年 全国順位", f"{current_rank}位 / 47")
c3.metric("人口増減(2010→15)", f"{diff_count:,}人", delta=f"{diff_rate:.2f}%")

st.divider()

st.subheader(f'{selected_year}年 男女人口比率')
fig = px.pie(
    values=[m_pop, f_pop], 
    names=['男性', '女性'],
    color_discrete_sequence=['#3498db', '#e74c3c'],
    hole=0.4
)
st.plotly_chart(fig)

st.subheader('統計詳細データ')

summary_df = pd.DataFrame({
    '項目': ['2010年人口', '2015年人口', '人口増減数', '人口増減率(%)'],
    '数値': [pop_2010, pop_2015, diff_count, round(diff_rate, 2)]
})
summary_df.index = summary_df.index + 1

def style_and_format(val):
    style = 'color: black;'
    if isinstance(val, (int, float)):
        if val < 0: style = 'color: red; font-weight: bold;'
        elif val > 0: style = 'color: blue;'
    return style

st.dataframe(
    summary_df.style.applymap(style_and_format).format(
        subset=['数値'], 
        formatter="{:,.2f}" if "率" in str(summary_df['項目']) else "{:,}"
    ),
    use_container_width=True
)

with st.expander(f"{selected_year}年の全県データ一覧を表示"):
    display_all_df = df_yearly[[col_pref, col_total, '順位']].reset_index(drop=True)
    display_all_df.index = display_all_df.index + 1
    st.dataframe(
        display_all_df.style.format({col_total: "{:,}"}),
        use_container_width=True
    )

st.write("この表によると、東京等の大規模都市以外では、人口が減少していることが確認できる")