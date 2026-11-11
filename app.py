import streamlit as st
from openai import OpenAI

# Configuração da Página
st.set_page_config(
    page_title="FitAI - Personal Trainer Futurista",
    page_icon="💪",
    layout="wide"
)

# --- ESTILO CSS FUTURISTA + FUNDO ESTILO WHATSAPP ---
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    [data-testid="stSidebar"] {
        background-color: #111827;
        color: #f3f4f6;
    }
    
    .stTextInput input, .stTextArea textarea {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid rgba(59, 130, 246, 0.3) !important;
        border-radius: 8px;
    }
    
    .content-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }

    /* Fundo estilo WhatsApp Dark Mode para o container do chat */
    .whatsapp-chat-bg {
        background-color: #0b141a !important;
        background-image: radial-gradient(circle, rgba(255, 255, 255, 0.05) 1px, transparent 1px);
        background-size: 20px 20px;
        border-radius: 12px;
        padding: 10px;
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
        help="Ex: gpt-4o-mini, gpt-4o, etc."
    )
    st.divider()
    st.markdown("### 🤖 Persona Ativa")
    st.info("Assistente configurado estritamente como **Personal Trainer Profissional** de elite.")

# --- ESTADO DA SESSÃO ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "Você é um Personal Trainer profissional, experiente, motivador e técnico. Seu objetivo é resolver qualquer dúvida sobre treinos, exercícios, biomecânica e periodização."
        }
    ]

if "last_topic" not in st.session_state:
    st.session_state.last_topic = "Visão Geral de Alta Performance"
if "last_image" not in st.session_state:
    st.session_state.last_image = "https://images.unsplash.com/photo-1517838277536-f5f99be501cd"

# --- INTERFACE PRINCIPAL DO SITE ---
st.markdown("<h1 style='text-align: center; background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⚡ NEXUS FIT TRAINING</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Plataforma inteligente de treinamento biomecânico e consultoria física.</p>", unsafe_allow_html=True)
st.divider()

# --- BOTÃO DE ACESSO AO CHAT ---
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    chat_popover = st.popover("💬 Abrir Chat com o Personal Trainer", use_container_width=True)

with chat_popover:
    st.markdown("### 🦾 Chatbot Personal Trainer")
    st.markdown('<p style="font-size: 12px; color: #10b981; margin-top: -10px;">● online agora</p>', unsafe_allow_html=True)
    st.divider()
    
    # Container estilizado estilo WhatsApp Dark
    st.markdown('<div class="whatsapp-chat-bg">', unsafe_allow_html=True)
    chat_container = st.container(height=350)
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    st.markdown('</div>', unsafe_allow_html=True)

    prompt = st.chat_input("Digite sua dúvida de treino...")
