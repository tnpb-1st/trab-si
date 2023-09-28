import streamlit as st
import pandas as pd
import plotly.express as px
import requests 

st.set_page_config(layout="wide")
st.title("Mapeamento CNES | Pernambuco")

tab1, tab2, tab3 = st.tabs(['Leitos', 'Estabelecimento', 'Funcionarios'])

with tab1:
    dict_df = pd.read_csv("./data/dict_df.csv")
    df_leito = pd.read_csv("./data/df_leito.csv")
    cloropeth_data = pd.read_csv("./data/cloropeth_data.csv")
    de_para = pd.read_csv("./data/depara.csv")

    tmp_df = df_leito.groupby(['data'])['quantidade_total'].sum().reset_index()
    fig1 = px.line(x=tmp_df.data, 
        y=tmp_df.quantidade_total, 
        title='Quantidade de leitos ao longo do tempo'
    )

    tmp_df = df_leito.groupby(['data', 'tipo_leito'])['quantidade_total'].sum().reset_index()
    fig2 = px.line(tmp_df, 
        x='data', 
        y='quantidade_total', 
        title='Quantidade de leitos ao longo do tempo, por tipo de leito', 
        color='tipo_leito'
    )

    tmp_df = df_leito.groupby(['data'])[['quantidade_contratado', 'quantidade_sus']].sum().reset_index()
    fig3 = px.line(tmp_df, 
        x='data', 
        y=['quantidade_contratado', 'quantidade_sus'], 
        title='Quantidade de leitos contratados e do SUS ao longo do tempo'
    )

    tmp_df = df_leito.groupby(['data', 'tipo_especialidade_leito'])['quantidade_total'].sum().reset_index()
    fig4 = px.line(tmp_df, x='data', y='quantidade_total', title='Quantidade de leitos ao longo do tempo, por tipo de especialidade do leito', color='tipo_especialidade_leito')
        
    cidades= requests.get('https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-26-mun.json').json()
    fig5 = px.choropleth(cloropeth_data, 
        geojson=cidades, 
        locations='id_municipio', 
        color='quantidade_total',
        color_continuous_scale="PuBu",
        featureidkey="properties.id",
        hover_name = 'nome_municipio',
        labels={'unemp':'unemployment rate'}
    )

    fig5.update_geos(
        center=dict(lat=-8.50, lon=-37.89),  # Centered on Brazil
        projection_scale=50,  # Adjust this value for an appropriate zoom level
    )

    fig5.update_layout(title="Distribuição de leitos em pernambuco")

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1)

        st.plotly_chart(fig2)

    with col2:
        st.plotly_chart(fig3)

        st.plotly_chart(fig4)

    st.plotly_chart(fig5)

with tab2:
    cols = ['tipo_esfera_administrativa', 'tipo_unidade', 'indicador_atencao_ambulatorial', 'indicador_atencao_hospitalar',
            'ano', 'mes', 'tipo_turno']
    df_estab = pd.read_pickle("./data/df_estab_pe.pkl")
    for col in [x for x in dict_df.query('id_tabela == "estabelecimento"').coluna.unique() if x in cols]:
        df_estab[col] = df_estab[col].map(dict_df.query(f'id_tabela == "estabelecimento" and coluna == "{col}"').set_index('chave')['valor'])
    
    df_estab['data'] = pd.to_datetime(df_estab['ano']+ '-' + df_estab['mes'].str.zfill(2) + '-' + '01')
    tmp_df = df_estab.groupby(['data']).size().rename('quantidade_total').reset_index()
    fig1 = px.line(x=tmp_df.data, y=tmp_df.quantidade_total, title='Quantidade de estabelecimentos ao longo do tempo')

    tmp_df = df_estab.groupby(['data', 'tipo_esfera_administrativa']).size().rename('quantidade_total').reset_index()
    fig2 = px.line(x=tmp_df.data, y=tmp_df.quantidade_total, color=tmp_df.tipo_esfera_administrativa, title='Quantidade de estabelecimentos ao longo do tempo, por tipo de esfera administrativa')

    tmp_df = df_estab.groupby(['data', 'tipo_unidade']).size().rename('quantidade_total').reset_index()
    fig3 = px.line(x=tmp_df.data, y=tmp_df.quantidade_total, color=tmp_df.tipo_unidade, title='Quantidade de estabelecimentos ao longo do tempo, por tipo de unidade')

    tmp_df = df_estab.groupby(['data', 'indicador_atencao_ambulatorial']).size().rename('quantidade_total').reset_index()
    fig4 = px.line(x=tmp_df.data, y=tmp_df.quantidade_total, color=tmp_df.indicador_atencao_ambulatorial, title='Quantidade de estabelecimentos ao longo do tempo, por existência de atenção ambulatorial')

    tmp_df = df_estab.groupby(['data', 'indicador_atencao_hospitalar']).size().rename('quantidade_total').reset_index()
    fig5 = px.line(x=tmp_df.data, y=tmp_df.quantidade_total, color=tmp_df.indicador_atencao_hospitalar, title='Quantidade de estabelecimentos ao longo do tempo, por existência de atenção hospitalar')

    tmp_df = df_estab.groupby(['data', 'tipo_turno']).size().rename('quantidade_total').reset_index()
    fig6 = px.line(x=tmp_df.data, y=tmp_df.quantidade_total, color=tmp_df.tipo_turno, title='Quantidade de estabelecimentos ao longo do tempo, por tipo de turno')

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig1)

        st.plotly_chart(fig2)

        st.plotly_chart(fig6)

    with col2:
        st.plotly_chart(fig4)

        st.plotly_chart(fig5)


    st.plotly_chart(fig3, use_container_width=True)
