import streamlit as st
from openai import AzureOpenAI

# Configuração da Página
st.set_page_config(
    page_title="FitAI - Personal Trainer Futurista",
    page_icon="💪",
    layout="wide"
)

# --- ESTILO CSS PARA O WIDGET FLUTUANTE ESTILO WHATSAPP (CANTO INFERIOR DIREITO) ---
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

    /* Estilização para o Popover simular o widget flutuante do WhatsApp */
    [data-testid="stPopover"] {
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        z-index: 999999 !important;
    }
    
    [data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%) !important;
        color: #0b0f19 !important;
        border-radius: 50px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        font-size: 15px !important;
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.4) !important;
        border: none !important;
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
    st.markdown("## ⚙️ Configurações da IA (Azure Foundry)")
    api_key = st.text_input("Chave da API (API Key):", type="password", placeholder="Insira sua chave do Foundry...")
    endpoint = st.text_input(
        "Endpoint da API:", 
        value="https://seu-recurso.cognitiveservices.azure.com/",
        help="URL base do endpoint do seu recurso no Azure AI Foundry"
    )
    model_name = st.text_input(
        "Nome do Deployment / Modelo:", 
        value="gpt-4.1-mini",
        help="Insira exatamente o nome do deployment criado no Foundry"
    )
    api_version = st.text_input(
        "Versão da API (Azure):",
        value="2024-08-01-preview",
        help="Versão da API do Azure"
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
    st.session_state.last_image = "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1000&auto=format&fit=crop"

# --- INTERFACE PRINCIPAL DO SITE ---
st.markdown("<h1 style='text-align: center; background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⚡ NEXUS FIT TRAINING</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Plataforma inteligente de treinamento biomecânico e consultoria física.</p>", unsafe_allow_html=True)
st.divider()

# --- WIDGET POP-UP FLUTUANTE (FIXO NO CANTO INFERIOR DIREITO VIA CSS) ---
with st.popover("💬 Suporte de Personal Online"):
    st.markdown("### 🦾 Chatbot Personal Trainer")
    st.markdown("<p style='font-size: 12px; color: #10b981; margin-top: -10px;'>● online agora</p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown('<div class="whatsapp-chat-bg">', unsafe_allow_html=True)
    chat_container = st.container(height=350)
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
    st.markdown('</div>', unsafe_allow_html=True)

    prompt = st.chat_input("Digite sua dúvida de treino...")
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
                        # Utilizando a classe nativa AzureOpenAI para direcionar corretamente as rotas do Azure
                        client = AzureOpenAI(
                            api_key=api_key,
                            azure_endpoint=endpoint,
                            api_version=api_version
                        )
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
                        
                        # Atualiza dinamicamente o painel de imagens ao lado
                        p_lower = prompt.lower()
                        st.session_state.last_topic = prompt[:45] + "..."
                        if "costas" in p_lower or "puxada" in p_lower or "dorsal" in p_lower:
                            st.session_state.last_image = "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=1000&auto=format&fit=crop"
                        elif "perna" in p_lower or "agachamento" in p_lower or "quadriceps" in p_lower:
                            st.session_state.last_image = "https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1000&auto=format&fit=crop"
                        elif "peito" in p_lower or "supino" in p_lower:
                            st.session_state.last_image = "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1000&auto=format&fit=crop"
                        
                        st.rerun()
                        
                    except Exception as e:
                        message_placeholder.error(f"Erro na API do Foundry: {e}")

# --- ÁREA DINÂMICA PRINCIPAL (PAINEL + IMAGENS) ---
col1, col2 = st.columns([1.5, 1], gap="large")

with col1:
    st.markdown("### 🧬 Painel de Informações e Diretrizes")
    st.markdown(f"""
    <div class="content-card">
        <h3>Foco Atual: <span style="color: #00f2fe;">{st.session_state.last_topic}</span></h3>
        <p style="color: #d1d5db; line-height: 1.6;">
            Esta área exibe em tempo real o contexto da sua consulta com o personal trainer. 
            Clique no botão flutuante no canto inferior direito para abrir a conversa, 
            e veja as orientações e referências visuais atualizarem-se automaticamente aqui.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📸 Referência Visual do Exercício")
    st.markdown(f"""
    <div class="content-card" style="text-align: center;">
        <img src="{st.session_state.last_image}" style="width: 100%; border-radius: 12px; object-fit: cover; max-height: 280px; border: 1px solid rgba(0, 242, 254, 0.3);">
        <p style="margin-top: 12px; font-size: 13px; color: #9ca3af;">Ilustração dinâmica baseada no último tópico consultado</p>
    </div>
    """, unsafe_allow_html=True)
