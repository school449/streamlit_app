# データについて
### 男女別人口－全国，都道府県(大正９年～平成27年)(国勢調査)
### データ取得日　2026/02/01

os.chdir 作業ディレクトリの固定  
df = pd.read_csv データの読み込み  
st.title タイトル  
st.markdown 概要と目的  
pref_list = df[col_pref].unique()  都道府県のリスト作成  
 selected_pref = st.sidebar.selectbox　サイドバーにセレクトボックスを表示  
 st.subheader　中見出し  
 selected_year = st.radio　ラジオボタン  
 ### データ抽出と計算
 pref_df = df[df[col_pref] == selected_pref].copy()
target_row = pref_df[pref_df[col_year] == selected_year]
pop_selected = target_row[col_total].values[0]
m_pop = target_row[col_male].values[0]
f_pop = target_row[col_female].values[0]

pop_2010 = pref_df[pref_df[col_year] == 2010][col_total].values[0]
pop_2015 = pref_df[pref_df[col_year] == 2015][col_total].values[0]
diff_count = pop_2015 - pop_2010
diff_rate = (diff_count / pop_2010) * 100

### rank関数を使った全国ランキングの算出
df_yearly = df[df[col_year] == selected_year].copy()
df_yearly['順位'] = df_yearly[col_total].rank(ascending=False, method='min').astype(int)
current_rank = df_yearly[df_yearly[col_pref] == selected_pref]['順位'].values[0]

st.header(f'{selected_pref} ({selected_year}年) の分析結果')

### メトリクス表示
c1, c2, c3 = st.columns(3)
c1.metric(f"{selected_year}年 総人口", f"{pop_selected:,}人")
c2.metric(f"{selected_year}年 全国順位", f"{current_rank}位 / 47")
c3.metric("人口増減(2010→15)", f"{diff_count:,}人", delta=f"{diff_rate:.2f}%")

###　男女比の円グラフ
st.subheader(f'{selected_year}年 男女人口比率')
fig = px.pie(
    values=[m_pop, f_pop], 
    names=['男性', '女性'],
    color_discrete_sequence=['#3498db', '#e74c3c'],
    hole=0.4
)
st.plotly_chart(fig)

 summary_df.style.applymap(style_and_format) 数値によって色分けする

### 授業外の要素
1.current_rank: rank関数を使ったランキングの導出  
2.st.plotly_chart(fig): 円グラフ  
3.summary_df.style.applymap(style_and_format): 数値によって色分け  

### 使用した理由
1.ランキングにしたほうが見やすいと思ったため  
2.円グラフにすることで男女比率がより見やすくなると思ったため  
3.色分けしてあるほうがより見やすいと思ったため  

### 生成AIについて
1.使用しました  
2.色分けする部分であったり、rank関数であったり、授業で習ってない部分の実装についてをAIに聞いて実装しました