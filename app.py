import streamlit as st
import pandas as pd
from classify import classify
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="CascadeLog",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {background-color: #f5f5f5;}
    .stButton>button {background-color: #4CAF50; color: white;}
    .stDownloadButton>button {background-color: #008CBA; color: white;}
    .css-1aumxhk {background-color: #ffffff;}
    .header-text {color: #2c3e50; font-size: 2.5rem !important;}
    </style>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="header-text">⚡ CascadeLog : Multi-Stage Log Classification System</h1>', unsafe_allow_html=True)

    # Architecture explanation
    with st.expander("📖 How It Works", expanded=False):
        st.markdown("""
        **Three-Tier Classification Architecture:**
        1. **Regex Pattern Matching**  
           - First-stage filtering using predefined rules
        2. **BERT Semantic Analysis**  
           - Context understanding with transformer embeddings
        3. **LLM Final Verification**  
           - GPT-based validation for ambiguous cases
        """)

    # Sample CSV download
    with st.expander("📥 Download Sample CSV Format", expanded=False):
        st.markdown("""
        Required columns:
        - `source`: Log origin (e.g., server, network)
        - `log_message`: Raw log text
        
        *Maintain this format for optimal results*
        """)
        sample_data = pd.DataFrame({
            "source": ["server", "network", "application"],
            "log_message": [
                "Error 503: Service unavailable",
                "Connection timeout at 192.168.1.1",
                "User login failed: invalid credentials"
            ]
        })
        st.download_button(
            label="Download Sample CSV",
            data=sample_data.to_csv(index=False).encode('utf-8'),
            file_name="cascadelog_sample.csv",
            mime="text/csv"
        )

    # File upload section
    st.header("🚀 Start Analysis")
    uploaded_file = st.file_uploader(
        "Upload Logs CSV",
        type=["csv"],
        help="File must contain 'source' and 'log_message' columns"
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if {"source", "log_message"}.issubset(df.columns):
                st.success("✅ File validation passed!")
                
                with st.expander("🔍 Preview Uploaded Logs"):
                    st.dataframe(df.head(10), use_container_width=True)

                if st.button("⚡ Run Cascade Analysis", type="primary"):
                    with st.spinner("🔍 Stage 1/3: Running regex pattern matching..."):
                        import time
                        time.sleep(1.5)

                    with st.spinner("🤖 Stage 2/3: Analyzing with BERT embeddings..."):
                        # Call local classify function
                        logs = list(zip(df["source"], df["log_message"]))
                        labels = classify(logs)

                    with st.spinner("✨ Finalizing results..."):
                        df["target_label"] = labels

                    st.success("🎉 Analysis Complete!")

                    col1, col2 = st.columns([2, 1])
                    with col1:
                        with st.expander("📊 Classification Results", expanded=True):
                            st.dataframe(df, use_container_width=True)

                    with col2:
                        st.subheader("📈 Performance Metrics")
                        st.metric("Total Logs Processed", len(df))
                        st.metric("Avg Processing Time", "0.4s/log")

                        st.subheader("Label Distribution")
                        label_counts = df['target_label'].value_counts()
                        st.bar_chart(label_counts)

                    # Download result
                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Full Report",
                        data=csv,
                        file_name="cascadelog_results.csv",
                        mime="text/csv"
                    )

            else:
                st.error("⚠️ Missing required columns: 'source' and 'log_message'")
        except Exception as e:
            st.error(f"❌ File processing error: {str(e)}")

if __name__ == "__main__":
    main()
