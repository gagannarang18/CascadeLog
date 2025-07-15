import streamlit as st
import pandas as pd
import requests
from io import BytesIO
import os
import time

# Set page config
st.set_page_config(
    page_title="CascadeLog",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Get API URL from environment variable
FASTAPI_URL = os.getenv("FASTAPI_URL", "/api")


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
                    with st.spinner("🔍 Processing logs through API..."):
                        # Send file to FastAPI
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                        start_time = time.time()
                        response = requests.post(
                            f"{FASTAPI_URL}/classify/", 
                            files=files
                        )
                        processing_time = time.time() - start_time

                    if response.status_code == 200:
                        st.success("🎉 Analysis Complete!")
                        
                        # Read result CSV
                        result_df = pd.read_csv(BytesIO(response.content))
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            with st.expander("📊 Classification Results", expanded=True):
                                st.dataframe(result_df, use_container_width=True)

                        with col2:
                            st.subheader("📈 Performance Metrics")
                            st.metric("Total Logs Processed", len(result_df))
                            st.metric("Processing Time", f"{processing_time:.2f}s")

                            st.subheader("Label Distribution")
                            label_counts = result_df['target_label'].value_counts()
                            st.bar_chart(label_counts)

                        # Download result
                        csv = result_df.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            label="📥 Download Full Report",
                            data=csv,
                            file_name="cascadelog_results.csv",
                            mime="text/csv"
                        )
                    else:
                        st.error(f"❌ API Error: {response.text}")
            else:
                st.error("⚠️ Missing required columns: 'source' and 'log_message'")
        except Exception as e:
            st.error(f"❌ File processing error: {str(e)}")

if __name__ == "__main__":
    main()