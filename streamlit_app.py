import streamlit as st

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
    
    # --- DADOS DOS ESTADOS DO NORDESTE (Base de Dados Interna) ---
    # Valores de ICMS baseados nas alíquotas modais projetadas para 2025
    # Irradiação Solar: Média aproximada (kWh/m²/dia) para capitais/região
    nordeste_data = {
        "Alagoas": {
            "lat": -9.66625, "lon": -35.7351, 
            "icms": 0.19, "pis_cofins": 0.0925, "irradiacao": 5.45
        },
        "Bahia": {
            "lat": -12.9704, "lon": -38.5124, 
            "icms": 0.205, "pis_cofins": 0.0925, "irradiacao": 5.80
        },
        "Ceará": {
            "lat": -3.71722, "lon": -38.5434, 
            "icms": 0.20, "pis_cofins": 0.0925, "irradiacao": 5.90
        },
        "Maranhão": {
            "lat": -2.53073, "lon": -44.3068, 
            "icms": 0.23, "pis_cofins": 0.0925, "irradiacao": 5.20
        },
        "Paraíba": {
            "lat": -7.11532, "lon": -34.861, 
            "icms": 0.20, "pis_cofins": 0.0925, "irradiacao": 5.90
        },
        "Pernambuco": {
            "lat": -8.05428, "lon": -34.8813, 
            "icms": 0.205, "pis_cofins": 0.0925, "irradiacao": 5.70
        },
        "Piauí": {
            "lat": -5.08921, "lon": -42.8016, 
            "icms": 0.225, "pis_cofins": 0.0925, "irradiacao": 5.85
        },
        "Rio Grande do Norte": {
            "lat": -5.79448, "lon": -35.211, 
            "icms": 0.20, "pis_cofins": 0.0925, "irradiacao": 6.10
        },
        "Sergipe": {
            "lat": -10.9472, "lon": -37.0731, 
            "icms": 0.19, "pis_cofins": 0.0925, "irradiacao": 5.40
        }
    }

    # 1. MAPA (Topo)
    st.subheader("📍 Localização Geográfica")
    
    # Criando DataFrame para o st.map
    import pandas as pd
    map_df = pd.DataFrame.from_dict(nordeste_data, orient='index')
    
    # Exibe o mapa com todos os pontos do Nordeste
    st.map(map_df, zoom=4, use_container_width=True)

    st.markdown("---")

    # 2. SELEÇÃO DE ESTADO
    st.subheader("Parâmetros Regionais")
    
    col_sel, col_info = st.columns([1, 2])
    
    with col_sel:
        state_selected = st.selectbox(
            "Selecione o Estado para Análise:",
            options=sorted(nordeste_data.keys())
        )
    
    # Recupera dados do estado selecionado
    state_info = nordeste_data[state_selected]

    # 3. EXIBIÇÃO DE DADOS (Metrics)
    with col_info:
        st.info(f"Dados Carregados para: **{state_selected}**")
        
        c1, c2, c3, c4 = st.columns(4)
        
        with c1:
            st.metric(
                label="ICMS (2025)",
                value=f"{state_info['icms']*100:.1f}%",
                help="Alíquota interna padrão projetada para 2025"
            )
        
        with c2:
            st.metric(
                label="PIS/COFINS (Médio)",
                value=f"{state_info['pis_cofins']*100:.2f}%",
                help="Alíquota federal média estimada para consumidores"
            )
            
        with c3:
            st.metric(
                label="Total Impostos",
                value=f"{(state_info['icms'] + state_info['pis_cofins'])*100:.2f}%"
            )

        with c4:
            st.metric(
                label="Irradiação Solar",
                value=f"{state_info['irradiacao']} kWh/m²",
                delta="Média Diária",
                help="Irradiação Global Horizontal (GHI) média estimada"
            )

    # Armazenar seleção no Session State para usar na próxima página (Análise)
    st.session_state['selected_state_data'] = state_info

elif page == "Análise":
    st.title("📊 Análise de Resultados")
    st.write("Em construção...")