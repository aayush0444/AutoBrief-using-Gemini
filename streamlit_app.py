import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.smart_analyzer import SmartAnalyzer

st.set_page_config(page_title="Dive in Data", page_icon="📊", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "analyzer" not in st.session_state:
    st.session_state.analyzer = None
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = []

# Sidebar
with st.sidebar:
    st.title("📊 Dive in Data")
    st.markdown("### Smart Data Analysis Chat")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.session_state.analyzer = SmartAnalyzer(st.session_state.df)
        st.success(f"✅ Loaded {len(st.session_state.df)} rows")
        st.markdown(f"**Columns:** {len(st.session_state.df.columns)}")
        
        with st.expander("📋 Column Names"):
            for col in st.session_state.df.columns:
                st.text(f"• {col}")
    
    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    st.markdown("- What's in this data?")
    st.markdown("- Show trends in sales over time")
    st.markdown("- Compare prices by category")
    st.markdown("- Plot age vs salary")
    st.markdown("- What's the average revenue?")
    st.markdown("- Show me missing values")
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.conversation_context = []
        st.rerun()

# Main chat interface
st.title("💬 Chat with your Data")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"])
            if "chart" in message and message["chart"]:
                st.plotly_chart(message["chart"], use_container_width=True)
        else:
            st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your data..."):
    if st.session_state.df is None:
        st.warning("⚠️ Please upload a CSV file first!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Get smart response with chart
                    result = st.session_state.analyzer.process_query(
                        prompt, 
                        st.session_state.conversation_context
                    )
                    
                    # Display text response
                    st.markdown(result['response'])
                    
                    # Display chart if generated
                    chart = None
                    if result['chart']:
                        st.plotly_chart(result['chart'], use_container_width=True)
                        chart = result['chart']
                    
                    # Save to messages
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": result['response'],
                        "chart": chart
                    })
                    
                    # Update context
                    st.session_state.conversation_context.append({
                        "user": prompt,
                        "assistant": result['response'][:300]
                    })
                    
                    # Keep only last 3 exchanges in context
                    if len(st.session_state.conversation_context) > 3:
                        st.session_state.conversation_context.pop(0)
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg, "chart": None})