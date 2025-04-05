import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

# Endpoints da API
API_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")

# Remover padding da página
st.markdown(
    """
    <style>
    .appview-container .main .block-container {
        padding-top: 10px !important;
        padding-bottom: 10px !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
    }
    .st-emotion-cache-z531s { /* Seletor para as colunas (opcional) */
        padding-left: 0px !important;
        padding-right: 0px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Análise de Dados de Jogos")

# Primeira linha de 3 gráficos
st.subheader("Análise Inicial")
col1, col2, col3 = st.columns(3)

# Gráfico 1: Jogos mais bem avaliados
with col1:
    st.markdown("#### Melhores Avaliações")
    response = requests.get(f"{API_URL}/jogos_mais_bem_avaliados")
    dados = response.json()
    df_positivos = pd.DataFrame(dados)
    fig_positivos = px.bar(df_positivos, x='name', y='positive_ratings',
                             labels={'positive_ratings': 'Positivas', 'name': 'Jogo'})
    st.plotly_chart(fig_positivos, use_container_width=True)

# Gráfico 2: Comparativo de avaliações
with col2:
    st.markdown("#### Avaliações +/-")
    response_negativos = requests.get(f"{API_URL}/jogos_mais_avaliacoes_ruins")
    dados_negativos = response_negativos.json()
    df_negativos = pd.DataFrame(dados_negativos)
    response_all_games = requests.get(f"{API_URL}/jogos_mais_bem_avaliados")
    all_games_data = response_all_games.json()
    df_all_games = pd.DataFrame(all_games_data)
    df_merged = pd.merge(df_negativos[['name', 'negative_ratings']],
                         df_all_games[['name', 'positive_ratings']],
                         on='name', how='left')
    df_merged['positive_ratings'] = df_merged['positive_ratings'].fillna(0)
    df_filtered = df_merged[(df_merged['negative_ratings'] > 0) & (df_merged['positive_ratings'] > 0)]
    df_top_filtered = df_filtered.nlargest(10, 'negative_ratings')
    fig_comparativo = go.Figure()
    fig_comparativo.add_trace(go.Bar(y=df_top_filtered['name'], x=df_top_filtered['negative_ratings'], orientation='h', name='Negativas', marker_color='red'))
    fig_comparativo.add_trace(go.Bar(y=df_top_filtered['name'], x=df_top_filtered['positive_ratings'], orientation='h', name='Positivas', marker_color='green'))
    fig_comparativo.update_layout(barmode='group', yaxis_title='Jogo', xaxis_title='Avaliações', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1), margin=dict(l=100, r=20, t=30, b=30))
    st.plotly_chart(fig_comparativo, use_container_width=True)

# Gráfico 3: Jogos com mais horas jogadas
with col3:
    st.markdown("#### Mais Horas Jogadas")
    response_horas = requests.get(f"{API_URL}/jogos_mais_horas_jogadas")
    dados_horas = response_horas.json()
    df_horas = pd.DataFrame(dados_horas)
    df_top_horas = df_horas.nlargest(10, 'average_playtime')
    fig_horas_scatter = px.scatter(df_top_horas, x='name', y='average_playtime',
                                     labels={'average_playtime': 'Tempo Médio', 'name': 'Jogo'},
                                     size='average_playtime',
                                     hover_data=['average_playtime'])
    st.plotly_chart(fig_horas_scatter, use_container_width=True)

st.markdown("---") # Quebra de linha visual

# Segunda linha de 3 gráficos
st.subheader("Análise Adicional")
col4, col5, col6 = st.columns(3)

# Gráfico 4: Gêneros mais recorrentes
with col4:
    st.markdown("#### Gêneros Recorrentes")
    response_generos = requests.get(f"{API_URL}/generos_mais_recorrentes")
    dados_generos = response_generos.json()
    generos_dict = dados_generos
    generos_series = pd.Series(generos_dict)
    generos_df = pd.DataFrame({'Gênero': generos_series.index, 'Quantidade': generos_series.values})
    fig_generos_pizza = px.pie(generos_df, names='Gênero', values='Quantidade', title='',
                                 hover_data=['Quantidade'], labels={'Quantidade': 'Número de Jogos'},
                                 color='Gênero', category_orders={'Gênero': generos_df['Gênero'].tolist()})
    fig_generos_pizza.update_traces(hovertemplate="<b>%{label}</b><br>Número de Jogos: %{value}<extra></extra>", pull=[0.1] * len(generos_df))
    st.plotly_chart(fig_generos_pizza, use_container_width=True)



# Gráfico 6: Top 5 Publishers por Ano (Interativo)
with col6:
    st.markdown("#### Top Publishers por Ano")
    response_years = requests.get(f"{API_URL}/available_years")
    available_years_data = response_years.json()
    if available_years_data:
        available_years = sorted(available_years_data, reverse=True)
        selected_year = st.selectbox("Selecione o Ano:", available_years, key="publisher_year_selector")
        if selected_year:
            publishers_response = requests.get(f"{API_URL}/publishers_by_year/{selected_year}")
            if publishers_response.status_code == 200:
                publishers_data = publishers_response.json()
                if publishers_data:
                    df_publishers = pd.DataFrame(publishers_data)
                    fig_publishers = px.bar(df_publishers, x='publisher', y='count',
                                             labels={'count': 'Número de Jogos', 'publisher': 'Publisher'},
                                             title=f'em {selected_year}')
                    st.plotly_chart(fig_publishers, use_container_width=True)
                else:
                    st.info(f"Nenhum dado de publisher encontrado para o ano {selected_year}.")
            else:
                st.error(f"Erro ao obter dados de publishers para {selected_year}: {publishers_response.status_code}")
    else:
        st.info("Lista de anos disponíveis não carregada.")