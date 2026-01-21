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
    st.write("Em construção...")

elif page == "Análise":
    st.title("📊 Análise de Resultados")
    st.write("Em construção...")