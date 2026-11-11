import streamlit as st
from openai import OpenAI

# Configuração da Página
st.set_page_config(
    page_title="FitAI - Personal Trainer Futurista",
    page_icon="💪",
    layout="wide"
)

# --- ESTILO CSS FUTURISTA E CORREÇÃO DO TEMA ESCURO ---
st.markdown("""
<style>
    /* Fundo geral escuro da aplicação */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Forçar fundo escuro e texto claro na barra lateral */
    [data-testid="stSidebar"] {
        background-color: #111827;
        color: #f3f4f6;
    }
    
    /* Estilizar inputs de texto para combinar com o design futurista */
    .stTextInput input, .stTextArea textarea {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px;
    }
    
    /* Estilo dos cards de conteúdo principal */
    .content-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (CONFIGURAÇÕES DA API) ---
with st.sidebar:
    st.markdown("## ⚙️ Configurações da IA")
    api_key = st.text_input("Chave da API (API Key):", type="password", placeholder="sk-...")
    endpoint = st.text_input(
        "Endpoint da API:", 
        value="https://api.openai.com/v1",
        help="URL base do provedor"
    )
    model_name = st.text_input(
        "Nome do Modelo:", 
        value="gpt-4o-mini",
        help="Ex: gpt-4o, llama-3, etc."
    )
    st.divider()
    st.markdown("### 🤖 Persona Ativa")
    st.info("Assistente configurado estritamente como **Personal Trainer Profissional** de elite.")

# --- ESTADO DA SESSÃO ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "Você é um Personal Trainer profissional, experiente, motivador e técnico. Seu objetivo é resolver qualquer dúvida sobre treinos, exercícios, biomecânica, periodização e nutrição esportiva básica. Responda com autoridade, clareza e foco em resultados seguros."
        }
    ]

if "last_topic" not in st.session_state:
    st.session_state.last_topic = "Visão Geral de Alta Performance"
if "last_image" not in st.session_state:
    st.session_state.last_image = "
