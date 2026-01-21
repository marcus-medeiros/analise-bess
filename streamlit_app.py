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
    
    # --- 1. BASE DE DADOS (Definida no início para ser usada em tudo) ---
    nordeste_data = {
        "Alagoas": {
            "lat": -9.66625, "lon": -35.7351, "irradiacao": 5.45,
            "concessionaria": "Equatorial AL",
            "tusd_p": 1841.93, "tusd_fp": 83.51, "te": -3.06, 
            "icms": 0.19, "pis": 0.01, "cofins": 0.04
        },
        "Bahia": {
            "lat": -12.9704, "lon": -38.5124, "irradiacao": 5.80,
            "concessionaria": "Neoenergia Coelba",
            "tusd_p": 2676.04, "tusd_fp": 101.42, "te": 32.93, 
            "icms": 0.205, "pis": 0.01, "cofins": 0.04
        },
        "Ceará": {
            "lat": -3.71722, "lon": -38.5434, "irradiacao": 5.90,
            "concessionaria": "Enel CE",
            "tusd_p": 1162.90, "tusd_fp": 88.46, "te": 38.09, 
            "icms": 0.20, "pis": 0.01, "cofins": 0.04
        },
        "Maranhão": {
            "lat": -2.53073, "lon": -44.3068, "irradiacao": 5.20,
            "concessionaria": "Equatorial MA",
            "tusd_p": 2377.47, "tusd_fp": 116.15, "te": 38.60, 
            "icms": 0.23, "pis": 0.01, "cofins": 0.04
        },
        "Paraíba": {
            "lat": -7.11532, "lon": -34.861, "irradiacao": 5.90,
            "concessionaria": "Energisa PB",
            "tusd_p": 1263.03, "tusd_fp": 96.59, "te": 30.30, 
            "icms": 0.20, "pis": 0.01, "cofins": 0.04
        },
        "Pernambuco": {
            "lat": -8.05428, "lon": -34.8813, "irradiacao": 5.70,
            "concessionaria": "Neoenergia Pernambuco",
            "tusd_p": 1244.41, "tusd_fp": 94.68, "te": 29.14, 
            "icms": 0.205, "pis": 0.01, "cofins": 0.04
        },
        "Piauí": {
            "lat": -5.08921, "lon": -42.8016, "irradiacao": 5.85,
            "concessionaria": "Equatorial PI",
            "tusd_p": 2296.63, "tusd_fp": 140.21, "te": 33.71, 
            "icms": 0.225, "pis": 0.01, "cofins": 0.04
        },
        "Rio Grande do Norte": {
            "lat": -5.79448, "lon": -35.211, "irradiacao": 6.10,
            "concessionaria": "Neoenergia Cosern",
            "tusd_p": 1867.81, "tusd_fp": 91.56, "te": 29.46, 
            "icms": 0.20, "pis": 0.01, "cofins": 0.04
        },
        "Sergipe": {
            "lat": -10.9472, "lon": -37.0731, "irradiacao": 5.40,
            "concessionaria": "Energisa SE",
            "tusd_p": 1702.94, "tusd_fp": 84.93, "te": 23.15, 
            "icms": 0.19, "pis": 0.01, "cofins": 0.04
        }
    }

    # --- 2. LÓGICA DE ZOOM DINÂMICO ---
    # Verifica qual estado está selecionado no session_state (pela chave 'state_selector')
    # Se ainda não houver seleção (primeira vez que roda), pega o primeiro da lista (Alagoas)
    default_state = sorted(nordeste_data.keys())[0]
    current_state_name = st.session_state.get("state_selector", default_state)
    
    # Define o centro e o zoom baseado no estado atual
    view_lat = nordeste_data[current_state_name]["lat"]
    view_lon = nordeste_data[current_state_name]["lon"]
    view_zoom = 7.0 # Zoom mais próximo para focar no estado
    
    map_df = pd.DataFrame.from_dict(nordeste_data, orient='index')

    states_list = list(nordeste_data.keys())
    irradiacao_list = [nordeste_data[s]['irradiacao'] for s in states_list]
    df_irr = pd.DataFrame({'Estado': states_list, 'Irradiação (kWh/m²/dia)': irradiacao_list})
    df_irr = df_irr.sort_values(by='Irradiação (kWh/m²/dia)', ascending=True)

    col_map_viz, col_chart_viz = st.columns([1, 1]) 

    with col_map_viz:
        st.subheader("📍 Localização Geográfica")
        # AQUI ESTÁ A MÁGICA: Passamos latitude, longitude e zoom dinâmicos
        st.map(
            map_df, 
            latitude=view_lat, 
            longitude=view_lon, 
            zoom=view_zoom, 
            use_container_width=True, 
            height=450
        )

    with col_chart_viz:
        st.subheader("☀️ Irradiação Média Regional")
        # Destacar a barra do estado selecionado
        colors = ['#1f77b4' if estado == current_state_name else '#d3d3d3' for estado in df_irr['Estado']]
        
        fig = px.bar(
            df_irr,
            x='Irradiação (kWh/m²/dia)',
            y='Estado',
            orientation='h',
            text='Irradiação (kWh/m²/dia)',
        )
        # Atualiza a cor para destacar o escolhido
        fig.update_traces(marker_color=colors, texttemplate='%{text:.2f}', textposition='outside')
        
        fig.update_layout(
            yaxis_title=None,
            xaxis_title="GHI Médio (kWh/m²/dia)",
            height=450,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)


    st.markdown("---")

    # --- 4. SELEÇÃO DE PARÂMETROS ---
    st.subheader("Definição de Parâmetros Tarifários (Grupo A4 - Verde)")
    
    # O parametro KEY é fundamental: ele conecta esse input com o session_state lido lá em cima
    state_selected = st.selectbox(
        "Selecione o Estado do Cliente:",
        options=sorted(nordeste_data.keys()),
        key="state_selector" 
    )
    
    state_info = nordeste_data[state_selected]
    st.session_state['selected_state_data'] = state_info

    # Exibição dos KPIs
    st.markdown(f"**Concessionária:** {state_info['concessionaria']}")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1: st.metric("TUSD Ponta", f"R$ {state_info['tusd_p']:.2f}")
    with kpi2: st.metric("TUSD Fora Ponta", f"R$ {state_info['tusd_fp']:.2f}")
    with kpi3: st.metric("Tarifa de Energia (TE)", f"R$ {state_info['te']:.2f}")
    with kpi4: st.metric("Total Ponta (s/ imp)", f"R$ {(state_info['tusd_p'] + state_info['te']):.2f}")

    st.markdown("##### Dados Tributários e Ambientais")
    imp1, imp2, imp3, amb1 = st.columns(4)
    with imp1: st.metric("ICMS", f"{state_info['icms']*100:.1f}%")
    with imp2: st.metric("PIS + COFINS", f"{(state_info['pis'] + state_info['cofins'])*100:.1f}%")
    with imp3: st.metric("Carga Tributária", f"{(state_info['icms'] + state_info['pis'] + state_info['cofins'])*100:.1f}%")
    with amb1: st.metric("Irradiação Local", f"{state_info['irradiacao']} kWh/m²")


elif page == "Análise":
    st.title("📊 Análise de Resultados")
    st.write("Em construção...")