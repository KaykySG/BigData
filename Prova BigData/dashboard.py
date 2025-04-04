import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# Endpoints da API
API_URL = "http://127.0.0.1:8000"

# Jogos mais bem avaliados
st.subheader("Jogos mais bem avaliados")
response = requests.get(f"{API_URL}/jogos_mais_bem_avaliados")
dados = response.json()
df_positivos = pd.DataFrame(dados)
fig_positivos = px.bar(df_positivos, x='name', y='positive_ratings', labels={'positive_ratings': 'Avaliações Positivas', 'name': 'Nome do Jogo'})
st.plotly_chart(fig_positivos)

# Gráfico comparativo de avaliações positivas e negativas
st.subheader("Comparativo de Avaliações Positivas e Negativas")
response_negativos = requests.get(f"{API_URL}/jogos_mais_avaliacoes_ruins")
dados_negativos = response_negativos.json()
df_negativos = pd.DataFrame(dados_negativos)

response_all_games = requests.get(f"{API_URL}/jogos_mais_bem_avaliados")
all_games_data = response_all_games.json()
df_all_games = pd.DataFrame(all_games_data)

# Mesclar as avaliações negativas e positivas
df_merged = pd.merge(df_negativos[['name', 'negative_ratings']],
                    df_all_games[['name', 'positive_ratings']],
                    on='name', how='left')

# Preencher NaN com 0 para facilitar a filtragem
df_merged['positive_ratings'] = df_merged['positive_ratings'].fillna(0)

# Filtrar jogos onde ambas as avaliações são maiores que zero
df_filtered = df_merged[(df_merged['negative_ratings'] > 0) & (df_merged['positive_ratings'] > 0)]

# Obter os top 10 com base nas avaliações negativas após a filtragem
df_top_filtered = df_filtered.nlargest(10, 'negative_ratings')

fig_comparativo = go.Figure()

# Avaliações Negativas (vermelho)
fig_comparativo.add_trace(go.Bar(
    y=df_top_filtered['name'],
    x=df_top_filtered['negative_ratings'],
    orientation='h',
    name='Avaliações Negativas',
    marker_color='red'
))

# Avaliações Positivas (verde)
fig_comparativo.add_trace(go.Bar(
    y=df_top_filtered['name'],
    x=df_top_filtered['positive_ratings'],
    orientation='h',
    name='Avaliações Positivas',
    marker_color='green'
))

fig_comparativo.update_layout(
    barmode='group',
    yaxis_title='Nome do Jogo',
    xaxis_title='Número de Avaliações',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=200, r=200, t=50, b=50) # Ajustar margens para os rótulos
)

st.plotly_chart(fig_comparativo, use_container_width=True)

# Jogos com mais horas jogadas (Gráfico de Dispersão)
st.subheader("Jogos com mais horas jogadas")
response_horas = requests.get(f"{API_URL}/jogos_mais_horas_jogadas")
dados_horas = response_horas.json()
df_horas = pd.DataFrame(dados_horas)
df_top_horas = df_horas.nlargest(10, 'average_playtime')
fig_horas_scatter = px.scatter(df_top_horas, x='name', y='average_playtime',
                                labels={'average_playtime': 'Tempo Médio', 'name': 'Nome'},
                                size='average_playtime',
                                hover_data=['average_playtime'])
st.plotly_chart(fig_horas_scatter)


# Gêneros mais recorrentes em jogos
st.subheader("Gêneros mais recorrentes em jogos")
response = requests.get(f"{API_URL}/generos_mais_recorrentes")
dados = response.json()
generos_dict = dados
generos_series = pd.Series(generos_dict)
generos_df = pd.DataFrame({'Gênero': generos_series.index, 'Quantidade': generos_series.values})

fig_generos_pizza = px.pie(
    generos_df,
    names='Gênero',
    values='Quantidade',
    title='Distribuição de Gêneros',
    hover_data=['Quantidade'],
    labels={'Quantidade': 'Número de Jogos'},
    color='Gênero',
    category_orders={'Gênero': generos_df['Gênero'].tolist()} # Manter a ordem das cores consistente com a legenda
)

fig_generos_pizza.update_traces(
    hovertemplate="<b>%{label}</b><br>Número de Jogos: %{value}<extra></extra>",
    pull=[0.1] * len(generos_df) # Inicialmente destacar todas as fatias um pouco
)

st.plotly_chart(fig_generos_pizza)