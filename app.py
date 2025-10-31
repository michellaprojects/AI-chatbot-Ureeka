import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import os
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(
    page_title="WrapAI",
    layout="wide",
    initial_sidebar_state="expanded"
)

greetings = ["Hello", "Bonjour", "你好", "Hola", "Ciao", "こんにちは", "Olá"]

if "messages" not in st.session_state:
    st.session_state.messages = []
if "model_selected" not in st.session_state:
    st.session_state.model_selected = "Gemini"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "top_p" not in st.session_state:
    st.session_state.top_p = 0.9
if "top_k" not in st.session_state:
    st.session_state.top_k = 40
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 2048

if len(st.session_state.messages) == 0:
    st.markdown("""
    <style>
    .centered-greeting {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1;
    }
    .typewriter-text {
        font-size: 80px;
        font-weight: 900;
        background: linear-gradient(135deg, #8b5cf6, #6366f1, #3b82f6, #8b5cf6);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    components.html(f"""
    <style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    body, html {{
        background: transparent !important;
        overflow: hidden;
    }}
    .typewriter-text {{
        font-size: 80px;
        font-weight: 900;
        background: linear-gradient(135deg, #8b5cf6, #6366f1, #3b82f6, #8b5cf6);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
        font-family: 'Poppins', sans-serif;
        text-align: center;
    }}
    @keyframes gradient-shift {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    </style>
    <div class="typewriter-text" id="typewriter"></div>
    <script>
    const greetings = {greetings};
    let currentIndex = 0;
    let currentText = '';
    let isDeleting = false;
    let charIndex = 0;

    function typeWriter() {{
        const element = document.getElementById('typewriter');
        const currentGreeting = greetings[currentIndex];
        
        if (!isDeleting && charIndex < currentGreeting.length) {{
            currentText = currentGreeting.substring(0, charIndex + 1);
            charIndex++;
            element.textContent = currentText;
            setTimeout(typeWriter, 150);
        }} else if (isDeleting && charIndex > 0) {{
            currentText = currentGreeting.substring(0, charIndex - 1);
            charIndex--;
            element.textContent = currentText;
            setTimeout(typeWriter, 100);
        }} else if (!isDeleting && charIndex === currentGreeting.length) {{
            isDeleting = true;
            setTimeout(typeWriter, 2000);
        }} else if (isDeleting && charIndex === 0) {{
            isDeleting = false;
            currentIndex = (currentIndex + 1) % greetings.length;
            setTimeout(typeWriter, 500);
        }}
    }}
    setTimeout(typeWriter, 100);
    </script>
    """, height=600)



st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');    
    
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0b2e 25%, #16213e 50%, #0f3460 75%, #1a1a2e 100%) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Sidebar styling - Fixed */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0221 0%, #1a0b2e 50%, #0f0524 100%) !important;
        border-right: 2px solid rgba(138, 43, 226, 0.3) !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: linear-gradient(180deg, #0d0221 0%, #1a0b2e 50%, #0f0524 100%) !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Sidebar text elements */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    
    /* Slider styling - Fixed */
    [data-testid="stSidebar"] .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #8b5cf6, #6366f1, #3b82f6) !important;
    }
    
    [data-testid="stSidebar"] .stSlider [role="slider"] {
        background: #ffffff !important;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.8) !important;
    }
    
    /* Selectbox styling - Fixed */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(139, 92, 246, 0.4) !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
    }
    
    /* Expander styling - Fixed */
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: rgba(139, 92, 246, 0.15) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        color: #ffffff !important;
    }
    
    @keyframes neon-snake {
        0% {
            box-shadow: 
                5px 0 15px #8b5cf6,
                0 0 5px #8b5cf6;
        }
        12.5% {
            box-shadow: 
                5px 5px 15px #6366f1,
                0 0 5px #6366f1;
        }
        25% {
            box-shadow: 
                0 5px 15px #3b82f6,
                0 0 5px #3b82f6;
        }
        37.5% {
            box-shadow: 
                -5px 5px 15px #6366f1,
                0 0 5px #6366f1;
        }
        50% {
            box-shadow: 
                -5px 0 15px #8b5cf6,
                0 0 5px #8b5cf6;
        }
        62.5% {
            box-shadow: 
                -5px -5px 15px #6366f1,
                0 0 5px #6366f1;
        }
        75% {
            box-shadow: 
                0 -5px 15px #3b82f6,
                0 0 5px #3b82f6;
        }
        87.5% {
            box-shadow: 
                5px -5px 15px #6366f1,
                0 0 5px #6366f1;
        }
        100% {
            box-shadow: 
                5px 0 15px #8b5cf6,
                0 0 5px #8b5cf6;
        }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
    }
    
    .stButton > button:hover {
        animation: neon-snake 2s linear infinite !important;
        transform: translateY(-2px) !important;
        background: linear-gradient(135deg, #7c3aed 0%, #9333ea 50%, #a855f7 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Message containers */
    .message-container {
        padding: 16px 20px;
        margin: 12px 0;
        border-radius: 16px;
        animation: fadeIn 0.4s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.15));
        border-left: 4px solid #6366f1;
        color: #ffffff;
        margin-left: 20%;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(168, 85, 247, 0.1));
        border-left: 4px solid #8b5cf6;
        color: #ffffff;
        margin-right: 20%;
    }
    
    /* Snake neon light animation for input field */
    @keyframes input-neon-snake {
        0% {
            box-shadow: 
                5px 0 15px #8b5cf6,
                0 0 5px #8b5cf6;
            border-color: #8b5cf6;
        }
        12.5% {
            box-shadow: 
                5px 5px 15px #6366f1,
                0 0 5px #6366f1;
            border-color: #6366f1;
        }
        25% {
            box-shadow: 
                0 5px 15px #3b82f6,
                0 0 5px #3b82f6;
            border-color: #3b82f6;
        }
        37.5% {
            box-shadow: 
                -5px 5px 15px #6366f1,
                0 0 5px #6366f1;
            border-color: #6366f1;
        }
        50% {
            box-shadow: 
                -5px 0 15px #8b5cf6,
                0 0 5px #8b5cf6;
            border-color: #8b5cf6;
        }
        62.5% {
            box-shadow: 
                -5px -5px 15px #6366f1,
                0 0 5px #6366f1;
            border-color: #6366f1;
        }
        75% {
            box-shadow: 
                0 -5px 15px #3b82f6,
                0 0 5px #3b82f6;
            border-color: #3b82f6;
        }
        87.5% {
            box-shadow: 
                5px -5px 15px #6366f1,
                0 0 5px #6366f1;
            border-color: #6366f1;
        }
        100% {
            box-shadow: 
                5px 0 15px #8b5cf6,
                0 0 5px #8b5cf6;
            border-color: #8b5cf6;
        }
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 12px 16px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        animation: input-neon-snake 2s linear infinite !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stat-box {
        background: rgba(139, 92, 246, 0.1) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 12px !important;
        padding: 16px !important;
        text-align: center !important;
        margin: 8px 0 !important;
    }
    
    .stat-box h3 {
        color: #8b5cf6 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        margin: 0 0 8px 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stat-box p {
        color: #ffffff !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        margin: 0 !important;
    }
    
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
        margin: 24px 0;
    }
    
    .stAlert {
        background: rgba(139, 92, 246, 0.08) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size: 28px; font-weight: 700; margin-bottom: 24px; text-align: center; color: #ffffff !important;">Settings</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="font-size: 14px; margin-bottom: 8px; font-weight: 600; opacity: 0.9; color: #ffffff !important;">Select AI Model</div>', unsafe_allow_html=True)
    
    model_choice = st.selectbox(
        "Choose your AI model",
        ["Gemini", "OpenAI GPT"],
        key="model_select",
        label_visibility="collapsed"
    )
    st.session_state.model_selected = model_choice
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    with st.expander("Advanced Settings", expanded=False):
        st.markdown('<div style="font-size: 12px; margin-bottom: 16px; opacity: 0.8; color: #ffffff !important;">Fine-tune model behavior</div>', unsafe_allow_html=True)
        
        st.session_state.temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        st.session_state.top_p = st.slider(
            "Top-P (Nucleus Sampling)",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.top_p,
            step=0.05,
            help="Controls diversity via nucleus sampling"
        )
        
        st.session_state.top_k = st.slider(
            "Top-K",
            min_value=1,
            max_value=100,
            value=st.session_state.top_k,
            step=1,
            help="Limits token choices to top K"
        )
        
        st.session_state.max_tokens = st.slider(
            "Max Tokens",
            min_value=256,
            max_value=4096,
            value=st.session_state.max_tokens,
            step=256,
            help="Maximum response length"
        )
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("Summarize", use_container_width=True, key="summarize_btn"):
        if st.session_state.messages:
            with st.spinner("Generating summary..."):
                conversation_text = "\n".join([
                    f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                    for msg in st.session_state.messages
                ])
                
                try:
                    if st.session_state.model_selected == "Gemini":
                        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])                        
                        model = genai.GenerativeModel("models/gemini-2.0-flash")
                        response = model.generate_content(
                            f"Provide a concise summary of this conversation:\n\n{conversation_text}",
                            generation_config=genai.types.GenerationConfig(
                                temperature=st.session_state.temperature,
                                top_p=st.session_state.top_p,
                                top_k=st.session_state.top_k,
                                max_output_tokens=st.session_state.max_tokens
                            )
                        )
                        summary = response.text
                    else:
                        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
                        response = client.chat.completions.create(
                            model="gpt-4o-mini",
                            messages=[{
                                "role": "user",
                                "content": f"Provide a concise summary of this conversation:\n\n{conversation_text}"
                            }],
                            temperature=st.session_state.temperature,
                            top_p=st.session_state.top_p,
                            max_tokens=st.session_state.max_tokens
                        )
                        summary = response.choices[0].message.content
                    st.markdown('<div class="stat-box"><h3>Chat Summary</h3></div>', unsafe_allow_html=True)
                    st.info(summary)
                except Exception as e:
                    st.error(f"Error generating summary: {str(e)}")
        else:
            st.warning("No messages to summarize yet")
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stat-box"><h3>Messages</h3><p>{len(st.session_state.messages)}</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-box"><h3>Model</h3><p>{st.session_state.model_selected[:3]}</p></div>', unsafe_allow_html=True)


# Center container for chat messages
st.markdown('<div style="max-width: 900px; margin: 0 auto;">', unsafe_allow_html=True)

chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message-container user-message"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-container assistant-message"><strong>AI:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Center the input area
st.markdown('<div style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)

col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Your message",
        placeholder="Type your message here...",
        label_visibility="collapsed",
        key="user_input"
    )

with col2:
    send_button = st.button("Send", use_container_width=True, key="send_btn")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    try:
        if st.session_state.model_selected == "Gemini":
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel("models/gemini-2.0-flash")
            response = model.generate_content(
                user_input,
                generation_config=genai.types.GenerationConfig(
                    temperature=st.session_state.temperature,
                    top_p=st.session_state.top_p,
                    top_k=st.session_state.top_k,
                    max_output_tokens=st.session_state.max_tokens
                )
            )
            assistant_message = response.text
        else:
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_input}],
                temperature=st.session_state.temperature,
                top_p=st.session_state.top_p,
                max_tokens=st.session_state.max_tokens
            )
            assistant_message = response.choices[0].message.content
        
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        st.rerun()
    
    except Exception as e:
        st.error(f"Error: {str(e)}")