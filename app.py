import streamlit as st
import google.generativeai as genai
from openai import OpenAI
import os
from datetime import datetime
import streamlit.components.v1 as components


greetings = ["Hello", "Bonjour", "你好", "Hola", "Ciao", "こんにちは", "Olá"]

components.html(f"""
<div class="typewriter-container">
    <div class="typewriter-text" id="typewriter"></div>
</div>

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

<style>
.typewriter-container {{
    text-align: center;
    margin-top: 20px;
}}
.typewriter-text {{
    font-size: 80px;
    font-weight: extrabold;
    color: #8b5cf6;
    font-family: 'Poppins', sans-serif;
}}
</style>
""", height=120)
st.set_page_config(
    page_title="WrapAI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with black-blue-purple gradient theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');    
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0b2e 25%, #16213e 50%, #0f3460 75%, #1a1a2e 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0221 0%, #1a0b2e 50%, #0f0524 100%);
        border-right: 2px solid rgba(138, 43, 226, 0.3);
        min-width: 320px !important;
        width: 320px !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 320px !important;
        width: 320px !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 320px !important;
        width: 320px !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #8b5cf6, #6366f1, #3b82f6);
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.6);
    }
    
    .stSlider [role="slider"] {
        background: #ffffff;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.8);
    }
    
    /* Selectbox styling */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(139, 92, 246, 0.4);
        color: #ffffff;
    }
    
    /* Expander styling */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 8px;
        color: #ffffff !important;
    }
    
    /* Neon button animation */
    @keyframes neon-border {
        0% {
            box-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6, 0 0 20px #8b5cf6;
        }
        25% {
            box-shadow: 0 0 10px #6366f1, 0 0 20px #6366f1, 0 0 30px #6366f1, 0 0 40px #6366f1;
        }
        50% {
            box-shadow: 0 0 5px #3b82f6, 0 0 10px #3b82f6, 0 0 15px #3b82f6, 0 0 20px #3b82f6;
        }
        75% {
            box-shadow: 0 0 10px #6366f1, 0 0 20px #6366f1, 0 0 30px #6366f1, 0 0 40px #6366f1;
        }
        100% {
            box-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6, 0 0 20px #8b5cf6;
        }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #a855f7 100%);
        color: #ffffff;
        border: 2px solid rgba(139, 92, 246, 0.5);
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
        position: relative;
        overflow: visible;
    }
    
    .stButton > button:hover {
        animation: neon-border 2s ease-in-out infinite;
        transform: translateY(-2px);
        background: linear-gradient(135deg, #7c3aed 0%, #9333ea 50%, #a855f7 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Typewriter animation */
    @keyframes blink {
        50% { border-color: transparent; }
    }
    
    @keyframes gradient-shift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .typewriter-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 60px;
        margin: 20px 0;
    }
    
    .typewriter-text {
        font-size: 48px;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6, #6366f1, #3b82f6, #8b5cf6);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradient-shift 3s ease infinite;
        white-space: nowrap;
        border-right: 3px solid #8b5cf6;
        animation: gradient-shift 3s ease infinite, blink 0.75s step-end infinite;
        min-height: 60px;
        display: inline-block;
    }
    
    .name-text {
        font-size: 56px;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-top: 20px;
        text-shadow: 0 0 20px rgba(139, 92, 246, 0.8), 0 0 40px rgba(99, 102, 241, 0.5);
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
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        color: #ffffff;
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
        position: relative;
    }
    
    @keyframes input-neon-border {
        0% {
            box-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6, 0 0 20px #8b5cf6;
            border-color: #8b5cf6;
        }
        25% {
            box-shadow: 0 0 10px #6366f1, 0 0 20px #6366f1, 0 0 30px #6366f1, 0 0 40px #6366f1;
            border-color: #6366f1;
        }
        50% {
            box-shadow: 0 0 5px #3b82f6, 0 0 10px #3b82f6, 0 0 15px #3b82f6, 0 0 20px #3b82f6;
            border-color: #3b82f6;
        }
        75% {
            box-shadow: 0 0 10px #6366f1, 0 0 20px #6366f1, 0 0 30px #6366f1, 0 0 40px #6366f1;
            border-color: #6366f1;
        }
        100% {
            box-shadow: 0 0 5px #8b5cf6, 0 0 10px #8b5cf6, 0 0 15px #8b5cf6, 0 0 20px #8b5cf6;
            border-color: #8b5cf6;
        }
    }
    
    .stTextInput > div > div > input:hover {
        animation: input-neon-border 2s ease-in-out infinite;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.6);
        animation: none;
    }
    
    /* Stat boxes */
    .stat-box {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        margin: 8px 0;
    }
    
    .stat-box h3 {
        color: #8b5cf6;
        font-size: 12px;
        font-weight: 600;
        margin: 0 0 8px 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stat-box p {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.5), transparent);
        margin: 24px 0;
    }
    
    /* Header */
    .header-title {
        font-size: 56px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #8b5cf6, #6366f1, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        text-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
    }
    
    .header-subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        font-size: 18px;
        margin-bottom: 40px;
    }
    
    /* Alert boxes */
    .stAlert {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        color: #ffffff;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Session state initialization
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

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size: 28px; font-weight: 700; margin-bottom: 24px; text-align: center;">Settings</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="font-size: 14px; margin-bottom: 8px; font-weight: 600; opacity: 0.9;">Select AI Model</div>', unsafe_allow_html=True)
    
    model_choice = st.selectbox(
        "Choose your AI model",
        ["Gemini", "OpenAI GPT"],
        key="model_select",
        label_visibility="collapsed"
    )
    st.session_state.model_selected = model_choice
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    with st.expander("Advanced Settings", expanded=False):
        st.markdown('<div style="font-size: 12px; margin-bottom: 16px; opacity: 0.8;">Fine-tune model behavior</div>', unsafe_allow_html=True)
        
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
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if st.button("Summarize Chat", use_container_width=True, key="summarize_btn"):
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


chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message-container user-message"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-container assistant-message"><strong>AI:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

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

if send_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    for m in genai.list_models():
        print(m.name)
    
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