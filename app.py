import streamlit as st
from openai import OpenAI

# Configuração da Página
st.set_page_config(
    page_title="FitAI - Personal Trainer Futurista",
    page_icon="💪",
    layout="wide"
)

# --- ESTILO CSS PARA O WIDGET FLUTUANTE E TEMA ESCURO ---
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
    st.info("Assistente configurado como **Personal Trainer Profissional**.")

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
    st.session_state.last_image = "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1000&auto=format&fit=crop"

# --- INTERFACE PRINCIPAL (DESIGN FUTURISTA) ---
st.markdown("<h1 style='text-align: center; background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⚡ NEXUS FIT TRAINING</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Plataforma inteligente de treinamento biomecânico e consultoria física.</p>", unsafe_allow_html=True)
st.divider()

# --- WIDGET POP-UP FLUTUANTE (CANTO INFERIOR DIREITO) ---
with st.popover("💬 Chat Personal Online"):
    st.markdown("### 🎧 Personal Trainer Online")
    st.markdown("<p style='font-size: 12px; color: #10b981; margin-top: -15px;'>● online agora</p>", unsafe_allow_html=True)
    st.divider()
    
    chat_container = st.container(height=350)
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    prompt = st.chat_input("Digite sua dúvida ou exercício...")
    if prompt:
        if not api_key:
            st.error("Insira sua Chave de API na barra lateral!")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            with chat_container:
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("Analisando...")
                    
                    try:
                        client = OpenAI(api_key=api_key, base_url=endpoint)
                        response = client.chat.completions.create(
                            model=model_name,
                            messages=st.session_state.messages,
                            stream=True
                        )
                        
                        full_response = ""
                        for chunk in response:
                            if chunk.choices[0].delta.content is not None:
                                full_response += chunk.choices[0].delta.content
                                message_placeholder.markdown(full_response + "▌")
                        
                        message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})
                        
                        # Atualiza dinamicamente o painel lateral de imagens/tópicos
                        p_lower = prompt.lower()
                        st.session_state.last_topic = prompt[:45] + "..."
                        if "costas" in p_lower or "puxada" in p_lower or "dorsal" in p_lower:
                            st.session_state.last_image = "
