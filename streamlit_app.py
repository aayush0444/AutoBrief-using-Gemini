import streamlit as st
import pandas as pd
from utils.summarizer import summarize_data, eda_, eda_and_summarize, clarifier
from utils.analyzer import numerical_analysis, categorical_analysis

st.set_page_config(page_title="Dive in Data", page_icon="📊", layout="wide")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "df" not in st.session_state:
    st.session_state.df = None
if "chathistory" not in st.session_state:
    st.session_state.chathistory = {}

# Sidebar for file upload
with st.sidebar:
    st.title(" Dive in Data")
    st.markdown("### Auto Summarizer App")
    st.markdown("---")
    
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.success(f" Loaded {len(st.session_state.df)} rows")
        st.markdown(f"**Columns:** {len(st.session_state.df.columns)}")
    
    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    st.markdown("- Summarize this data")
    st.markdown("- Show me EDA")
    st.markdown("- EDA and summarize")
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chathistory = {}
        st.rerun()

# Main chat interface
st.title("💬 Chat with your Data")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
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
            with st.spinner("Analyzing..."):
                try:
                    # Prepare data
                    sample_data = st.session_state.df.sample(min(50, len(st.session_state.df)))
                    df_string = sample_data.to_csv(index=False)
                    
                    # Analyze dataset
                    eda_answers = {
                        'categorical_summary': categorical_analysis(st.session_state.df),
                        'numerical_summary': numerical_analysis(st.session_state.df)
                    }
                    
                    # Clarify user intent
                    res = clarifier(prompt.lower(), st.session_state.chathistory)
                    
                    summarizer_prompt = f'{prompt}+{df_string}'
                    
                    # Route to appropriate function
                    if 'eda and summarize' in res.text.lower():
                        response = eda_and_summarize(summarizer_prompt, eda_answers)
                        answer = response.text
                    elif 'only eda' in res.text.lower():
                        response = eda_(summarizer_prompt, eda_answers)
                        answer = response.text
                    elif 'only summarize' in res.text.lower():
                        response = summarize_data(summarizer_prompt)
                        answer = response.text
                    else:
                        # Default to EDA and summarize
                        response = eda_and_summarize(summarizer_prompt, eda_answers)
                        answer = response.text
                    
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})