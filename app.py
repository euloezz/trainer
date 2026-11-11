import streamlit as st
from openai import OpenAI

# Configuração da Página
st.set_page_config(
    page_title="FitAI - Personal Trainer",
    page_icon="💪",
    layout="wide"
)

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

# --- INTERFACE PRINCIPAL ---
st.title("⚡ NEXUS FIT TRAINING")
st.markdown("Plataforma inteligente de treinamento biomecânico e consultoria física.")
st.divider()

# Layout em duas colunas principais para garantir visibilidade total
col_chat, col_info = st.columns([1, 1], gap="large")

# --- COLUNA DA ESQUERDA: CHATBOT ---
with col_chat:
    st.subheader("💬 Chatbot Personal Trainer")
    
    chat_container = st.container(height=450)
    
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

    prompt = st.chat_input("Digite sua dúvida sobre treino ou exercício...")
    if prompt:
        if not api_key:
            st.error("Insira sua Chave de API na barra lateral esquerda!")
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
                        
                        # Atualiza dinamicamente o painel lateral com base na conversa
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
                        message_placeholder.error(f"Erro na API: {e}")

# --- COLUNA DA DIREITA: PAINEL DE INFORMAÇÕES E IMAGENS ---
with col_info:
    st.subheader("🧬 Painel Dinâmico & Referência")
    st.info(f"**Foco Atual:** {st.session_state.last_topic}")
    st.markdown("""
    Esta área exibe em tempo real o contexto da sua consulta com o personal trainer. 
    À medida que conversa, as orientações chave e as referências visuais adaptam-se automaticamente ao exercício discutido.
    """)
    st.image(st.session_state.last_image, use_container_width=True, caption="Ilustração técnica do exercício atual")
