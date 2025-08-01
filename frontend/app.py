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

FASTAPI_URL = st.secrets["FASTAPI_URL"]

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

    with st.expander("📥 Download Sample CSV Format", expanded=False):
        st.markdown("""
        Required columns:
        - `source`: Log origin (e.g., server, network)
        - `log_message`: Raw log text

        *Maintain this format for optimal results*
        """)
        sample_data = pd.DataFrame({
            "source": [
                "ModernCRM",
                "BillingSystem",
                "AnalyticsEngine",
                "AnalyticsEngine",
                "ModernHR",
                "ModernHR",
                "LegacyCRM",
                "LegacyCRM",
                "LegacyCRM",
                "LegacyCRM"
            ],
            "log_message": [
                "IP 192.168.133.114 blocked due to potential attack",
                "User 12345 logged in.",
                "File data_6957.csv uploaded successfully by user User265.",
                "Backup completed successfully.",
                "GET /v2/54fadb412c4e40cdbaed9335e4c35a9e/servers/detail HTTP/1.1 RCODE  200 len: 1583 time: 0.1878400",
                "Admin access escalation detected for user 9429",
                "Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active.",
                "Invoice generation process aborted for order ID 8910 due to invalid tax calculation module.",
                "The 'BulkEmailSender' feature is no longer supported. Use 'EmailCampaignManager' for improved functionality.",
                "The 'ReportGenerator' module will be retired in version 4.0. Please migrate to the 'AdvancedAnalyticsSuite' by Dec 2025"
            ]
        })
        st.download_button(
            label="Download Sample CSV",
            data=sample_data.to_csv(index=False).encode('utf-8'),
            file_name="cascadelog_sample.csv",
            mime="text/csv"
        )


    # 🚀 Start Analysis
    st.header("🚀 Start Analysis")
    uploaded_file = st.file_uploader(
        "Upload Logs File",
        type=None,  # Allows all file types (mobile-friendly)
        help="Upload a file containing 'source' and 'log_message' columns"
    )

    if uploaded_file is not None:
        if not uploaded_file.name.lower().endswith(".csv"):
            st.warning("⚠️ This file doesn't seem to be a CSV. Proceeding anyway...")

        try:
            df = pd.read_csv(uploaded_file)
            if {"source", "log_message"}.issubset(df.columns):
                st.success("✅ File validation passed!")

                with st.expander("🔍 Preview Uploaded Logs"):
                    st.dataframe(df.head(10), use_container_width=True)

                if st.button("⚡ Run Cascade Analysis", type="primary"):
                    with st.spinner("🔍 Processing logs through API..."):
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
                        start_time = time.time()
                        response = requests.post(f"{FASTAPI_URL}/classify/", files=files)
                        processing_time = time.time() - start_time

                    if response.status_code == 200:
                        st.success("🎉 Analysis Complete!")

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

                        st.download_button(
                            label="📥 Download Full Report",
                            data=result_df.to_csv(index=False).encode('utf-8'),
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
