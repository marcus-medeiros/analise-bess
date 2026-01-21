import streamlit as st
# --- PREPARAÇÃO DE DADOS PARA VISUALIZAÇÃO ---
import pandas as pd
import plotly.express as px
import pydeck as pdk # Importando a biblioteca de mapas avançada
import folium
from streamlit_folium import st_folium

# 1. Configuração da Página
st.set_page_config(
    page_title="Análise BESS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR ---
with st.sidebar:
    # Espaço para Logo (Placeholder)

    st.image("besssfv.png", use_container_width=True)
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
    
    # --- 1. BASE DE DADOS ---
    nordeste_data = {
        "Alagoas": {"lat": -9.66625, "lon": -35.7351, "irradiacao": 5.45, "concessionaria": "Equatorial AL", "tusd_p": 1841.93, "tusd_fp": 83.51, "te": -3.06, "icms": 0.19, "pis": 0.01, "cofins": 0.04},
        "Bahia": {"lat": -12.9704, "lon": -38.5124, "irradiacao": 5.80, "concessionaria": "Neoenergia Coelba", "tusd_p": 2676.04, "tusd_fp": 101.42, "te": 32.93, "icms": 0.205, "pis": 0.01, "cofins": 0.04},
        "Ceará": {"lat": -3.71722, "lon": -38.5434, "irradiacao": 5.90, "concessionaria": "Enel CE", "tusd_p": 1162.90, "tusd_fp": 88.46, "te": 38.09, "icms": 0.20, "pis": 0.01, "cofins": 0.04},
        "Maranhão": {"lat": -2.53073, "lon": -44.3068, "irradiacao": 5.20, "concessionaria": "Equatorial MA", "tusd_p": 2377.47, "tusd_fp": 116.15, "te": 38.60, "icms": 0.23, "pis": 0.01, "cofins": 0.04},
        "Paraíba": {"lat": -7.11532, "lon": -34.861, "irradiacao": 5.90, "concessionaria": "Energisa PB", "tusd_p": 1263.03, "tusd_fp": 96.59, "te": 30.30, "icms": 0.20, "pis": 0.01, "cofins": 0.04},
        "Pernambuco": {"lat": -8.05428, "lon": -34.8813, "irradiacao": 5.70, "concessionaria": "Neoenergia Pernambuco", "tusd_p": 1244.41, "tusd_fp": 94.68, "te": 29.14, "icms": 0.205, "pis": 0.01, "cofins": 0.04},
        "Piauí": {"lat": -5.08921, "lon": -42.8016, "irradiacao": 5.85, "concessionaria": "Equatorial PI", "tusd_p": 2296.63, "tusd_fp": 140.21, "te": 33.71, "icms": 0.225, "pis": 0.01, "cofins": 0.04},
        "Rio Grande do Norte": {"lat": -5.79448, "lon": -35.211, "irradiacao": 6.10, "concessionaria": "Neoenergia Cosern", "tusd_p": 1867.81, "tusd_fp": 91.56, "te": 29.46, "icms": 0.20, "pis": 0.01, "cofins": 0.04},
        "Sergipe": {"lat": -10.9472, "lon": -37.0731, "irradiacao": 5.40, "concessionaria": "Energisa SE", "tusd_p": 1702.94, "tusd_fp": 84.93, "te": 23.15, "icms": 0.19, "pis": 0.01, "cofins": 0.04}
    }

    # Lógica de Seleção (Antes do Mapa)
    default_state = sorted(nordeste_data.keys())[0]
    
    # Verifica se já existe seleção no Session State
    if "state_selector" in st.session_state:
        current_state_name = st.session_state.state_selector
    else:
        current_state_name = default_state

    # Coordenadas de Visão (Foco no estado selecionado)
    view_lat = nordeste_data[current_state_name]["lat"]
    view_lon = nordeste_data[current_state_name]["lon"]
    # Ajuste o zoom_start conforme necessário (7 costuma ser bom para estados médios)
    view_zoom = 7 

    # --- 3. CRIAÇÃO DO MAPA FOLIUM ---
    # Cria o objeto mapa forçando o centro e o zoom
    m = folium.Map(location=[view_lat, view_lon], zoom_start=view_zoom)

    # Adiciona os marcadores
    for estado, dados in nordeste_data.items():
        is_selected = (estado == current_state_name)
        
        # Cor do marcador: Vermelho se selecionado, Azul se não
        icon_color = 'red' if is_selected else 'blue'
        icon_prefix = 'fa' if is_selected else 'glyphicon' # Ícone diferente para destaque
        
        folium.Marker(
            [dados['lat'], dados['lon']],
            popup=f"{estado}: {dados['irradiacao']} kWh/m²",
            tooltip=estado,
            icon=folium.Icon(color=icon_color, icon='info-sign')
        ).add_to(m)

    # --- 4. LAYOUT VISUAL ---
    col_map_viz, col_chart_viz = st.columns([1, 1]) 

    with col_map_viz:
        st.subheader("📍 Localização Geográfica")
        # Renderiza o mapa Folium no Streamlit
        # height=450 garante o alinhamento com o gráfico ao lado
        st_folium(m, height=450, use_container_width=True)

    with col_chart_viz:
        st.subheader("☀️ Irradiação Média Regional")
        
        # Prepara dados grafico
        df_irr = pd.DataFrame.from_dict(nordeste_data, orient='index').reset_index()
        df_irr.columns = ['Estado', 'lat', 'lon', 'irradiacao', 'concessionaria', 'tusd_p', 'tusd_fp', 'te', 'icms', 'pis', 'cofins']
        df_irr = df_irr[['Estado', 'irradiacao']].sort_values(by='irradiacao')
        
        colors = ['#EF553B' if estado == current_state_name else '#d3d3d3' for estado in df_irr['Estado']]
        
        fig = px.bar(
            df_irr,
            x='irradiacao',
            y='Estado',
            orientation='h',
            text='irradiacao',
        )
        fig.update_traces(marker_color=colors, texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(
            yaxis_title=None,
            xaxis_title="GHI Médio (kWh/m²/dia)",
            height=450,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # --- 5. INPUTS E DADOS ---
    st.subheader("Definição de Parâmetros Tarifários (Grupo A4 - Verde)")

    # Selectbox controlando a variável 'state_selector'
    state_selected = st.selectbox(
        "Selecione o Estado do Cliente:",
        options=sorted(nordeste_data.keys()),
        key="state_selector" 
    )
    
    # Atualiza Session State Geral e Exibe Dados
    state_info = nordeste_data[state_selected]
    st.session_state['selected_state_data'] = state_info

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
    st.title("📊 Análise de Perfil e Demanda")
    
    # Verifica se já temos dados do estado (da página anterior)
    if 'selected_state_data' in st.session_state:
        dados_estado = st.session_state['selected_state_data']
        st.info(f"Base de cálculo: Tarifas de **{dados_estado.get('concessionaria', 'Estado Selecionado')}**")
    else:
        st.warning("⚠️ Nenhum estado selecionado na aba 'Cenário'. Usando valores padrão.")

    # --- 1. INPUTS DO CLIENTE ---
    st.subheader("1. Caracterização da Carga")
    
    col_input1, col_input2, col_input3 = st.columns(3)
    
    with col_input1:
        consumo_mensal = st.number_input(
            "Consumo Médio Mensal (kWh)", 
            min_value=100.0, 
            value=15000.0, 
            step=500.0,
            help="Média de consumo da fatura de energia."
        )
    
    with col_input2:
        perc_ponta = st.slider(
            "% Consumo na Ponta (18h-21h)", 
            min_value=0, 
            max_value=100, 
            value=15,
            help="Quanto do consumo total ocorre no horário de ponta."
        )
        # Cálculo automático da Fora Ponta
        perc_fora_ponta = 100 - perc_ponta
        st.caption(f"Consumo Fora Ponta: **{perc_fora_ponta}%**")

    with col_input3:
        perfil_tipo = st.selectbox(
            "Tipo de Perfil de Carga",
            ["Comunidade/Residencial", "Escola/Comercial Diurno", "Hospital/Industrial 24h"]
        )

    # --- 2. GERAÇÃO DA CURVA DE CARGA (SIMULAÇÃO) ---
    import numpy as np
    import pandas as pd

    # Definição dos perfis base (pesos horários de 0h a 23h)
    # Esses pesos dão o "formato" da curva
    perfis_base = {
        "Comunidade/Residencial": [
            0.4, 0.3, 0.3, 0.3, 0.4, 0.6, 1.0, 1.2, 1.0, 0.9, 0.9, 1.0, 
            1.1, 1.1, 1.0, 1.2, 1.5, 1.8, 2.5, 2.4, 2.2, 1.8, 1.2, 0.8
        ],
        "Escola/Comercial Diurno": [
            0.1, 0.1, 0.1, 0.1, 0.1, 0.2, 0.5, 1.5, 2.0, 2.2, 2.3, 2.2, 
            1.5, 2.3, 2.4, 2.3, 2.0, 1.0, 0.5, 0.2, 0.1, 0.1, 0.1, 0.1
        ],
        "Hospital/Industrial 24h": [
            0.8, 0.8, 0.8, 0.8, 0.8, 0.9, 1.0, 1.1, 1.2, 1.2, 1.2, 1.2, 
            1.2, 1.2, 1.2, 1.2, 1.1, 1.1, 1.0, 1.0, 0.9, 0.9, 0.8, 0.8
        ]
    }

    # Seleciona o perfil base
    curve_shape = np.array(perfis_base[perfil_tipo])
    
    # Horário de Ponta considerado (ex: 18h, 19h, 20h - 3 horas)
    indices_ponta = [18, 19, 20] 
    indices_fora_ponta = [h for h in range(24) if h not in indices_ponta]

    # --- ALGORITMO DE AJUSTE DE CURVA ---
    # Objetivo: Manter o formato, mas garantir que a soma da energia bata com o input do usuário
    
    consumo_diario = consumo_mensal / 30
    meta_ponta = consumo_diario * (perc_ponta / 100)
    meta_fora_ponta = consumo_diario * (perc_fora_ponta / 100)

    # Separa os pesos atuais do perfil base
    soma_pesos_ponta = sum(curve_shape[i] for i in indices_ponta)
    soma_pesos_fora = sum(curve_shape[i] for i in indices_fora_ponta)

    # Fatores de correção para atingir a meta
    fator_ponta = meta_ponta / soma_pesos_ponta if soma_pesos_ponta > 0 else 0
    fator_fora = meta_fora_ponta / soma_pesos_fora if soma_pesos_fora > 0 else 0

    # Cria a curva final ajustada (kW médio por hora)
    curva_final = np.zeros(24)
    for i in range(24):
        if i in indices_ponta:
            curva_final[i] = curve_shape[i] * fator_ponta
        else:
            curva_final[i] = curve_shape[i] * fator_fora

    # Cria DataFrame para o gráfico
    df_curva = pd.DataFrame({
        "Hora": list(range(24)),
        "Consumo (kW)": curva_final
    })
    df_curva.set_index("Hora", inplace=True)

    # --- 3. VISUALIZAÇÃO (Atualizado com Destaque na Ponta) ---
    import plotly.graph_objects as go

    st.markdown("---")
    st.subheader("2. Perfil de Carga Diário Estimado")
    
    col_graph, col_kpi = st.columns([3, 1])

    with col_graph:
        # Criação do Gráfico com Plotly para ter controle total
        fig = go.Figure()

        # Adiciona a curva de carga (Área preenchida)
        fig.add_trace(go.Scatter(
            x=df_curva.index,
            y=df_curva["Consumo (kW)"],
            fill='tozeroy',
            mode='lines',
            line=dict(width=2, color='#0068c9'),
            name='Demanda (kW)'
        ))

        # Adiciona o Retângulo de Destaque (Horário de Ponta: 18h as 21h)
        # O x0=18 e x1=20.9 garante que cubra as colunas das 18, 19 e 20h visualmente
        fig.add_vrect(
            x0=18, x1=21, 
            fillcolor="red", opacity=0.30, 
            layer="below", line_width=0,
            annotation_text="Horário de Ponta", 
            annotation_position="top left",
            annotation_font_color="red"
        )

        # Ajustes visuais do gráfico
        fig.update_layout(
        title="Curva de Carga Diária Típica",
        xaxis=dict(
            tickmode='linear',
            dtick=2,
            range=[0, 23.5],
            showgrid=False   # ❌ remove grid do eixo X
        ),
        yaxis=dict(
            showgrid=False   # ❌ remove grid do eixo Y
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=400,
        hovermode="x unified"
    )

        st.plotly_chart(fig, use_container_width=True)
        st.caption("A área sombreada em vermelho indica o período de Horário de Ponta (18h às 21h), onde a tarifa de energia é mais cara.")

    with col_kpi:
        st.markdown("##### Resumo Diário")
        pico_demanda = max(curva_final)
        hora_pico = np.argmax(curva_final)
        
        st.metric("Consumo Diário", f"{consumo_diario:,.0f} kWh")
        st.metric("Demanda Máxima", f"{pico_demanda:,.1f} kW", help=f"Ocorre às {hora_pico}h")
        
        # Métrica com cor diferente para chamar atenção
        st.markdown("---")
        st.metric("Consumo na Ponta", f"{meta_ponta:,.1f} kWh", delta=f"{perc_ponta}% do total", delta_color="inverse")
        st.metric("Consumo Fora Ponta", f"{meta_fora_ponta:,.1f} kWh")