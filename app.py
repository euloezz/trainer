import streamlit as st
from openai import OpenAI

# Configuração da Página
st.set_page_config(
    page_title="FitAI - Personal Trainer Futurista",
    page_icon="💪",
    layout="wide"
)

# --- ESTILO CSS FUTURISTA E WIDGET WHATSAPP ---
st.markdown("""
<style>
    /* Tema escuro futurista de fundo */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
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
    
    /* Botão flutuante estilo WhatsApp */
    .whatsapp-float {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        color: #0b0f19;
        border-radius: 50px;
        padding: 15px 25px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 20px rgba(0, 242, 254, 0.4);
        z-index: 999;
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
        transition: 0.3s;
    }
    .whatsapp-float:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(0, 242, 254, 0.6);
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
    st.markdown("### 🤖 Persona")
    st.info("O assistente está configurado como um **Personal Trainer Profissional** de elite.")

# --- ESTADO DA SESSÃO ---
if "messages" not in st.session_state:
    # System prompt definindo a persona estrita de Personal Trainer
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "Você é um Personal Trainer profissional, experiente, motivador e técnico. Seu objetivo é resolver qualquer dúvida sobre treinos, exercícios, biomecânica, periodização e nutrição esportiva básica. Responda com autoridade, clareza e foco em resultados seguros."
        }
    ]

if "last_topic" not in st.session_state:
    st.session_state.last_topic = "Bem-vindo ao Futuro do Treinamento"
if "last_image" not in st.session_state:
    st.session_state.last_image = "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=1000&auto=format&fit=crop"

# --- INTERFACE PRINCIPAL (DESIGN FUTURISTA) ---
st.markdown("<h1 style='text-align: center; background: linear-gradient(to right, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>⚡ NEXUS FIT TRAINING</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9ca3af;'>Sua plataforma inteligente de alta performance física.</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### 🧬 Painel de Análise e Execução")
    st.markdown(f"""
    <div class="content-card">
        <h3>Tópico Atual: <span style="color: #38bdf8;">{st.session_state.last_topic}</span></h3>
        <p>Aqui o sistema exibe os conceitos detalhados, dicas avançadas e diretrizes biomecânicas com base na sua última interação com o Personal Trainer ao lado.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### 📸 Referência Visual")
    st.markdown(f"""
    <div class="content-card" style="text-align: center;">
        <img src="{st.session_state.last_image}" style="width: 100%; border-radius: 12px; object-fit: cover; max-height: 250px;">
        <p style="margin-top: 10px; font-size: 14px; color: #9ca3af;">Ilustração técnica do exercício/foco atual</p>
    </div>
    """, unsafe_allow_html=True)

# --- POP-UP DO CHAT (ESTILO WHATSAPP) ---
# Usamos o popover nativo do Streamlit para simular a gaveta flutuante de chat
with st.popover("💬 Abrir Chat Personal", help="Clique para conversar com seu personal trainer"):
    st.markdown("### 🦾 Chatbot Personal Trainer")
    st.markdown("Tire suas dúvidas sobre treinos em tempo real.")
    
    # Exibir histórico (ignorando a mensagem system interna)
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input do chat
    if prompt := st.chat_input("Ex: Como montar um treino de hipertrofia para pernas?"):
        if not api_key:
            st.error("Insira sua Chave de API na barra lateral!")
        else:
            # Adiciona mensagem do usuário
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Resposta do assistente
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                message_placeholder.markdown("Analisando seu treino...")
                
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
                    
                    # Atualiza dinamicamente o painel principal com base na conversa
                    st.session_state.last_topic = prompt[:40] + "..."
                    if "costas" in prompt.lower() or "pulldown" in prompt.lower():
                        st.session_state.last_image = "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=1000&auto=format&fit=crop"
                    elif "perna" in prompt.lower() or "agachamento" in prompt.lower():
                        st.session_state.last_image = "https://images.unsplash.com/photo-1574680096145-d05b474e2155?q=80&w=1000&auto=format&fit=crop"
                    
                except Exception as e:
                    message_placeholder.error(f"Erro ao comunicar com a API: {e}")
