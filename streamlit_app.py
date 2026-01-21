import streamlit as st

# 1. Configuração da Página (Aba do Navegador)
st.set_page_config(
    page_title="Análise BESS",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR (Barra Lateral) ---
with st.sidebar:
    # 2. Espaço para a Logo
    # Substitua "logo.png" pelo caminho da sua imagem quando tiver o arquivo.
    # Coloquei um link de exemplo para você ver o layout funcionando.
    st.image("https://placehold.co/250x100/png?text=LOGO+BESS", use_container_width=True)
    
    st.markdown("---") # Linha divisória para estética
    
    st.header("Menu Principal")
    
    # 3. Menu de Navegação (Estilo Radio Button igual à imagem)
    page = st.radio(
        "Navegue pelas seções:",
        ["Página Inicial", "Cenário", "Análise"]
    )

# --- CONTEÚDO PRINCIPAL (Muda conforme a seleção) ---

if page == "Página Inicial":
    st.title("🏠 Página Inicial")
    st.write("Bem-vindo à plataforma de Análise Econômica do BESS.")
    st.info("Utilize o menu lateral para navegar entre a configuração de cenários e a análise de resultados.")

elif page == "Cenário":
    st.title("⚙️ Configuração de Cenário")
    st.write("Aqui definiremos as variáveis do projeto (CAPEX, Bateria, Tarifas).")
    # Futuramente colocaremos os inputs aqui

elif page == "Análise":
    st.title("📊 Análise de Resultados")
    st.write("Aqui serão exibidos os gráficos e indicadores financeiros.")
    # Futuramente colocaremos os gráficos aqui