import streamlit as st
# --- PREPARAÇÃO DE DADOS PARA VISUALIZAÇÃO ---
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(
    page_title="Análise BESS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR ---
with st.sidebar:
    # Espaço para Logo (Placeholder)
    st.image("https://placehold.co/250x100/png?text=LOGO+BESS", use_container_width=True)
    st.markdown("---")
    
    st.header("Menu Principal")
    page = st.radio(
        "Navegue pelas seções:",
        ["Página Inicial", "Cenário", "Análise"]
    )

# --- CONTEÚDO PRINCIPAL ---

if page == "Página Inicial":
    st.title("🏠 Metodologia de Análise")
    
    st.markdown("""
    Esta plataforma utiliza uma abordagem sequencial para determinar a viabilidade econômica da hibridização de sistemas de armazenamento (BESS) com geração fotovoltaica (FV). A metodologia é dividida em quatro etapas fundamentais:
    """)

    # Etapa 1
    st.subheader("1. Análise do Perfil de Carga e Cliente")
    st.markdown("""
    A primeira etapa consiste na caracterização do consumo energético do cliente. Serão avaliadas as curvas de carga para identificar picos de demanda e oportunidades de *peak shaving* ou *energy arbitrage*.
    """)

    # Etapa 2
    st.subheader("2. Análise Tarifária (Nordeste)")
    st.markdown("""
    O modelo considera as especificidades das estruturas tarifárias vigentes nos estados do Nordeste brasileiro (ex: Grupo A, Horossazonal Verde/Azul). A análise compara o custo da energia da rede versus o custo nivelado da energia armazenada.
    """)

    # Etapa 3
    st.subheader("3. Dimensionamento (BESS + FV)")
    st.markdown("""
    Nesta etapa, define-se a capacidade nominal do banco de baterias ($kWh$) e a potência do sistema fotovoltaico ($kWp$) necessários para atender à demanda estipulada e maximizar a eficiência do sistema híbrido.
    """)

    # Etapa 4 - Financeiro (Com LaTeX rigoroso)
    st.subheader("4. Indicadores de Viabilidade Econômica")
    st.markdown("Para a conclusão do estudo, são calculados os seguintes indicadores financeiros:")

    st.markdown("#### a) Valor Presente Líquido (VPL)")
    st.latex(r'''
    VPL = \sum_{t=1}^{N} \frac{FC_t}{(1 + TMA)^t} - I_0
    ''')
    st.markdown("""
    Onde:
    * $FC_t$: Fluxo de caixa no período $t$
    * $TMA$: Taxa Mínima de Atratividade
    * $N$: Vida útil do projeto (anos)
    * $I_0$: Investimento inicial (CAPEX)
    """)

    st.markdown("#### b) Taxa Interna de Retorno (TIR)")
    st.markdown("A TIR é a taxa $i^*$ que zera o VPL do projeto:")
    st.latex(r'''
    \sum_{t=1}^{N} \frac{FC_t}{(1 + i^*)^t} - I_0 = 0
    ''')

    st.markdown("#### c) Payback Simples e Descontado")
    st.markdown("O tempo de retorno é calculado encontrando-se o período $T$ onde a soma dos fluxos de caixa iguala o investimento inicial:")
    st.latex(r'''
    Payback = \min \{ T \mid \sum_{t=0}^{T} FC_t \ge 0 \}
    ''')

# --- MANTENDO AS OUTRAS PÁGINAS VAZIAS POR ENQUANTO ---
elif page == "Cenário":
    st.title("⚙️ Configuração de Cenário")
    
    # --- DADOS DOS ESTADOS DO NORDESTE (Base Interna) ---
    # Mesmo dicionário anterior
    nordeste_data = {
        "Alagoas": {"lat": -9.66625, "lon": -35.7351, "icms": 0.19, "pis_cofins": 0.0925, "irradiacao": 5.45},
        "Bahia": {"lat": -12.9704, "lon": -38.5124, "icms": 0.205, "pis_cofins": 0.0925, "irradiacao": 5.80},
        "Ceará": {"lat": -3.71722, "lon": -38.5434, "icms": 0.20, "pis_cofins": 0.0925, "irradiacao": 5.90},
        "Maranhão": {"lat": -2.53073, "lon": -44.3068, "icms": 0.23, "pis_cofins": 0.0925, "irradiacao": 5.20},
        "Paraíba": {"lat": -7.11532, "lon": -34.861, "icms": 0.20, "pis_cofins": 0.0925, "irradiacao": 5.90},
        "Pernambuco": {"lat": -8.05428, "lon": -34.8813, "icms": 0.205, "pis_cofins": 0.0925, "irradiacao": 5.70},
        "Piauí": {"lat": -5.08921, "lon": -42.8016, "icms": 0.225, "pis_cofins": 0.0925, "irradiacao": 5.85},
        "Rio Grande do Norte": {"lat": -5.79448, "lon": -35.211, "icms": 0.20, "pis_cofins": 0.0925, "irradiacao": 6.10},
        "Sergipe": {"lat": -10.9472, "lon": -37.0731, "icms": 0.19, "pis_cofins": 0.0925, "irradiacao": 5.40}
    }

    # DataFrame para o Mapa
    map_df = pd.DataFrame.from_dict(nordeste_data, orient='index')

    # DataFrame para o Gráfico de Barras (Extraindo dados do dicionário)
    states_list = list(nordeste_data.keys())
    irradiacao_list = [nordeste_data[s]['irradiacao'] for s in states_list]
    df_irr = pd.DataFrame({'Estado': states_list, 'Irradiação (kWh/m²/dia)': irradiacao_list})
    # Ordenando para o gráfico ficar mais fácil de ler
    df_irr = df_irr.sort_values(by='Irradiação (kWh/m²/dia)', ascending=True)


    # --- LAYOUT LADO A LADO (Visualização) ---
    # Cria duas colunas: Esquerda para Mapa, Direita para Gráfico
    col_map_viz, col_chart_viz = st.columns([1, 1]) # Proporção 50%/50%

    with col_map_viz:
        st.subheader("📍 Localização Geográfica")
        # O parâmetro height ajuda a alinhar a altura com o gráfico ao lado
        st.map(map_df, zoom=5, use_container_width=True, height=450)

    with col_chart_viz:
        st.subheader("☀️ Irradiação Média Regional")
        # Criando o gráfico de barras horizontal
        fig = px.bar(
            df_irr,
            x='Irradiação (kWh/m²/dia)',
            y='Estado',
            orientation='h', # 'h' define que é horizontal
            text='Irradiação (kWh/m²/dia)', # Mostra o valor na barra
            color='Irradiação (kWh/m²/dia)', # Cor gradiente baseada no valor
            color_continuous_scale='YlOrRd' # Escala de cor (Amarelo -> Laranja -> Vermelho)
        )
        
        # Ajustes finos de layout do gráfico
        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            yaxis_title=None, # Remove rótulo do eixo Y (já são os nomes dos estados)
            xaxis_title="GHI Médio (kWh/m²/dia)",
            height=450, # Altura igual ao mapa para ficarem alinhados
            margin=dict(l=0, r=0, t=30, b=0) # Margens para otimizar espaço
        )
        # Oculta a barra de cores lateral para economizar espaço
        fig.update_coloraxes(showscale=False)
        
        st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")

    # --- SELEÇÃO E DETALHES (Mantido abaixo) ---
    st.subheader("Definição de Parâmetros do Projeto")
    
    state_selected = st.selectbox(
        "Selecione o Estado do Cliente:",
        options=sorted(nordeste_data.keys())
    )
    
    # Recupera dados do estado selecionado
    state_info = nordeste_data[state_selected]

    st.info(f"Parâmetros Tributários e Ambientais: **{state_selected}**")
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("ICMS (Proj. 2025)", f"{state_info['icms']*100:.1f}%")
    with c2: st.metric("PIS/COFINS", f"{state_info['pis_cofins']*100:.2f}%")
    with c3: st.metric("Carga Tributária Total", f"{(state_info['icms'] + state_info['pis_cofins'])*100:.2f}%")
    # Adicionei um destaque na métrica de irradiação do estado selecionado
    with c4: st.metric("Irradiação Local", f"{state_info['irradiacao']} kWh/m²", delta="Referência para Cálculo")

    # Salva no session state
    st.session_state['selected_state_data'] = state_info

elif page == "Análise":
    st.title("📊 Análise de Resultados")
    st.write("Em construção...")