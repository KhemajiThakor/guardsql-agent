import streamlit as st
import pandas as pd
from datetime import datetime

from api_service import APIService

st.set_page_config(
    page_title="GuardSQL",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

st.markdown("""
<style>
    /* Global */
    .stApp {
        background: #0a0a0a;
    }
    
    .main .block-container {
        padding: 180px 1rem 1rem 1rem !important;
        max-width: 900px !important;
    }
    
    /* Hide elements */
    #MainMenu, footer, header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stSidebar"] {display: none;}
    
    /* Messages */
    .message {
        display: flex;
        margin: 1rem 0;
        animation: fadeIn 0.3s;
    }
    
    .message-user {
        justify-content: flex-end;
    }
    
    .message-assistant {
        justify-content: flex-start;
    }
    
    .bubble {
        max-width: 75%;
        padding: 0.875rem 1.125rem;
        border-radius: 1.25rem;
        font-size: 0.9375rem;
        line-height: 1.5;
    }
    
    .bubble-user {
        background: #1e3a8a;
        color: #ffffff;
        border-bottom-right-radius: 0.25rem;
    }
    
    .bubble-assistant {
        background: #1f1f1f;
        color: #e5e5e5;
        border-bottom-left-radius: 0.25rem;
    }
    
    /* Loading */
    .loading {
        display: flex;
        gap: 0.375rem;
        padding: 0.875rem 1.125rem;
    }
    
    .dot {
        width: 8px;
        height: 8px;
        background: #666;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .dot:nth-child(1) { animation-delay: -0.32s; }
    .dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Input */
    .stTextArea textarea {
        background: #1f1f1f !important;
        color: #e5e5e5 !important;
        border: 1px solid #333 !important;
        border-radius: 1.25rem !important;
        font-size: 0.9375rem !important;
        padding: 0.875rem 1.125rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #1e3a8a !important;
        box-shadow: 0 0 0 1px #1e3a8a !important;
    }
    
    .stButton button {
        background: #1e3a8a !important;
        color: white !important;
        border: none !important;
        border-radius: 1.25rem !important;
        padding: 0.875rem 1.75rem !important;
        font-weight: 500 !important;
        transition: all 0.2s !important;
    }
    
    .stButton button:hover {
        background: #1e40af !important;
    }
    
    .stButton button:disabled {
        background: #333 !important;
        cursor: not-allowed !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 3px;
    }
    
    /* Error */
    .error {
        background: #7f1d1d;
        border: 1px solid #991b1b;
        color: #fca5a5;
        padding: 0.875rem;
        border-radius: 0.75rem;
        margin: 0.5rem 0;
    }
    
    /* Metrics */
    .metrics {
        display: flex;
        gap: 0.75rem;
        margin: 0.75rem 0;
        flex-wrap: wrap;
    }
    
    .metric {
        background: #0a0a0a;
        border: 1px solid #333;
        padding: 0.5rem 0.875rem;
        border-radius: 0.75rem;
        font-size: 0.8125rem;
    }
    
    .metric-value {
        color: #60a5fa;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .metric-label {
        color: #999;
        font-size: 0.75rem;
    }
    
    /* Table */
    .stDataFrame {
        background: #1f1f1f !important;
    }
</style>
""", unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_area(
            "Message",
            placeholder="Type your message... (Ctrl+Enter to send)",
            height=70,
            disabled=st.session_state.processing,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown('<div style="height: 12px;"></div>', unsafe_allow_html=True)
        send = st.form_submit_button(
            "Send",
            use_container_width=True,
            disabled=st.session_state.processing,
            type="primary"
        )

# Render messages below input
for idx, msg in enumerate(st.session_state.messages):
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="message message-user">
                <div class="bubble bubble-user">{msg["content"]}</div>
            </div>
        """, unsafe_allow_html=True)
    
    elif msg["role"] == "assistant":
        st.markdown("""
            <div class="message message-assistant">
                <div class="bubble bubble-assistant">
        """, unsafe_allow_html=True)
        
        if msg.get("error"):
            st.markdown(f'<div class="error">❌ {msg["error"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown("✅ Query executed successfully")
            
            st.markdown(f"""
                <div class="metrics">
                    <div class="metric">
                        <div class="metric-value">{msg["row_count"]}</div>
                        <div class="metric-label">Rows</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{msg["col_count"]}</div>
                        <div class="metric-label">Columns</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{msg["exec_time"]}ms</div>
                        <div class="metric-label">Time</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("📝 SQL", expanded=False):
                st.code(msg["sql"], language="sql")
            
            if msg["results"]:
                import pandas as pd
                df = pd.DataFrame(msg["results"])
                st.dataframe(df, use_container_width=True, height=300)
                
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download",
                    csv,
                    f"results_{idx}.csv",
                    "text/csv",
                    key=f"dl_{idx}"
                )
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    elif msg["role"] == "loading":
        st.markdown("""
            <div class="message message-assistant">
                <div class="bubble bubble-assistant">
                    <div class="loading">
                        <div class="dot"></div>
                        <div class="dot"></div>
                        <div class="dot"></div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

if send and user_input and not st.session_state.processing:
    st.session_state.processing = True
    
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    st.session_state.messages.append({
        "role": "loading"
    })
    
    st.rerun()

if st.session_state.messages and st.session_state.messages[-1]["role"] == "loading":
    st.session_state.messages.pop()
    
    user_msg = [m for m in st.session_state.messages if m["role"] == "user"][-1]["content"]
    
    result = APIService.execute_query(user_msg)
    
    if result["success"]:
        data = result["data"]
        st.session_state.messages.append({
            "role": "assistant",
            "sql": data["sql"],
            "row_count": data["row_count"],
            "col_count": len(data["columns"]),
            "exec_time": data["execution_time_ms"],
            "results": data["results"],
            "columns": data["columns"]
        })
    else:
        st.session_state.messages.append({
            "role": "assistant",
            "error": result["error"]
        })
    
    st.session_state.processing = False
    st.rerun()

if st.session_state.messages:
    st.markdown('<script>window.scrollTo(0, document.body.scrollHeight);</script>', unsafe_allow_html=True)
